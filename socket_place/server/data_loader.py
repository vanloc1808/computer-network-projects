"""Load and query the JSON database used by the UDP server."""

import json
import os
from typing import Any, Dict, List, Tuple

_database: List[Dict[str, Any]] | None = None
_db_base_dir: str | None = None


def _module_dir() -> str:
    """Return the absolute directory path for this module."""
    return os.path.dirname(os.path.abspath(__file__))


def initialize_database(db_path: str | None = None) -> None:
    """Load the JSON database once and cache it in memory.

    If db_path is not provided, loads from the packaged `server/db.json`.
    Also records the base directory for resolving relative image paths.
    """
    global _database, _db_base_dir
    if _database is not None:
        return

    if db_path is None:
        db_path = os.path.join(_module_dir(), "db.json")

    _db_base_dir = os.path.dirname(db_path)
    with open(db_path, "r", encoding="utf-8") as database_file:
        _database = json.load(database_file)


def _ensure_initialized() -> Tuple[List[Dict[str, Any]], str]:
    """Ensure the database is loaded and return it with its base directory."""
    if _database is None:
        initialize_database()
    # mypy/pylint safeguards; at this point they are not None
    assert _database is not None
    assert _db_base_dir is not None
    return _database, _db_base_dir


def query_all_places() -> bytes:
    """Return a JSON bytes array of all places with minimal metadata."""
    database, _ = _ensure_initialized()
    result: List[Dict[str, Any]] = []

    for place in database:
        place_id = place["id"]
        name = place["name"]
        img_list = place["images"]
        this_place = {"ID": place_id, "Name": name, "NOI": len(img_list)}
        result.append(this_place)
    return json.dumps(result).encode()


def query_one_place(place_id: str) -> bytes:
    """Return a JSON bytes object describing a single place by id."""
    database, _ = _ensure_initialized()
    this_place: Dict[str, Any] = {
        "ID": "",
        "Name": "",
        "Coordinate": "",
        "Description": "",
    }

    for place in database:
        if place["id"] == place_id:
            this_place = {
                "ID": place["id"],
                "Name": place["name"],
                "Coordinate": place["coordinate"],
                "Description": place["description"],
            }
            break

    return json.dumps(this_place).encode()


def _resolve_path(base_dir: str, maybe_relative_path: str) -> str:
    """Resolve relative image paths from the db against ``base_dir``."""
    if os.path.isabs(maybe_relative_path):
        return maybe_relative_path
    return os.path.normpath(os.path.join(base_dir, maybe_relative_path))


def query_avatar(place_id: str) -> bytes:
    """Return the raw bytes of the avatar image for the given place id."""
    database, base_dir = _ensure_initialized()
    avt_path = ""
    for place in database:
        if place["id"] == place_id:
            avt_path = _resolve_path(base_dir, place["avatar"])
            break
    if avt_path == "":
        raise ValueError("No such ID")
    with open(avt_path, "rb") as img:
        return img.read()


def query_image(place_id: str, idx: int) -> bytes:
    """Return the raw bytes of the indexed image for the given place id."""
    database, base_dir = _ensure_initialized()
    img_list: List[str] = []
    for place in database:
        if place["id"] == place_id:
            # Resolve each image to absolute path relative to db.json
            img_list = [_resolve_path(base_dir, p) for p in place["images"]]
            break
    if not img_list:
        raise ValueError("No such ID")
    if idx < 0 or idx >= len(img_list):
        raise IndexError("Image index out of bounds")
    with open(img_list[idx], "rb") as img:
        return img.read()
