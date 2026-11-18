"""mini_path_type_sniffer: classify a path without raising on missing entries.

Public API:
    sniff(path) -> str
"""

from .core import sniff

__all__ = ["sniff"]
