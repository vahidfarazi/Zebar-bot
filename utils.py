"""
utils.py

General utility functions for Azarakhsh system.
No business logic allowed here.
"""

import uuid
import os
from datetime import datetime


# -----------------------------
# Generate UUID
# -----------------------------
def generate_uuid() -> str:
    """
    Generate unique identifier.
    """
    return str(uuid.uuid4())


# -----------------------------
# Format Date
# -----------------------------
def format_date(dt: datetime) -> str:
    """
    Convert datetime to ISO format string.
    """
    return dt.isoformat()


# -----------------------------
# Safe Filename
# -----------------------------
def safe_filename(filename: str) -> str:
    """
    Create safe filename for uploads.
    """
    ext = os.path.splitext(filename)[1]
    return f"{uuid.uuid4().hex}{ext}"


# -----------------------------
# Simple slug generator (optional MVP helper)
# -----------------------------
def slugify(text: str) -> str:
    """
    Convert text to simple slug.
    """
    return (
        text.strip()
        .replace(" ", "_")
        .replace("/", "_")
        .lower()
    )
