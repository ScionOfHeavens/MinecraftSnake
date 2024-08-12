from __future__ import annotations
from typing import Callable
from enum import Enum
from random import randint

from entity import Entity
from mcpi import block
from minecraftstuff import ShapeBlock, MinecraftShape

from my_mcpi_and_stuff.vec3 import Vector3

from event import Event

from static_objects.minecraft import MINECRAFT
from collide_system import CanCollide

class Fence(CanCollide):
    __shape: MinecraftShape
    def __init__(self, size: int, pos: Vector3) -> None:
        shape_blocks: list[ShapeBlock] = []
        for y in range(size):
            shape_blocks.append(ShapeBlock(0, y, 0, block.OBSIDIAN))
            shape_blocks.append(ShapeBlock(0, y, size, block.OBSIDIAN))
        for z in range(size):
            shape_blocks.append(ShapeBlock(0, 0, z, block.OBSIDIAN))
            shape_blocks.append(ShapeBlock(0, size, z, block.OBSIDIAN))
        self.__shape = MinecraftShape(MINECRAFT, pos, shape_blocks)

    def get_collider(self) -> list[Vector3]:
        positions: dict[CanCollide,Vector3]= []
        for block in self.__shape.shapeBlocks:
            positions.append(block.actualPos)
        return positions

    def on_collide(self, obj: CanCollide, collide_point: Vector3) -> None:
        pass