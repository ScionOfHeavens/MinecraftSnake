from __future__ import annotations
from typing import Any

from mcpi.vec3 import Vec3

class Vector3(Vec3):
    def __init__(self, x=0, y=0, z=0):
        super().__init__(int(x), int(y), int(z))

    def __cmp__(self, other: Vector3 | Vec3):
        return self.length - other.length
    
    def __truediv__(self, number: int | float):
        return self.__itruediv__(self, number)
    
    def __itruediv__(self, number: int | float):
        return Vector3(self.x / number, self.y / number, self.z / number)
    
    def __ifloordiv__(self, number: int | float):
        return Vector3(self.x // number, self.y // number, self.z // number)
    
    def __floordiv__(self, number: int | float):
        return self.__ifloordiv__(self, number)
    
    def __neg__(self):
        return Vector3(-self.x, -self.y, -self.z)
    
    def clone(self):
        return Vector3(self.x, self.y, self.z)
    
    def to_dict(self):
        return {"coordinates": [self.x, self.y, self.z]}
    
    def __iter__(self) -> None:
        return iter([self.x, self.y, self.z])
    
    @staticmethod
    def from_dict(json_dict: dict) -> Vector3:
        return Vector3(*(json_dict["coordinates"]))
    
    @staticmethod
    def normalize_coordinates(first: Vector3, second: Vector3) -> tuple[Vector3,Vector3]:
        x1,y1,z1 = first
        x2,y2,z2 = second
        normalized_first = Vector3(min(x1, x2), min(y1, y2),min(z1, z2))
        normalized_second = Vector3(max(x1, x2), max(y1, y2),max(z1, z2))
        return normalized_first, normalized_second

IDENTITY_VECTOR = Vector3(1, 1, 1)
