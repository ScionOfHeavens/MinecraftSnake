from minecraftstuff import ShapeBlock, MinecraftShape
from mcpi import block
from mcpi.minecraft import Minecraft, Vec3

MINECRAFT = Minecraft.create()
shape_blocks = []
pos = MINECRAFT.player.getPos()
pos = Vec3(pos.x + 2, pos.y, pos.z)
shape_blocks.append(ShapeBlock(0, 0, 0, block.DIAMOND_BLOCK))
shape_blocks.append(ShapeBlock(0, -1, 0, block.GOLD_BLOCK))
shape_blocks.append(ShapeBlock(0, -2, 0, block.GOLD_BLOCK))
shape = MinecraftShape(MINECRAFT,pos, shape_blocks)

while True:
    for i in range(10):
        shape.moveBy(0, 1, 0)
    for i in range(10):
        shape.moveBy(0, -1, 0)