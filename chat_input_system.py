from __future__ import annotations
from enum import Enum
from typing import Callable

from event import Event
from entity import Entity

from static_objects.minecraft import MINECRAFT

class ChatCommandType(Enum):
    START_GAME = "Start game"
    FINISH_GAME = "Finish game"
    ADD_SHAPE = "add shape"

class ChatInputSystem(Entity):
    __commands_event: dict[ChatCommandType, Event]

    def __init__(self) -> None:
        self.__commands_event = {}
        for command_type in ChatCommandType:
            self.__commands_event[command_type] = Event()

    def subscribe_on_command(self, command_type: ChatCommandType, action: Callable[[None],None]) -> None:
        if not isinstance(action, Callable) or not isinstance(command_type, ChatCommandType):
            return
        self.__commands_event[command_type] += action
    
    def update(self) -> None:
        chat_events = MINECRAFT.events.pollChatPosts()
        for event in chat_events:
            try:
                command_type: ChatCommandType = ChatCommandType(event.message)
                command: Callable[[None], None] = self.__commands_event[command_type]
                command()
            except Exception as e:
                print("Just a message in chat", event.message, e)

CHAT_INPUT_SYSTEM = ChatInputSystem()