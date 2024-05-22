# Lebedev, M. A., Vizilter, Y. V., Vygolov, O. V., Knyaz, V. A., and Rubis, A. Y.: CHANGE DETECTION IN REMOTE SENSING IMAGES USING CONDITIONAL ADVERSARIAL NETWORKS, Int. Arch. Photogramm. Remote Sens. Spatial Inf. Sci., XLII-2, 565–571, https://doi.org/10.5194/isprs-archives-XLII-2-565-2018, 2018.

from glob import glob
from os.path import join, basename

import numpy as np

from . import CDDataset


class CDDDataset(CDDataset):
    def __init__(
        self, 
        root, phase='train', 
        transforms=(None, None, None), 
        repeats=1,
        subset='val',
    ):
        super().__init__(root, phase, transforms, repeats, subset)

    def _read_file_paths(self):
        t1_list, t2_list, tar_list = [], [], []

        set_dir = self.root

        pattern = '*.jpg'
        refs = sorted(glob(join(set_dir, self.subset, 'OUT', pattern)))
        t1s = (join(set_dir, self.subset, 'A', basename(ref)) for ref in refs)
        t2s = (join(set_dir, self.subset, 'B', basename(ref)) for ref in refs)

        tar_list.extend(refs)
        t1_list.extend(t1s)
        t2_list.extend(t2s)

        return t1_list, t2_list, tar_list

    def fetch_target(self, target_path):
        # To {0,1}
        return (super().fetch_target(target_path) > 127).astype(np.bool)  