import os
import socket
import stat
import tempfile
import unittest

from mini_path_type_sniffer import sniff


class TestSniff(unittest.TestCase):
    def test_missing(self):
        self.assertEqual(sniff("/this/path/does/not/exist"), "missing")

    def test_regular_file(self):
        with tempfile.NamedTemporaryFile() as f:
            self.assertEqual(sniff(f.name), "file")

    def test_directory(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(sniff(d), "directory")

    def test_symlink(self):
        with tempfile.TemporaryDirectory() as d:
            target = os.path.join(d, "target")
            link = os.path.join(d, "link")
            with open(target, "w") as f:
                f.write("x")
            os.symlink(target, link)
            self.assertEqual(sniff(link), "symlink")

    def test_broken_symlink(self):
        with tempfile.TemporaryDirectory() as d:
            link = os.path.join(d, "broken")
            os.symlink(os.path.join(d, "nope"), link)
            self.assertEqual(sniff(link), "broken symlink")

    def test_fifo(self):
        with tempfile.TemporaryDirectory() as d:
            fifo_path = os.path.join(d, "fifo")
            os.mkfifo(fifo_path)
            self.assertEqual(sniff(fifo_path), "fifo")

    def test_socket(self):
        with tempfile.TemporaryDirectory() as d:
            sock_path = os.path.join(d, "sock")
            s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            try:
                s.bind(sock_path)
                self.assertEqual(sniff(sock_path), "socket")
            finally:
                s.close()

    def test_device(self):
        # /dev/null is a character device on Unix-like systems.
        if os.path.exists("/dev/null"):
            self.assertEqual(sniff("/dev/null"), "device")

    def test_symlink_to_directory(self):
        with tempfile.TemporaryDirectory() as d:
            target = os.path.join(d, "realdir")
            os.mkdir(target)
            link = os.path.join(d, "linkdir")
            os.symlink(target, link)
            self.assertEqual(sniff(link), "symlink")

    def test_symlink_loop(self):
        with tempfile.TemporaryDirectory() as d:
            a = os.path.join(d, "a")
            b = os.path.join(d, "b")
            os.symlink(b, a)
            os.symlink(a, b)
            self.assertEqual(sniff(a), "broken symlink")


if __name__ == "__main__":
    unittest.main()
