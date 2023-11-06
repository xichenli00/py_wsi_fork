# import py_wsi
# import py_wsi.imagepy_toolkit as tk
#
# file_dir = r"H:\gliomaAnnotation\svs\wsi_xml_data"
# db_location = r"H:\gliomaAnnotation\svs\disk_images"
# xml_dir = file_dir
# patch_size = 1024
# level = 16
# db_name = "patch_db"
# overlap = 0
#
#
# label_map = {
#     'tumor': 1,
#     'Tumor': 1,
#     'normal': 0,
#     'Normal': 0,
# }
#
#
#
# turtle = py_wsi.Turtle(file_dir, db_location, db_name, xml_dir=xml_dir, label_map=label_map, storage_type='disk')
#
# print("Total WSI images:    " + str(turtle.num_files))
# print("LMDB name:           " + str(turtle.db_name))
# print("File names:          " + str(turtle.files))
# print("XML files found:     " + str(turtle.get_xml_files()))
#
# level_count, level_tiles, level_dims = turtle.retrieve_tile_dimensions(file_name='8.svs', patch_size=1024)
# print("Level count:         " + str(level_count))
# print("Level tiles:         " + str(level_tiles))
# print("Level dimensions:    " + str(level_dims))
#
# turtle.sample_and_store_patches(patch_size, level, overlap, load_xml=True, limit_bounds=True)
#
#
# # patches, coords, classes, labels, segmaps = turtle.get_patches_from_file("2.svs", verbose=True)
# #
# # tk.show_labeled_patches(patches[:20], classes[:20])
#
#
# import py_wsi.dataset as ds
#
# dataset = ds.read_datasets(turtle, set_id=1, valid_id=0, total_sets=2, shuffle_all=True, augment=True)
#
# print("Total training set patches:     " + str(len(dataset.train.images)))
# print("Total validation set patches:   " + str(len(dataset.valid.images)))
#
# tk.show_images(dataset.train.images, 7, 1)
#
# tk.show_labeled_patches(dataset.train.images, dataset.train.image_cls)


import py_wsi
import py_wsi.imagepy_toolkit as tk

file_dir = r"H:\gliomaAnnotation\svs\wsi_xml_data"
db_location = r"H:\gliomaAnnotation\svs\wsi_xml_data"
xml_dir = file_dir
patch_size = 1024
level = 16
db_name = "patch_db"
overlap = 0


label_map = {
    'tumor': 1,
    'Tumor': 1,
    'normal': 0,
    'Normal': 0,
}

# ----------------------------------------disk--------------------------------------------------

turtle = py_wsi.Turtle(file_dir, db_location, db_name, xml_dir=xml_dir, label_map=label_map, storage_type='disk')

print("Total WSI images:    " + str(turtle.num_files))
print("LMDB name:           " + str(turtle.db_name))
print("File names:          " + str(turtle.files))
print("XML files found:     " + str(turtle.get_xml_files()))

level_count, level_tiles, level_dims = turtle.retrieve_tile_dimensions(file_name='1.svs', patch_size=1024)
print("Level count:         " + str(level_count))
print("Level tiles:         " + str(level_tiles))
print("Level dimensions:    " + str(level_dims))

turtle.sample_and_store_patches(patch_size, level, overlap, load_xml=True, limit_bounds=True)

patches, coords, classes, labels, segmaps = turtle.get_patches_from_file("2.svs", verbose=True)

tk.show_labeled_patches(patches[:20], classes[:20])


import py_wsi.dataset as ds

dataset = ds.read_datasets(turtle, set_id=1, valid_id=0, total_sets=2, shuffle_all=True, augment=True)

print("Total training set patches:     " + str(len(dataset.train.images)))
print("Total validation set patches:   " + str(len(dataset.valid.images)))

tk.show_images(dataset.train.images, 7, 1)

tk.show_labeled_patches(dataset.train.images, dataset.train.image_cls)

