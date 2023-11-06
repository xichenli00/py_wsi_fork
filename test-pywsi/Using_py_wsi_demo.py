import py_wsi
import py_wsi.imagepy_toolkit as tk

file_dir = r"H:\gliomaAnnotation\svs\wsi_xml_data"
db_location = r"H:\gliomaAnnotation\svs\disk_images"
xml_dir = file_dir
patch_size = 1024
level = 14
db_name = "patch_db"
overlap = 0

# All possible labels mapped to integer ids in order of increasing severity.
# label_map = {'Normal': 0,
#              'Benign': 1,
#              'Carcinoma in situ': 2,
#              'In situ carcinoma': 2,
#              'Carcinoma invasive': 3,
#              'Invasive carcinoma': 3,
#             }
label_map = {
    'tumor': 1,
    'Tumor': 1,
    'normal': 0,
    'Normal': 0,
}

turtle = py_wsi.Turtle(file_dir, db_location, db_name, xml_dir=xml_dir, label_map=label_map, storage_type='lmdb')

print("Total WSI images:    " + str(turtle.num_files))
print("LMDB name:           " + str(turtle.db_name))
print("File names:          " + str(turtle.files))
print("XML files found:     " + str(turtle.get_xml_files()))

level_count, level_tiles, level_dims = turtle.retrieve_tile_dimensions(file_name='1.svs', patch_size=256)
print("Level count:         " + str(level_count))
print("Level tiles:         " + str(level_tiles))
print("Level dimensions:    " + str(level_dims))

# patch_1 = turtle.retrieve_sample_patch("1.svs", 256, 12, overlap=12)
# patch_2 = turtle.retrieve_sample_patch("1.svs", 128, 12, overlap=12)
# patch_3 = turtle.retrieve_sample_patch("1.svs", 64, 12, overlap=12)

# tk.show_images([patch_1, patch_2, patch_3], 3, 1)
# tk.show_patch_and_gt([patch_1, patch_2, patch_3],)

print("Patch size:", patch_size)

#  ------------------------------------------lmdb---------------------------------------
# turtle.sample_and_store_patches(patch_size, level, overlap, load_xml=True, limit_bounds=True)
# #  1.get_xml_files() 2._sample_store_disk() 3.sample_store_lmdb() 4.sample_store_hdf5()  5. start-time() && end_time()
# patches, coords, classes, labels, segmaps = turtle.get_patches_from_file("1.svs")
#
# tk.show_labeled_patches(patches[:10], coords[:10])

# ------------------------------turtle.get_set_patches----------------------------------------
# set_id = 0
# total_sets = 2
# patches, coords, classes, labels, segmaps = turtle.get_set_patches(set_id, total_sets)
#
# tk.show_labeled_patches(patches[50:60], classes[50:60])

#  --------------------------------turtle.get_set_patches--------------------------------------------
# custom_set_select = [0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1]
# total_sets = 2
# set_id = 1
#
# patches, coords, classes, labels, segmaps = turtle.get_set_patches(set_id, total_sets, select=custom_set_select)
#
# tk.show_labeled_patches(patches[:10], classes[:10])

# ----------------------------------------disk--------------------------------------------------

turtle = py_wsi.Turtle(file_dir, db_location, db_name, xml_dir=xml_dir, label_map=label_map, storage_type='disk')

print("Total WSI images:    " + str(turtle.num_files))
print("LMDB name:           " + str(turtle.db_name))
print("File names:          " + str(turtle.files))
print("XML files found:     " + str(turtle.get_xml_files()))

level_count, level_tiles, level_dims = turtle.retrieve_tile_dimensions(file_name='1.svs', patch_size=256)
print("Level count:         " + str(level_count))
print("Level tiles:         " + str(level_tiles))
print("Level dimensions:    " + str(level_dims))

turtle.sample_and_store_patches(patch_size, level, overlap, load_xml=True, limit_bounds=True)

patches, coords, classes, labels, segmaps = turtle.get_patches_from_file("2.svs", verbose=True)

tk.show_labeled_patches(patches[:20], classes[:20])

# ------------------------------------------hdf5------------------------------------------------------------------------------------

# turtle = py_wsi.Turtle(file_dir, db_location, db_name, xml_dir=xml_dir, label_map=label_map, storage_type='hdf5')
#
# turtle.sample_and_store_patches(patch_size, level, overlap, load_xml=True, limit_bounds=True)
#
# patches, coords, classes, labels, segmaps = turtle.get_patches_from_file("2.svs", verbose=True)
#
# tk.show_labeled_patches(patches[:10], classes[:10])



import py_wsi.dataset as ds

dataset = ds.read_datasets(turtle, set_id=1, valid_id=0, total_sets=2, shuffle_all=True, augment=True)

print("Total training set patches:     " + str(len(dataset.train.images)))
print("Total validation set patches:   " + str(len(dataset.valid.images)))

tk.show_images(dataset.train.images, 7, 1)

tk.show_labeled_patches(dataset.train.images, dataset.train.image_cls)

