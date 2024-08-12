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

class Apple(Entity, CanCollide):
    __left_extreme_pos: Vector3
    __right_extreme_pos: Vector3
    __shape: MinecraftShape
    __on_die: Event = Event()
    
    def __init__(self, left_extreme_pos: Vector3, right_extreme_pos: Vector3) -> None:
        self.__left_extreme_pos = left_extreme_pos
        self.__right_extreme_pos = right_extreme_pos
        body_block: ShapeBlock = [ShapeBlock(*Vector3(), block.TNT)]
        self.__shape = MinecraftShape(MINECRAFT, Vector3(), body_block, False)
        self.__set_position()

    def __set_position(self) -> None:
        x1, y1, z1 = list(self.__left_extreme_pos)
        x2, y2, z2 = list(self.__right_extreme_pos)
        self.__shape.move(int(x1),randint(int(y1),int(y2)),randint(int(z1),int(z2)))
        self.__shape.visible = True
        self.__shape.draw()

    def update(self) -> None:
        pass

    def get_collider(self) -> list[Vector3]:
        return [self.__shape.shapeBlocks[0].actualPos]
    
    def subsctibe_on_die(self, action: Callable[[type], None]):
        self.__on_die += action
     
    def on_collide(self, obj: CanCollide, collide_point: Vector3) -> None:
        if str(obj.__class__.__name__) == "Snake":
            self.__on_die(self)
            self.__shape.visible = False
            self.__set_position()
            
