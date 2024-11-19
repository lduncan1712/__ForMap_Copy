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


class two_frame:
    def __init__(self, path, title, id, parent_id, phase1):


        self.directory_id = parent_id
        self.path = path + title
        self.id = id
        self.title = title



        self.format_metadata()
        self.db = five_database()

        #ONly metadata formatting required, add frame to database
        if phase1:
            self.db.setup_connection(self, True)
            #return self.tilt



    def return_l(self):
        return self.points, self.boxes, self.image










    # Set Frame Tilt And Roll Accordingly
    @staticmethod
    def isolate_tilt_roll(description, choose_tilt):
        slices = re.split('=|/', description)
        if (choose_tilt == True):
            return float(slices[1].strip())
        else:
            return  float(slices[3].strip())


    def define_AOV(self, dim1, dim2):
        if self.oldx > self.oldy:
            self.HAOV = max(dim1, dim2)
            self.VAOV = min(dim1, dim2)
        else:
            self.HAOV = min(dim1, dim2)
            self.VAOV = max(dim1, dim2)

    def calculate_AOV(self, x, y):
        angle = math.radians(abs(self.roll))



        p1 = int((y * math.sin(angle)))  # + RS
        p2 = int((x * math.cos(angle)))  # + LS
        p3 = int((math.cos(angle) * y))  # + Bott
        p4 = int((math.sin(angle) * x))  # + Top

        #print(f" {p1} {p2} {p3} {p4}")
        self.HAOV = abs(p1) + abs(p2)
        self.VAOV = abs(p3) + abs(p4)




        # print(f"ENDING FOVS {self.HAOV} {self.VAOV}")


    def convert_pixel_slope_to_degree(self):
        #references a ratio of pixels, but im not sure photo dimensios are proportional to photo angle
        #especially when strethced
        print("CONVERT PIXEL SLOPE NEEDED?")
        #solution change ratio to degree,

        #EASIER TO CHANGE SLOPE AT ROOT???


    @staticmethod
    def calculate_new_dimensions_static(x,y,angle):
        angle = math.radians(abs(angle))
        p1 = int((y * math.sin(angle)))  # + RS
        p2 = int((x * math.cos(angle)))  # + LS
        p3 = int((math.cos(angle) * y))  # + Bott
        p4 = int((math.sin(angle) * x))  # + Top

        new_x = int(p1 + p2)
        new_y = int(p3 + p4)

        if angle <= 0:
                                #Left,    TOP,        Right,       Bottom
            old_corners = [(0, p4), (p2,0), (x, p3), (p1, y) ]
            oc = old_corners

            left_slope =  (oc[0][1] - oc[1][1]) / (oc[0][0] - oc[1][0])
            right_slope = (oc[1][1] - oc[2][1]) / (oc[1][0] - oc[2][0])
        else:
                                # Bottom                 Right,              Top,           Left
            old_corners = [(x - p1, y)  , (x, p4), (x - p2, 0), (0, p3) ]

            oc = old_corners

            left_slope = (oc[2][1] - oc[3][1]) / (oc[2][0] - oc[3][0])
            right_slope = (oc[1][1] - oc[2][1]) / (oc[1][0] - oc[2][0])

        return new_x, new_y, old_corners, left_slope, right_slope


    @staticmethod
    def is_out_side_of_frame(self, point, v_tolerance, oc, ls, rs, y, roll):
        return not (two_frame.get_edge_of_old_box(point[0], True, roll, oc, ls, rs, y) - v_tolerance <= point[1] < two_frame.get_edge_of_old_box(point[0], False, roll, oc, ls, rs, y) + v_tolerance)

    @staticmethod
    def get_edge_of_old_box_static(x, bool_top, roll, old_corners, left_slope, right_slope, y):
        #NEGATIVE ROLL
        if roll <= 0:
            #IF LOOKING FOR TOP POINT
            if bool_top == True:

                #IF ON RIGHT SIDE OF IMAGE
                if x > old_corners[1][0]:
                    return abs(right_slope) * (x - old_corners[1][0])   #POSITIVE
                #IF ON LEFT SIDE
                else:
                    return old_corners[0][1] - (x * abs(left_slope))
            #LOOKING FOR BOTTOM POINT
            else:
                #IF ON RIGHT SIDE OF IMAGE
                if x > old_corners[3][0]:
                    return (old_corners[3][1]) - (abs(left_slope) * (x - old_corners[3][0]))
                #IF ON LEFT SIDE
                else:
                    return old_corners[0][1] + abs(right_slope) * x


        # Bottom                 Right,              Top,           Left
        #POSITIVE ROLL
        else:
            if bool_top == True:

                #IF ON RIGHT SIDE OF IMAGE
                if x > old_corners[2][0]:
                    return (x - old_corners[2][0]) * abs(right_slope)
                #IF ON LEFT SIDE
                else:
                    return old_corners[3][1] - (x * abs(left_slope))

            #LOOKING FOR BOTTOM POINT
            else:
                #IF ON RIGHT SIDE OF IMAGE
                if x > old_corners[0][0]:
                    return y - (x - old_corners[0][0]) * abs(left_slope)
                #IF ON LEFT SIDE
                else:
                    return old_corners[3][1] + x * abs(right_slope)




    # Returns the new size of image (after tilt)
    def calculate_new_dimensions(self, x, y,):
        angle = math.radians(abs(self.roll))

        p1 = int((y * math.sin(angle)))  #+ RS
        p2 = int((x * math.cos(angle)))  #+ LS
        p3 = int((math.cos(angle) * y))  #+ Bott
        p4 = int((math.sin(angle) * x))  #+ Top

        self.x = int(p1 + p2)
        self.y = int(p3 + p4)


        print(self.roll)
        if self.roll <= 0:
                                #Left,    TOP,        Right,       Bottom
            self.old_corners = [(0, p4), (p2,0), (self.x, p3), (p1, self.y) ]
            oc = self.old_corners

            self.left_slope =  (oc[0][1] - oc[1][1]) / (oc[0][0] - oc[1][0])
            self.right_slope = (oc[1][1] - oc[2][1]) / (oc[1][0] - oc[2][0])
        else:
                                # Bottom                 Right,              Top,           Left
            self.old_corners = [(self.x - p1, self.y)  , (self.x, p4), (self.x - p2, 0), (0, p3) ]

            oc = self.old_corners

            self.left_slope = (oc[2][1] - oc[3][1]) / (oc[2][0] - oc[3][0])
            self.right_slope = (oc[1][1] - oc[2][1]) / (oc[1][0] - oc[2][0])


    #THE PURPOSE OF THIS FUNCTION, IS TO DETERMINE, WHETHER THE VIEW OF FRAME, EXTENDS BEYOND SINGLE HEMISHEPERE
    #OR IF THERE IS A REGION WHOSE DIRECTION IS ACTUALLY 180 off recorded
    def degree_assessment(self):
        #centre is known
        center = self.tilt

        upper_application = center + self.VAOV/2
        lower_application = center - self.VAOV/2

        if (upper_application > 90 or lower_application < -90):
            print("EXTENDED BEYOND SPHERES, MORE DRASTIC WORK REQUIRED")


    #FUNCTION TO DETERMINE IF A GIVEN POINT IS WITHIN OLD EDGES
    def is_out_side_of_frame(self, point, v_tolerance):
        return not (self.get_edge_of_old_box(point[0], True) - v_tolerance <= point[1] < self.get_edge_of_old_box(point[0], False) + v_tolerance)


    def distance_from_frame_vertical(self, point, bool_top):
        #WHEN WITHIN TOP, POINT > EDGE, SO POSITIVE
        if bool_top:
            return point[1] - self.get_edge_of_old_box(point[0], True)

        #WHEN WITHIN BOTTOM, POINT < EDGE, SO POSITIVE
        else:
            return self.get_edge_of_old_box(point[0], False) - point[1]



    # Handles All Metadata Related
    def format_metadata(self):







        #MAKES METADATA
        try:
            metadata =  exif.Image(self.path).get_all()
        except:
            print("A_-----------------------------------------------------------------------")
        #Identifies Tilt/Roll

        self.tilt = self.isolate_tilt_roll(metadata.get('image_description', 'F'), True)
        self.roll = self.isolate_tilt_roll(metadata.get('image_description', 'F'), False)







        self.oldx = metadata.get('pixel_x_dimension', 'F')
        self.oldy = metadata.get('pixel_y_dimension', 'F')


        print(f" PHOTOS: {self.oldx} {self.oldy}")

        #print(f"X WIDTH: {self.oldx}")
        #print(f" Y HEIGHT: {self.oldy}")


        #print(f"ANGLE CHANGE: {self.roll}")

        #PREVIOUSLY 108, 85

        self.define_AOV(108, 85)

        self.calculate_AOV(self.HAOV, self.VAOV)

        #print(f"HOR VIEW: {self.HAOV}")
        #

        #Finds New Dimensions
        self.calculate_new_dimensions(self.oldx,self.oldy)


        #IDK HOW TO FIND THIS

        # for m in metadata.keys():
        #     print(f"KEY : {m}  /  VALUE: {metadata.get(m)}")


        self.longitude = metadata.get('gps_longitude', 'F')
        self.latitude = metadata.get('gps_latitude', 'F')
        self.altitude = metadata.get('gps_altitude', 'F')
        self.dop = metadata.get('gps_dop', 'F')
        self.gps_direction = metadata.get('gps_img_direction', 'F')   #ANOUTHERTAG???????????


        self.date_time = metadata.get('datetime', 'F')

        #print(self.date_time)
        #print("---------------------------------------")

        #xit
        self.date_time = datetime.strptime(self.date_time, '%Y:%m:%d %H:%M:%S')
        self.date_time = int(self.date_time.timestamp())


        #print(f"LONG LAT {self.longitude} {self.latitude}")
        #Long
        self.convert_dms_to_dd(True, -1)

        #lat
        self.convert_dms_to_dd(False, 1)

    def convert_dms_to_dd(self, bool_long, hemisphere_sign):
        #measures longitude
        if bool_long == True:
            self.longitude = hemisphere_sign * (self.longitude[2]/3600 + self.longitude[1]/60 + self.longitude[0])
        #else does latitude
        else:
            self.latitude = hemisphere_sign * (self.latitude[2]/3600 + self.latitude[1]/60 + self.latitude[0])



    #CONVERTS THE DIRECTION RELATIVE TO ANOUTHER (WHICH CAN END UP BEING NEGATIVE, OR GREATER THEN 360, TO ITS VALUE
    def reform_impossible_direction(self, direction):
            #
        if direction < 0:
            return direction + 360
        else:
            return direction % 360



    #REFERENCE LINES FOR VISUAL (CENTRE RELATIVE FRAME LINES PREVIOUSLY ADDED), THESE ARE OBJECTIVE
    def obtain_coordinate_system_line_positions(self):
        top = self.get_degree_at_y(0)
        left = self.get_degree_at_x(0)
        list = []

        #UP DOWN LINES
        degree_from_top_to_start = top % 15
        delta_y = 15*(self.y/self.VAOV)

        y_starting_point = (self.y/self.VAOV)*degree_from_top_to_start






        for y in range(int(y_starting_point), self.y, int(delta_y)):
            list.append([ (0, y), (self.x, y)])




        degree_from_left_to_start = left % 15
        delta_x = 15*(self.x/self.HAOV)

        x_starting_point = (self.x/self.HAOV)*degree_from_left_to_start

        for x in range(int(x_starting_point), self.x, int(delta_x)):
            list.append( [(x, 0), (x, self.y)])




        return list




    def convert_instances(self, key_point_instances, pred_box_instances):
        self.list_of_instances = []
        x = 0;
        for set_keypoints in key_point_instances:
            self.list_of_instances.append(four_tree(self, set_keypoints, pred_box_instances[x], x))
            x = x + 1


        self.db.setup_connection(self, False)









    def get_degree_at_y(self, y):
        #MEANING BELOW
        if y >= int(self.y/2):
            degree = self.tilt - (y - self.y/2)*(self.VAOV/self.y)
        else:
            degree = self.tilt + (self.y/2 - y)*(self.VAOV/self.y)
        return degree;

    def get_degree_at_x(self, x):


        #MEANING RIGHT
        if x >= int(self.x/2):
            degree = self.gps_direction + (x - self.x/2)*(self.HAOV/self.x)


        else:
            degree = self.gps_direction - (self.x/2 - x)*(self.HAOV/self.x)
        return degree






    def get_edge_of_old_box(self, x, bool_top):
        #NEGATIVE ROLL
        if self.roll <= 0:
            #IF LOOKING FOR TOP POINT
            if bool_top == True:

                #IF ON RIGHT SIDE OF IMAGE
                if x > self.old_corners[1][0]:
                    return abs(self.right_slope) * (x - self.old_corners[1][0])   #POSITIVE
                #IF ON LEFT SIDE
                else:
                    return self.old_corners[0][1] - (x * abs(self.left_slope))
            #LOOKING FOR BOTTOM POINT
            else:
                #IF ON RIGHT SIDE OF IMAGE
                if x > self.old_corners[3][0]:
                    return (self.old_corners[3][1]) - (abs(self.left_slope) * (x - self.old_corners[3][0]))
                #IF ON LEFT SIDE
                else:
                    return self.old_corners[0][1] + abs(self.right_slope) * x


        # Bottom                 Right,              Top,           Left
        #POSITIVE ROLL
        else:
            if bool_top == True:

                #IF ON RIGHT SIDE OF IMAGE
                if x > self.old_corners[2][0]:
                    return (x - self.old_corners[2][0]) * abs(self.right_slope)
                #IF ON LEFT SIDE
                else:
                    return self.old_corners[3][1] - (x * abs(self.left_slope))

            #LOOKING FOR BOTTOM POINT
            else:
                #IF ON RIGHT SIDE OF IMAGE
                if x > self.old_corners[0][0]:
                    return self.y - (x - self.old_corners[0][0]) * abs(self.left_slope)
                #IF ON LEFT SIDE
                else:
                    return self.old_corners[3][1] + x * abs(self.right_slope)

