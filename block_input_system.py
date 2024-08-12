from __future__ import annotations
from typing import Callable
from enum import Enum

from event import Event
from entity import Entity

from mcpi import block

from static_objects.minecraft import MINECRAFT

class BlockTypes(Enum):
    DIAMOND = block.DIAMOND_BLOCK.id
    GOLD = block.GOLD_BLOCK.id
    IRON = block.IRON_BLOCK.id
    STONE = block.STONE.id

    OBSIDIAN = block.OBSIDIAN.id

class BlockInputSystem(Entity):
    __commands_event: dict[BlockTypes, Event]

    def __init__(self) -> None:
        self.__commands_event = {}
        for block_type in BlockTypes:
            self.__commands_event[block_type] = Event()

    def subscribe_on_command(self, block_type: BlockTypes, action: Callable[[None],None]) -> None:
        if not isinstance(action, Callable) or not isinstance(block_type, BlockTypes):
            return
        self.__commands_event[block_type] += action
    
    def update(self) -> None:
        block_events = MINECRAFT.events.pollBlockHits()
        for event in block_events:
            try:
                command_type: BlockTypes = BlockTypes(MINECRAFT.getBlock(*event.pos))
                command: Callable[[None], None] = self.__commands_event[command_type]
                command()
            except:
                print("This block has been not added yet", MINECRAFT.getBlock(*event.pos))

BLOCK_INPUT_SYSTEM = BlockInputSystem()
