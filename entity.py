from abc import ABC, abstractmethod

class Entity(ABC):
    @abstractmethod
    def update(self)->None:
        pass