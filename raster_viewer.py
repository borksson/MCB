import rasterio
from rasterio.plot import show

import anvil

import math

fp = r'rasters/timp.tif'
src = rasterio.open(fp)

array = src.read()[0]

max = array.max()
min = array.min()

print(array.shape, max, min)

# with open("array.txt", "w") as f:
#     for row in array:
#         for item in row:
#             f.write(str(item) + " ")
#         f.write("\n")

region = anvil.Region.from_file("/home/borkson/.minecraft/saves/build_test_1_15 (1)/region/r.0.0.mca")
# You can also provide the region file name instead of the object
print(region)
chunk = anvil.Chunk.from_region(region, 0, 0)

# If `section` is not provided, will get it from the y coords
# and assume it's global
block = chunk.get_block(0, 3, 0)

print(block) # <Block(minecraft:air)>
print(block.id) # air
print(block.properties) # {}

region = anvil.EmptyRegion(0, 0)

# Create `Block` objects that are used to set blocks
stone = anvil.Block('minecraft', 'stone')
dirt = anvil.Block('minecraft', 'dirt')

# Make a 16x16x16 cube of either stone or dirt blocks

for z in range(512):
    for x in range(512):
        val = math.floor((array[x][z]*10)-(min*10))
        if val > 255:
            val = 255
        region.set_block(stone, x, val, z)


region.save("/home/borkson/.minecraft/saves/build_test_1_15 (1)/region/r.0.0.mca")