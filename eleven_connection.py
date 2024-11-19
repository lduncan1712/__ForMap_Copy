import math
import time
import matplotlib.colors as colors
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.patches import Wedge
from shapely.geometry import Point, LineString, Polygon
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np
import nine_fragment
import one_directory
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from shapely.geometry import Polygon

from file_thirteen import file_thirteen
from five_database import five_database

class eleven_connection:




    #TO BE USED FOR MEAT AND POTATOS
    def __init__(self, ts, f1, f2, polygon, connections, lof):
        self.ts = ts
        self.f1 = f1
        self.f2 = f2
        self.list_of_frames = lof




        if True:

            # for outer_index in range(0, len(self.list_of_frames)):
            #     row = []
            #     for inner_index in range(0, len(self.list_of_frames)):
            #         if inner_index > outer_index:
            #             polygon = self.ts.create_direct_polygon(self.list_of_frames[outer_index], self.list_of_frames[inner_index], False, False,
            #                                                  True, True)
            #             row.append(polygon)
            #         else:
            #             row.append(0)

            global formal_list
            formal_list = []

            #Making List
            self.ts.create_formal_list(self.list_of_frames)
            print("DONE FORMAL LIST")
            print(self.ts.formal_list)

            ft = file_thirteen(self, self.ts.formal_list, self.list_of_frames)
            ft.make_master_list()




            #print("DONE")
            #self.ts.omni_filter(self.list_of_frames[0].frame_id,
            #                                   self.list_of_frames[1].frame_id)
            # print("AFFTER OMNI")
            #
            #a = self.ts.create_simple_relative_polygon(self.list_of_frames[1], self.list_of_frames[2], True, False, True)

            #b = self.ts.create_simple_relative_polygon(self.list_of_frames[2], self.list_of_frames[1], False, True, True)

            # x, y = b.exterior.xy
            # self.ts.plot_perspective.plot(x, y, color="blue", marker="o")



            #x, y = a.exterior.xy
            #self.ts.plot_perspective.plot(x, y, color="red", marker="*")

            #self.ts.create_cascaded_polygons(self.list_of_frames[0], True)


        else:
            self.solve_attempt((1.5138753922815722, -0.9095622563311929), 'red')

    #Makes All Points That Within Range Of Overlapping







    def print_p(self, poly, color):
        x,y = poly.exterior.xy
        self.ts.plot_perspective.plot(x,y, color=color, marker="*")






    #Attempts to solve at a specific position
    def solve_attempt(self, to_try, color):
        #Make Line Segments
        self.f2.make_set_line_segments(to_try, 0, True)

        self.ts.solve_attempt_visuals(to_try, 'red')





        # Makes intersections
        intersections = self.build_intersections(to_try)

        # Adds Non-Relative Traits
        intersections = self.build_non_rel_traits(intersections)

        # Adds Delta Measurements
        intersections = self.build_delta(intersections)

        #self.opportunity_to_disregard(self.frame1, self.frame2, perspect1, perspect2, intersections )







        # Filter By Widths (NEEDS TO BE UPDATED FOR COVERED)      (SINGLE WIDTH)
        intersections = self.filter_by_width(intersections, 0.25)

        #Filters by Delta (NEEDS TO BE UPDATED FOR COVERED)   (SINGLE DELTA)
        intersections = self.filter_by_deltas(intersections, 2 )

        intersections = self.filter_by_extreme_difference(intersections, 20)






        # Adds Relative Traits (RELATIVE COMPADABILITY WITH OTHERS, NEEDED BEFORE
        intersections = self.build_rel_traits(intersections, False, to_try)

        # global chain_sub_list
        # chain_sub_list = []
        #
        # self.make_all_possibilities(intersections, 0, [])
        #
        # # Filters Items Based On Percieved Height/Base
        # filtered_combo = self.combo_filter_by_height(intersections, chain_sub_list)
        #
        # max = 0
        # for combo in filtered_combo:
        #     print(combo)
        #     val = self.test_max_count(combo)
        #     if val > max:
        #         max = val



        #weight, actual = self.obtain_best_comb(filtered_combo, intersections)
        #print(v)



        #return max



        self.ts.visualize_hills_in_board(intersections)
        self.ts.visualize_intersections(intersections)
        self.ts.visualize_checker(intersections)
        self.ts.visualize_hills(intersections)
        self.ts.visualize_stock(1, intersections)

        # #
        # #self.unvisualize()

        #NEED TO RETURN THE TOP COMBOS AND THEIR EFFICIENCYS


        #return actual, weight, intersections


    #CREATES LIST OF INTERSECTIONS
    def build_intersections(self, position_to_try):
        intersections = []
        for one_index, one_fragment in enumerate(self.f1.fragments):
            frame_1_one_fragments_intersections = []
            for two_index, two_fragment in enumerate(self.f2.fragments):

                #IF THIS INDEX BLACKLISTED
                if self.ts.system_blacklist[one_index][two_index] == 0:
                    frame_1_one_fragments_intersections.append([-1])
                    continue

                # Assuming segments are already made
                sect = one_fragment.current_line_segment.intersection(two_fragment.current_line_segment)

                if sect.is_empty:
                    # No Intersection
                    frame_1_one_fragments_intersections.append([0])
                else:
                    # Intersection occurs
                    s = (round(sect.x,5), round(sect.y,5))  #1
                    dist_from_1 = round(one_fragment.get_distance_between_points((0, 0), s), 5)  #2
                    dist_from_2 = round(two_fragment.get_distance_between_points(position_to_try, s), 5)  #3

                    data = [1, s, dist_from_1, dist_from_2]

                    frame_1_one_fragments_intersections.append(data)
            intersections.append(frame_1_one_fragments_intersections)
        return intersections

    def build_non_rel_traits(self, intersections):


        for index_1, single_1 in enumerate(intersections):

            for index_2, box in enumerate(intersections[index_1]):

                if box[0] == -1 or box[0] == 0:
                    continue

                should_be_width1 = round(self.f1.fragments[index_1].calculate_rad_at_distance(box[2]), 5)
                should_be_width2 = round(self.f2.fragments[index_2].calculate_rad_at_distance(box[3]), 5)

                ratio = round(should_be_width1 / should_be_width2, 5)

                box.append(round(should_be_width1,2))   #4
                box.append(round(should_be_width2,2))    #5
                box.append(round(ratio, 2))  #6


                angle_bound_1 = self.tolerated_error_bound_at_distance(1, box[2], self.f1.fragments[index_1].base_d)
                angle_bound_2 = self.tolerated_error_bound_at_distance(1, box[3], self.f2.fragments[index_2].base_d)

                actual_1 = round(self.calculate_height_relative_to_camera(box[2],self.f1.fragments[index_1].base_d, 0),2)
                lower_1 = round(self.calculate_height_relative_to_camera(box[2],self.f1.fragments[index_1].base_d - angle_bound_1, 0),2)
                upper_1 = round(self.calculate_height_relative_to_camera(box[2],self.f1.fragments[index_1].base_d + angle_bound_1, 0),2)

                actual_2 = round(self.calculate_height_relative_to_camera(box[3], self.f2.fragments[index_2].base_d, 0),2)
                lower_2 = round(self.calculate_height_relative_to_camera(box[3], self.f2.fragments[index_2].base_d - angle_bound_2, 0),2)
                upper_2 = round(self.calculate_height_relative_to_camera(box[3], self.f2.fragments[index_2].base_d + angle_bound_2, 0),2)

                r1 = (upper_1, actual_1, lower_1)
                r2 = (upper_2, actual_2, lower_2)

                box.append(r1)  #7
                box.append(r2)  #8

                box.append([])  #9

                box.append([0,0,0,0,0,0])  #10

                box.append(0)

        return intersections


    def build_rel_traits(self, intersections, prohibit_same, to_try):

        for row_index_outer, row in enumerate(intersections):

            for column_index_outer, box in enumerate(row):

                #IF BOX IS A MATCH
                if box[0] == 1:



                    #----------------------------------------------------------
                    #PERHAPS BY INTERSECTION THAT IT CANT BE COMPADABLE WITH FOR SIZE REASONS
                    #---------------------------------------------------------------

                    for row_index_inner, inner_row in enumerate(intersections):
                     for column_index_inner, inner_box in enumerate(inner_row):
                         if (row_index_inner != row_index_outer) and (column_index_inner != column_index_outer) and inner_box[0] == 1:

                             return intersections
        return intersections


        return intersections


    #Returns the worst and best case height differences
    def maximum_minimum_difference_between_points(self, p1, p2):
        pot1 = p1[0] - p2[2]
        pot2 = p1[2] - p2[0]
        av = p1[1] - p2[1]

        return (pot1, av, pot2)



    def filter_by_extreme_difference(self, intersections, extreme):
        #BASIS IDEA
        #ASSUEM MAXOMU HEIGHT DIFFERENT OF FRAMEPER SECOND
        for row_index, row in enumerate(intersections):

            for column_index, box in enumerate(row):

                #CHECKS VALID
                if box[0] == 1:
                    (max, av, min) = self.maximum_minimum_difference_between_points(box[7], box[8])

                    #ABOVE THRESHHOLD
                    if (max > extreme and av > extreme and min > extreme) or \
                            (max < -1*extreme and av < -1*extreme and min < -1*extreme):
                        box[0] = box[0] + 15
                    else:
                        continue
        return intersections

   # Filters by Huge Width Discrepencies  (NEEDS UPDATE FOR OVERLAP)
    def filter_by_width(self, intersections, fraction_accepted):

        for row_index, row in enumerate(intersections):

            for column_index, box in enumerate(row):

                #CHECKS VALID
                if box[0] == 0 or box[0] == -1:
                    continue

                #CONFIRMED TO WORTH CONSIDER
                else:
                    #IF WITHIN VALID RANGE
                    if (1 - fraction_accepted)*(1 - fraction_accepted) <= box[6] <= (1 + fraction_accepted)*(1 + fraction_accepted):
                        continue

                    #TOO DRASTIC CHANGE
                    else:
                        box[0] = box[0] + 3
                        box[10][0] = 1
        return intersections


    # Filter by deltas
    def filter_by_deltas(self, intersections, tolerance):

        for ind1, row in enumerate(intersections):
            for ind2, box in enumerate(row):
                if box[0] == 1:
                    # IF DELTA IS NOT
                    if (1 - tolerance) <= box[11] <= (1 + tolerance):
                        box[10][0] = box[10][0]  # FILLER
                    else:
                        box[0] = box[0] + 11

        return intersections


 #Observes the changes in expected width, compared to real
    def obtain_delta_measurement(self, box, ind1, ind2):
        # FIRST ORDER OF BUSINESS, IF NOT INVERTED, OR EVEN CLOSE, GET RID OF

        starting_width = self.f1.fragments[ind1].width_d/2
        ending_width = self.f2.fragments[ind2].width_d/2

        starting_distance = box[2]
        ending_distance = box[3]

        starting_size = box[4]
        ending_size = box[5]

        #print(f" {ind1} {ind2}    W: {starting_width}   {ending_width}      D: {starting_distance}  {ending_distance}       S: {starting_size}   {ending_size}")

        angle2_actual = ending_width

        angle2_projected = math.degrees(math.atan((starting_size/ending_distance)))

        #print(f" {ind1} {ind2}  {starting_distance}  {ending_distance}   {starting_size}  {ending_size}                {angle2_actual}   {angle2_projected}  ((({math.pow((abs(angle2_actual - angle2_projected)),0.5)/(angle2_actual + angle2_projected)}")






        #print(f"F                D: {angle2_projected/angle2_actual}")
        return angle2_actual/angle2_projected


#Applies this fraction to intersections
    def build_delta(self, intersections):
        for ind1, row in enumerate(intersections):
            for ind2, box in enumerate(row):
                if box[0] == 1:
                    box[11] = self.obtain_delta_measurement( box, ind1, ind2)
        return intersections


    #Returns the tolerates Error Angle At Given Distance
    def tolerated_error_bound_at_distance(self, k, distance, starting_angle):


        a = 20
        b = 1
        c = 0.5

        angle_dev =  a/   (distance*b + c*abs(-90 - starting_angle))

        #angle_dev = (1/distance)  * (1/(abs(-90 - starting_angle)))

        #angle_dev = math.pow(abs(starting_angle),1.1)*(math.pow(distance,-0.8))


        av = round(self.calculate_height_relative_to_camera(distance, starting_angle, 0),2)


        return angle_dev

    #Calculates how low it will be relative to camera
    def calculate_height_relative_to_camera(self, distance_from_frame, angle_of_base, optional_camera_height):
        return distance_from_frame * math.tan(math.radians(angle_of_base))
