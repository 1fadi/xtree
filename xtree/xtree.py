'''This module provides XTree main module.'''

import os
import pathlib
import sys

PIPE = '│'
ELBOW = '└──'
TEE = '├──'
PIPE_PREFIX = '│   '
SPACE_PREFIX = '    '


class DirectoryTree:
    def __init__(
        self,
        root_dir,
        dir_only: bool = False,
        output_file=sys.stdout,
        ignore_dir: list[str] = None,
        sort_by: str = "Default",
        reverse: bool = False
    ):
        self._output_file = output_file
        self._generator = _TreeGenerator(
            root_dir,
            dir_only=dir_only,
            ignore_dir=ignore_dir,
            sort_by=sort_by,
            reverse=reverse
        )

    def generate(self):
        tree = self._generator.build_tree()
        if self._output_file != sys.stdout:
            tree.insert(0, "```")
            tree.append("```")
            self._output_file = open(
                self._output_file, mode="w", encoding="UTF-8"
            )
        with self._output_file as stream:
            print("")
            for entry in tree:
                print(entry, file=stream)
            print("")


class _TreeGenerator:
    sort_by = {
        "DATE": os.path.getmtime,
        "NAME": None,
        "SIZE": os.path.getsize,

        "Default": lambda entry: entry.is_file()
    }
    def __init__(
        self,
        root_dir, *,
        dir_only: bool = False,
        ignore_dir: list[str] = None,
        sort_by: str = "Default",
        reverse: bool = False
    ):
        self._root_dir = pathlib.Path(root_dir)
        self._dir_only = dir_only
        self._ignore_dir = [] if ignore_dir is None else ignore_dir
        self._sort_by = _TreeGenerator.sort_by.get(sort_by, "Default") 
        self._reverse = reverse
        self._tree = []
        self._check_gitignore()

    def build_tree(self) -> list:
        self._tree_head()
        self._tree_body(self._root_dir)
        return self._tree

    def _tree_head(self):
        self._tree.append(f"{self._root_dir}{os.sep}")
        self._tree.append(PIPE)

    def _tree_body(self, directory, prefix=''):
        entries = self._prepare_entries(directory)
        entries_count = len(entries)
        for index, entry in enumerate(entries):
            connector = ELBOW if index == entries_count - 1 else TEE
            if entry.is_dir():
                self._add_directory(
                        entry, index, entries_count, prefix, connector
                )
            else:
                self._add_file(entry, prefix, connector)

    def _prepare_entries(self, directory):
        entries = directory.iterdir()
        entries = sorted(entries, key=self._sort_by, reverse=self._reverse)
        if self._dir_only:
            entries = [entry for entry in entries if entry.is_dir()]
            return entries
        return entries

    def _add_directory(
        self, directory, index, entries_count, prefix, connector
    ):
        self._tree.append(f"{prefix}{connector} {directory.name}{os.sep}")
        if index != entries_count - 1:
            prefix += PIPE_PREFIX
        else:
            prefix += SPACE_PREFIX
        if len(list(filter(lambda x: directory.match(x),
            self._ignore_dir))) == 0:
            self._tree_body(
                directory=directory,
                prefix=prefix
            )
            self._tree.append(prefix.rstrip())

    def _add_file(self, file, prefix, connector):
        self._tree.append(f"{prefix}{connector} {file.name}")

    def _check_gitignore(self):
        gitignore_path = os.path.join(self._root_dir, '.gitignore')
        if os.path.exists(gitignore_path):
            with open(gitignore_path) as file:
                gitignore = list(map(lambda x: x.partition('#')[0].rstrip(),
                    file.readlines()))  # strip comments
            gitignore.append(".git")  # ignore .git
            self._ignore_dir += gitignore
