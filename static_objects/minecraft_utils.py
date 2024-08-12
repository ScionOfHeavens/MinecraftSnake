from __future__ import annotations

from static_objects.minecraft import MINECRAFT
from my_mcpi_and_stuff.shape import Shape
from my_mcpi_and_stuff.vec3 import Vector3, IDENTITY_VECTOR
from my_mcpi_and_stuff.block import ShapeBlock

def AddNewShape(first_vertex: Vector3, second_vertex: Vector3, name: str) -> Shape:
    blocks = MINECRAFT.scan_cube_area(first_vertex, second_vertex)
    shape = Shape(MINECRAFT.player.getPos() + Vector3(10, 0, 0), name, blocks, visible=False)
    return shape

def CreateNewShape(position: Vector3, label: str, blocks: list[ShapeBlock]) -> None:
    return Shape(position, label, blocks, True)

