"""
utils.py

General utility functions used across the project.
Must NOT contain business logic.
"""

import uuid
import os
import re
from datetime import datetime
from typing import Optional


# -----------------------------
# Date & Time
# -----------------------------
def format_date(dt: datetime) -> str:
    """
    Format datetime to readable string.
    """
    return dt.strftime("%Y-%m-%d %H:%M:%S")


# -----------------------------
# UUID
# -----------------------------
def generate_uuid() -> str:
    """
    Generate a unique identifier.
    """
    return str(uuid.uuid4())


# -----------------------------
# File Safety
# -----------------------------
def safe_filename(filename: str) -> str:
    """
    Convert unsafe filename to safe format.
    """
    filename = filename.strip().replace(" ", "_")
    filename = re.sub(r"[^a-zA-Z0-9_.-]", "", filename)
    return filename


# -----------------------------
# Path Helpers
# -----------------------------
def ensure_directory(path: str) -> None:
    """
    Ensure directory exists.
    """
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


# -----------------------------
# Text Helpers
# -----------------------------
def truncate_text(text: str, max_length: int) -> str:
    """
    Truncate long text safely.
    """
    if len(text) <= max_length:
        return text
    return text[:max_length].rstrip() + "..."
