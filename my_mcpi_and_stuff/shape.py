from __future__ import annotations
from typing import Any

from static_objects.minecraft import MINECRAFT
from minecraftstuff import MinecraftShape

from my_mcpi_and_stuff.vec3 import Vector3
from my_mcpi_and_stuff.block import ShapeBlock

class Shape(MinecraftShape):
    label: str

    def __init__(self, label: str, position: Vector3 = Vector3(), shapeBlocks: list[ShapeBlock]=[], visible:bool = False):
        super().__init__(MINECRAFT, position, shapeBlocks, visible)
        self.label = label

    @property
    def extreme_blocks(self) -> tuple[ShapeBlock, ShapeBlock]:
        return self.shapeBlocks[0], self.shapeBlocks[-1]
        
    def to_dict(self):
        #todo: check for instance
        return {
            "label": self.label,
            "blocks": [block.to_dict() for block in self.shapeBlocks]
        }
    
    def clone(self) -> Shape:
        return Shape(self.label, self.position, self.shapeBlocks, False)
    
    @staticmethod
    def from_dict(json_dict: dict) -> Shape:
        blocks: list[ShapeBlock] = []
        for block_dict in json_dict['blocks']:
            blocks.append(ShapeBlock.from_dict(block_dict))
        return Shape(json_dict['label'], Vector3(), blocks, visible = False)