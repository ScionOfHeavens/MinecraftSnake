from __future__ import annotations
from functools import total_ordering

from minecraftstuff import ShapeBlock
from my_mcpi_and_stuff.vec3 import Vector3    

@total_ordering
class ShapeBlock(ShapeBlock):
    def __init__(self, pos: Vector3, blockType: int, blockData=0, tag=""):
        super().__init__(*pos, blockType, blockData, tag)
        self.actualPos = pos
        self.relativePos = pos
        self.originalPos = pos

    def __hash__(self):
        return super().__hash__()

    def to_dict(self):
        return {
            "relative position": self.relativePos.to_dict(),
            "block type": self.blockType
        }
    
    @staticmethod
    def from_dict(json_dict: dict) -> ShapeBlock:
        return ShapeBlock(Vector3.from_dict(json_dict["relative position"]), json_dict["block type"])
    
    def __eq__(self, other: ShapeBlock):
        return super().__eq__(other)
        
    def __lt__(self, other:ShapeBlock):
        return self.actualPos.lengthSqr < other.actualPos.lengthSqr