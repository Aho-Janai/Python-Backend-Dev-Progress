"""Convert a Photoshop Actions file (.atn) with recorded brush/eraser strokes
into rows for the PsStroke table.

Container layout: tonton-pixel's "Photoshop Actions File Format" (documented).
Stroke payload (the `toolRecordingData` raw blob): reverse-engineered from two
sample files, so only the fields below are trusted. Everything else is skipped.

Blob layout (big-endian):
    u32 6, u8 ?, u32 ?, 3 x name (u32 len + bytes), "<NULL>" (u32 len + bytes),
    u32 record_count, then record_count x 63-byte records.

Record (63 bytes), fields used here:
    byte 0       1 on the last record of the stroke
    bytes 12-19  double  t  seconds since stroke start (whole milliseconds)
    bytes 20-23  float32 x
    bytes 24-27  float32 y
A stroke has ~10^5 records but only ~10 distinct (x, y) positions; the records
repeat the latest input position. We keep one point per position change.

Usage:
    python atn_import.py recording.atn [--json rows.json] [--session-id ID]
"""
from __future__ import annotations

import argparse
import json
import struct
import sys
import uuid
from dataclasses import dataclass, field

RECORD = struct.Struct(">B7x4xdff35x")  # last-flag, t, x, y; skips unknown bytes
assert RECORD.size == 63
BLOB_VERSION = 6
TOOLS = {"PbTl": "brush", "ErTl": "eraser"}


class AtnError(ValueError):
    """The file does not match the layout this module understands."""


class _Reader:
    def __init__(self, data: bytes, pos: int = 0):
        self.b, self.p = data, pos

    def _need(self, n: int) -> None:
        if self.p + n > len(self.b):
            raise AtnError(f"unexpected end of data at byte {self.p}")

    def raw(self, n: int) -> bytes:
        self._need(n)
        v = self.b[self.p:self.p + n]
        self.p += n
        return v

    def u8(self) -> int:
        return self.raw(1)[0]

    def u16(self) -> int:
        return struct.unpack(">H", self.raw(2))[0]

    def u32(self) -> int:
        return struct.unpack(">I", self.raw(4))[0]

    def i32(self) -> int:
        return struct.unpack(">i", self.raw(4))[0]

    def i64(self) -> int:
        return struct.unpack(">q", self.raw(8))[0]

    def f64(self) -> float:
        return struct.unpack(">d", self.raw(8))[0]

    def ustr(self) -> str:  # u32 char count + UTF-16BE incl. terminator
        return self.raw(self.u32() * 2).decode("utf-16-be", "replace").rstrip("\x00")

    def bstr(self) -> str:  # u32 length + bytes
        return self.raw(self.u32()).decode("latin-1")

    def ident(self) -> str:  # u32 length (0 -> 4-char code) + bytes
        n = self.u32()
        return self.raw(4 if n == 0 else n).decode("latin-1")


def _read_item(r: _Reader):
    t = r.raw(4).decode("latin-1")
    if t == "bool":
        return t, bool(r.u8())
    if t == "long":
        return t, r.i32()
    if t == "comp":
        return t, r.i64()
    if t == "doub":
        return t, r.f64()
    if t == "UntF":
        return t, (r.raw(4).decode("latin-1"), r.f64())
    if t == "TEXT":
        return t, r.ustr()
    if t == "enum":
        return t, (r.ident(), r.ident())
    if t in ("type", "GlbC"):
        return t, (r.ustr(), r.ident())
    if t in ("Objc", "GlbO"):
        return t, _read_object(r)
    if t == "VlLs":
        return t, [_read_item(r) for _ in range(r.u32())]
    if t == "tdta":
        return t, r.raw(r.u32())
    if t == "obj ":
        refs = []
        for _ in range(r.u32()):
            form = r.raw(4).decode("latin-1")
            if form == "Clss":
                refs.append((form, r.ustr(), r.ident()))
            elif form == "Enmr":
                refs.append((form, r.ustr(), r.ident(), r.ident(), r.ident()))
            elif form == "prop":
                refs.append((form, r.ustr(), r.ident(), r.ident()))
            elif form in ("Idnt", "indx"):
                refs.append((form, r.i32()))
            elif form == "name":
                refs.append((form, r.ustr(), r.ident(), r.ustr()))
            elif form == "rele":
                refs.append((form, r.ustr(), r.ident(), r.i32()))
            else:
                raise AtnError(f"unknown reference form {form!r} at byte {r.p - 4}")
        return t, refs
    raise AtnError(f"unknown item type {t!r} at byte {r.p - 4}")


def _read_object(r: _Reader):
    r.ustr()  # class name
    class_id = r.ident()
    items = {}
    for _ in range(r.u32()):
        key = r.ident()
        items[key] = _read_item(r)
    return class_id, items


@dataclass
class Command:
    index: int
    event: str
    items: dict


