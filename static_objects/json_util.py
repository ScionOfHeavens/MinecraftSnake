from __future__ import annotations

import json
import typing
from io import TextIOWrapper
import time

from minecraftstuff import MinecraftShape, ShapeBlock
from mcpi.event import BlockEvent, ChatEvent
from mcpi.vec3 import Vec3

from static_objects.minecraft import MINECRAFT
from static_objects.minecraft_utils import AddNewShape, CreateNewShape
from my_mcpi_and_stuff.shape import Shape

class JSONHandler:
    @property
    def JSON_ENTITY_FOLDER(self):
        return r"C:\Users\webda\OneDrive\Desktop\Pixel\MinecraftLesson3\game_shapes"
    
    def write_new_shape(self, shape: Shape) -> None:
        with open(f"{self.JSON_ENTITY_FOLDER}\\{shape.label}.json", "w") as json_file:
            json.dump(shape.to_dict(), json_file, indent=4)
    
    def read_shape(self, label: str) -> Shape:
        try:
            with open(f"{self.JSON_ENTITY_FOLDER}\\{label}.json", "r") as json_file:
                shape = Shape.from_dict(json.load(json_file))
            return shape
        except:
            print()

def ParseCmd(message: str):
    if message.find("AddShape") == 0:
        MINECRAFT.postToChat("prepare cmd")
        shape_label = message.replace("AddShape ", "")
        events: list[BlockEvent] = []
        while len(events) != 2:
            mine_events = MINECRAFT.events.pollBlockHits()
            if len(mine_events) > 0:
                events.append(mine_events[0])
                MINECRAFT.postToChat("touch registered")
        first_vertex: Vec3 = events[0].pos
        second_vertex: Vec3 = events[1].pos
        MINECRAFT.postToChat("prepare shape")
        shape = AddNewShape(first_vertex, second_vertex, shape_label)
        JSON_HANDLER.write_new_shape(shape)
        MINECRAFT.postToChat("shape is ready")

    if message.find("CreateShape") == 0:
        MINECRAFT.postToChat("prepare cmd")
        shape_label = message.replace("CreateShape ", "")
        event: BlockEvent = None
        while event == None:
            mine_events = MINECRAFT.events.pollBlockHits()
            if len(mine_events) > 0:
                event = mine_events[0]
                MINECRAFT.postToChat("touch registered")
        create_position = event.pos + Vec3(1,1,1)
        
        MINECRAFT.postToChat("prepare shape")
        shape = JSON_HANDLER.read_shape(shape_label)
        shape.visible = True
        shape.move(*create_position)
        
        MINECRAFT.postToChat("shape is ready")
        
        


JSON_HANDLER = JSONHandler()

if __name__ == "__main__":
    while True:
        events: list[ChatEvent] = MINECRAFT.events.pollChatPosts()
        if events != None and len(events) != 0:
            ParseCmd(events[0].message)
