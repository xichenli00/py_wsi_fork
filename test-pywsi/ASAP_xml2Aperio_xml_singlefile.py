import os.path
import xml.etree.ElementTree as ET
file_dir = r"H:\gliomaAnnotation\svs\wsi_xml_data"
file_name = "2.xml"
# 读取文件B
# tree_b = ET.parse(file_dir+'\\'+file_name)
tree_b = ET.parse(os.path.join(file_dir,file_name))
root_b = tree_b.getroot()

# 创建新的XML文件A
root_a = ET.Element('Annotations', MicronsPerPixel="0.466667")

# 初始化Id和DisplayId
next_id = 1
next_display_id = 1

# 遍历文件B中的Annotations
for annotation_b in root_b.findall('./Annotations/Annotation'):
    annotation_a = ET.SubElement(root_a, 'Annotation', Id=str(next_id), Type="4", LineColor="65280", Visible="1", Selected="1", MarkupImagePath="", MacroName="")
    coordinates_a = ET.SubElement(annotation_a, 'Vertices')

    # 遍历文件B中的Coordinates并转换为文件A格式的Vertices
    for coordinate_b in annotation_b.findall('./Coordinates/Coordinate'):
        vertex = ET.SubElement(coordinates_a, 'Vertex', X=coordinate_b.get('X'), Y=coordinate_b.get('Y'), Z="0")

    # 获取PartOfGroup属性并添加到Attribute中
    part_of_group = annotation_b.get('PartOfGroup')
    if part_of_group:
        attributes_a = ET.SubElement(annotation_a, 'Attributes')
        attribute_a = ET.SubElement(attributes_a, 'Attribute', Name="1", Id="0", Value=part_of_group)

    # 递增Id和DisplayId
    next_id += 1
    next_display_id += 1

# 创建XML树
tree_a = ET.ElementTree(root_a)

# 将XML数据格式化输出到文件
tree_a.write(file_dir+'\\' + "2_aperio.xml", encoding='utf-8', xml_declaration=True, method='xml', short_empty_elements=True)

# 将XML文件内容格式化输出
from xml.dom.minidom import parseString
xml_string = ET.tostring(root_a, encoding='utf-8', method='xml')
dom = parseString(xml_string)
with open(file_dir+'\\' + "2_aperio.xml", 'w') as f:
    f.write(dom.toprettyxml())

