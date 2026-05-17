import hashlib
import json
import os

_CACHE_DIR = ".cache"


def file_hash(path: str) -> str:
    """Generate a unique MD5 hash from file contents."""
    return hashlib.md5(open(path, "rb").read()).hexdigest()


def text_hash(text: str) -> str:
    """Generate a unique MD5 hash from text content."""
    return hashlib.md5(text.encode()).hexdigest()


def get_cache(key: str) -> dict | None:
    """Return cached result if it exists, otherwise None."""
    path = os.path.join(_CACHE_DIR, f"{key}.json")
    if os.path.exists(path):
        print(f"[CACHE] Hit: {key}")
        return json.load(open(path))
    return None


def set_cache(key: str, data: dict) -> None:
    """Save result to cache."""
    os.makedirs(_CACHE_DIR, exist_ok=True)
    json.dump(data, open(os.path.join(_CACHE_DIR, f"{key}.json"), "w"))


def clear_cache() -> None:
    """Delete all cached results."""
    if os.path.exists(_CACHE_DIR):
        for f in os.listdir(_CACHE_DIR):
            os.remove(os.path.join(_CACHE_DIR, f))
        print("[CACHE] Cleared")
