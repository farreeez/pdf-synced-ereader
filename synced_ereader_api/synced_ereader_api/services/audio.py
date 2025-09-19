"""Audio related helper functions.

Placeholder utilities for reading/deriving audio metadata. Real implementations
might use `pydub`, `ffprobe`, or `python-vlc`.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass(slots=True)
class AudioMetadata:
    path: str
    size_bytes: int
    inferred_duration: Optional[float]  # Could be None if unknown
    codec: Optional[str]


def load_audio_metadata(audio_path: str) -> AudioMetadata:
    p = Path(audio_path)
    size = p.stat().st_size if p.exists() else 0
    # We do not attempt to read actual headers yet.
    return AudioMetadata(
        path=str(p),
        size_bytes=size,
        inferred_duration=None,
        codec=None,
    )
