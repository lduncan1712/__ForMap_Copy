import math
import re
from datetime import datetime

import exif
from shapely.geometry import Point, Polygon
import three_image_det
from five_database import five_database
from four_tree import four_tree
from scipy import ndimage
from shapely.geometry import Point, Polygon

import one_directory

class _0frame:

    def __init__(self, path, id, parent_id, phase1):

        self.directory_id = parent_id
        self.path = path
        self.id = id


        if not one_directory.det_testing:
            self.format_metadata()


        if phase1:
            three_image_det.three_image_det.create_image_predictions(path, self, -1 * self.roll)


        else:
            if not one_directory.det_testing:
                db = five_database()
                db.setup_connection(self)



        print(f"FRAME NUMBER {id}")









