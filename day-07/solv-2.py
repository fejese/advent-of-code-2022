#!/usr/bin/env python3

from typing import Dict, Optional

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

TOTAL_DISK_SPACE: int = 70000000
REQUIRED_DISK_SPACE: int = 30000000


class Dir:
    def __init__(self, parent: Optional["Dir"] = None) -> None:
        self._dirs: Dict[str, "Dir"] = {}
        self._direct_size: int = 0
        self.parent: Optional["Dir"] = parent
        self._cached_size: Optional[int] = None

    @property
    def size(self) -> int:
        if not self._cached_size:
            size = self._direct_size
            size += sum(d.size for d in self._dirs.values())
            self._cached_size = size
        return self._cached_size

    def add_new_dir(self, name: str) -> None:
        self._cached_size = None
        new_dir = Dir(parent=self)
        self._dirs[name] = new_dir

    def add_file(self, name: str, size: int) -> None:
        if self._cached_size is not None:
            self._cached_size += size
        self._direct_size += size

    def __repr__(self) -> str:
        ret = ""
        for name, d in self._dirs.items():
            ret += f"- {name} ({d._direct_size}; {d.size})\n"
            for line in d.__repr__().splitlines(keepends=True):
                ret += f"  {line}"
        return ret

    def get_smallest_above(self, limit: int) -> Optional[int]:
        subs = [d.get_smallest_above(limit) for d in self._dirs.values()]
        subs = [s for s in subs if s]
        if subs:
            return min(subs)

        if self.size >= limit:
            return self.size

        return None


tomb = Dir()
tomb.add_new_dir("/")
current_dir = tomb


with open(INPUT_FILE_NAME, "r") as input_file:
    for line in input_file:
        parts = line.strip().split(" ")
        if parts[0] == "$":
            if parts[1] == "cd":
                if parts[2] == "..":
                    current_dir = current_dir.parent
                else:
                    current_dir = current_dir._dirs[parts[2]]
            elif parts[1] == "ls":
                pass
        elif parts[0] == "dir":
            current_dir.add_new_dir(parts[1])
        else:
            current_dir.add_file(parts[1], int(parts[0]))

print(tomb)
used_space = tomb.size
print(f"total used: {used_space}")
free_space = TOTAL_DISK_SPACE - used_space
print(f"free space: {free_space}")
required_additional_space = REQUIRED_DISK_SPACE - free_space
print(f"required additional space: {required_additional_space}")
smallest = tomb.get_smallest_above(required_additional_space)
print(f"smallest to be deleted: {smallest}")
