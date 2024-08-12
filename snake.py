from __future__ import annotations
from typing import Callable
from enum import Enum
from event import Event

from entity import Entity
from mcpi import block
from minecraftstuff import ShapeBlock, MinecraftShape

from my_mcpi_and_stuff.vec3 import Vector3

from static_objects.minecraft import MINECRAFT
from collide_system import CanCollide

class Direction(Enum):
    UP = Vector3(0, 1, 0)
    RIGHT = Vector3(0, 0, 1)
    DOWN = Vector3(0, -1, 0)
    LEFT = Vector3(0, 0, -1)

class Snake(Entity, CanCollide):
    __direction: Vector3
    __direction_before: Vector3 = Vector3()
    __shape: MinecraftShape
    __head_relative_pos : Vector3 = Vector3()
    __on_die: Event = Event()
    def __init__(self, pos: Vector3) -> None:
        self.__direction = Direction.UP.value
        shape_blocks: list[ShapeBlock] = []
        shape_blocks.append(ShapeBlock(0, 0, 0, block.DIAMOND_BLOCK.id))
        shape_blocks.append(ShapeBlock(0, -1, 0, block.GOLD_BLOCK.id))
        shape_blocks.append(ShapeBlock(0, -2, 0, block.GOLD_BLOCK.id))
        self.__shape = MinecraftShape(MINECRAFT, pos, shape_blocks, True)

    def move_left(self) -> None:
        if self.__direction_before == Direction.RIGHT.value:
            return
        self.__direction = Direction.LEFT.value
    def move_right(self) -> None:
        if self.__direction_before == Direction.LEFT.value:
            return
        self.__direction = Direction.RIGHT.value
    def move_up(self) -> None:
        if self.__direction_before == Direction.DOWN.value:
            return
        self.__direction = Direction.UP.value
    def move_down(self) -> None:
        if self.__direction_before == Direction.UP.value:
            return
        self.__direction = Direction.DOWN.value

    def __move(self):
        self.__direction_before = self.__direction
        for i in range(len(self.__shape.shapeBlocks)-1, 0, -1):
            next_block: ShapeBlock = self.__shape.shapeBlocks[i-1]
            current_block: ShapeBlock = self.__shape.shapeBlocks[i]
            current_block.actualPos = next_block.actualPos
        head: ShapeBlock = self.__shape.shapeBlocks[0]
        head.actualPos = head.actualPos + self.__direction
        self.__shape.redraw()

    def update(self) -> None:
        self.__move()
        self.__head_relative_pos += self.__direction

    def get_collider(self) -> list[Vector3]:
        positions: dict[CanCollide,Vector3]= []
        for block in self.__shape.shapeBlocks:
            positions.append(block.actualPos)
        return positions
    
    def __add_tail(self):
        old_tail: ShapeBlock = self.__shape.shapeBlocks[-1]
        new_tail = ShapeBlock(*old_tail.actualPos, old_tail.blockType)
        self.__shape.shapeBlocks.append(new_tail)

    def subsctibe_on_die(self, action: Callable[[type], None]):
        self.__on_die += action

    def die(self) -> None:
        self.__on_die()

    def on_collide(self, obj: CanCollide, collide_point: Vector3) -> None:
        if str(obj.__class__.__name__) == "Apple" and collide_point == self.__head_relative_pos + self.__shape.originalPos:
            self.__add_tail()
        if str(obj.__class__.__name__) == "Snake" and collide_point == self.__head_relative_pos + self.__shape.originalPos:
            self.die()
        if str(obj.__class__.__name__) == "Fence" and collide_point == self.__head_relative_pos + self.__shape.originalPos:
            self.die()