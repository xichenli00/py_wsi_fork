#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ICIAR2018 - Grand Challenge on Breast Cancer Histology Images
https://iciar2018-challenge.grand-challenge.org/home/
读取svs图像，将其转换为numpy.nparray存储
"""
from matplotlib import pyplot as plt
# from scipy.misc import imsave, imresize
# from openslide import open_slide # http://openslide.org/api/python/
import numpy as np
OPENSLIDE_PATH = r"E:\Java\openslide-win64-20221217\bin"
import os
if hasattr(os, 'add_dll_directory'):
    # Windows
    with os.add_dll_directory(OPENSLIDE_PATH):
        import openslide
else:
    import openslide
save = True

# dir_img = 'PATH TO THE DATASET FOLDER'
dir_img = r"H:\gliomaAnnotation\svs\wsi_xml_data"


valid_images = ['.svs']

# patch_size = (2000,2000)
patch_size = (1024, 1024)

for f in os.listdir(dir_img):
    ext = os.path.splitext(f)[1]
    if ext.lower() not in valid_images:
        continue
    curr_path = os.path.join(dir_img,f)
    print(curr_path)

    # open scan
    scan = openslide.OpenSlide(curr_path)
    
    orig_w = int(scan.properties.get('aperio.OriginalWidth')) # 42113
    orig_h = int(scan.properties.get('aperio.OriginalHeight')) # 62625
    # orig_h = scan.dimensions[0]
    # orig_w = scan.dimensions[1]
    # create an array to store our ima  ge
    img_np = np.zeros((orig_w,orig_h,3),dtype=np.uint8)

    for r in range(0,orig_w,patch_size[0]): # 行
        for c in range(0, orig_h,patch_size[1]): # 列
            if c+patch_size[1] > orig_h and r+patch_size[0]<= orig_w:
                p = orig_h-c
                img = np.array(scan.read_region((c,r),0,(p,patch_size[1])),dtype=np.uint8)[...,0:3]
            elif c+patch_size[1] <= orig_h and r+patch_size[0] > orig_w:
                p = orig_w-r
                img = np.array(scan.read_region((c,r),0,(patch_size[0],p)),dtype=np.uint8)[...,0:3]
            elif  c+patch_size[1] > orig_h and r+patch_size[0] > orig_w:
                p = orig_h-c
                pp = orig_w-r
                img = np.array(scan.read_region((c,r),0,(p,pp)),dtype=np.uint8)[...,0:3]
            else:    
                img = np.array(scan.read_region((c,r),0,(patch_size[0],patch_size[1])),dtype=np.uint8)[...,0:3]
            img_np[r:r+patch_size[0],c:c+patch_size[1]] = img


    if save:
        name_no_ext = os.path.splitext(f)[0]
        np.save(dir_img + name_no_ext, img_np)
        img_np = None

    scan.close()
    
    