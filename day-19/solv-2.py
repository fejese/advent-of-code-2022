#!/usr/bin/env python3

import re
from dataclasses import dataclass, field, replace
from datetime import datetime
from enum import Enum, auto
from typing import Dict, Optional, Tuple


# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"
MAX_STEPS: int = 32


# 1 ore-collecting robot
# ore -> clay -> obisidan -> geode
#
# ore bot: ore -> ore
# clay bot: ore -> clay
# obsidian bot: ore + clay -> obsidian
# geode bot: ore + osidian -> geode
# q: max(geode)


@dataclass
class Blueprint:
    blueprint_id: int
    ore_robot_cost_ore: int
    clay_robot_cost_ore: int
    obsidian_robot_cost_ore: int
    obsidian_robot_cost_clay: int
    geode_robot_cost_ore: int
    geode_robot_cost_obsidian: int
    max_cost_ore: int = field(init=False)

    @staticmethod
    def from_line(line: str) -> "Blueprint":
        nums = [int(n) for n in re.compile("\d+").findall(line)]
        return Blueprint(*nums[:7])

    def __post_init__(self):
        self.max_cost_ore = max(
            self.ore_robot_cost_ore,
            self.clay_robot_cost_ore,
            self.obsidian_robot_cost_ore,
            self.geode_robot_cost_ore,
        )


class Bot(Enum):
    ORE: int = auto()
    CLAY: int = auto()
    OBSIDIAN: int = auto()
    GEODE: int = auto()


@dataclass
class State:
    next_bot: Optional[Bot]
    ore_bots: int = 1
    clay_bots: int = 0
    obsidian_bots: int = 0
    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geode: int = 0

    def __hash__(self) -> int:
        return str(self).__hash__()


def can_build_geode_robot(blueprint: Blueprint, state: State) -> bool:
    return (
        blueprint.geode_robot_cost_ore <= state.ore
        and blueprint.geode_robot_cost_obsidian <= state.obsidian
    )


def can_build_obsidian_robot(blueprint: Blueprint, state: State) -> bool:
    return (
        blueprint.obsidian_robot_cost_ore <= state.ore
        and blueprint.obsidian_robot_cost_clay <= state.clay
    )


def should_build_obsidian_robot(
    blueprint: Blueprint, state: State, just_built_obsidian_bot: bool = False
) -> bool:
    return blueprint.geode_robot_cost_obsidian > (
        state.obsidian_bots + (1 if just_built_obsidian_bot else 0)
    )


def can_build_clay_robot(blueprint: Blueprint, state: State) -> bool:
    return blueprint.clay_robot_cost_ore <= state.ore


def should_build_clay_robot(
    blueprint: Blueprint, state: State, just_built_clay_bot: bool = False
) -> bool:
    return blueprint.obsidian_robot_cost_clay > (
        state.clay_bots + (1 if just_built_clay_bot else 0)
    )


def can_build_ore_robot(blueprint: Blueprint, state: State) -> bool:
    return blueprint.ore_robot_cost_ore <= state.ore


def should_build_ore_robot(
    blueprint: Blueprint, state: State, just_built_ore_bot: bool = False
) -> bool:
    return blueprint.max_cost_ore > (state.ore_bots + (1 if just_built_ore_bot else 0))


