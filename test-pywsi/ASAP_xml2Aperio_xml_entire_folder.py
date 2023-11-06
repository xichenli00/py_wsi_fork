# import os
# import xml.etree.ElementTree as ET
# from xml.dom.minidom import parseString
#
# # 指定文件夹路径
# folder_path = r"H:\gliomaAnnotation\svs\wsi_xml_data"
#
# # 列出文件夹中的所有XML文件
# xml_files = [f for f in os.listdir(folder_path) if f.endswith('.xml')]
#
# # 循环处理每个XML文件
# for xml_file in xml_files:
#     file_path = os.path.join(folder_path, xml_file)
#
#     # 读取文件B
#     tree_b = ET.parse(file_path)
#     root_b = tree_b.getroot()
#
#     # 创建新的XML文件A
#     root_a = ET.Element('Annotations', MicronsPerPixel="0.466667")
#
#     # 初始化Id和DisplayId
#     next_id = 1
#     next_display_id = 1
#
#     # 遍历文件B中的Annotations
#     for annotation_b in root_b.findall('./Annotations/Annotation'):
#         annotation_a = ET.SubElement(root_a, 'Annotation', Id=str(next_id), Type="4", LineColor="65280", Visible="1", Selected="1", MarkupImagePath="", MacroName="")
#         coordinates_a = ET.SubElement(annotation_a, 'Vertices')
#
#         # 遍历文件B中的Coordinates并转换为文件A格式的Vertices
#         for coordinate_b in annotation_b.findall('./Coordinates/Coordinate'):
#             vertex = ET.SubElement(coordinates_a, 'Vertex', X=coordinate_b.get('X'), Y=coordinate_b.get('Y'), Z="0")
#
#         # 获取PartOfGroup属性并添加到Attribute中
#         part_of_group = annotation_b.get('PartOfGroup')
#         if part_of_group:
#             attributes_a = ET.SubElement(annotation_a, 'Attributes')
#             attribute_a = ET.SubElement(attributes_a, 'Attribute', Name="1", Id="0", Value=part_of_group)
#
#         # 递增Id和DisplayId
#         next_id += 1
#         next_display_id += 1
#
#     # 创建XML树
#     tree_a = ET.ElementTree(root_a)
#
#     # 将XML数据格式化输出到新文件
#     new_file_path = os.path.join(folder_path, 'new_' + xml_file)
#     tree_a.write(new_file_path, encoding='utf-8', xml_declaration=True, method='xml', short_empty_elements=True)
#
#     # 将XML文件内容格式化输出
#     with open(new_file_path, 'r', encoding='utf-8') as f:
#         xml_string = f.read()
#     dom = parseString(xml_string)
#     with open(new_file_path, 'w', encoding='utf-8') as f:
#         f.write(dom.toprettyxml())
#
# print("Conversion completed for all XML files.")
#

import os
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString

# 指定文件夹路径
folder_path = r"H:\gliomaAnnotation\svs\wsi_xml_data\原xml"

# 列出文件夹中的所有XML文件
xml_files = [f for f in os.listdir(folder_path) if f.endswith('.xml')]

# 循环处理每个XML文件
for xml_file in xml_files:
    file_path = os.path.join(folder_path, xml_file)

    # 读取文件B
    tree_b = ET.parse(file_path)
    root_b = tree_b.getroot()

    # 创建新的XML文件A
    root_a = ET.Element('Annotations', MicronsPerPixel="0.466667")

    # 初始化Id和DisplayId
    next_id = 1
    next_display_id = 1

    regions_a = ET.SubElement(root_a, 'Regions')

    # 遍历文件B中的Annotations
    for annotation_b in root_b.findall('./Annotations/Annotation'):
        region_a = ET.SubElement(regions_a, 'Region', Id=str(next_id), Type="0", Zoom="0.500000", Selected="0", ImageLocation="", ImageFocus="-1", Length="0", Area="0", LengthMicrons="0", AreaMicrons="0", Text="", NegativeROA="0", InputRegionId="0", Analyze="1", DisplayId=str(next_display_id))
        coordinates_a = ET.SubElement(region_a, 'Vertices')

        # 遍历文件B中的Coordinates并转换为文件A格式的Vertices
        for coordinate_b in annotation_b.findall('./Coordinates/Coordinate'):
            vertex = ET.SubElement(coordinates_a, 'Vertex', X=coordinate_b.get('X'), Y=coordinate_b.get('Y'), Z="0")

        # 获取PartOfGroup属性并添加到Attribute中
        part_of_group = annotation_b.get('PartOfGroup')
        if part_of_group:
            attributes_a = ET.SubElement(region_a, 'Attributes')
            attribute_a = ET.SubElement(attributes_a, 'Attribute', Name="1", Id="0", Value=part_of_group)

        # 递增Id和DisplayId
        next_id += 1
        next_display_id += 1

    # 创建XML树
    tree_a = ET.ElementTree(root_a)

    # 将XML数据格式化输出到新文件
    new_file_path = os.path.join(folder_path, 'new_' + xml_file)
    tree_a.write(new_file_path, encoding='utf-8', xml_declaration=True, method='xml', short_empty_elements=True)

    # 将XML文件内容格式化输出
    with open(new_file_path, 'r', encoding='utf-8') as f:
        xml_string = f.read()
    dom = parseString(xml_string)
    with open(new_file_path, 'w', encoding='utf-8') as f:
        f.write(dom.toprettyxml())

print("Conversion completed for all XML files.")



"""将new_x开头且.xml结尾的文件重命名为x.xml"""

def transform_name():
    # 指定文件夹路径
    folder_path = r"H:\gliomaAnnotation\svs\wsi_xml_data"

    # 列出文件夹中的所有XML文件
    xml_files = [f for f in os.listdir(folder_path) if f.startswith('new_') and f.endswith('.xml')]

    # 循环处理每个XML文件
    for xml_file in xml_files:
        file_path = os.path.join(folder_path, xml_file)

        # 提取文件名中的数字部分
        file_number = xml_file.split('_')[1].split('.')[0]

        # 构建新的文件名
        new_file_name = file_number + '.xml'
        new_file_path = os.path.join(folder_path, new_file_name)

        # 重命名文件
        os.rename(file_path, new_file_path)

    print("File renaming completed.")

# transform_name()