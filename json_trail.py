#!/usr/bin/env python3
"""Extract a value from a local JSON file using a slash-delimited pointer."""
import argparse
import json
from pathlib import Path
import re
import sys


def resolve(document, pointer):
    if not pointer:
        return document
    if not pointer.startswith("/"):
        raise ValueError("a pointer must be empty or begin with /")
    value = document
    for raw in pointer[1:].split("/"):
        if re.search(r"~(?![01])", raw):
            raise ValueError(f"invalid escape in {raw!r}")
        token = raw.replace("~1", "/").replace("~0", "~")
        if isinstance(value, dict):
            if token not in value:
                raise ValueError(f"object has no key {token!r}")
            value = value[token]
        elif isinstance(value, list):
            if not re.fullmatch(r"0|[1-9][0-9]*", token):
                raise ValueError(f"invalid array index {token!r}")
            index = int(token)
            if index >= len(value):
                raise ValueError(f"array has no index {index}")
            value = value[index]
        else:
            raise ValueError(f"cannot look up {token!r} inside a scalar")
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", help="path or - for standard input")
    parser.add_argument("pointer", nargs="?", default="")
    parser.add_argument("--keys", action="store_true", help="list object keys or array indices")
    parser.add_argument("--compact", action="store_true")
    args = parser.parse_args()
    try:
        source = sys.stdin.read() if args.file == "-" else Path(args.file).read_text(encoding="utf-8-sig")
        value = resolve(json.loads(source), args.pointer)
        if args.keys:
            if isinstance(value, dict):
                value = list(value)
            elif isinstance(value, list):
                value = list(range(len(value)))
            else:
                raise ValueError("--keys needs an object or array")
        formatting = {"separators": (",", ":")} if args.compact else {"indent": 2}
        print(json.dumps(value, ensure_ascii=False, allow_nan=False, **formatting))
    except (OSError, ValueError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
