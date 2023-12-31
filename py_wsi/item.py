'''

This is somewhat equivalent to the Caffe Datum class, encapsulating an individual image and all its
related information required to save in a binary string as a key, value pair in LMDBs.

Author: @ysbecca, Fabian Bongratz
'''

import pickle
import numpy as np
from PIL import Image

class Item(object):

    def __init__(self, patch, coords, label):

        self.channels = patch.shape[2]
        # Assuming only square images.
        self.size = patch.shape[0]
        self.data = patch.tobytes()
        self.label = label # Integer label ie, 2 = Carcinoma in situ
        self.coords = coords

    def get_label_array(self, num_classes):
        l = np.zeros((num_classes))
        l[self.label] = 1
        return l

    def get_patch(self):
        return np.fromstring(self.data, dtype=np.uint8).reshape(self.size, self.size, self.channels)

    def get_patch_as_image(self):
        return Image.fromarray(self.get_patch(), 'RGB')

# ------------------------------------------------------------
class SegItem(Item):
    """
    Subclass of Item: Stores segmentation maps together with the patches
    """
    def __init__(self, patch, coords, label, seg_map):

        super().__init__(patch, coords, label)
        # Assume one channel in segmentation map
        self.seg_map = seg_map.tobytes()

    def get_seg_map(self):
        return np.fromstring(self.seg_map, dtype=np.uint8).reshape(self.size,
                                                                   self.size, 1)

    def get_seg_map_as_image(self):
        return Image.fromarray(self.get_seg_map(), 'L')



