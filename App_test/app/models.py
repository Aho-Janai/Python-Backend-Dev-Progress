from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db


class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    posts: so.WriteOnlyMapped['Post'] = so.relationship(
        back_populates='author')

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(140))
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
                                               index=True)

    author: so.Mapped[User] = so.relationship(back_populates='posts')

    def __repr__(self):
        return '<Post {}>'.format(self.body)


class PsStroke(db.Model):
    __tablename__ = 'ps_strokes'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    session_id: so.Mapped[str] = so.mapped_column(sa.String(36), index=True)
    seq: so.Mapped[int]                        # order within the session, starts at 1
    t_ms: so.Mapped[Optional[int]]             # ms since session start; None for .atn imports
    tool: so.Mapped[str] = so.mapped_column(sa.String(16))   # 'brush' | 'eraser' | 'unknown:XXXX'
    layer: so.Mapped[Optional[str]] = so.mapped_column(sa.String(128))
    brush: so.Mapped[Optional[str]] = so.mapped_column(sa.String(128))
    color: so.Mapped[Optional[str]] = so.mapped_column(sa.String(7))   # "#rrggbb"
    size: so.Mapped[Optional[float]]           # brush size in px
    opacity: so.Mapped[Optional[float]]
    fidelity: so.Mapped[str] = so.mapped_column(sa.String(16))  # 'points' | 'event_only'
    duration_ms: so.Mapped[Optional[int]]      # pen down to pen up
    points: so.Mapped[Optional[list]] = so.mapped_column(
        sa.JSON(none_as_null=True))            # [[x, y, pressure|None, ms since stroke start], ...]
    created_at: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))   # when it was imported

    __table_args__ = (
        sa.UniqueConstraint('session_id', 'seq', name='uq_ps_strokes_session_seq'),
        sa.CheckConstraint("fidelity IN ('points', 'event_only')",
                           name='ck_ps_strokes_fidelity'),
        sa.CheckConstraint("(fidelity = 'points') = (points IS NOT NULL)",
                           name='ck_ps_strokes_points_match'),
    )

    def svg_points(self, box=160, pad=10):
        """The path as an SVG polyline 'x,y x,y ...', scaled into a box x box
        square with the aspect ratio kept and the path centered."""
        if not self.points:
            return ''
        xs = [p[0] for p in self.points]
        ys = [p[1] for p in self.points]
        w, h = max(xs) - min(xs), max(ys) - min(ys)
        inner = box - 2 * pad
        k = inner / (max(w, h) or 1)
        ox = pad + (inner - w * k) / 2
        oy = pad + (inner - h * k) / 2
        return ' '.join(f'{ox + (x - min(xs)) * k:.1f},{oy + (y - min(ys)) * k:.1f}'
                        for x, y in zip(xs, ys))

    def __repr__(self):
        return '<PsStroke {} #{} {}>'.format(self.session_id[:8], self.seq, self.tool)
