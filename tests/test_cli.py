import subprocess
import sys
import unittest

from json_trail import resolve


class JsonTrailTests(unittest.TestCase):
    def test_pointer_escapes(self):
        self.assertEqual(resolve({"a/b": {"~": [42]}}, "/a~1b/~0/0"), 42)

    def test_invalid_array_index(self):
        with self.assertRaisesRegex(ValueError, "invalid array index"):
            resolve([1, 2], "/01")

    def test_compact_stdin(self):
        result = subprocess.run(
            [sys.executable, "json_trail.py", "-", "/items", "--compact"],
            input='{"items": [1, 2]}', text=True, capture_output=True, check=True,
        )
        self.assertEqual(result.stdout, "[1,2]\n")

    def test_missing_pointer_fails(self):
        result = subprocess.run(
            [sys.executable, "json_trail.py", "-", "/missing"],
            input="{}", text=True, capture_output=True,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("object has no key", result.stderr)