def read_commands(data: bytes) -> list[Command]:
    """Parse the container into a flat list of commands (all actions)."""
    r = _Reader(data)
    r.u32()  # file version (16)
    r.ustr()  # set name
    r.u8()  # expanded
    commands: list[Command] = []
    for _ in range(r.u32()):  # actions
        r.u16(); r.u8(); r.u8(); r.u16()  # function key, shift, command, color
        r.ustr(); r.u8()  # action name, expanded
        for _ in range(r.u32()):  # commands
            r.u8(); r.u8(); r.u8(); r.u8()  # expanded, enabled, dialog, options
            selector = r.raw(4)
            if selector == b"long":
                event = r.raw(4).decode("latin-1")
            elif selector == b"TEXT":
                event = r.raw(r.u32()).decode("latin-1")
            else:
                raise AtnError(f"unknown event selector {selector!r}")
            r.bstr()  # dictionary name
            items = _read_object(r)[1] if r.i32() != 0 else {}
            commands.append(Command(len(commands), event, items))
    if r.p != len(data):
        raise AtnError(f"{len(data) - r.p} unparsed bytes at end of file")
    return commands


@dataclass
class Stroke:
    seq: int
    tool: str
    points: list  # [x, y, pressure(None), t_ms since stroke start]
    duration_ms: int
    record_count: int


@dataclass
class Result:
    strokes: list[Stroke] = field(default_factory=list)
    skipped: list[tuple[int, str]] = field(default_factory=list)  # (command index, reason)
    warnings: list[str] = field(default_factory=list)


def parse_blob(blob: bytes) -> tuple[list, int, int]:
    """Return (points, duration_ms, record_count) from a toolRecordingData blob."""
    r = _Reader(blob)
    version = r.u32()
    if version != BLOB_VERSION:
        raise AtnError(f"unsupported blob version {version}")
    r.u8(); r.u32()  # unknown
    for _ in range(3):
        r.bstr()  # tool class name, repeated three times
    r.bstr()  # "<NULL>"
    count = r.u32()
    if len(blob) - r.p != count * RECORD.size:
        raise AtnError(f"record count {count} does not match blob size")
    points: list = []
    last_xy = None
    max_t = 0.0
    for _flag, t, x, y in RECORD.iter_unpack(memoryview(blob)[r.p:]):
        max_t = max(max_t, t)
        if (x, y) != last_xy:
            points.append([round(x, 2), round(y, 2), None, round(t * 1000)])
            last_xy = (x, y)
    return points, round(max_t * 1000), count


def parse_atn(source: bytes | str) -> Result:
    data = source if isinstance(source, bytes) else open(source, "rb").read()
    result = Result()
    for cmd in read_commands(data):
        if cmd.event != "toolRecording":
            continue
        refs = cmd.items.get("null", ("", []))[1]
        class_id = refs[0][2] if refs and refs[0][0] == "Clss" else "?"
        blob = cmd.items.get("toolRecordingData", ("", None))[1]
        if blob is None:
            result.skipped.append((cmd.index, "toolRecording without data"))
            continue
        try:
            points, duration_ms, count = parse_blob(blob)
        except AtnError as e:
            result.skipped.append((cmd.index, f"{class_id}: {e}"))
            continue
        times = [p[3] for p in points]
        if times != sorted(times):
            result.warnings.append(f"command {cmd.index}: point times not increasing")
        result.strokes.append(Stroke(
            seq=len(result.strokes) + 1,
            tool=TOOLS.get(class_id, f"unknown:{class_id}"),
            points=points, duration_ms=duration_ms, record_count=count))
    return result


def to_rows(strokes: list[Stroke], session_id: str) -> list[dict]:
    """Rows for PsStroke(**row). Fields the .atn does not carry stay None."""
    return [dict(
        session_id=session_id, seq=s.seq, t_ms=None, tool=s.tool,
        layer=None, brush=None, color=None, size=None, opacity=None,
        fidelity="points", duration_ms=s.duration_ms, points=s.points,
    ) for s in strokes]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("atn")
    ap.add_argument("--json", help="write the rows to this JSON file")
    ap.add_argument("--session-id", default=str(uuid.uuid4()))
    args = ap.parse_args(argv)
    res = parse_atn(args.atn)
    print(f"{len(res.strokes)} stroke(s), {len(res.skipped)} skipped")
    for s in res.strokes:
        print(f"  seq {s.seq}: {s.tool:6s} {len(s.points):3d} points from {s.record_count} records, "
              f"{s.duration_ms} ms")
    for i, why in res.skipped:
        print(f"  skipped command {i}: {why}")
    for w in res.warnings:
        print("  warning:", w)
    if args.json:
        with open(args.json, "w") as f:
            json.dump(to_rows(res.strokes, args.session_id), f, indent=1)
        print("rows written to", args.json)
    return 0


if __name__ == "__main__":
    sys.exit(main())
