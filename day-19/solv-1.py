#!/usr/bin/env python3

import re
from dataclasses import dataclass, field, replace
from typing import Dict, Optional, Tuple


# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"
MAX_STEPS: int = 24


# 1 ore-collecting robot
# ore -> clay -> obisidan -> geode
# ore bot: ore -> ore
# clay bot: ore -> clay
# obsidian bot: ore + clay -> obsidian
# geode bot: ore + osidian -> geode
# q: max(geode)


CacheKey = Tuple["State", int]


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
        if self.max_max_steps < key[1]:
            self.max_max_steps = key[1]

        if len(self.storage) % 1000000 == 0:
            self.report()


@dataclass
class State:
    blueprint_id: int
    ore_robot_cost_ore: int = field(repr=False)
    clay_robot_cost_ore: int = field(repr=False)
    obsidian_robot_cost_ore: int = field(repr=False)
    obsidian_robot_cost_clay: int = field(repr=False)
    geode_robot_cost_ore: int = field(repr=False)
    geode_robot_cost_obsidian: int = field(repr=False)
    ore_bots: int = 0
    clay_bots: int = 0
    obsidian_bots: int = 0
    geode_bots: int = 0
    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geode: int = 0

    @staticmethod
    def from_line(line: str) -> "State":
        nums = [int(n) for n in re.compile("\d+").findall(line)]
        return State(
            *nums,
            ore_bots=1,
        )

    def __hash__(self) -> int:
        return str(self).__hash__()


def get_max_geode(cache: Cache, state: State, max_steps: int = MAX_STEPS) -> int:
    # indent = (MAX_STEPS - max_steps) * "  "
    # print(f"{indent}{state}")
    if max_steps == 0:
        return state.geode

    cache_key = (state, max_steps)
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    next_states = []
    if (
        state.geode_robot_cost_ore <= state.ore
        and state.geode_robot_cost_obsidian <= state.obsidian
    ):
        next_state = replace(
            state,
            geode_bots=state.geode_bots + 1,
            ore=state.ore + state.ore_bots - state.geode_robot_cost_ore,
            clay=state.clay + state.clay_bots,
            obsidian=state.obsidian
            + state.obsidian_bots
            - state.geode_robot_cost_obsidian,
            geode=state.geode + state.geode_bots,
        )
        next_states.append(next_state)
    if (
        state.obsidian_robot_cost_ore <= state.ore
        and state.obsidian_robot_cost_clay <= state.clay
    ):
        next_state = replace(
            state,
            obsidian_bots=state.obsidian_bots + 1,
            ore=state.ore + state.ore_bots - state.obsidian_robot_cost_ore,
            clay=state.clay + state.clay_bots - state.obsidian_robot_cost_clay,
            obsidian=state.obsidian + state.obsidian_bots,
            geode=state.geode + state.geode_bots,
        )
        next_states.append(next_state)
    if state.clay_robot_cost_ore <= state.ore:
        next_state = replace(
            state,
            clay_bots=state.clay_bots + 1,
            ore=state.ore + state.ore_bots - state.clay_robot_cost_ore,
            clay=state.clay + state.clay_bots,
            obsidian=state.obsidian + state.obsidian_bots,
            geode=state.geode + state.geode_bots,
        )
        next_states.append(next_state)
    if state.ore_robot_cost_ore <= state.ore:
        next_state = replace(
            state,
            ore_bots=state.ore_bots + 1,
            ore=state.ore + state.ore_bots - state.ore_robot_cost_ore,
            clay=state.clay + state.clay_bots,
            obsidian=state.obsidian + state.obsidian_bots,
            geode=state.geode + state.geode_bots,
        )
        next_states.append(next_state)
    next_state = replace(
        state,
        ore=state.ore + state.ore_bots,
        clay=state.clay + state.clay_bots,
        obsidian=state.obsidian + state.obsidian_bots,
        geode=state.geode + state.geode_bots,
    )
    next_states.append(next_state)

    result = max(
        get_max_geode(cache, next_state, max_steps - 1) for next_state in next_states
    )
    cache.put(cache_key, result)
    return result


maxes: Dict[int, int] = {}
with open(INPUT_FILE_NAME, "r") as input_file:
    for line in input_file:
        cache: Cache = Cache()
        state = State.from_line(line)
        print(state)
        maxes[state.blueprint_id] = get_max_geode(cache, state)
        cache.report()
        print(f"{state.blueprint_id} => {maxes[state.blueprint_id]}")


print(maxes)
sum_quality = 0
for blueprint_id, max_geode in maxes.items():
    quality = blueprint_id * max_geode
    print(f"{state.blueprint_id} => {maxes[state.blueprint_id]} => {quality}")
    sum_quality += quality

print(sum_quality)
