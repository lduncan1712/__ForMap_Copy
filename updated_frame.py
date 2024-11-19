import random

from shapely.geometry import Point

import one_directory
import updated_fragment
from five_database import five_database


class updated_frame:

    #Holds:
        #id - index
        #coordinate x, y
        #left/right most angle

    def __init__(self, frame_id, x, y, left_angle, width, accuracy, time, updated_visual):

        # setting static data
        self.left_range = left_angle % 360
        self.right_range = (left_angle + width) % 360


        self.middle_average = (left_angle + width/2) % 360


        self.accuracy = accuracy
        self.frame_id = frame_id
        self.time = time
        self.width = width

        print(
            f" {self.frame_id - one_directory.starting_id}  {self.left_range}  {self.middle_average}  {self.right_range}")

        self.total_width_in_frame = 0

        new_x, new_y = five_database.omni_obtain_relative_position((x,y), updated_visual.corners)

        self.centre = (new_x, new_y)

        self.frame_lifetime = self.get_life_time(self.frame_id)

        # print(f"FRAME {self.frame_id} LIFE {self.frame_lifetime}")
        #
        # print(f" NEW FRAME:"
        #       f"    LR: {self.left_range}"
        #       f"    RR: {self.right_range}"
        #       f"    ACC: {self.accuracy}"
        #       f"    ID: {self.frame_id}"
        #       f"    TIME: {self.time}"
        #       f"    LOCATION: {str(self.centre)}")


        self.bound = Point(new_x,new_y).buffer(accuracy)



        self.fragments = []

        self.obtain_fragments()

        self.color = tuple([random.random() for _ in range(3)])






    def __str__(self):
        return print(f" NEW FRAME: {self.frame_id}   LR: {self.left_range} RR: {self.right_range}"
              f"    ACC: {self.accuracy} TIME: {self.time} LOCATION: {str(self.centre)}")


    #Returns The Range of Frame Connection
    def get_life_time(self, id):
        fd = five_database()

        value = [id, id]

        for amount_below in range(1, 50):

            connections = fd.translate_entire_photo(id - amount_below, id)

            if len(connections) == 0:
                break
            else:
                value[0] = id - amount_below


        for amount_above in range(1, 50):

            connections = fd.translate_entire_photo(id, id + amount_above)

            if len(connections) == 0:
                break
            else:
                value[1] = id + amount_above

        return value


    def get_angle_relative(self, a1, a2):

        diff, circular_diff = self.get_angle_difference(a1, a2)

        #MEANS NORMAL
        if diff <= 180: #self.width/2:



            if a1 >= a2:
                return circular_diff
            else:
                return -1*circular_diff
        else:
            if a1 > a2:
                return -1*circular_diff
            else:
                return circular_diff












        # # Adjust for circular range
        # circular_diff = min(diff, 360 - diff)
        #
        # return circular_diff

    def get_angle_difference(self, a1, a2):
        diff = abs(a1 - a2)

        # Adjust for circular range
        circular_diff = min(diff, 360 - diff)

        return diff, circular_diff




    def obtain_fragments(self):
        for frg in five_database.omni_obtain_fragments(self.frame_id):
            f = updated_fragment.updated_fragment(frg)

            #FIRST IS ONE RELATIVE TO SECOND
            f.middle_relative = self.get_angle_relative(f.p0_dir, self.middle_average)
            print(f" {f.middle_relative} ((({f.p0_dir}))")

            self.fragments.append(f)
            #CONTINUES BELOW BOTTOM RANGE