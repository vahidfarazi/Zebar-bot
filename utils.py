"""
utils.py

Common utility functions for Azarakhsh system.
Must not contain business logic.
"""

import uuid
import os
import re
from datetime import datetime


# -----------------------------
# UUID Generator
# -----------------------------
def generate_uuid() -> str:
    """
    Generate a unique identifier.
    """
    return str(uuid.uuid4())


# -----------------------------
# Safe Filename
# -----------------------------
def safe_filename(filename: str) -> str:
    """
    Sanitize filename to prevent path injection.
    """

    if not filename:
        return "file"

    # remove path traversal
    filename = os.path.basename(filename)

    # remove unsafe chars
    filename = re.sub(r"[^a-zA-Z0-9._-]", "_", filename)

    return filename


# -----------------------------
# Date Formatter
# -----------------------------
def format_date(dt: datetime, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Format datetime object to string.
    """
    return dt.strftime(fmt)


# -----------------------------
# Chunk Text (for messaging limits)
# -----------------------------
def chunk_text(text: str, size: int = 3000) -> list[str]:
    """
    Split long text into chunks for messaging limits.
    """

    if not text:
        return []

    return [text[i:i + size] for i in range(0, len(text), size)]
