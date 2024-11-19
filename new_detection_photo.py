import re
from datetime import datetime

import exif

from five_database import five_database


class new_detection_photo:

    def __init__(self, photo_name, id):

        self.path = photo_name
        self.id = id

        self.directory_id = 1

        self.get_metadata()

        #MEANS CREATES PHOTO BUT NOT TREES
        five_database().setup_connection(self, True)




    def get_metadata(self):

        try:
            metadata =  exif.Image(self.path).get_all()
        except:
            print("A_-----------------------------------------------------------------------")


        #Identifies Tilt/Roll
        self.tilt = self.isolate_tilt_roll(metadata.get('image_description', 'F'), True)
        self.roll = self.isolate_tilt_roll(metadata.get('image_description', 'F'), False)

        self.oldx = metadata.get('pixel_x_dimension', 'F')
        self.oldy = metadata.get('pixel_y_dimension', 'F')

        self.HAOV = 85
        self.VAOV = 108

        self.longitude = metadata.get('gps_longitude', 'F')
        self.latitude = metadata.get('gps_latitude', 'F')
        self.altitude = metadata.get('gps_altitude', 'F')
        self.dop = metadata.get('gps_dop', 'F')
        self.gps_direction = metadata.get('gps_img_direction', 'F')  # ANOUTHERTAG???????????

        self.date_time = metadata.get('datetime', 'F')
        self.date_time = datetime.strptime(self.date_time, '%Y:%m:%d %H:%M:%S')
        self.date_time = int(self.date_time.timestamp())

        # print(f"LONG LAT {self.longitude} {self.latitude}")
        # Long
        self.convert_dms_to_dd(True, -1)

        # lat
        self.convert_dms_to_dd(False, 1)


        print(f" {self.longitude} {self.latitude}")






    @staticmethod
    def isolate_tilt_roll(description, choose_tilt):
        slices = re.split('=|/', description)
        if (choose_tilt == True):
            return float(slices[1].strip())
        else:
            return float(slices[3].strip())



    def convert_dms_to_dd(self, bool_long, hemisphere_sign):
        #measures longitude
        if bool_long == True:
            self.longitude = hemisphere_sign * (self.longitude[2]/3600 + self.longitude[1]/60 + self.longitude[0])
        #else does latitude
        else:
            self.latitude = hemisphere_sign * (self.latitude[2]/3600 + self.latitude[1]/60 + self.latitude[0])
