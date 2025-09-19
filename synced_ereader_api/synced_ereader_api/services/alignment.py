"""Audio related helper functions.

Placeholder utilities for reading/deriving audio metadata. Real implementations
might use `pydub`, `ffprobe`, or `python-vlc`.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional


# @dataclass(slots=True)
# class AudioMetadata:
#     path: str
#     size_bytes: int
#     inferred_duration: Optional[float]  # Could be None if unknown
#     codec: Optional[str]