def get_max_geode(blueprint: Blueprint, max_steps: int) -> int:
    print(f"Processing {blueprint}")
    blueprint_start = datetime.now()

    states = {State(Bot.ORE), State(Bot.CLAY)}
    for step in range(max_steps):
        print(f"  Step no. {step:2d}: {len(states)} states ... ")
        step_start = datetime.now()

        steps_remain = max_steps - step - 1

        if step < max_steps - 1:
            next_states = set()
            for state in states:
                default_next_step = replace(
                    state,
                    ore=min(
                        state.ore + state.ore_bots,
                        blueprint.max_cost_ore * steps_remain,
                    ),
                    clay=min(
                        state.clay + state.clay_bots,
                        blueprint.obsidian_robot_cost_clay * steps_remain,
                    ),
                    obsidian=min(
                        state.obsidian + state.obsidian_bots,
                        blueprint.geode_robot_cost_obsidian * steps_remain,
                    ),
                )

                if state.next_bot == Bot.GEODE:
                    if can_build_geode_robot(blueprint, state):
                        next_states.update(
                            [
                                replace(
                                    state,
                                    next_bot=next_bot,
                                    ore=min(
                                        state.ore
                                        + state.ore_bots
                                        - blueprint.geode_robot_cost_ore,
                                        blueprint.max_cost_ore * steps_remain,
                                    ),
                                    clay=min(
                                        state.clay + state.clay_bots,
                                        blueprint.obsidian_robot_cost_clay
                                        * steps_remain,
                                    ),
                                    obsidian=min(
                                        state.obsidian
                                        + state.obsidian_bots
                                        - blueprint.geode_robot_cost_obsidian,
                                        blueprint.geode_robot_cost_obsidian
                                        * steps_remain,
                                    ),
                                    geode=state.geode + steps_remain,
                                )
                                for next_bot in Bot
                                if (
                                    (next_bot == Bot.GEODE)
                                    or (
                                        next_bot == Bot.OBSIDIAN
                                        and should_build_obsidian_robot(
                                            blueprint, state
                                        )
                                    )
                                    or (
                                        next_bot == Bot.CLAY
                                        and should_build_clay_robot(blueprint, state)
                                    )
                                    or (
                                        next_bot == Bot.ORE
                                        and should_build_ore_robot(blueprint, state)
                                    )
                                )
                            ]
                        )
                    else:
                        next_states.add(default_next_step)
                    continue

                if state.next_bot == Bot.OBSIDIAN:
                    if can_build_obsidian_robot(blueprint, state):
                        next_states.update(
                            [
                                replace(
                                    state,
                                    next_bot=next_bot,
                                    obsidian_bots=state.obsidian_bots + 1,
                                    ore=min(
                                        state.ore
                                        + state.ore_bots
                                        - blueprint.obsidian_robot_cost_ore,
                                        blueprint.max_cost_ore * steps_remain,
                                    ),
                                    clay=min(
                                        state.clay
                                        + state.clay_bots
                                        - blueprint.obsidian_robot_cost_clay,
                                        blueprint.obsidian_robot_cost_clay
                                        * steps_remain,
                                    ),
                                    obsidian=min(
                                        state.obsidian + state.obsidian_bots,
                                        blueprint.geode_robot_cost_obsidian
                                        * steps_remain,
                                    ),
                                )
                                for next_bot in Bot
                                if (
                                    (next_bot == Bot.GEODE)
                                    or (
                                        next_bot == Bot.OBSIDIAN
                                        and should_build_obsidian_robot(
                                            blueprint, state, True
                                        )
                                    )
                                    or (
                                        next_bot == Bot.CLAY
                                        and should_build_clay_robot(blueprint, state)
                                    )
                                    or (
                                        next_bot == Bot.ORE
                                        and should_build_ore_robot(blueprint, state)
                                    )
                                )
                            ]
                        )
                    else:
                        next_states.add(default_next_step)
                    continue

                if state.next_bot == Bot.CLAY:
                    if can_build_clay_robot(blueprint, state):
                        next_states.update(
                            [
                                replace(
                                    state,
                                    next_bot=next_bot,
                                    clay_bots=state.clay_bots + 1,
                                    ore=min(
                                        state.ore
                                        + state.ore_bots
                                        - blueprint.clay_robot_cost_ore,
                                        blueprint.max_cost_ore * steps_remain,
                                    ),
                                    clay=min(
                                        state.clay + state.clay_bots,
                                        blueprint.obsidian_robot_cost_clay
                                        * steps_remain,
                                    ),
                                    obsidian=min(
                                        state.obsidian + state.obsidian_bots,
                                        blueprint.geode_robot_cost_obsidian
                                        * steps_remain,
                                    ),
                                )
                                for next_bot in Bot
                                if (
                                    (next_bot == Bot.GEODE)
                                    or (
                                        next_bot == Bot.OBSIDIAN
                                        and should_build_obsidian_robot(
                                            blueprint, state
                                        )
                                    )
                                    or (
                                        next_bot == Bot.CLAY
                                        and should_build_clay_robot(
                                            blueprint, state, True
                                        )
                                    )
                                    or (
                                        next_bot == Bot.ORE
                                        and should_build_ore_robot(blueprint, state)
                                    )
                                )
                            ]
                        )
                    else:
                        next_states.add(default_next_step)
                    continue

                if state.next_bot == Bot.ORE:
                    if can_build_ore_robot(blueprint, state):
                        next_states.update(
                            [
                                replace(
                                    state,
                                    next_bot=next_bot,
                                    ore_bots=state.ore_bots + 1,
                                    ore=min(
                                        state.ore
                                        + state.ore_bots
                                        - blueprint.ore_robot_cost_ore,
                                        blueprint.max_cost_ore * steps_remain,
                                    ),
                                    clay=min(
                                        state.clay + state.clay_bots,
                                        blueprint.obsidian_robot_cost_clay
                                        * steps_remain,
                                    ),
                                    obsidian=min(
                                        state.obsidian + state.obsidian_bots,
                                        blueprint.geode_robot_cost_obsidian
                                        * steps_remain,
                                    ),
                                )
                                for next_bot in Bot
                                if (
                                    (next_bot == Bot.GEODE)
                                    or (
                                        next_bot == Bot.OBSIDIAN
                                        and should_build_obsidian_robot(
                                            blueprint, state
                                        )
                                    )
                                    or (
                                        next_bot == Bot.CLAY
                                        and should_build_clay_robot(blueprint, state)
                                    )
                                    or (
                                        next_bot == Bot.ORE
                                        and should_build_ore_robot(
                                            blueprint, state, True
                                        )
                                    )
                                )
                            ]
                        )
                    else:
                        next_states.add(default_next_step)
                    continue

            states = next_states

        step_end = datetime.now()
        step_max = max(state.geode for state in states)
        print(f"    Took {step_end - step_start} Current max: {step_max}")

    blueprint_end = datetime.now()
    print(f"  Took {blueprint_end - blueprint_start} Max: {step_max}")

    return step_max


maxes: Dict[int, int] = {}
with open(INPUT_FILE_NAME, "r") as input_file:
    for line in input_file:
        blueprint = Blueprint.from_line(line)
        if blueprint.blueprint_id not in (1, 2, 3):
            continue
        maxes[blueprint.blueprint_id] = get_max_geode(blueprint, MAX_STEPS)
        print(f"{blueprint.blueprint_id} => {maxes[blueprint.blueprint_id]}")


print(maxes)
prod_maxes = 1
for blueprint_id, max_geode in maxes.items():
    print(f"{blueprint_id} => {maxes[blueprint_id]}")
    prod_maxes *= maxes[blueprint_id]

print(prod_maxes)
