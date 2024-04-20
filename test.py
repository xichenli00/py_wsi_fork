import os

from openslide import open_slide
from openslide.deepzoom import DeepZoomGenerator

slide = open_slide()
tiles = DeepZoomGenerator(slide, tile_size=512, overlap=0)

print(tiles.level_count)
print(tiles.level_tiles)
print(tiles.level_dimensions)