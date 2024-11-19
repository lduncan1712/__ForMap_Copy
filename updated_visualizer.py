from random import random

import numpy as np
from scipy.spatial import ConvexHull
from shapely.geometry import Polygon, LineString

import eigth_simple_frame
import one_directory
import updated_frame
from file_thirteen import file_thirteen
from five_database import five_database
import matplotlib.pyplot as plt

from updated_mover import updated_mover
from updated_polygons import updated_polygons


class updated_visualizer:


    def __init__(self):
        self.lof = []

        #Obtain Corner:
        self.corners = five_database.omni_obtain_plot_baseline(1, 100)

        print(f" CORNERS: {self.corners}")

        print("CONS:")
        print(five_database().translate_entire_photo(one_directory.starting_id + 0,
                                                   one_directory.starting_id + 2))

        #Sets Up List
        self.setup_list_of_photos()

        #Prints GPS values
        self.absolute_print_map()

        #-----------------------------------------------------------------------

        fig, ax = plt.subplots()


        # LOCATION TESTS
        if True:
            # COMPLEX
            # 0.9-2  (24)
            test_1 = [[1.3649962548191457, -4.931671180709142],
                      [0.4490092300141741, -3.5874047971315592],
                      [0.013720269757588097, -2.135615577396166],
                      [0.0, 0.0],
                      [-0.6960483304382913, 0.5704969717761484],
                      [-1.500922155513317, 2.0485049307984196],
                      [-2.216205208640084, 3.2452114139452743],
                      [-3.0724117923295555, 3.566521030682418],
                      [-3.434146364140133, 4.785390483708703]]
            # 0.9-2 (25.7)
            test_2 = [[1.3277839589653004, -4.741251808445405], [0.43768875449180294, -3.4433911864568505], [-0.009749791262657435, -1.8540275091448737], [0.0, 0.0], [-0.6960483304382913, 0.5704969717761484], [-1.4892877255060353, 2.024781359722126], [-2.2258583113672312, 3.1890109553274644], [-3.036151727700291, 3.5175683244562546], [-3.392620315332118, 4.783179632340688]]

            #0.8-10 (23.5)
            test_3 = [[1.2007837513963413, -4.305951308785925], [0.3956045193246917, -3.10709094873], [0.017786075635881957, -1.9040903173416939], [0.0, 0.0], [-0.6187090176248619, 0.5071092410796912], [-1.3000237831549706, 1.8725213140960644], [-2.0648926387542645, 3.06463112774668], [-2.892367528815511, 3.4024109906471116], [-3.2650680673298487, 4.739479528236388]]

            test_4 = [[1.3307184306442437, -4.649314546987351], [0.45625268561164684, -3.3843256646498343], [0.04215536209523566, -2.0300764892043737], [0.0, 0.0], [-0.6187090176248619, 0.5071092410796912], [-1.4008408971896595, 1.9425822797134125], [-2.1365226811672255, 3.101299694094057], [-2.9320337896468156, 3.4202879150341503], [-3.2844240806425975, 4.708927798061369]]

            test_5 = [[1.139991824027291, -4.200977918929169], [0.38227549893193336, -3.123547773868351], [0.02115560679049625, -1.9189632049484833], [0.0, 0.0], [-0.6187090176248619, 0.5071092410796912], [-1.2657555383627659, 1.8383128699597595], [-1.9830351904328556, 3.1147992368307817], [-2.941950110360542, 3.460359843936282], [-3.3249798705439555, 4.63772116545668]]

            test_6 = [[1.138022957624074, -4.205986082070967], [0.37965695476842765, -3.102224036189324], [0.02225257766736161, -1.9308545732620073], [0.0, 0.0], [-0.6187090176248619, 0.5071092410796912], [-1.2677323652744148, 1.8266589395921815], [-2.0425061796969253, 3.0485181175184204], [-2.875754406086907, 3.384544664440446], [-3.250917961394677, 4.737785215367742]]

            test_7 = [[1.0603763214015143, -3.7963186394216546], [0.37532754881599506, -2.7480697985597926], [0.07944528468378792, -1.795377201861677], [0.0, 0.0], [-0.43838551106877355, 0.36428370539984295], [-1.05585907814795, 1.4749596022715448], [-1.6392754118813295, 2.521033269305676], [-2.3942535357481263, 2.7866919372500045], [-2.696753414284731, 3.6833672169951424]]
            test_8 = [[1.0644457345840377, -3.734567588078839], [0.38732175853755546, -2.7460507992751224], [0.07755835046213341, -1.7527345365800906], [0.0, 0.0], [-0.44272240568979426, 0.36286709025362424], [-1.0251288587541678, 1.545396307993284], [-1.778289271909725, 2.716634947526883], [-2.5583447795624785, 3.0352793794996376], [-2.918665797303205, 4.29884384692507]]
            test_9 = [[1.4354374083700427, -5.005609152581565], [0.49022498505757167, -3.570885769842423], [0.07685681217632759, -2.200251068389163], [0.0, 0.0], [-0.5836105081273821, 0.4800957195414484], [-1.4583766456357876, 1.9161989953463952], [-2.1588423078921184, 3.0341791176097566], [-2.887823687616626, 3.3228021745649565], [-3.2091287970944613, 4.5112311355134445]]

            test_10 = [[-40,-40], [-30,-30], [-20,-20], [-10,-10],
                       [0,0], [10,10], [20,20], [30,30],
                       [40,40]]
            # NO COMPLEX

            test_11 = [[0.6114059536807671, -2.3348651072098847], [0.20982529873388556, -1.7164600260845073], [0.06540196583962636, -1.263470695818649], [0.0, 0.0], [-0.2753117842721129, -0.022979376755617217], [-0.5306964874097635, 0.8568232107632943], [-1.4602848737473764, 2.351807405958824], [-2.398510074146077, 2.756436751597755], [-2.8128288559948205, 4.202768001407584]]
            #09/06 - 8:52
            test_12 = [[1.3580715669535472, -4.8137224932731915], [0.49104187263725324, -3.577582465981862], [0.0785877015698492, -2.1198292463804673], [0.0, 0.0], [-0.5696989876715121, 0.5049289658830813], [-1.345973233784594, 1.9063267605492735], [-2.1598880474043187, 3.180114600063984], [-2.996351693386864, 3.510974772598875], [-3.379454555747742, 4.866764468270463]]


        test = test_12


        #CREATE POLYGONS
        uv = updated_polygons(self.lof, False, True, one_directory.care_about_complex)

        #CHANGING CONTANT INDEX (FOR MISMATCH CAUSED BY SIMPLE POLYGON
        if one_directory.automatic_placement:
            for index, val in enumerate(test):
                if val[0] == 0 and val[1] == 0:
                    uv.smallest_index = index

        #CREATING RELATIVE POLYGON
        um = updated_mover(uv.polygons, self.lof, uv.smallest_index)

        #Making Lines (USING STARTING POSITIONS)
        um.create_set_up(True)

        #SETUP ANGLES INVALID
        um.obtain_indexs_of_angle_invalid()

        start_not_necessarily_within = um.convert_location_to_tuple()

        #MOVES POINTS NOT WITHIN TO WITHIN
        um.create_polygon_set_up()

        to_print = []

        print(f"  STARTING LOCATIONS: {um.points_locations}")

        distances = []

        for iteration in range(0, one_directory.iterations_to_do):

            #IF AUTOMATIC (SIMPLY MOVE TO LOCATION)
            if one_directory.automatic_placement:
                movement_list = []
                for index, current in enumerate(um.points_locations):
                    d_y =  test[index][1] - current.y
                    d_x = test[index][0] - current.x
                    movement_list.append([d_x, d_y])


                um.move_all_segments_according_to_list(movement_list, um.index_to_use, ignore_bounds=True)

                movement_list, \
                number_of_polygons_failed, \
                dist_of_polygons = um.movement_elicated_from_all_polygons()

                movement_list_2, \
                total_distance, \
                num_inter, \
                num_failed = um.movement_elicated_from_all_intersections()

                print("START AT LOCATIONS:")
                print(um.points_locations)
                print("MOVEMENTS:")
                print(movement_list_2)
                print(f"-----------------------------------")

                lis = um.convert_location_to_tuple()

                print(
                        f" DIST: {total_distance} POL_DIST: {dist_of_polygons}  FAIL: {num_failed} POL_FAIL: {number_of_polygons_failed}  {lis}")

                p3 = um.points_locations

            #NOT AUTOMATIC
            else:
                #print("NOT AUTOMATIC")
                #MEANS START AT SELECTED LOCATION
                if one_directory.care_about_initial_position:

                    new = test
                else:

                    new = start_not_necessarily_within




                #FIRST MOVE BACK TO PRE_LOCATIONS
                movement_list = []
                for index, current in enumerate(um.points_locations):
                    d_y = new[index][1] - current.y
                    d_x = new[index][0] - current.x
                    movement_list.append([d_x, d_y])

                #um.index_to_use = 0
                #print(f" PREV: {um.points_locations}")
                um.move_all_segments_according_to_list(movement_list, um.index_to_use, ignore_bounds=True)
                #print(f" NEW POINTS: {um.points_locations}")
                if not one_directory.care_about_initial_position:

                    #PLACES THEM RANDOMLY WITHIN AGAIN
                    um.create_polygon_set_up()

                #MOVE
                um.iterate_to_location()

                p3 = um.points_locations.copy()

                movement_list_2, \
                total_distance, \
                num_inter, \
                num_failed = um.movement_elicated_from_all_intersections()

                distances.append(total_distance)


                new = []
                for val in p3:
                    new.append([val.x, val.y])

                print(new)
                to_print.append(p3)

        print(f"----------------------")
        print(f" FINALS:")
        print(distances)


        if one_directory.iterations_to_do == 1:




            # plt.xlim(-8, 5)
            # plt.ylim(-8, 8)



            #PRINTS LINES
            for index, tree in enumerate(um.tree_list):
                if len(tree.list_of_indexs) > 3:
                    segs = um.get_tree_segments(tree)

                    color = tree.color #self.get_tree_color(index)

                    for seg in segs:
                        x,y = seg.xy
                        plt.plot(x,y,color=color)

            #POINTS
            for index, point in enumerate(um.points_locations):
                plt.plot(point.x, point.y, marker="*")
                plt.text(point.x, point.y, f"{index}")

            #INTERSECTIONS
            for t_index, tree in enumerate(um.tree_list):
                if len(tree.list_of_indexs) > 1:

                    #NOTE ONLY GETS ONES WITH UNIQUE ENOUGH ANGLES!!!!!!!!!!!!!!
                    intersections, cyp, num_intersection, number_not_touching = um.obtain_intersection_list_from_segments(t_index)

                    non_shapely = []
                    for po in intersections:
                        non_shapely.append((po.x, po.y))

                    #USE POLYGONS
                    if False:
                        if len(non_shapely) < 3:
                            continue
                        pol = Polygon(non_shapely).convex_hull

                        x, y = pol.exterior.xy

                        xx, yy = pol.buffer(0.3).exterior.xy

                        plt.fill(x, y)
                        plt.plot(xx,yy,color="black", marker="*")

                    else:

                        for poi in intersections:
                            x,y = poi.buffer(0.15).exterior.xy



                            plt.fill(x,y,color=tree.color) #tree.color)

                    if len(intersections) == 0:
                        continue
                    else:

                        plt.text(non_shapely[0][0], non_shapely[0][1], f"{tree.starting_photo} - {tree.starting_photo + len(tree.list_of_indexs) - 1} -- {tree.list_of_indexs[0]}")


            #HIGHLIGHTS SPECIFIC FRAMES
            to_highlight = [5,6,7,8]

        else:
            fig, ax = plt.subplots()
            for set in to_print:
                # PRINTS POINTS
                for index in range(0, len(um.frames)):
                    col = um.get_frame_index_color(index)

                    plt.plot(set[index].x, set[index].y, color=col, marker="*")
                    plt.text(set[index].x, set[index].y, f"{index}")



        plt.show()


    # def get_tree_color(self, index):
    #     colors = [
    #         (255, 0, 0),  # Red
    #         (0, 255, 0),  # Green
    #         (0, 0, 255),  # Blue
    #         #(255, 255, 0),  # Yellow
    #         #(255, 0, 255),  # Magenta
    #         #(0, 255, 255),  # Cyan
    #         #(255, 128, 0),  # Orange
    #         (128, 0, 255),  # Purple
    #         (0, 128, 255),  # Light Blue
    #         (128, 255, 0),  # Lime Green
    #         (255, 0, 128),  # Rose
    #         (0, 255, 128),  # Teal
    #         (128, 128, 0),  # Olive
    #         (128, 0, 128),  # Purple 2
    #         (0, 128, 128),  # Grayish Blue
    #         (192, 192, 192),  # Light Gray
    #         (255, 165, 0),  # Orange 2
    #         (0, 255, 64),  # Green 2
    #         (255, 0, 64),  # Red 2
    #         #(64, 0, 255),  # Blue 2
    #         #(255, 64, 0),  # Vermilion
    #         (64, 255, 0),  # Spring Green
    #         (0, 64, 255),  # Cobalt Blue
    #         #(255, 128, 128),  # Salmon
    #         (128, 255, 128),  # Light Green
    #         (128, 128, 255),  # Light Violet
    #         (255, 128, 255),  # Pink
    #         (128, 255, 255),  # Sky Blue
    #         (255, 255, 128),  # Pale Yellow
    #         (128, 255, 255),  # Turquoise
    #         (255, 128, 128)  # Dark Pink
    #     ]
    #
    #     return colors[index]


    #Obtains All Photos Within Range (od.sr - od.er
    def setup_list_of_photos(self):
        print(five_database.omni_obtain_frames())
        # obtaining all frame from database (can be improved)
        for frame in five_database.omni_obtain_frames():
            # Assuming Id's Start With 0
            self.lof.append(
                updated_frame.updated_frame(frame[0], frame[1],
                                            frame[2], frame[3],
                                            frame[4], frame[5],
                                                      frame[6], self))







    #Prints All Points On Map
    def absolute_print_map(self):
        fig, ax = plt.subplots()

        for perspective_location in self.lof:

            #BOUND POLYGON POSSIBLE
            ax.fill(*perspective_location.bound.exterior.xy, color=perspective_location.color, alpha=0.1)
            plt.plot(*perspective_location.bound.exterior.xy, color=perspective_location.color)

            #EXACT LOCATION
            loc = perspective_location.centre
            plt.plot(loc[0], loc[1], marker="o", color=perspective_location.color)

            #TEXT
            plt.text(loc[0], loc[1], "ID " + str(perspective_location.frame_id - one_directory.starting_id), fontsize=12, color='red')


        self.absolute_time_filter()

        for perspective_location in self.lof:
            #BOUND POLYGON POSSIBLE
            ax.fill(*perspective_location.bound.exterior.xy, color=perspective_location.color, alpha=0.1)
            plt.plot(*perspective_location.bound.exterior.xy, color=perspective_location.color)

        plt.grid()


    def absolute_time_filter(self):

        for outer_index, outer_frame in enumerate(self.lof):
            # For every frame within
            for inner_index, inner_frame in enumerate(self.lof):
                #Diagonalization to avoid repitition or equality
                if outer_index > inner_index:



                    # Max possible distance appart (time distance)
                    distance = abs(outer_frame.time - inner_frame.time)*one_directory.speed_per_second

                    # Creates buffered Distances extending
                    fo_e = outer_frame.bound.buffer(distance)
                    fi_e = inner_frame.bound.buffer(distance)

                    # The new frame 1 possibilities are the overlap between f1, original, and f2_e
                    outer_frame.bound = outer_frame.bound.intersection(fi_e)
                    # The new frame 2 possibilities are the overlap between f2 original and f1_1


                    inner_frame.bound = inner_frame.bound.intersection(fo_e)

    def start_lines(self):
        fig, ax = plt.subplots()

        #um = updated_mover(True, self.lof)

        for index, perspective_location in enumerate(um.points_locations):

            #EXACT LOCATION
            loc = perspective_location
            plt.plot(loc.x, loc.y, marker="o", color="black")

            #TEXT
            plt.text(loc.x, loc.y, "ID " + str(index), fontsize=12, color='blue')


        um.iterate_to_location(plt)

        for index, perspective_location in enumerate(um.points_locations):

            #EXACT LOCATION
            loc = perspective_location
            plt.plot(loc.x, loc.y, marker="o", color="black")

            #TEXT
            plt.text(loc.x, loc.y, "ID " + str(index), fontsize=12, color='red')


        for tree in um.tree_list:
            segs = um.get_tree_segments(tree)
            # if len(segs) < 3:
            #     continue

            for index, seg in enumerate(segs):
                #if index + tree.starting_photo - one_directory.starting_id < 4:
                if True:
                    x,y = seg.xy
                    plt.plot(x,y,color=tree.color)







        plt.show()











    def relative_print_lines(self):

        fig, ax = plt.subplots()


        plt.grid()
        print("AAHA")
