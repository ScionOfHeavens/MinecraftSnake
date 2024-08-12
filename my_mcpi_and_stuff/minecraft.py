from __future__ import annotations
from typing import Callable, Any

from mcpi.minecraft import Minecraft
from mcpi.connection import Connection

from my_mcpi_and_stuff.vec3 import Vector3, IDENTITY_VECTOR
from my_mcpi_and_stuff.block import ShapeBlock

class MyMinecraft(Minecraft):
    def create(address = "localhost", port = 4711):
        return MyMinecraft(Connection(address, port))

    def scan_cube_area(self, vertex1: Vector3, vertex2: Vector3) -> list[ShapeBlock]:
        vertex1, vertex2 = Vector3.normalize_coordinates(vertex1,vertex2)
        vertex1 += IDENTITY_VECTOR
        vertex2 -= IDENTITY_VECTOR
        blocks: list[ShapeBlock] = []
        blocks_id = list(self.getBlocks(vertex1,vertex2))
        diagonal_vector: Vector3 = vertex2 - vertex1 + IDENTITY_VECTOR
        for x in range(diagonal_vector.x):
            for y in range(diagonal_vector.y):
                for z in range(diagonal_vector.z):
                    index = (y)*(diagonal_vector.x)*(diagonal_vector.z) + (x)*(diagonal_vector.z) + z
                    v = Vector3(x,y,z)
                    blocks.append(ShapeBlock(v,blocks_id[index]))
        return blocks
