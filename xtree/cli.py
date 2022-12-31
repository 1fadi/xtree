"""This module provides XTree CLI."""

import argparse
import pathlib
import sys

from . import __version__
from .xtree import DirectoryTree


def main():
    args = parse_cmd_line_args()
    root_dir = pathlib.Path(args.root_dir)
    sorting = {
            "NAME": args.by_name,
            "DATE": args.by_date,
            "SIZE": args.by_size
    }
    try:
        sort_by = list(filter(lambda x: sorting[x], sorting))[0]
    except IndexError:
        sort_by = "Default"

    if not root_dir.is_dir():
        print("the specified root directory doesn't exist.")
        sys.exit()
    tree = DirectoryTree(
        root_dir, 
        dir_only=args.dir_only, 
        output_file=args.output_file, 
        ignore_dir=args.ignore_dir, 
        sort_by=sort_by, 
        reverse=args.reverse
    )
    tree.generate()


def parse_cmd_line_args():
    parser = argparse.ArgumentParser(
        prog='tree',
        description='XTree, a directory tree generator',
        epilog='Thanks for using XTree.',
    )
    parser.version = f"XTree v{__version__}"
    parser.add_argument("-v", "--version", action="version")
    parser.add_argument(
        "root_dir",
        metavar="ROOT_DIR",
        nargs="?",
        default=".",
        help="Generate a full directory tree starting at ROOT_DIR"
    )
    parser.add_argument(
        "-d",
        "--dir-only",
        action="store_true",
        help="Generate a directory-only tree."
    )
    parser.add_argument(
        "-o",
        "--output-file",
        metavar="OUTPUT_FILE",
        nargs="?",
        default=sys.stdout,
        help="Generate a full directroy tree and save the output to a file"
    )
    parser.add_argument(
        "-i",
        "--ignore-dir",
        metavar="IGNORE_DIR",
        nargs="+",
        help="Don't list files from these directories. (e.g. env, __pycache__)"
    )
    sort_group = parser.add_mutually_exclusive_group()
    sort_group.add_argument(
        '--by-name',
        action='store_true', 
        help='list the files by name.'
    )
    sort_group.add_argument(
        '--by-size', 
        action='store_true', 
        help='list the files by size.'
    )
    sort_group.add_argument(
        '--by-date', 
        action='store_true', 
        help='list the files by date.'
    )
    parser.add_argument(
        '-r', 
        '--reverse', 
        action='store_true', 
        help='reverse the order.'
    )
    return parser.parse_args()
