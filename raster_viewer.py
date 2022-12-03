import rasterio
from rasterio.plot import show

import anvil

import math

from tqdm import tqdm

fp = r'rasters/grand.tif'
src = rasterio.open(fp)
show(src)

array = src.read()[0]

max = array.max()
min = array.min()

print(array.shape, max, min)

# with open("array.txt", "w") as f:
#     for row in array:
#         for item in row:
#             f.write(str(item) + " ")
#         f.write("\n")

region_folder = "C:/Users/aaron/AppData/Roaming/.minecraft/saves/timp_build/region/"

# region = anvil.Region.from_file("/home/borkson/.minecraft/saves/build_test_1_15 (1)/region/r.0.0.mca")
# # You can also provide the region file name instead of the object
# print(region)
# chunk = anvil.Chunk.from_region(region, 0, 0)

# # If `section` is not provided, will get it from the y coords
# # and assume it's global
# block = chunk.get_block(0, 3, 0)

# print(block) # <Block(minecraft:air)>
# print(block.id) # air
# print(block.properties) # {}

region = anvil.EmptyRegion(0, 0)

# Create `Block` objects that are used to set blocks
stone = anvil.Block('minecraft', 'stone')
dirt = anvil.Block('minecraft', 'dirt')

# Make a 16x16x16 cube of either stone or dirt blocks

ratio = math.floor(array.shape[0]/512)

for z in tqdm(range(512)):
    for x in range(512):
        val = math.floor(((array[x*ratio][z*ratio])-(min))/(max/256))
        #print(val)
        if val > 255:
            val = 255
        elif val <0 :
            val = 0
        for y in range(val):
            region.set_block(stone, x, y, z)


region.save(region_folder+"r.0.0.mca")