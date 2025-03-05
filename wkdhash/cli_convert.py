# MIT License
#
# Copyright (c) 2025 Gregor Vollmer
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
import argparse
from .wkdhash import userid_to_wkd_hash


def main():
    parser = argparse.ArgumentParser(
        description="Read OpenPGP User IDs line-by-line and print their "
                    "corresponding Web-Key-Directory hashed-user-id (hu).",
        epilog="MIT License, Copyright (c) 2025 Gregor Vollmer",
        )
    parser.add_argument(
            "-F",
            "--full",
            action="store_true",
            default=False,
            help="If set, output 'hu@domain', instead of just 'hu'",
            )
    parser.add_argument(
            "-o",
            "--output",
            metavar="outfile",
            dest="outfile",
            type=argparse.FileType("r"),
            default=sys.stdout,
            help="Output, default stdout",
            )
    parser.add_argument(
            "infile",
            nargs="?",
            type=argparse.FileType("r"),
            default=sys.stdin,
            help="Input OpenPGP UserID, defaults to stdin",
            )
    args = parser.parse_args()
    for line in args.infile:
        if not line:
            break
        hu = userid_to_wkd_hash(line.strip(), include_domain=args.full)
        args.outfile.write(hu)
        if line[-1] == "\n":
            args.outfile.write("\n")
        else:
            break
