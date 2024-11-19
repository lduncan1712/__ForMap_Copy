import math
import random

from matplotlib import pyplot as plt
from shapely.affinity import translate
from shapely.geometry import LineString, Point, Polygon

import one_directory
from five_database import five_database
from fixed_point import fixed_point


from shapely.ops import nearest_points



class updated_mover:

    # Obtains the segments of a corasponding tree
    def get_tree_segments(self, tree):
        list_to_return = []
        starting_index = tree.starting_photo - one_directory.starting_id

        for index, value in enumerate(tree.list_of_indexs):
            list_to_return.append(self.fragments_locations[index + starting_index][value])

        return list_to_return

    # Given f1, f2, and end_range, creates tree objects
    # MAKES A SET OF TREES
    def create_trees(self, frame1, frame2, range_end):
        master_tree_list = []
        fd = five_database()

        # Create Simple First
        # (Trees That Appear In First)
        for first_index_values in range(0, len(frame1.fragments)):
            tree = fixed_point()
            val = tree.create_and_cascade(frame1.frame_id, first_index_values)
            master_tree_list.append(tree)

        # Create Complex Later
        # (Trees Thats Appear Later, but arnt already covered)
        for later_index_values in range(frame2.frame_id, range_end + 1):

            direct_connections = fd.translate_entire_photo(later_index_values - 1,
                                                           later_index_values)
            prev_ind_list = []
            curr_ind_list = []
            for conn in direct_connections:
                prev_ind_list.append(conn[0])
                curr_ind_list.append(conn[1])

            frame = self.frames[later_index_values - one_directory.starting_id]

            for later_index_fragment in range(0, len(frame.fragments)):
                if not later_index_fragment in curr_ind_list:
                    tree = fixed_point()
                    val = tree.create_and_cascade(later_index_values, later_index_fragment)
                    master_tree_list.append(tree)

        return master_tree_list

    # creates a list holding lists, where all indexs in each index, tell which trees exist during which frames
    def ledger_from_trees(self):

        ledger = []

        # Creates A List For Every Frame
        for photo_index in range(0, len(self.frames)):
            ledger.append([])

        # Adds Tree Indexs, to whatever frames they occur in
        for index, tree in enumerate(self.tree_list):
            for after in range(0, len(tree.list_of_indexs)):
                ledger[after + tree.starting_photo - one_directory.starting_id].append(index)
        return ledger



    def __init__(self, formal_list_polygon, formal_list_frames, index_to_use):
        # Sets Frames (as given list)
        self.frames = formal_list_frames

        self.index_to_use = index_to_use

        # Sets Polygons Of Frames
        self.polygon_maps = formal_list_polygon

        # Creates The List Of Tree Lines
        self.tree_list = self.create_trees(self.frames[0], self.frames[1],
                                           len(self.frames) - 1 + one_directory.starting_id)

        # Creates A List Of Which Trees Exist During Which Frames
        self.ledger = self.ledger_from_trees()

        # Where Points Are
        self.points_locations = []
        # Where Fragments Are
        self.fragments_locations = []







    def create_set_up(self, print_copy_first):

        for index in range(0, len(self.frames)):
            self.points_locations.append(0)


        # Establishing First
        starting_point = self.frames[self.index_to_use].centre
        self.points_locations[self.index_to_use] = Point(0, 0)

        # Locate Every Other Point
        for next_photo_index in range(0, len(self.frames)):

            if next_photo_index != self.index_to_use:


                next_location = self.frames[next_photo_index].centre
                # Now Making Location Relative To Polygons
                next_location = Point(next_location[0] - starting_point[0],
                                  next_location[1] - starting_point[1])

                # next_location = [next_photo_index * 30, next_photo_index * 30]

                self.points_locations[next_photo_index] = next_location


                # IF NOT WITHIN (PROBL IMPOSSIBLE TO GET ON RIGHT TRACK??

        # Creating According Line Segments // Angles
        for index, photo in enumerate(self.frames):

            row_list = []
            angle_list = []

            # Location To Start From
            starting_location = self.points_locations[index]

            for fragment in photo.fragments:
                close_point = self.move_random_along_angle(fragment.p0_dir,
                                                           fragment.min_dist,
                                                           starting_location)
                far_point = self.move_random_along_angle(fragment.p0_dir,
                                                         fragment.max_dist,
                                                         starting_location)
                linestring = LineString([close_point, far_point])

                row_list.append(linestring)
                angle_list.append(fragment.p0_dir)

            self.fragments_locations.append(row_list)


    def reverse_polygon(self, polygon):
        coords = []

        for soc in list(polygon.exterior.coords):
            coords.append((soc[0]*-1, soc[1]*-1))

        return Polygon(coords)

    def create_polygon_set_up(self):
        self.polygon_to_remain_within = []



        for index in range(0, len(self.frames)):
            if index == self.index_to_use:
                self.polygon_to_remain_within.append(0)
                continue
            else:

                pol = self.polygon_maps[self.index_to_use][index]

                if not index > self.index_to_use:
                    pol = self.reverse_polygon(self.polygon_maps[index][self.index_to_use])

                self.polygon_to_remain_within.append(pol)


                poi = self.points_locations[index]


                if pol.contains(poi):

                    #plt.plot(poi.x, poi.y, color=self.get_frame_index_color(index), marker="*")
                    continue

                #MEANS POINT NOT WITHIN
                else:

                    exter = list(pol.exterior.coords)
                    #OBTAINS 4 UNIQUE POINTS INDEXS

                    #NEEDS TO ACCOUNT WHEN LESS THEN 4 POINTS???


                    ui = random.sample(range(0, len(exter)), 4)


                    #CREATES 2 LINESEGMENTS

                    av_x = (exter[ui[0]][0] + exter[ui[1]][0] + exter[ui[2]][0] + exter[ui[3]][0]) / 4
                    av_y = (exter[ui[0]][1] + exter[ui[1]][1] + exter[ui[2]][1] + exter[ui[3]][1]) / 4

                    new_p = Point(av_x, av_y)

                    #plt.plot(new_p.x, new_p.y, color=self.get_frame_index_color(index), marker="*" )

                    diff_x = av_x - poi.x
                    diff_y = av_y - poi.y

                    new_list_of_segs = []

                    for old_seg in self.fragments_locations[index]:
                        a = self.move_line_segment(old_seg, diff_x, diff_y)
                        new_list_of_segs.append(a)


                    self.fragments_locations[index] = new_list_of_segs
                    self.points_locations[index] = new_p










    #START IS BLACK
    def get_frame_index_color(self, index):
        if index == 0:
            return "black"
        elif index == 1:
            return "purple"
        elif index == 1:
            return "indigo"
        elif index == 1:
            return "blue"
        elif index == 4:
            return "green"
        elif index == 5:
            return "yellow"
        elif index == 6:
            return "orange"
        elif index == 7:
            return "red"
        elif index == 8:
            return "brown"
        else:
            return "silver"


                # Method that returns a point in a given direction, and distance from starting

    def move_random_along_angle(self, angle, absolute, xy):
        angle = math.radians(angle)
        dx = absolute * math.sin(angle)
        dy = absolute * math.cos(angle)

        return (dx + xy.x, dy + xy.y)

    def move_line_segment(self, linesegment, x, y):
        coords_to_add = []
        for coord in list(linesegment.coords):
            coords_to_add.append((coord[0] + x, coord[1] + y))

        return LineString(coords_to_add)

    def move_point(self, point, x, y):
        return Point(point.x + x, point.y + y)

    #THE INTERSECTION OF SPACE BETWEEN PERSEPCIVES WITH GIVEN LOCATION
    def get_control_polygon(self, index):

        pol = 0

        for i in range(0, len(self.frames)):
            if i == index:
                continue

            perspective = self.get_active_pol(i, index)

            if pol == 0:
                pol = perspective
            else:
                pol = pol.intersection(perspective)

        return pol

    # Moves Location Of Segments At Each Index According To List
    #AND MOVES LOCATION OF POINTS
    def move_all_segments_according_to_list(self, movement, index_to_ignare, ignore_bounds):


        for index, movement in enumerate(movement):


            if index == index_to_ignare:
                continue

            poly = self.polygon_to_remain_within[index].buffer(0)
            previous_location = self.points_locations[index]
            new_location_to_try = self.move_point(self.points_locations[index], movement[0], movement[1])

            total_polygon = 0

            #IF NOT WITHIN
            #BASIC IDEA
            if not poly.contains(new_location_to_try):


                closest_point_geometry1, ignore = nearest_points(poly, new_location_to_try)

                #IDEA FIND THE CLOSEST POINT WITHIN THE POLYGON TO THE POINT TO TRY TO


                if not ignore_bounds:
                    movement[0] = closest_point_geometry1.x - previous_location.x
                    movement[1] = closest_point_geometry1.y - previous_location.y

                    new_location_to_try = closest_point_geometry1



            self.points_locations[index] = new_location_to_try


            list_to_return = []


            for segment_index, individual_tree_segment in enumerate(self.fragments_locations[index]):
                list_to_return.append(self.move_line_segment(individual_tree_segment, movement[0], movement[1]))
            self.fragments_locations[index] = list_to_return





    def iterate_to_location(self):
        #prev = 1000000
        #fig, ax = plt.subplots()
        distance_to_be_asertained = []


        for it_num in range(0, 1000):

            # if it_num % 2 == 1:
            #     one_directory.method_of_tree_weighting = 0
            # else:
            #     one_directory.method_of_tree_weighting = 1

            movement_list, \
            number_of_polygons_failed, \
            dist_of_polygons =       self.movement_elicated_from_all_polygons()

            movement_list_2, \
            total_distance, \
            num_inter, \
            num_failed = self.movement_elicated_from_all_intersections()

            lis = self.convert_location_to_tuple()




            print(f" DIST: {total_distance} POL_DIST: {dist_of_polygons}  FAIL: {num_failed} POL_FAIL: {number_of_polygons_failed}  {lis}")


            if it_num < 500 or it_num % 5 == 1:
                self.move_all_segments_according_to_list(movement_list, self.index_to_use, True)
                #plt.plot(it_num, total_distance, color="red",marker="o")


            else:

                #plt.plot(it_num, total_distance, color="green", marker="o")

                self.move_all_segments_according_to_list(movement_list_2, self.index_to_use, True)



        #TESTING OUT

        # fig, ax = plt.subplots()
        #
        # for index in range(0, len(self.frames)):
        #
        #     plt.plot(self.points_locations[index].x,
        #              self.points_locations[index].y,
        #              color=self.frames[index].color,
        #              marker="o")
        #     for inner_index in range(0, len(self.frames)):
        #         if index == inner_index:
        #             continue
        #         pol = self.get_active_pol(index, inner_index)
        #
        #         x,y = pol.exterior.xy
        #         plt.plot(x,y,color=self.frames[inner_index].color)




    def convert_location_to_tuple(self):
        new = []
        for index, current in enumerate(self.points_locations):
            new.append([current.x, current.y])
        return new





    #IDEA, IF A GIVEN POINT IS WITHIN THE OTHERS POLYGON, GOOD, ELSE MOVE TOWARDS IT FOR ALL
    def movement_elicated_from_all_polygons(self):

        total_fails = 0
        to_dist = 0

        #MAKING INFORMATION STORAGE
        movement_total = []
        movement_denom = []
        for index in range(0, len(self.frames)):
            movement_total.append([0,0])
            movement_denom.append(0)

        #For Every Existing Point
        for point_index, point_location in enumerate(self.points_locations):

            #From Every other index, the Point needs to be within the polygon gained by P
            for polygon_index in range(0, len(self.points_locations)):
                if point_index != polygon_index:

                    polygon_this_point_needs_to_be_within = self.get_active_pol(polygon_index, point_index)

                    #MEANS POINT ALREADY WITHIN DESIRED
                    #IDEA BRING CLOSER TO CENTERS (TO PREVENT TIP TOUCHING)
                    if polygon_this_point_needs_to_be_within.contains(point_location):
                        continue
                    #POINT NOT WITHIN POLYGON
                    #IDEA MOVE TOWARD EACH OTHER
                    else:

                        #Need To Find Closest Point To It, To Then Determine Desired Movement
                        point_that_needs_to_be_within_polygon = point_location

                        closest_point_to_this_point, ignore = nearest_points(polygon_this_point_needs_to_be_within,
                                                                             point_that_needs_to_be_within_polygon)

                        #MOVEMENT OF POINT ---> POLYGON
                        x_move = closest_point_to_this_point.x - point_that_needs_to_be_within_polygon.x
                        y_move = closest_point_to_this_point.y - point_that_needs_to_be_within_polygon.y

                        #SCALING
                        if True:
                            val = one_directory.wiggle_distance

                            #Print NEED TO UPDATE

                            if x_move > 0:
                                x_move += val
                            else:
                                x_move -= val

                            if y_move > 0:
                                y_move += val
                            else:
                                y_move -= val


                            x_move *= 0.5
                            y_move *= 0.5

                        movement_total[point_index][0] += x_move
                        movement_total[point_index][1] += y_move

                        movement_total[polygon_index][0] -= x_move
                        movement_total[polygon_index][1] -= y_move

                        movement_denom[point_index] += 1
                        movement_denom[polygon_index] += 1

                        total_fails += 1
                        to_dist += math.sqrt(x_move**2 + y_move**2)





        #REformat Move
        new_list = []

        for index, movement in enumerate(movement_total):
            if movement_denom[index] != 0:
                new_list.append([movement[0]/movement_denom[index], movement[1]/movement_denom[index]])
            else:
                new_list.append([movement[0], movement[1]])


        return new_list, total_fails, to_dist







    def movement_elicated_from_all_intersections(self):

        movement_total = []
        movement_denom = []
        for index in range(0, len(self.frames)):
            movement_total.append([0, 0])
            movement_denom.append(0)

        total_valuable = 0
        total_missed = 0

        total_distance = 0


        #FOR EVERY TREE
        for t_index, tree in enumerate(self.tree_list):
            #print(t_index)
            #IF IT HAS LINES TO INTERSECT
            if len(tree.list_of_indexs) >= one_directory.minimum_number_of_segs:

                intersection_list, \
                intersection_cypher, \
                num_good, \
                num_failed = self.obtain_intersection_list_from_segments(t_index)

                total_valuable+=num_good
                total_missed+=num_failed

                #CREATE MOVEMENT FROM INTERSECTIONS
                for intersection_one_index, intersection_one in enumerate(intersection_list):
                    for intersection_two_index, intersection_two in enumerate(intersection_list):
                        #IF MORE
                        if intersection_one_index < intersection_two_index:

                            #GOING FROM ONE TO TWO
                            x_movement_from_one_to_two = intersection_two.x - intersection_one.x
                            y_movement_from_one_to_two = intersection_two.y - intersection_one.y

                            total_distance += math.sqrt(x_movement_from_one_to_two**2 + y_movement_from_one_to_two**2)

                            if True:
                                scalar = one_directory.distance_exponent

                                if x_movement_from_one_to_two > 0:
                                    x_movement_from_one_to_two = math.pow(x_movement_from_one_to_two, scalar)
                                else:
                                    x_movement_from_one_to_two = -1*math.pow(abs(x_movement_from_one_to_two), scalar)



                                if y_movement_from_one_to_two > 0:
                                    y_movement_from_one_to_two = math.pow(y_movement_from_one_to_two, scalar)
                                else:
                                    y_movement_from_one_to_two = -1*math.pow(abs(y_movement_from_one_to_two), scalar)


                                x_movement_from_one_to_two *= 0.5
                                y_movement_from_one_to_two *= 0.5

                                method = one_directory.method_of_tree_weighting

                                #ALL EVERY TREE EQUAL
                                if method == 1:
                                    x_movement_from_one_to_two /= len(intersection_list)
                                    y_movement_from_one_to_two /= len(intersection_list)

                                if method == 2:
                                    x_movement_from_one_to_two /= len(intersection_list)
                                    y_movement_from_one_to_two /= len(intersection_list)

                                    x_movement_from_one_to_two *= len(tree.list_of_indexs)
                                    y_movement_from_one_to_two *= len(tree.list_of_indexs)


                            cypher_one = intersection_cypher[intersection_one_index]
                            cypher_two = intersection_cypher[intersection_two_index]

                            # movement_total[cypher_one[0]][0] += x_movement_from_one_to_two
                            # movement_total[cypher_one[1]][1] += y_movement_from_one_to_two
                            #
                            # movement_total[cypher_two[0]][0] -= x_movement_from_one_to_two
                            # movement_total[cypher_two[1]][1] -= y_movement_from_one_to_two

                            #ORIG (ABOVE)
                            #ALL (BELOW)

                            # movement_total[cypher_one[0]][0] += x_movement_from_one_to_two
                            # movement_total[cypher_one[0]][1] += y_movement_from_one_to_two
                            #
                            # movement_total[cypher_one[1]][0] += x_movement_from_one_to_two
                            # movement_total[cypher_two[1]][1] += y_movement_from_one_to_two
                            #
                            # movement_total[cypher_two[0]][0] -= x_movement_from_one_to_two
                            # movement_total[cypher_two[0]][1] -= y_movement_from_one_to_two
                            #
                            # movement_total[cypher_two[1]][0] -= x_movement_from_one_to_two
                            # movement_total[cypher_two[1]][1] -= y_movement_from_one_to_two

                            ind1 = random.randint(0, 1)
                            ind2 = random.randint(0, 1)


                            movement_total[cypher_one[ind1]][0] += x_movement_from_one_to_two
                            movement_total[cypher_one[ind1]][1] += y_movement_from_one_to_two

                            movement_total[cypher_two[ind2]][0] -= x_movement_from_one_to_two
                            movement_total[cypher_two[ind2]][1] -= y_movement_from_one_to_two



                            if method == 1:
                                denominator = 1/len(intersection_list)

                            elif method == 2:
                                denominator = (1/len(intersection_list))*len(tree.list_of_indexs)
                            else:
                                denominator = 1


                            movement_denom[cypher_one[0]] += denominator
                            movement_denom[cypher_one[1]] += denominator

                            movement_denom[cypher_two[0]] += denominator
                            movement_denom[cypher_two[1]] += denominator


        new_list = []

        #print(f"    INTERSECTIONS:  TOT GOOD: {total_valuable}  MISSED: {total_missed}  ANGLE:{total_angle_removed}  DIST: {total_distance} ({total_distance/(total_valuable + total_missed)}")

        for index, movement in enumerate(movement_total):
            if movement_denom[index] != 0:
                new_list.append([movement[0] / movement_denom[index], movement[1] / movement_denom[index]])
            else:
                new_list.append([movement[0], movement[1]])

        return new_list, total_distance, total_valuable, total_missed

    def movement_elicated_from_all_lines(self, index):
        tree = self.tree_list[index]
        segs = self.get_tree_segments(tree)

        movement_total = []
        movement_denom = []
        for index in range(0, len(self.frames)):
            movement_total.append([0, 0])
            movement_denom.append(0)

        non_intersection_cypher = []
        #MAKE NON INTERSECTIONS
        for outer_index, outer_seg in enumerate(segs):
            for inner_index, inner_seg in enumerate(segs):
                if outer_index < inner_index:
                    inter = outer_seg.intersection(inner_seg)

                    # IF INTERSECTS
                    if not inter.is_empty:
                        continue
                    #DOESNT SO VALUABLE
                    else:
                        non_intersection_cypher.append([outer_index, inner_index])

        #

    def obtain_intersection_list_from_segments(self, index):
        # OBTAIN THEM (with indexs being at starting_frame)
        tree = self.tree_list[index]
        segs = self.get_tree_segments(tree)

        angle_valid = self.angle_valid_list[index]

        # MAKE A LIST TO STORE INTERSECTIONS
        intersection_list = []
        intersection_cypher = []

        number_that_dont_touch = 0
        counter = 0

        # MAKES INTERSECTIONS TO STORE IN INT_LIST
        for outer_index, outer_seg in enumerate(segs):
            for inner_index, inner_seg in enumerate(segs):
                if outer_index < inner_index:
                    counter+=1
                    if angle_valid[counter - 1] == 0:
                        continue

                    inter = outer_seg.intersection(inner_seg)

                    # IF INTERSECTS
                    if not inter.is_empty:
                        intersection_list.append(inter)
                        intersection_cypher.append([outer_index + tree.starting_photo - one_directory.starting_id,
                                                    inner_index + tree.starting_photo - one_directory.starting_id])
                    else:
                        number_that_dont_touch+=1

        return intersection_list, intersection_cypher, len(intersection_list), number_that_dont_touch







    def movement_elicated_from_all_lines(self):
        print("I")

    #Determines A Starting List of valid angles
    def obtain_indexs_of_angle_invalid(self):
        list_of_valid = []
        list_of_numbers_failed = []

        for tree in self.tree_list:
            list_of_index_values = []
            number_failed = 0

            segs = self.get_tree_segments(tree)

            for outer_index, outer_seg in enumerate(segs):
                for inner_index, inner_seg in enumerate(segs):
                    if outer_index < inner_index:

                        b = tree.starting_photo - one_directory.starting_id
                        # MAKE SURE ANGLES ARE FAR ENOUGH APART (EVEN 350 - 5)
                        o_f = self.frames[b + outer_index].fragments[tree.list_of_indexs[outer_index]]
                        i_f = self.frames[b + inner_index].fragments[tree.list_of_indexs[inner_index]]

                        diff = abs(o_f.p0_dir - i_f.p0_dir)

                        # Adjust for circular range
                        circular_diff = min(diff, 360 - diff)

                        # circular_diff = self.difference_in_angle(o_f.p0_dir, i_f.p0_dir)

                        #TOO SMALL (REMOVE)
                        if circular_diff < one_directory.angle_variety:
                            list_of_index_values.append(0)
                            number_failed+=1
                        #VALID
                        else:
                            list_of_index_values.append(1)
            list_of_valid.append(list_of_index_values)
            list_of_numbers_failed.append(number_failed)
        self.angle_valid_list = list_of_valid
        self.angle_failed_count = list_of_numbers_failed



    # #Returns A List Of Recommended_Movement For Each Index
    # def movement_elicated_from_all_trees(self, use_slide):
    #     total_movement = []
    #     denominator_movement = []
    #
    #     for index in range(0, len(self.frames)):
    #         total_movement.append([0,0])
    #         denominator_movement.append(0)
    #
    #     for tree in self.tree_list:
    #         if len(tree.list_of_indexs) > 1:
    #             segs = self.get_tree_segments(tree)
    #             starting_position = tree.starting_photo - one_directory.starting_id
    #
    #             movement, weights = self.single_tree_movement(segs, use_slide)
    #
    #             #ADDING TO TOTAL
    #             for index in range(0, len(segs)):
    #                 total_movement[index + starting_position][0] += movement[index][0]
    #                 total_movement[index + starting_position][1] += movement[index][1]
    #                 denominator_movement[index + starting_position] += weights[index]
    #
    #
    #     for index, value in enumerate(total_movement):
    #         if denominator_movement[index] != 0:
    #             value[0] /= denominator_movement[index]
    #             value[1] /= denominator_movement[index]
    #
    #     return total_movement


    # #Determines the MOVEMENT, and WEIGHT allocated to movement
    # def single_tree_movement(self, segs, use_slide):
    #
    #     disjoint_movement = []
    #     sliding_movement = []
    #
    #     disjoint_weight = []
    #     sliding_weight = []
    #
    #     total_disjoint = 0
    #     total_sliding = 0
    #
    #     list_of_intersections = []
    #
    #
    #     #MAKES LISTS
    #     for index in range(0, len(segs)):
    #         disjoint_movement.append([0,0])
    #         sliding_movement.append([0,0])
    #
    #         disjoint_weight.append(0)
    #         sliding_weight.append(0)
    #
    #
    #     #CREATES ALL INTERSECTIONS AND MAKES DISJOINT MOVEMENT
    #     for outer_index, outer_seg in enumerate(segs):
    #         row = []
    #         for inner_index, inner_seg in enumerate(segs):
    #             if outer_index < inner_index:
    #
    #                 inter = outer_seg.intersection(inner_seg)
    #
    #                 #IF INTERSECTS
    #                 if not inter.is_empty:
    #                     row.append(inter)
    #
    #                     #print("DOES")
    #                 #IF DOESNT
    #                 else:
    #                     #print("NOT")
    #                     row.append(0)
    #
    #                     if not use_slide:
    #                         #GIVES VECTOR BETWEEN (NOT TOTALLY CLOSEST POINT)
    #                         x, y = self.single_intersection_movement(outer_seg, inner_seg, True)
    #
    #                         # x *= 0.5
    #                         # y *= 0.5
    #
    #                         if x > 0:
    #                             x = math.pow(x, 0.8)*0.5
    #                         else:
    #                             x = -1*math.pow(abs(x), 0.8)*0.5
    #
    #                         if y > 0:
    #                             y = math.pow(y, 0.8)*0.5
    #                         else:
    #                             y = -1*math.pow(abs(y), 0.8)*0.5
    #
    #
    #
    #
    #
    #                         disjoint_movement[outer_index][0] += x
    #                         disjoint_movement[outer_index][1] += y
    #
    #                         disjoint_movement[inner_index][0] -= x
    #                         disjoint_movement[inner_index][1] -= y
    #
    #                         disjoint_weight[outer_index] += 1
    #                         disjoint_weight[inner_index] += 1
    #
    #                         total_disjoint += 2
    #
    #
    #         list_of_intersections.append(row)
    #
    #
    #     #USES INTERSECTION FOR INTERSECTION MOVMENET
    #
    #     #LIST INDEX TELLS VALUE OF ONE SEGMENT
    #
    #
    #
    #     #FOR EVERY LIST OF INTERSECTIONS
    #     for o_index_1, o_list in enumerate(list_of_intersections):
    #         if not use_slide:
    #             break
    #         print("DOING END")
    #         #FOR EVERY INTERSECTION WITHIN IT
    #         for temp, o_intersection in enumerate(o_list):
    #             o_index_2 = temp + o_index_1 + 1
    #
    #             if o_intersection == 0:
    #                 continue
    #
    #             #COMPARING TO EVERY LIST OF INTERSECTIONS
    #             for i_index_1, i_list in enumerate(list_of_intersections):
    #                 #INNER LIST MUST BE SAME OR GREATER LIST
    #                 if not i_index_1 >= o_index_1:
    #                     continue
    #
    #                 #FOR EVERY INTERSECTION IN THIS LIST
    #                 for temp_2, i_intersection in enumerate(i_list):
    #                     i_index_2 = temp_2 + i_index_1 + 1
    #
    #                     #IF SAME LIST NEEDS TO BE LATER,
    #                     if i_index_1 == o_index_1:
    #                         if not o_index_2 < i_index_2:
    #                             continue
    #
    #                     if i_intersection == 0:
    #                         continue
    #
    #                     #print(f" {o_index_1}  {o_index_2}  {i_index_1} {i_index_2}")
    #
    #
    #                     # x_delta_2 = ((i_intersection.x - o_intersection.x) / 2)
    #                     # y_delta_2 = ((i_intersection.y - o_intersection.y) / 2)
    #
    #                     x_delta_2 = i_intersection.x - o_intersection.x
    #                     y_delta_2 = i_intersection.y - o_intersection.y
    #
    #                     if x_delta_2 > 0:
    #                         x_delta_2 = math.pow(x_delta_2, 0.8) * 0.5
    #                     else:
    #                         x_delta_2 = -1 * math.pow(abs(x_delta_2), 0.8) * 0.5
    #
    #                     if y_delta_2 > 0:
    #                         y_delta_2 = math.pow(y_delta_2, 0.8) * 0.5
    #                     else:
    #                         y_delta_2 = -1 * math.pow(abs(y_delta_2), 0.8) * 0.5
    #
    #
    #
    #                     sliding_weight[o_index_1] += 1
    #                     sliding_weight[o_index_2] += 1
    #                     sliding_weight[i_index_1] += 1
    #                     sliding_weight[i_index_2] += 1
    #
    #
    #
    #                     sliding_movement[o_index_1][0] += x_delta_2
    #                     sliding_movement[o_index_1][1] += y_delta_2
    #
    #                     sliding_movement[o_index_2][0] += x_delta_2
    #                     sliding_movement[o_index_2][1] += y_delta_2
    #
    #                     sliding_movement[i_index_1][0] -= x_delta_2
    #                     sliding_movement[i_index_1][1] -= y_delta_2
    #
    #                     sliding_movement[i_index_2][0] -= x_delta_2
    #                     sliding_movement[i_index_2][1] -= y_delta_2
    #
    #                     total_sliding += 4
    #
    #     if not use_slide:
    #         return disjoint_movement, disjoint_weight
    #     else:
    #         return sliding_movement, sliding_weight
    #


























    #Determines the movement (x,y) to centre of seg1, seg2




    # RETURNS THE POLYGON OF ST -> ED, EXTENDING FROM LOCATION OF ST
    def get_active_pol(self, st, ed):

        # NORMAL
        if st < ed:
            pol_rel_zero = self.polygon_maps[st][ed]
        # SWAPPED
        else:
            pol_rel_zero = self.reverse_polygon(self.polygon_maps[ed][st])

        # MOVING IT RELATIVE TO STARTING
        moved_pol = translate(pol_rel_zero,
                                  xoff=self.points_locations[st].x,
                                  yoff=self.points_locations[st].y)
        return moved_pol


    def single_intersection_movement(self, seg1, seg2, bool_scale):
        middle_point = self.pull_corners_average(seg1, seg2, False)

        closest_to_s1, closest_to_s2 = self.pull_average_closest(seg1, seg2, middle_point)

        distance = seg1.distance(seg2)

        scalar = self.pull_scaled_movement(closest_to_s1, closest_to_s2, distance)

        x_diff = (closest_to_s2.x - closest_to_s1.x)/2
        y_diff = (closest_to_s2.y - closest_to_s1.y)/2

        if bool_scale:
            return x_diff*scalar, y_diff*scalar
        else:
            return x_diff, y_diff



    #Returns The Points, on outer, inner, closest to middle
    def pull_average_closest(self, seg1, seg2, middle):
        closest_to_seg1 = seg1.interpolate(seg1.project(middle))
        closest_to_seg2 = seg2.interpolate(seg2.project(middle))

        return closest_to_seg1, closest_to_seg2

    #Returns Average Of Corners Interaction
    # and optionally all corners
    def pull_corners_average(self, seg1, seg2, bool_all):
        seg1_coords = list(seg1.coords)
        seg2_coords = list(seg2.coords)

        c1 = seg1.interpolate(seg1.project(Point(seg2_coords[0][0], seg2_coords[0][1])))
        c2 = seg1.interpolate(seg1.project(Point(seg2_coords[1][0], seg2_coords[1][1])))
        c3 = seg2.interpolate(seg2.project(Point(seg1_coords[0][0], seg1_coords[0][1])))
        c4 = seg2.interpolate(seg2.project(Point(seg1_coords[1][0], seg1_coords[1][1])))

        av_x = (c1.x + c2.x + c3.x + c4.x) / 4
        av_y = (c1.y + c2.y + c3.y + c4.y) / 4

        p = Point(av_x, av_y)

        if not bool_all:
            return p
        else:
            return p, c1, c2, c3, c4

    #Returns A scalar on force,
    def pull_scaled_movement(self, c1, c2, distance):
        x_change = c2.x - c1.x
        y_change = c2.y - c1.y

        #Gives Us Scaled Movement (BETWEEN)
        distance_using_points = math.sqrt(x_change*x_change + y_change*y_change)
        distance_minimum = distance

        factor = distance_minimum/distance_using_points

        return factor















