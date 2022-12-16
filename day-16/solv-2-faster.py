#!/usr/bin/env python3

import re

from typing import Dict, Set, List, Optional, Tuple

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

MAX_STEPS: int = 26


LINE_PATTERN: re.Pattern = re.compile(
    r"Valve (?P<valve>\S+) has flow rate=(?P<flow>\d+); tunnels? leads? to valves? (?P<tunnels>.*)$"
)

CacheKey = Tuple[str, str, str, int, int]


class Cache:
    def __init__(self) -> None:
        self.storage: Dict[CacheKey, int] = {}
        self.hits: int = 0
        self.misses: int = 0
        self.max_max_steps: int = 0

    @property
    def ratio(self) -> float:
        return self.hits / (self.hits + self.misses)

    def report(self) -> None:
        print("Cache size:", len(self.storage))
        print("Cache hist:", self.hits)
        print("Cache misses:", self.misses)
        print("Cache max max steps:", self.max_max_steps)
        print(f"Cache hit ratio: {self.ratio:.3f}")

    def get(self, key: CacheKey) -> Optional[int]:
        value = self.storage.get(key)
        if value is None:
            self.misses += 1
        else:
            self.hits += 1
        return value

    def put(self, key: CacheKey, value: int) -> None:
        self.storage[key] = value
        if self.max_max_steps < key[2]:
            self.max_max_steps = key[2]

        if len(self.storage) % 500000 == 0:
            self.report()


def get_cache_key(
    current_valve: str, current_valve_e: str, open_valves: Set[str], max_steps: int
) -> CacheKey:
    return (
        "|".join((current_valve, current_valve_e)),
        "|".join(sorted(open_valves)),
        max_steps,
    )


def get_next_steps_list(
    shortest_paths: Dict[str, Dict[str, List[str]]],
    current_valve: str,
    open_valves: Set[str],
) -> Dict[str, List[str]]:
    assert current_valve in shortest_paths
    return {
        end: path
        for end, path in shortest_paths[current_valve].items()
        if end not in open_valves
    }


def mprint(prefix: str, line: str) -> None:
    # print(f"{prefix}{line}")
    pass


