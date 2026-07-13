"""Shared tool for writing finished pipeline output (itinerary, packing list) to disk.

Agents never get direct filesystem access — they only produce text. This tool takes
that text as a parameter and performs the actual write, so it can be shared by any
agent that produces a final markdown artifact (Coordinator, Packing List Agent, ...).
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Literal

from agents import function_tool

OUTPUT_ROOT = Path("output")

_FILE_NAMES: dict[str, str] = {
    "itinerary": "itinerary.md",
    "packing_list": "packing-list.md",
}


def _slugify(destination: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", destination.strip().lower()).strip("-")
    return slug or "trip"


@function_tool
def write_output(destination: str, kind: Literal["itinerary", "packing_list"], content: str) -> str:
    """Write finished markdown output to output/<destination>/<kind file>.

    Call this once you have the final markdown text ready to persist. `destination`
    is the travel destination (used as the folder name). `kind` selects the file:
    "itinerary" writes itinerary.md, "packing_list" writes packing-list.md. `content`
    is the complete markdown text to write — pass the exact text you present to the
    user, not a summary.
    """
    folder = OUTPUT_ROOT / _slugify(destination)
    folder.mkdir(parents=True, exist_ok=True)
    file_path = folder / _FILE_NAMES[kind]
    file_path.write_text(content, encoding="utf-8")
    return f"Wrote {file_path}"
