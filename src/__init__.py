# Stub package to mirror legacy import paths used in tests
from importlib import import_module

for _mod in ("youtube_parser", "transcript_handler", "llm_providers"):
    try:
        globals()[_mod] = import_module(f"src.{_mod}")
    except Exception:
        pass
