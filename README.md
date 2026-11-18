# mini_path_type_sniffer

Classifies a path as `file`, `directory`, `symlink`, `broken symlink`, `socket`, `fifo`, `device`, or `missing` without raising on missing entries.

```python
from mini_path_type_sniffer import sniff

sniff("/etc/hosts")        # 'file'
sniff("/tmp")              # 'directory'
sniff("/no/such/path")     # 'missing'
```

## Why this exists

`os.path` and `os.stat` raise `FileNotFoundError` when a path is absent, which forces every caller to wrap them in `try`/`except`.  This library centralises that decision: a missing path is a valid classification, not an exception.  The trade-off is that the function returns a string rather than an enum or a richer object, keeping the API small and dependency-free.  It uses `os.lstat` so symlinks are reported as such, and it checks `os.path.exists` to distinguish a working symlink from a broken one.

## Edge case

A symlink loop (two symlinks pointing at each other) is reported as `broken symlink` because `os.path.exists` returns `False` for a loop.  This is the same behaviour as the standard library's `os.path.exists` and is the only reasonable choice without adding cycle detection.
