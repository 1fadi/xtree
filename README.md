# XTree
A Directory Tree Generator

### Installation

`pip install fadi-xtree` to install the package in your python enviroment.

### Usage
```
usage: tree [-h] [-v] [-d] [-o [OUTPUT_FILE]] [-i IGNORE_DIR [IGNORE_DIR ...]]
            [--by-name | --by-size | --by-date] [-r]
            [ROOT_DIR]

XTree, a directory tree generator

positional arguments:
  ROOT_DIR              Generate a full directory tree starting at ROOT_DIR

options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -d, --dir-only        Generate a directory-only tree.
  -o [OUTPUT_FILE], --output-file [OUTPUT_FILE]
                        Generate a full directroy tree and save the output to a file
  -i IGNORE_DIR [IGNORE_DIR ...], --ignore-dir IGNORE_DIR [IGNORE_DIR ...]
                        Don't list files from these directories. (e.g. env, __pycache__)
  --by-name             list the files by name.
  --by-size             list the files by size.
  --by-date             list the files by date.
  -r, --reverse         reverse the order.

Thanks for using XTree.
```
