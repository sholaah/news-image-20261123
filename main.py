#!/usr/bin/env python3
"""Entry program for news-image-20261123.

Writes the pre-rendered cover for Monday 23 November 2026 to
/output/entry.png. The image itself is drawn by build_image.py and
shipped in this repository as entry.png; this program only copies it,
so both runs of the program produce byte-identical output.
Standard library only, no network.
"""

import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(source, target)
    print("wrote", target, os.path.getsize(target), "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
