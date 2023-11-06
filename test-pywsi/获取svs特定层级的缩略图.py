
import os
OPENSLIDE_PATH = r"E:\Java\openslide-win64-20221217\bin"
os.add_dll_directory(OPENSLIDE_PATH)
import openslide
import openslide.deepzoom as deepzoom
from PIL import Image

# 打开 SVS 图像文件
svs_file = r"H:\gliomaAnnotation\svs\wsi_xml_data\8.svs"
slide = openslide.open_slide(svs_file)
tiles = deepzoom.DeepZoomGenerator(slide,
                              tile_size=256,
                              overlap=0,
                              limit_bounds=True)
# 指定 Deep Zoom 层级（level），通常从 0 开始
level = 5  # 例如，这里指定层级 3
converted_coords = tiles.get_tile_coordinates(level, (0, ))[0]
print(slide.level_dimensions)
# 获取层级的宽度和高度
width, height = slide.level_dimensions[level]
# 指定坐标位置（x, y）
x, y = 0, 0  # 例如，这里指定坐标位置 (1000, 1000)

# 读取缩略图
thumbnail = slide.read_region((x, y), level, (width, height))


# 将 OpenSlide 图像对象转换为 Pillow 图像对象
thumbnail_pil = Image.new("RGB", thumbnail.size)
thumbnail_pil.paste(thumbnail, (0, 0))
thumbnail_pil.show()

