from __future__ import annotations
from typing import Callable
from enum import Enum

from mcpi import block

from event import Event

from static_objects.minecraft import MINECRAFT

from entity import Entity
        
import time

class Game:
    __is_running: bool = False
    __entities: list[Entity]
    
    __start_event: Event = Event()
    __finish_event: Event = Event()
    
    def __init__(self, entities: list[Entity]) -> None:
        self.__entities = entities
        print("Game awaked")
    
    def subscribe_on_start(self, action: Callable[[None],None]) -> None:
        self.__start_event += action

    def subscribe_on_finish(self, action: Callable[[None],None]) -> None:
        self.__finish_event += action

    def add_entity(self, entity: object):
        self.__entities.append(entity)

    def remove_entity(self, entity: object):
        self.__entities.remove(entity)
        print(self.__entities)

    def start(self)->None:
        self.__start_event()

    def finish(self)->None:
        self.__finish_event()
        self.__is_running = False

    def loop(self):
        self.__is_running = True
        while self.__is_running:
            for entity in self.__entities:
                entity.update()
            time.sleep(0.5)