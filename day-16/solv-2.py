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


def get_max_flow(
    cache: Cache,
    valves: Dict[str, int],
    tunnels: Dict[str, Set[str]],
    current_valve: str,
    current_valve_e: str,
    open_valves: Set[str],
    max_steps: int,
) -> int:
    if max_steps == 0:
        return 0

    cache_key = get_cache_key(current_valve, current_valve_e, open_valves, max_steps)
    cached_value = cache.get(cache_key)
    if cached_value is not None:
        return cached_value

    noop = sum(valves[v] for v in open_valves)

    # both move
    cases = [
        get_max_flow(
            cache,
            valves,
            tunnels,
            tunnel,
            tunnel_e,
            open_valves,
            max_steps - 1,
        )
        for tunnel in tunnels[current_valve]
        for tunnel_e in tunnels[current_valve_e]
    ]
    can_open_current_valve = (
        current_valve not in open_valves and valves[current_valve] > 0
    )
    can_open_current_valve_e = (
        current_valve_e not in open_valves and valves[current_valve_e] > 0
    )
    # E moves, I open
    if can_open_current_valve:
        cases.extend(
            [
                get_max_flow(
                    cache,
                    valves,
                    tunnels,
                    current_valve,
                    tunnel_e,
                    set([*open_valves, current_valve]),
                    max_steps - 1,
                )
                for tunnel_e in tunnels[current_valve_e]
            ]
        )

    if current_valve != current_valve_e:
        # I move, E open
        if can_open_current_valve_e:
            cases.extend(
                [
                    get_max_flow(
                        cache,
                        valves,
                        tunnels,
                        tunnel,
                        current_valve_e,
                        set([*open_valves, current_valve_e]),
                        max_steps - 1,
                    )
                    for tunnel in tunnels[current_valve]
                ]
            )

            # both open
            if can_open_current_valve:
                cases.append(
                    get_max_flow(
                        cache,
                        valves,
                        tunnels,
                        current_valve,
                        current_valve_e,
                        set([*open_valves, current_valve, current_valve_e]),
                        max_steps - 1,
                    )
                )

    max_flow = max(cases) + noop
    cache.put(cache_key, max_flow)
    return max_flow


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

print(valves)
print(tunnels)
print(get_max_flow(cache, valves, tunnels, "AA", "AA", set(), MAX_STEPS))
cache.report()
