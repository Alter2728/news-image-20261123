#!/usr/bin/env python3
"""Entry runner for the news-image-20261123 infographic.

Copies the pre-rendered entry.png from this folder into the output
folder named by MAKEFUN_OUTPUT_DIR (falling back to /output).
Pure standard library, no network access, same bytes every run.
"""

import hashlib
import os
import shutil
import sys

SOURCE_NAME = "entry.png"


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, SOURCE_NAME)
    if not os.path.isfile(source):
        print("missing:", source, file=sys.stderr)
        return 1
    dest_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, SOURCE_NAME)
    shutil.copyfile(source, dest)
    digest = hashlib.sha256(open(dest, "rb").read()).hexdigest()
    print("copied", dest, digest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
