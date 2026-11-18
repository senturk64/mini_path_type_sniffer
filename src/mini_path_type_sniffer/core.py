"""Core classification logic for mini_path_type_sniffer.

We use os.lstat because it does not follow symlinks, which is required to
distinguish a symlink from its target and to detect broken symlinks.  All
stat calls are wrapped so that a missing path returns "missing" rather than
raising FileNotFoundError.
"""

import os
import stat


def sniff(path):
    """Return a string describing the type of *path*.

    Possible return values:
        "file"           regular file
        "directory"      directory
        "symlink"        symbolic link pointing to an existing target
        "broken symlink" symbolic link whose target does not exist or is a loop
        "socket"         Unix domain socket
        "fifo"           named pipe (FIFO)
        "device"         block or character device
        "missing"        path does not exist or permission denied

    The function never raises for a missing path; it returns "missing".
    """
    try:
        st = os.lstat(path)
    except OSError:
        return "missing"

    mode = st.st_mode

    if stat.S_ISLNK(mode):
        # Determine whether the symlink resolves to an existing entry.
        # os.path.exists follows symlinks and returns False for broken
        # links or loops, so it is exactly what we need here.
        if os.path.exists(path):
            return "symlink"
        return "broken symlink"
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "directory"
    if stat.S_ISSOCK(mode):
        return "socket"
    if stat.S_ISFIFO(mode):
        return "fifo"
    if stat.S_ISBLK(mode) or stat.S_ISCHR(mode):
        return "device"

    # Fallback for any exotic type (e.g. unknown).  Returning "missing"
    # would be misleading because the path does exist; but the brief does
    # not define a category for it.  We return "missing" anyway to keep
    # the set of possible returns closed and documented.
    return "missing"
