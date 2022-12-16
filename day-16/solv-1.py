#!/usr/bin/env python3

import re

from typing import Dict, Set, Tuple

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

MAX_STEPS: int = 30


LINE_PATTERN: re.Pattern = re.compile(
    r"Valve (?P<valve>\S+) has flow rate=(?P<flow>\d+); tunnels? leads? to valves? (?P<tunnels>.*)$"
)

CacheKey = Tuple[str, str, int, int]
CACHE: Dict[CacheKey, int] = {}
CACHE_HIT: int = 0
CACHE_MISS: int = 0


def get_cache_key(
    current_valve: str, open_valves: Set[str], max_steps: int
) -> CacheKey:
    return (current_valve, "|".join(sorted(open_valves)), max_steps)


def get_max_flow(
    valves: Dict[str, int],
    tunnels: Dict[str, Set[str]],
    current_valve: str,
    open_valves: Set[str],
    max_steps: int,
) -> int:
    if max_steps == 0:
        return 0

    global CACHE
    global CACHE_HIT
    global CACHE_MISS
    cache_key = get_cache_key(current_valve, open_valves, max_steps)
    if cache_key in CACHE:
        CACHE_HIT += 1
        return CACHE[cache_key]
    CACHE_MISS += 1

    noop = sum(valves[v] for v in open_valves)

    cases = [
        get_max_flow(
            valves,
            tunnels,
            tunnel,
            open_valves,
            max_steps - 1,
        )
        for tunnel in tunnels[current_valve]
    ]
    if current_valve not in open_valves and valves[current_valve] > 0:
        cases.append(
            get_max_flow(
                valves,
                tunnels,
                current_valve,
                set([*open_valves, current_valve]),
                max_steps - 1,
            )
        )

    max_flow = max(cases) + noop
    CACHE[cache_key] = max_flow
    return max_flow


valves: Dict[str, int] = {}
tunnels: Dict[str, Set[str]] = {}

with open(INPUT_FILE_NAME, "r") as input_file:
    for line in input_file:
        match = LINE_PATTERN.match(line.strip())
        assert match, line
        valve = match.group("valve")
        valves[valve] = int(match.group("flow"))
        tunnels[valve] = set(match.group("tunnels").split(", "))

print(valves)
print(tunnels)
print(get_max_flow(valves, tunnels, "AA", set(), MAX_STEPS))
print("Cache size:", len(CACHE))
print("Cache hist:", CACHE_HIT)
print("Cache misses:", CACHE_MISS)
hit_rate = CACHE_HIT / (CACHE_HIT + CACHE_MISS)
print(f"Cache hit ratio: {hit_rate:.3f}")
