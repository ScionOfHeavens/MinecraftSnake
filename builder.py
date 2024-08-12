from __future__ import annotations
from typing import Callable

from my_mcpi_and_stuff.vec3 import Vector3, IDENTITY_VECTOR

from static_objects.minecraft import MINECRAFT

from entity import Entity
from block_input_system import BlockTypes, BLOCK_INPUT_SYSTEM
from chat_input_system import ChatCommandType, CHAT_INPUT_SYSTEM
from collide_system import COLLIDE_SYSTEM
from snake import Snake
from game import Game
from apple import Apple
from fence import Fence
from score_system import SCORE_SYSTEM

class Builder:
    __map_size: int
    def __init__(self, map_size: int = 40) -> None:
        self.__map_size = map_size
    
    def build(self) -> Game:
        pos: Vector3 = Vector3(*MINECRAFT.player.getPos()) + Vector3(4,0,0)
        self.__build_player_controller(pos.clone())
        left_bot_map_angle: Vector3 = pos + Vector3(20,-self.__map_size//2,-self.__map_size//2)
        self.__build_game_field(left_bot_map_angle.clone(), Vector3(0, self.__map_size, self.__map_size))
        fence = Fence(self.__map_size+2, left_bot_map_angle.clone() - IDENTITY_VECTOR)
        snake = self.__build_snake(pos.clone() + Vector3(19,0,0))
        apple = Apple(left_bot_map_angle.clone()+Vector3(-1,0,0), left_bot_map_angle.clone()+Vector3(-1,0,0)+Vector3(0,self.__map_size,self.__map_size))
        entities: list[Entity] = [CHAT_INPUT_SYSTEM, BLOCK_INPUT_SYSTEM, COLLIDE_SYSTEM, snake, apple]
        game = Game(entities)
        COLLIDE_SYSTEM.add_entity(apple)
        COLLIDE_SYSTEM.add_entity(snake)
        COLLIDE_SYSTEM.add_entity(fence)
        snake.subsctibe_on_die(game.finish)
        apple.subsctibe_on_die(SCORE_SYSTEM.add_to_score)
        game.subscribe_on_finish(SCORE_SYSTEM.on_finish)
        CHAT_INPUT_SYSTEM.subscribe_on_command(ChatCommandType.FINISH_GAME, game.finish)
        return game
        
    
    def __build_player_controller(self, pos: Vector3)->None:
        MINECRAFT.setBlock(*pos + Vector3(), BlockTypes.DIAMOND.value)
        MINECRAFT.setBlock(*pos + Vector3(0, 2, 0), BlockTypes.IRON.value)
        MINECRAFT.setBlock(*pos + Vector3(0, 1, 1), BlockTypes.GOLD.value)
        MINECRAFT.setBlock(*pos + Vector3(0, 1, -1), BlockTypes.STONE.value)

    def __build_game_field(self, pos: Vector3, size: Vector3):
        MINECRAFT.setBlocks(*pos, *(pos+size), BlockTypes.OBSIDIAN.value)

    def __build_snake(self, pos: Vector3) -> Snake:
        snake = Snake(pos)
        BLOCK_INPUT_SYSTEM.subscribe_on_command(BlockTypes.IRON, snake.move_up)
        BLOCK_INPUT_SYSTEM.subscribe_on_command(BlockTypes.DIAMOND, snake.move_down)
        BLOCK_INPUT_SYSTEM.subscribe_on_command(BlockTypes.GOLD, snake.move_right)
        BLOCK_INPUT_SYSTEM.subscribe_on_command(BlockTypes.STONE, snake.move_left)
        return snake

import time
time.sleep(3)
BUILDER = Builder()
GAME = BUILDER.build()
GAME.loop()