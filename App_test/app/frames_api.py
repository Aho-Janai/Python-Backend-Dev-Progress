  import hashlib
import json
import os
import re

import sqlalchemy as sa
from flask import jsonify, request
from app import app, db
from app.models import Frame

SAFE_NAME = re.compile(r"^frame_\d+_doc\d+\.jpg$")
HEX_COLOR = re.compile(r"^#[0-9a-f]{6}$")


def _folder():
    folder = app.config.get("FRAMES_FOLDER") or os.path.join(app.instance_path, "frames")
    os.makedirs(folder, exist_ok=True)
    return folder


@app.post("/api/frames")
def upload_frame():
    token = app.config.get("FRAMES_API_TOKEN")
    if token and request.headers.get("X-Api-Token") != token:
        return jsonify(error="bad token"), 401

    frame, meta_file = request.files.get("frame"), request.files.get("meta")
    if not frame or not meta_file:
        return jsonify(error="need multipart parts 'frame' and 'meta'"), 400

    jpeg = frame.read()
    if jpeg[:3] != b"\xff\xd8\xff":
        return jsonify(error="'frame' is not a JPEG"), 400
    try:
        meta = json.loads(meta_file.read().decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        return jsonify(error="'meta' is not valid JSON"), 400
    if not isinstance(meta, dict):
        return jsonify(error="'meta' must be a JSON object"), 400

    digest = hashlib.sha256(jpeg).hexdigest()
    existing = db.session.scalar(sa.select(Frame).where(Frame.sha256 == digest))
    if existing:
        return jsonify(id=existing.id, duplicate=True), 200

    # Never trust a client-supplied filename: use ours unless it matches the pattern.
    name = meta.get("frame")
    if not isinstance(name, str) or not SAFE_NAME.match(name):
        name = digest[:16] + ".jpg"
    path = os.path.join(_folder(), name)
    if os.path.exists(path):  # same name, different pixels
        name = digest[:16] + "_" + name
        path = os.path.join(_folder(), name)
    with open(path, "wb") as f:
        f.write(jpeg)

    color = meta.get("foreground_color")
    row = Frame(
        sha256=digest, filename=name,
        document=meta.get("document") if isinstance(meta.get("document"), str) else None,
        document_id=meta.get("document_id") if isinstance(meta.get("document_id"), int) else None,
        layer=meta.get("layer") if isinstance(meta.get("layer"), str) else None,
        foreground_color=color if isinstance(color, str) and HEX_COLOR.match(color) else None,
        captured_at_ms=meta.get("captured_at_ms") if isinstance(meta.get("captured_at_ms"), int) else None,
        meta=meta)
    db.session.add(row)
    db.session.commit()
    return jsonify(id=row.id, duplicate=False), 201
