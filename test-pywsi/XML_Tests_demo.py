import os
OPENSLIDE_PATH = r"E:\Java\openslide-win64-20221217\bin"
os.add_dll_directory(OPENSLIDE_PATH)

from xml.dom import minidom
import numpy as np
import openslide
from openslide import open_slide
from openslide.deepzoom import DeepZoomGenerator
from shapely.geometry import Polygon, Point

# 该代码的功能是从一个XML文件中读取标记的区域，
# 然后根据给定的点坐标判断该点属于哪个区域，并生成相应的标签。
# 接着，根据给定的参数，从一个WSI（Whole Slide Image）文件中提取补丁（patch）,
# 并为每个补丁生成相应的坐标和标签。
#
# 代码的具体步骤如下：
#
# 1. 导入所需的库和模块。
# 2. 定义一些常量和路径。
# 3. 解析给定的XML文件，获取标记的区域和标签。
# 4. 定义一个函数`get_dimensions`，用于获取列表的维度。
# 5. 打印标记的区域和标签的维度。
# 6. 定义一个字典`label_map`，将标签映射到数字。
# 7. 定义一个函数`generate_label`，根据给定的点坐标判断该点属于哪个区域，并返回相应的标签。
# 8. 调用`generate_label`函数，传入标记的区域、标签和点坐标，获取生成的标签。
# 9. 定义一些参数，如补丁大小、重叠百分比、文件路径等。
# 10. 打开WSI文件，并使用`DeepZoomGenerator`生成器创建一个可迭代的对象`tiles`。
# 11. 检查所请求的级别是否存在。
# 12. 获取在给定级别下的水平和垂直补丁数量。
# 13. 打印水平和垂直补丁数量。
# 14. 获取指定补丁的坐标。
# 15. 初始化一些变量。
# 16. 循环遍历所有的补丁。
# 17. 获取当前补丁的像素值，并将其添加到补丁列表中。
# 18. 将当前补丁的坐标添加到坐标列表中。
# 19. 增加计数器。
# 20. 如果提供了XML文件，则根据补丁的中心点计算补丁的标签。
# 21. 更新水平坐标。
# 22. 更新垂直坐标。
# 23. 打印补丁、坐标和标签的形状。
# 24. 计算标签中非零元素的数量。
# 25. 打印文件名的前缀部分。

# 获取list的维度
def get_dimensions(lst):
    if isinstance(lst, list):
        # 如果是列表，递归检查第一个元素的维度
        return [len(lst)] + get_dimensions(lst[0])
    else:
        # 如果不是列表，返回空列表表示维度结束
        return []


# 根据给定的点坐标判断该点属于哪个区域，并返回相应的标签
def generate_label(regions, region_labels, point):
    # regions = array of vertices (all_coords)
    # point [x, y]
    for i in range(len(region_labels)):
        poly = Polygon(regions[i])
        if poly.contains(Point(point[0], point[1])):
            return label_map[region_labels[i]]
    return label_map['Normal']
# generate_label(regions, region_labels, [7500, 21600])


path = r"H:\gliomaAnnotation\svs\wsi_xml_data\1.xml"


# 1. def get_regions()
xml = minidom.parse(path)
# 第一个标记的区域总是肿瘤的轮廓
regions_ = xml.getElementsByTagName("Region")
regions, region_labels = [], []

# 获取xml文件中的regions，然后得到每个region的顶点坐标组成的ndarray。
for region in regions_:
    vertices = region.getElementsByTagName("Vertex")
    attribute = region.getElementsByTagName("Attribute")
    if len(attribute) > 0:
        r_label = attribute[0].attributes['Value'].value
    else:
        r_label = region.getAttribute('Text')
    region_labels.append(r_label)

    # Store x, y coordinates into a 2D array in format [x1, y1], [x2, y2], ...
    coords = np.zeros((len(vertices), 2))

    for i, vertex in enumerate(vertices):
        coords[i][0] = vertex.attributes['X'].value
        coords[i][1] = vertex.attributes['Y'].value

    regions.append(coords)


print("\n")
print(f" regions的维度是：{get_dimensions(regions)}")
print(f" region_labels的维度是：{get_dimensions(region_labels)}")
print("\n")
# print(np.shape(regions))
# print(np.shape(region_labels))
# print(region_labels)
# print('\n')

# label映射
# label_map = {'Normal': 0,
#              'Benign': 1,
#              'Carcinoma in situ': 2,
#              'Carcinoma invasive': 3,
#             }
label_map = {
    'tumor': 1,
    'Tumor': 1,
    'normal': 0,
    'Normal': 0,
}

patch_size = 256
percent_overlap = 0
file_dir = r"H:\gliomaAnnotation\svs\wsi_xml_data"
file_name = "1.svs"
xml_file = "1.xml"
xml_dir = r"H:\gliomaAnnotation\svs\wsi_xml_data\1.xml"
level = 12

overlap = int(patch_size*percent_overlap / 2.0)
tile_size = patch_size - overlap*2

slide = open_slide(os.path.join(file_dir,file_name))
tiles = DeepZoomGenerator(slide, tile_size=tile_size, overlap=overlap, limit_bounds=False)





# 2.def sample_and_store_patches
if level >= tiles.level_count:
    print("Error: requested level does not exist. Slide level count: " + str(tiles.level_count))
# 获取在给定级别下的水平和垂直补丁数量
x_tiles, y_tiles = tiles.level_tiles[level]
print(f"x_tiles的数量是：+{x_tiles}")
print(f"y_tiles的数量是：+{y_tiles}")


#  获取指定补丁的左上角坐标
# tiles.get_tile_coordinates(level, (5, 2))[0]
# tiles.get_tile_coordinates(level,(5,2))[1]

patches, coords, labels = [], [], []
x, y = 0, 0
count = 0
while y < y_tiles:
    while x < x_tiles:
        new_tile = np.array(tiles.get_tile(level, (x, y)), dtype=np.int8)
        # OpenSlide calculates overlap in such a way that sometimes depending on the dimensions, edge
        # patches are smaller than the others. We will ignore such patches.
        if np.shape(new_tile) == (patch_size, patch_size, 3):
            patches.append(new_tile)
            coords.append(np.array([x, y]))
            count += 1

            # Calculate the patch label based on centre point.
            if xml_file:
                # 先根据tiles的坐标（x_tiles,y_tiles）获取单个tile的中心点坐标，
                # 再根据补丁的中心点计算补丁的label
                converted_coords_1 = tiles.get_tile_coordinates(level, (x, y))[0]
                converted_coords_2 = tuple(x + int(patch_size/2) for x in converted_coords_1)

                labels.append(generate_label(regions, region_labels, converted_coords_2))
        x += 1
    y += 1
    x = 0

# image_ids = [im_id]*count
print(f"patches的形状（维度）是：+{np.shape(patches)}")
print(f"coords的形状（维度）是：+{np.shape(coords)}")
print(f"labels的形状（维度）是：+{np.shape(labels)}")

# 计算label != 0的数量
print(f"label != 0 的数量是： {np.count_nonzero(labels)}")
name = 'tester.svs'
print(name[:-4])