from __future__ import annotations
from abc import ABC, abstractmethod

from my_mcpi_and_stuff.vec3 import Vector3
from entity import Entity

class CanCollide(ABC):
    @abstractmethod
    def get_collider(self) -> list[Vector3]:
        pass
    @abstractmethod
    def on_collide(self, obj: CanCollide, collide_point: Vector3) -> None:
        pass

class ColliderSystem(Entity):
    __entities: dict[CanCollide, list[Vector3]] = {}

    def add_entity(self, entity: CanCollide) -> None:
        if not isinstance(entity, CanCollide):
            return
        self.__entities[entity] = None

    def update(self) -> None:
        self.update_colliders()
        entities = self.__entities.copy()
        while len(entities)>0:
            entity_type_outer, positions_outer = entities.popitem()
            test_result = self.test_collision(positions_outer, positions_outer, True)
            if test_result[0] == True:
                entity_type_outer.on_collide(entity_type_outer, test_result[1])
            for entity_type_inner, positions_inner in entities.items():
                test_result = self.test_collision(positions_outer, positions_inner, False)
                if test_result[0] == True:
                    entity_type_inner.on_collide(entity_type_outer, test_result[1])
                    entity_type_outer.on_collide(entity_type_inner, test_result[1])

    def update_colliders(self) -> None:
        for entity in self.__entities.keys():
            self.__entities[entity] = entity.get_collider()

    def test_collision(
            self, positions_outer: list[Vector3],
            positions_inner: list[Vector3], is_same_entity: bool
            ) -> tuple[bool, Vector3]:
        for i in range(len(positions_outer)):
            for j in range(len(positions_inner)):
                if is_same_entity and i == j:
                    continue
                if positions_outer[i] == positions_inner[j]:
                    return True, positions_outer[i]
        return False, Vector3()
                
COLLIDE_SYSTEM = ColliderSystem()