def get_max_flow(
    cache: Cache,
    valves: Dict[str, int],
    tunnels: Dict[str, Set[str]],
    non_zero_valves: Set[str],
    shortest_paths: Dict[str, Dict[str, List[str]]],
    max_steps: int = MAX_STEPS + 1,
    current_valve: str = "AA",
    current_valve_e: str = "AA",
    open_valves: Set[str] = None,
    next_steps: List[str] = None,
    next_steps_e: List[str] = None,
) -> int:
    log_prefix = (MAX_STEPS + 1 - max_steps) * "  "
    mprint(
        log_prefix,
        f"max_steps: {max_steps}, "
        f"open_valves: {open_valves}, "
        f"current_valve: {current_valve}, "
        f"current_valve_e: {current_valve_e}, "
        f"next_steps: {next_steps}, "
        f"next_steps_e: {next_steps_e}, ",
    )

    # cache_key = get_cache_key(current_valve, current_valve_e, open_valves, max_steps)
    # cached_value = cache.get(cache_key)
    # if cached_value is not None:
    #     return cached_value

    if not open_valves:
        open_valves = set()

    noop = sum(valves[v] for v in open_valves)
    mprint(log_prefix, f"noop: {noop}")

    if max_steps == 1:
        mprint(log_prefix, "ran out of steps => noop")
        return noop

    # both move
    if next_steps and next_steps_e:
        mprint(log_prefix, "both move")
        cases = [
            get_max_flow(
                cache,
                valves,
                tunnels,
                non_zero_valves,
                shortest_paths,
                max_steps - 1,
                next_steps[0],
                next_steps_e[0],
                open_valves,
                next_steps[1:],
                next_steps_e[1:],
            )
        ]

    # both open
    elif not next_steps and not next_steps_e:
        mprint(log_prefix, "both open")
        if current_valve in open_valves or current_valve_e in open_valves:
            mprint(log_prefix, "one of the valves to be opened was already opened => 0")
            return 0
        open_valves = set([*open_valves, current_valve, current_valve_e])
        next_steps_list = get_next_steps_list(
            shortest_paths, current_valve, open_valves
        )
        next_steps_list_e = get_next_steps_list(
            shortest_paths, current_valve_e, open_valves
        )
        cases = [
            get_max_flow(
                cache,
                valves,
                tunnels,
                non_zero_valves,
                shortest_paths,
                max_steps - 1,
                current_valve,
                current_valve_e,
                open_valves,
                next_steps,
                next_steps_e,
            )
            for next_valve, next_steps in next_steps_list.items()
            for next_valve_e, next_steps_e in next_steps_list_e.items()
            # if next_valve != next_valve_e or len(open_valves) + 1 == len(non_zero_valves)
        ]

    # I move, E opens
    elif next_steps:
        mprint(log_prefix, "moves, E opens")
        if current_valve_e in open_valves:
            return 0
        open_valves = set([*open_valves, current_valve_e])
        next_steps_list_e = get_next_steps_list(
            shortest_paths, current_valve_e, open_valves
        )
        cases = [
            get_max_flow(
                cache,
                valves,
                tunnels,
                non_zero_valves,
                shortest_paths,
                max_steps - 1,
                next_steps[0],
                current_valve_e,
                open_valves,
                next_steps[1:],
                next_steps_e,
            )
            for next_steps_e in next_steps_list_e.values()
            # if next_steps[-1] != next_steps_e[-1]
        ]

    # E moves, I opens
    elif next_steps_e:
        mprint(log_prefix, "opens, E moves")
        if current_valve in open_valves:
            return 0
        open_valves = set([*open_valves, current_valve])
        next_steps_list = get_next_steps_list(
            shortest_paths, current_valve, open_valves
        )
        cases = [
            get_max_flow(
                cache,
                valves,
                tunnels,
                non_zero_valves,
                shortest_paths,
                max_steps - 1,
                current_valve,
                next_steps_e[0],
                open_valves,
                next_steps,
                next_steps_e[1:],
            )
            for next_steps in next_steps_list.values()
            # if next_steps[-1] != next_steps_e[-1]
        ]
    else:
        raise Exception("wat")

    if not cases:
        # all valves are open but have time left
        new_noop = sum(valves[v] for v in open_valves)
        remainder = noop + new_noop * (max_steps - 1)
        mprint(log_prefix, f"all valves are open => {remainder}")
        return remainder

    max_flow = max(cases) + noop
    mprint(log_prefix, f"max_flow: {max_flow}")
    # cache.put(cache_key, max_flow)
    return max_flow


def find_shortest_path(
    tunnels: Dict[str, List[str]],
    start: str,
    end: str,
) -> Tuple[int, List[str]]:
    curr = start
    found = {curr}
    to_visit = {curr: []}
    while to_visit:
        new_to_visit = {}
        for elem, path in to_visit.items():
            for next_elem in tunnels[elem]:
                if next_elem in found:
                    continue
                new_path = [*path, next_elem]
                if next_elem == end:
                    return new_path
                found.add(next_elem)
                new_to_visit[next_elem] = new_path
        to_visit = new_to_visit


cache: Cache = Cache()
valves: Dict[str, int] = {}
tunnels: Dict[str, List[str]] = {}

with open(INPUT_FILE_NAME, "r") as input_file:
    for line in input_file:
        match = LINE_PATTERN.match(line.strip())
        assert match, line
        valve = match.group("valve")
        valves[valve] = int(match.group("flow"))
        tunnels[valve] = sorted(match.group("tunnels").split(", "))

non_zero_valves = set([v for v, f in valves.items() if f])

print(len(valves), valves)
print(len(tunnels), tunnels)
print(len(non_zero_valves), non_zero_valves)


shortest_paths: Dict[str, Dict[str, List[str]]] = {
    start: {end: find_shortest_path(tunnels, start, end) for end in non_zero_valves}
    for start in ["AA", *non_zero_valves]
}
print(find_shortest_path(tunnels, "AA", "EE"))


print(
    get_max_flow(
        cache,
        valves,
        tunnels,
        non_zero_valves,
        shortest_paths,
    )
)
# cache.report()
