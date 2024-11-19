import math
import random

from matplotlib import pyplot as plt
from shapely.affinity import translate
from shapely.geometry import LineString, Point, Polygon
from shapely.ops import nearest_points

from five_database import five_database
import one_directory
import updated_frame
from fixed_point import fixed_point
from pure_polygon import pure_polygon


class pure_mover:

    def __init__(self):
        self.lof = []

        # Obtain Corner:
        self.corners = five_database.omni_obtain_plot_baseline(1, 100)

        print(f" CORNERS: {self.corners}")

        print("CONS:")
        print(five_database().translate_entire_photo(one_directory.starting_id + 0,
                                                     one_directory.starting_id + 2))

        # Sets Up List
        self.make_list_of_photos()

        # Prints GPS values
        self.absolute_print_map()



        #MOVEMENT PREP RELATED
        if True:
            #CREATES TREE LIST
            self.tree_list = self.make_trees(self.lof[0], self.lof[1],
                                           len(self.lof) - 1 + one_directory.starting_id)

            #CREATE ANGLE INVALID LIST  (0 bad, 1 good)
            self.angles_1 = self.make_angle_list(True)
            self.angles_2 = self.make_angle_list(False)

            self.pure_polygons = pure_polygon(self.lof)

            #CREATE RANDOM LOCATIONS:
            self.point_locations = self.make_location_set(use_gps=not one_directory.initial_location_random)

            #MAKE SEGMENTS FROM THE
            self.fragment_locations = self.make_segment_set()



        #MOVEMENT RELATED
        if False:

            print("START AT LOCATIONS:")
            print(self.point_locations)

            #MAKES NEEDED INTERSECTION VALUES
            total_intersections = 0

            for tree in self.angles_1:
                for val in tree:
                    total_intersections += val


            prepped_for_polygon_limited_movement = False
            for iter in range(0,one_directory.movement_iteration): #one_directory.movement_iteration):

                #NOTE ONLY APPLIES ON ANGLE VALID FUNCTIONS

                # MOVEMENT TOTAL, #DENOM TOTAL
                #TOTAL INTERSECTIONS
                # HOW MANY EVENTS THE TOTAL DISTANCE IS SPREAD OVER,
                # TOTAL DISTANCE
                move1, denom1, total_intersections1, quantity_to_divide1, total_distance1 = self.get_movement_from_intersections()

                #MOVEMENT TOTAL, #DENOM TOTAL
                #NUMBER OF EVENTS DISTANCE IS FROM
                #TOTAL DISTANCE
                move2, denom2, quantity_to_divide2, total_distance2 = self.get_movement_from_lines()


                move3, denom3, total_quantity_to_divide3, total_distance3 = self.get_movement_from_polygons(use_frag=True)



                #SINCE ODDS OF HAVING NO INTERSECTIONS ARE LOW AFTER LIKE ITER 1, ASSUME QU > 0


                #START SHOULD DEAL WITH ENSURING ALL INTERSECTIONS ARE MADE
                # ONLY LINES SEEMS TO HANDLE THIS
                if iter < 200:
                    if total_intersections1 == total_intersections:
                        mo_ = move3
                        de_ = denom3
                        v = 3
                    else:
                        mo_ = move2
                        de_ = denom2
                        v = 2
                else:

                    if prepped_for_polygon_limited_movement == False and total_distance3 == 0:
                        prepped_for_polygon_limited_movement = True
                        #print("PREPPED")




                    if True: #iter % 3 == 0:
                        mo_ = move1
                        de_ = denom1
                        v = 1




                print(
                    f" {iter}: {v}          I:{total_intersections1}(({total_intersections})) DIST: {round(total_distance1, 3)}  DIST_P: {round(total_distance3, 3)}  M1={move1}")

                new = []
                for index, val in enumerate(mo_):
                    if de_[index] == 0:
                        new.append([0,0])
                    elif index == one_directory.m_have_locked_index:
                        new.append([0,0])
                    else:
                        new.append([(val[0] / de_[index])*one_directory.m_multiplier     ,
                                    (val[1] / de_[index])*one_directory.m_multiplier])



                if iter != one_directory.movement_iteration - 1:
                    self.move_according_to_list(new, adhere_to_poly=prepped_for_polygon_limited_movement,
                                                use_frag=True)
                else:
                    print(f"DIDNT DO LAST: {self.point_locations}")
                    current_intersections = total_intersections1

                move3, denom3, total_quantity_to_divide3, total_distance3 = self.get_movement_from_polygons(
                    use_frag=True)

                #print(f"AFTER MOVEMENT: {total_quantity_to_divide3}")

        self.iterate()

        #PRINTING FOLLOWING
        if True:
            fig, ax = plt.subplots()


            #ALL POSSIBLE SEGMENTS (FOR VISUAL - IGNORE NOW)
            if False:
                print("STARTING SEGMENT PRINTING")
                #ASSUME PLOTS ARE SEPERATED EFFECTIVELY
                #PRINTING ALL PHOTOS,
                #BUT JUST NEEDING TO PRINT APPROPREITE LINES

                index_of_valid_tree = -1
                colors = ["blue", "red", "green", "orange", "purple", "black", "brown", "grey"]
                for t_index, tree in enumerate(self.tree_list):
                    start = tree.starting_photo - one_directory.starting_id

                    number_of_intersects = 0
                    for angle_accept in self.invalid_angles[t_index]:
                        if angle_accept == 1:
                            number_of_intersects+=1

                    if number_of_intersects > 0:
                        index_of_valid_tree+=1

                        for index, segment in enumerate(tree.list_of_indexs):
                            print("SEGS")
                            seg = self.fragment_locations[index + start][segment]

                            x,y = seg.xy

                            plt.plot(x,y,color=colors[index_of_valid_tree],marker="o")







            for index in range(0, len(self.point_locations)):

                super = self.super_polygon(index, False)
                #print(f"  {index} {super.area}")
                x,y = super.exterior.xy
                plt.plot(x,y,color=self.get_point_color(index))



            total_intersection = 0
            #POLYGONS






            #INTERSECTION STUFF
            if True:
                # ONLY PRINTING RELEVANT LINES
                for t_index, tree in enumerate(self.tree_list):
                    starting = tree.starting_photo - one_directory.starting_id
                    segs = self.get_tree_segments(tree)

                    list_already_printed = []
                    intersections, cypher = self.get_intersections_super(True, True, t_index)

                    for i_index, i_cypher in enumerate(cypher):
                        seg1 = segs[i_cypher[0] - starting]
                        seg2 = segs[i_cypher[1] - starting]

                        if not i_cypher[0] in list_already_printed:
                            x, y = seg1.xy
                            plt.plot(x, y, color=tree.color)
                            list_already_printed.append(i_cypher[0])

                        if not i_cypher[1] in list_already_printed:
                            x, y = seg2.xy
                            plt.plot(x, y, color=tree.color)
                            list_already_printed.append(i_cypher[1])

                # INTERSECTIONS
                for t_index, tree in enumerate(self.tree_list):
                    if len(tree.list_of_indexs) > 1:

                        # NOTE ONLY GETS ONES WITH UNIQUE ENOUGH ANGLES!!!!!!!!!!!!!!
                        intersections, cypher = self.get_intersections_super(True, True, t_index)

                        if len(intersections) == 0:
                            continue

                        non_shapely = []
                        for po in intersections:
                            non_shapely.append((po.x, po.y))

                        # USE POLYGONS
                        if False:
                            if len(non_shapely) < 3:
                                continue
                            pol = Polygon(non_shapely).convex_hull

                            x, y = pol.exterior.xy

                            xx, yy = pol.buffer(0.3).exterior.xy

                            plt.fill(x, y)
                            plt.plot(xx, yy, color="black", marker="*")

                        else:

                            for poi in intersections:
                                x, y = poi.buffer(0.05).exterior.xy

                                plt.fill(x, y, color=tree.color)  # tree.color)

                        # if len(intersections) == 0:
                        #     continue
                        # else:
                        #
                        #     plt.text(non_shapely[0][0], non_shapely[0][1],
                        #                 f"{tree.starting_photo} - {tree.starting_photo + len(tree.list_of_indexs) - 1} -- {tree.list_of_indexs[0]}")



            # POINTS
            for index, point in enumerate(self.point_locations):
                plt.plot(point[0], point[1], marker="*", color=self.get_point_color(index))
                plt.text(point[0], point[1], f"{index}")

        plt.show()












    def get_point_color(self, i):
        if i == 0:
            return "black"
        elif i == 1:
            return "brown"
        elif i == 2:
            return "red"
        elif i == 3:
            return "orange"
        elif i == 4:
            return "green"
        elif i == 5:
            return "blue"
        elif i ==6:
            return "purple"
        elif i == 7:
            return "grey"
        else:
            return "gold"
















    def move_according_to_list(self, movement, adhere_to_poly, use_frag):


        for index, movement in enumerate(movement):


            previous_location = self.point_locations[index]


            polygon_to_remain_within = self.pure_polygons.get_overlap(index, self.point_locations, 1, 1, use_frag)

            new_location_to_try = self.move_point(previous_location, movement[0], movement[1])

            if adhere_to_poly:

                shapely_new_location_to_try = Point(new_location_to_try[0], new_location_to_try[1])

                #IF ALREADY WITHIN, THEN WERE GOOD
                if polygon_to_remain_within.contains(shapely_new_location_to_try):
                    new_location_to_use = new_location_to_try

                else:
                    #print(f"IMPACTED {index} {polygon_to_remain_within.contains(Point(previous_location[0], previous_location[1]))}")

                    segment_of_movement = LineString([previous_location, new_location_to_try])

                    new_segment_of_movement = segment_of_movement.intersection(polygon_to_remain_within)


                    new_location_to_use = self.get_random_point_in_ls(new_segment_of_movement)



                    movement[0] = new_location_to_use[0] - previous_location[0]
                    movement[1] = new_location_to_use[1] - previous_location[1]

                    if abs(movement[0]) < 0.001:
                        movement[0] = 0

                    if abs(movement[1]) < 0.001:
                        movement[1] = 0

                    if abs(movement[0]) < 0.001 and abs(movement[1]) < 0.001:
                        new_location_to_use = previous_location





                    # max_ = [0,0]
                    #
                    # max_[0] = new_location_to_try[0] - previous_location[0]
                    # max_[1] = new_location_to_try[1] - previous_location[1]



                    # print(f" STARTING SEG: {segment_of_movement}  ")
                    # print(f" ENDING SEG: {segment_of_movement}")
                    # print(f"  MOVE: {movement[0]} {movement[1]}  ((((")

            else:
                new_location_to_use = new_location_to_try



            self.point_locations[index] = new_location_to_use

            list_to_return = []
            for segment_index, individual_tree_segment in enumerate(self.fragment_locations[index]):
                list_to_return.append(self.move_line_segment(individual_tree_segment, movement[0], movement[1]))
            self.fragment_locations[index] = list_to_return

    def get_random_point_in_ls(self, seg):
        coords = list(seg.coords)

        x1, y1 = coords[0][0], coords[0][1]
        x2, y2 = coords[1][0], coords[1][1]

        # Generate a random value 't' between 0 and 1
        t = random.uniform(0, 1)

        # Calculate the random point along the line segment
        random_x = x1 + t * (x2 - x1)
        random_y = y1 + t * (y2 - y1)

        return [random_x, random_y]



    def get_tree_segments(self, tree):
        list_to_return = []
        starting_index = tree.starting_photo - one_directory.starting_id

        for index, value in enumerate(tree.list_of_indexs):
            list_to_return.append(self.fragment_locations[index + starting_index][value])

        return list_to_return

    # def get_movement_from_intersections(self):
    #
    #     total_distance_between_valid_intersections = 0
    #     number_of_angle_valid_non_intersections = 0
    #
    #     #NUMBER OF FAILED CAN BE GOT FROM ANGLE_LIST (SUM OF 0)
    #
    #     total_intersections = 0
    #     total_lacks = 0
    #     denominator_quantity = 0
    #
    #     movement, denom = self.make_count_set()
    #
    #     #For every tree
    #     for tree_index, tree in enumerate(self.tree_list):
    #         #if not just single segment
    #         if len(tree.list_of_indexs) > 1:
    #
    #             intersection_list, intersection_cypher, num_missed = self.get_1_intersection_list(tree_index)
    #
    #
    #             number_of_angle_valid_non_intersections += num_missed
    #
    #             total_intersections += len(intersection_list)
    #
    #             for x in range(1, len(intersection_list)):
    #                 denominator_quantity += x
    #
    #
    #
    #
    #             for intersection_one_index, intersection_one in enumerate(intersection_list):
    #                 for intersection_two_index, intersection_two in enumerate(intersection_list):
    #                     #IF MORE
    #                     if intersection_one_index < intersection_two_index:
    #
    #                         #GOING FROM ONE TO TWO
    #                         x_movement_from_one_to_two = intersection_two.x - intersection_one.x
    #                         y_movement_from_one_to_two = intersection_two.y - intersection_one.y
    #
    #
    #                         total_distance_between_valid_intersections += \
    #                             math.sqrt(math.pow(x_movement_from_one_to_two, 2) +
    #                                       math.pow(y_movement_from_one_to_two, 2))
    #
    #
    #                         x_move, y_move, scale_denom = \
    #                             self.scale_movement(x_movement_from_one_to_two,
    #                                                 y_movement_from_one_to_two,
    #                                                 denominator_quantity)
    #
    #
    #
    #
    #
    #                         cypher_one = intersection_cypher[intersection_one_index]
    #                         cypher_two = intersection_cypher[intersection_two_index]
    #
    #
    #
    #                         #WAY_0  (4)
    #
    #                         movement[cypher_one[0]][0] += x_move
    #                         movement[cypher_one[1]][1] += y_move
    #
    #                         movement[cypher_two[0]][0] -= x_move
    #                         movement[cypher_two[1]][1] -= y_move
    #
    #                         random1 = random.uniform(0,1)
    #                         random2 = random.uniform(0,1)
    #
    #                         # movement[cypher_one[random1]][0] += x_move
    #                         # movement[cypher_one[random1]][1] += y_move
    #                         #
    #                         # movement[cypher_two[random2]][0] -= x_move
    #                         # movement[cypher_two[random2]][1] -= y_move
    #
    #
    #
    #
    #                         #WAY_1 (8)
    #                         # movement[cypher_one[0]][0] += x_move
    #                         # movement[cypher_one[0]][1] += y_move
    #                         #
    #                         # movement[cypher_one[1]][0] += x_move
    #                         # movement[cypher_one[1]][1] += y_move
    #                         #
    #                         # movement[cypher_two[0]][0] -= x_move
    #                         # movement[cypher_two[0]][1] -= y_move
    #                         #
    #                         # movement[cypher_two[1]][0] -= x_move
    #                         # movement[cypher_two[1]][1] -= y_move
    #                         #
    #
    #
    #                         denom[cypher_one[0]] += scale_denom
    #                         denom[cypher_one[1]] += scale_denom
    #
    #                         denom[cypher_two[0]] += scale_denom
    #                         denom[cypher_two[1]] += scale_denom
    #
    #
    #
    #
    #
    #     #RETURNS THE MOVEMENT TOTAL, DENOMINATOR, total number of intersections, total_distance_between
    #     return movement, denom, total_intersections, denominator_quantity, total_distance_between_valid_intersections

    def get_1_intersection_list(self, index_of_tree):

        tree = self.tree_list[index_of_tree]
        segs = self.get_tree_segments(tree)
        angle_valid = self.invalid_angles[index_of_tree]
        counter = 0
        failed_counter = 0
        intersection_list = []
        intersection_cypher = []

        # MAKES INTERSECTIONS TO STORE IN INT_LIST
        for outer_index, outer_seg in enumerate(segs):
            for inner_index, inner_seg in enumerate(segs):
                if outer_index < inner_index:
                    counter += 1
                    if angle_valid[counter - 1] == 0:
                        continue

                    inter = outer_seg.intersection(inner_seg)

                    # IF INTERSECTS
                    if not inter.is_empty:
                        intersection_list.append(inter)
                        intersection_cypher.append([outer_index + tree.starting_photo - one_directory.starting_id,
                                                        inner_index + tree.starting_photo - one_directory.starting_id])
                    else:
                        failed_counter += 1

        return intersection_list, intersection_cypher, failed_counter

        # USED FOR LINES
        # RETURNS THE LIST OF LINES THAT DONT INTERCECT,
        #    AND RETURNS THE LIST OF LINES (REMOVED BY ANGLES THAT DONT INTERCECT)
        #                               JUST NEED TO BE CLOSE)


    #-------------------------------------------------------------------------------------------------------
    # IF INTERSECTIONS OR LACK, AND
    def get_intersections_super(self, bool_intersections, bool_intersection_angles, t_index):

        tree = self.tree_list[t_index]
        segs = self.get_tree_segments(tree)
        base = tree.starting_photo - one_directory.starting_id

        intersections = []
        cypher = []

        #IF USING INTERSECTION REQUIREMENT
        if bool_intersection_angles:
            angle_valid = self.angles_1[t_index]
        #USING LINE REQUIREMENTS
        else:
            angle_valid = self.angles_2[t_index]


        a_index = -1
        for outer_index, outer_seg in enumerate(segs):
            for inner_index, inner_seg in enumerate(segs):
                if inner_index > outer_index:
                    a_index+=1
                    if angle_valid[a_index] == 0:
                        continue

                    intersection_maybe = outer_seg.intersection(inner_seg)

                    #IF AN INTERSECTION EXISTS
                    if not intersection_maybe.is_empty:
                        #IF LOOKING FOR INTERSECTIONS
                        if bool_intersections:
                            intersections.append(intersection_maybe)
                            cypher.append([outer_index + base, inner_index + base])
                        #LOOKING FOR NON INTERSECTIONS
                        else:
                            continue
                    #IF NO INTERSECTION EXISTS
                    else:

                        # IF LOOKING FOR INTERSECTIONS
                        if bool_intersections:
                            continue
                        # LOOKING FOR NON INTERSECTIONS
                        else:
                            cypher.append([outer_index + base, inner_index + base])

        #LOOKING TO RETURN INTERSECTIONS
        if bool_intersections:
            return intersections, cypher
        else:
            return cypher



    def get_movement_from_intersections(self):
        distance_between_intersections = 0
        total_intersections = 0
        denominator_quantity = 0

        movement, denom = self.make_count_set()

        for t_index, tree in enumerate(self.tree_list):

            intersection_list, intersection_cypher = self.get_intersections_super(True, True, t_index)

            total_intersections += len(intersection_list)

            for x in range(1, len(intersection_list)):
                denominator_quantity += x

            for intersection_one_index, intersection_one in enumerate(intersection_list):
                for intersection_two_index, intersection_two in enumerate(intersection_list):
                    # IF MORE
                    if intersection_one_index < intersection_two_index:
                        # GOING FROM ONE TO TWO
                        x_movement_from_one_to_two = intersection_two.x - intersection_one.x
                        y_movement_from_one_to_two = intersection_two.y - intersection_one.y

                        distance_between_intersections += \
                            math.sqrt(math.pow(x_movement_from_one_to_two, 2) +
                                      math.pow(y_movement_from_one_to_two, 2))

                        x_move, y_move, scale_denom = \
                            self.scale_movement(x_movement_from_one_to_two,
                                                y_movement_from_one_to_two,
                                                denominator_quantity)

                        cypher_one = intersection_cypher[intersection_one_index]
                        cypher_two = intersection_cypher[intersection_two_index]

                        # movement[cypher_one[0]][0] += x_move
                        # movement[cypher_one[1]][1] += y_move
                        #
                        # movement[cypher_two[0]][0] -= x_move
                        # movement[cypher_two[1]][1] -= y_move
                        #
                        # random1 = random.uniform(0, 1)
                        # random2 = random.uniform(0, 1)

                        # movement[cypher_one[random1]][0] += x_move
                        # movement[cypher_one[random1]][1] += y_move
                        #
                        # movement[cypher_two[random2]][0] -= x_move
                        # movement[cypher_two[random2]][1] -= y_move

                        # WAY_1 (8)
                        movement[cypher_one[0]][0] += x_move
                        movement[cypher_one[0]][1] += y_move

                        movement[cypher_one[1]][0] += x_move
                        movement[cypher_one[1]][1] += y_move

                        movement[cypher_two[0]][0] -= x_move
                        movement[cypher_two[0]][1] -= y_move

                        movement[cypher_two[1]][0] -= x_move
                        movement[cypher_two[1]][1] -= y_move
                        #

                        denom[cypher_one[0]] += scale_denom
                        denom[cypher_one[1]] += scale_denom

                        denom[cypher_two[0]] += scale_denom
                        denom[cypher_two[1]] += scale_denom
        return movement, denom, total_intersections, denominator_quantity, distance_between_intersections


    def get_movement_from_lines(self):
        total_distance_between_lines = 0
        total_events = 0

        movement, denom = self.make_count_set()

        for tree_index, tree in enumerate(self.tree_list):
            # if not just single segment
            if len(tree.list_of_indexs) > 1:

                base = tree.starting_photo - one_directory.starting_id

                segs = self.get_tree_segments(tree)

                non_intersections = self.get_intersections_super(False, False, tree_index)

                total_events += len(non_intersections)

                # FOR ALL VALID
                for lack_inter in non_intersections:
                    #ABSOLUTE
                    ind1 = lack_inter[0]
                    ind2 = lack_inter[1]

                    #SEGMENT INDEX
                    seg1 = segs[ind1 - base]
                    seg2 = segs[ind2 - base]

                    x_movement_from_1_to_2, \
                    y_movement_from_1_to_2 = self.get_starting_x_y_movement(seg1, seg2)

                    total_distance_between_lines += math.sqrt(x_movement_from_1_to_2 ** 2 + y_movement_from_1_to_2 ** 2)

                    x_move, y_move, den = self.scale_movement(x_movement_from_1_to_2,
                                                              y_movement_from_1_to_2,
                                                              len(non_intersections))

                    movement[ind1][0] += x_move
                    movement[ind1][1] += y_move

                    movement[ind2][0] -= x_move
                    movement[ind2][1] -= y_move

                    denom[ind1] += den
                    denom[ind2] += den

        # print(f" WHATS RETURNED FROM FUNCTION: {movement}")
        return movement, denom, total_events, total_distance_between_lines

    def get_movement_from_polygon(self, use_frag):
        total_fails = 0
        to_dists = 0

        fail_list = []

        movement, denom = self.make_count_set()

        # For Every Existing Point
        for point_index, point_location in enumerate(self.point_locations):
            # From Every other index, the Point needs to be within the polygon gained by P
            for polygon_index in range(0, len(self.point_locations)):
                # ASSUMING NOT SAME
                if point_index < polygon_index:

                    polygon_this_point_needs_to_be_within = self.get_active_pol(polygon_index, point_index, use_frag)

                    shapely_location = Point(point_location[0], point_location[1])

                    # MEANS POINT ALREADY WITHIN DESIRED
                    # IDEA BRING CLOSER TO CENTERS (TO PREVENT TIP TOUCHING)
                    if polygon_this_point_needs_to_be_within.contains(shapely_location):
                        continue
                    # POINT NOT WITHIN POLYGON
                    # IDEA MOVE TOWARD EACH OTHER
                    else:

                        # Need To Find Closest Point To It, To Then Determine Desired Movement
                        point_that_needs_to_be_within_polygon = shapely_location

                        closest_point_to_this_point, ignore = nearest_points(polygon_this_point_needs_to_be_within,
                                                                             point_that_needs_to_be_within_polygon)

                        # MOVEMENT OF POINT ---> POLYGON
                        x_move = closest_point_to_this_point.x - point_that_needs_to_be_within_polygon.x
                        y_move = closest_point_to_this_point.y - point_that_needs_to_be_within_polygon.y

                        fail_list.append( [point_index, polygon_index, "||||", x_move, y_move])

                        # SCALING
                        if True:




                            val = random.uniform(0, one_directory.m_jitter)

                            x_move, y_move = self.extend_by_n(x_move, y_move, val)

                            # Print NEED TO UPDATE

                            x_move *= 0.5
                            y_move *= 0.5




                        movement[point_index][0] += x_move
                        movement[point_index][1] += y_move

                        movement[polygon_index][0] -= x_move
                        movement[polygon_index][1] -= y_move

                        denom[point_index] += 1
                        denom[polygon_index] += 1

                        total_fails += 1
                        to_dists += math.sqrt(x_move ** 2 + y_move ** 2)

        #print(f"V --  FAIL LIST: {fail_list}")

        return movement, denom, total_fails, to_dists



        # BASIC IDEA:
        #    same as before, except
        #    make a polygon of all relatives its within,
        #    make sure to stay within that (POSSIBLY MAKES SEPERATE

    def super_move(self, movements, use_frag, maintain_within):
        actual_movement = []
        for x in range(0, len(movements)):
            actual_movement.append(0)

        order = list(range(0, len(movements)))
        random.shuffle(order)

        for m_index in order:
            #in a perfect world this is how much we move
            movement_to_try = movements[m_index]

            current_location = self.point_locations[m_index]

            suggested_new_location = self.move_point(current_location,
                                                     movement_to_try[0],
                                                     movement_to_try[1])
            shapely_suggested_new_location = Point(suggested_new_location[0],
                                                   suggested_new_location[1])

            poly_to_remain_in = self.super_polygon(m_index, use_frag=False)




            #MEANS NO CURRENT BARRIERS
            if poly_to_remain_in == 0 or not maintain_within:
                movement_to_do = movement_to_try
                #print(f" {m_index} NO BARRIER")
            #CURRENT BARRIERS EXIST
            else:

                #print(poly_to_remain_in.contains(Point(current_location[0], current_location[1])))

                #IF NEW POINT IS WITHIN BARRIER, NO PROBLEM
                if poly_to_remain_in.contains(shapely_suggested_new_location):
                    movement_to_do = movement_to_try
                    #print(f" {m_index} NO BARRIER NO PROBLEM")

                #NOT WITHIN
                else:
                    #MEANS WITHIN JUST BARELY (WOULDNT MOVE)
                    if not poly_to_remain_in.contains(Point(current_location[0], current_location[1])):
                        movement_to_do = [0,0]
                        #print(f" {m_index} BARELY WITHIN")


                    #VALID AREA
                    else:

                        segment_of_movement = LineString([current_location, suggested_new_location])

                        new_segment_of_movement = segment_of_movement.intersection(poly_to_remain_in)
                        #print(new_segment_of_movement)
                        #MEANS ONLY EDGE CURRENTLY IN
                        if isinstance(new_segment_of_movement, Point):
                            new_location_to_use = current_location
                            #print(f" {m_index} POINT INTERSECTION:")
                        else:
                            new_location_to_use = self.get_random_point_in_ls(new_segment_of_movement)
                            #print(f" {m_index}  RANDOM LOCATION: PREV: {current_location}  ---> {new_location_to_use}")

                        movement_to_do = [0,0]
                        movement_to_do[0] = new_location_to_use[0] - current_location[0]
                        movement_to_do[1] = new_location_to_use[1] - current_location[1]



            self.point_locations[m_index] = self.move_point(self.point_locations[m_index],
                                                            movement_to_do[0],
                                                            movement_to_do[1])

            for index in range(0, len(self.fragment_locations[m_index])):
                self.fragment_locations[m_index][index] = self.move_line_segment(self.fragment_locations[m_index][index],
                                                                                 movement_to_do[0],
                                                                                 movement_to_do[1])
            actual_movement[m_index] = movement_to_do
        return actual_movement


        # POLYGON THAT RETURNS THE INTERSECTION OF ALL RELATIVES ITS WITHIN

    #A POLYGON OF WHERE POINT CAN GO TO REMAIN WITHIN ALL CURRENTLY WITHIN POLYGONS
    def super_polygon(self, index, use_frag):

        list_point_is_currently_within = []
        cl = self.point_locations[index]
        shapely_cl = Point(cl[0], cl[1])

        #ADDS TO LIST
        for point_index in range(0, len(self.point_locations)):

            if point_index != index:
                pol = self.get_active_pol(point_index, index, use_frag=use_frag)

                if pol.contains(shapely_cl):
                    list_point_is_currently_within.append(pol)
                else:
                    continue


        to_remain_in = 0

        for polygon_to_intersect in list_point_is_currently_within:
            if to_remain_in == 0:
                to_remain_in = polygon_to_intersect
            else:
                to_remain_in = to_remain_in.intersection(polygon_to_intersect)


        return to_remain_in







    def iterate(self):

        total_intersections_to_reach = 0

        for angles in self.angles_1:
            for angle in angles:
                total_intersections_to_reach += angle



        print(f" INTERSECTIONS TOTAL: {total_intersections_to_reach}")


        for iter in range(0, one_directory.movement_iteration):

            move1, denom1, total_intersections1, denom_quantity1, dist1 = self.get_movement_from_intersections()

            move2, denom2, denom_quantity2, dist2 = self.get_movement_from_lines()

            move3, denom3, denom_quantity3, dist3 = self.get_movement_from_polygon(use_frag=False)




            #IF BOTH ARE ACHIEVED (BEGIN INTER, AND MAINTAIN)
            if total_intersections1 == total_intersections_to_reach and \
                denom_quantity3 == 0:
                movement_to_use = 1
                maintenance = True
            else:

                #IF ONLY INTERSECTIONS IS REACHED --> DO POLYGON
                if total_intersections1 == total_intersections_to_reach:
                    movement_to_use = 3
                    maintenance = False

                #IF ONLY POLYGONS, DO ---> LINES  (POSSIBLE????)
                elif denom_quantity3 == 0:
                    movement_to_use = 2
                    maintenance = True


                #IF NEITHER ARE REACHED (DO POLYGONS???)
                else:
                    movement_to_use = 3
                    maintenance = False


            if movement_to_use == 3:
                a_move = move3
                a_den = denom3
            elif movement_to_use == 2:
                a_move = move2
                a_den = denom2
            else:
                a_move = move1
                a_den = denom1

            scaled_movement = []
                                    #######
            for m_index, u_move in enumerate(a_move):
                ###
                den = a_den[m_index]

                if den == 0:
                    scaled_movement.append([0,0])
                else:
                    scaled_movement.append([u_move[0]/den, u_move[1]/den])


            #print(f" SCALED MOVEMENT: {scaled_movement}")
            #print(f" ORIG: {move1}")


            if iter != one_directory.movement_iteration - 1:

                movement_done = self.super_move(scaled_movement, use_frag=False, maintain_within=maintenance)
                print(
                    f" {iter} {movement_to_use}    T_I: {total_intersections1}(({total_intersections_to_reach})) -- {round(dist1, 3)}     "
                    f"            T_P: -{denom_quantity3} -- {round(dist3, 3)}")
                #print(f"                                    {scaled_movement}")

            else:

                print(
                    f" {iter}     T_I: {total_intersections1}(({total_intersections_to_reach})) -- {round(dist1, 3)}     "
                    f"            T_P: -{denom_quantity3} -- {round(dist3, 3)}")
                print(f"LAST {self.point_locations}")
                #print(f"                                    {scaled_movement}")

























    #---------------------------------------------------------------------------------------------










    # def get_movement_from_lines(self):
    #     total_distance_between_lines = 0
    #
    #     total_events = 0
    #
    #     movement, denom = self.make_count_set()
    #
    #
    #     for tree_index, tree in enumerate(self.tree_list):
    #         #if not just single segment
    #         if len(tree.list_of_indexs) > 1:
    #
    #             base = tree.starting_photo - one_directory.starting_id
    #
    #             segs = self.get_tree_segments(tree)
    #
    #             non_intersections, angle_non_intersections, \
    #             num_failed, num_angle_failed = self.get_2_non_intersection_list(tree_index)
    #
    #
    #
    #
    #
    #             total_events += len(non_intersections)
    #
    #
    #             #FOR ALL VALID
    #             for lack_inter in non_intersections:
    #
    #                 ind1 = lack_inter[0] + base
    #                 ind2 = lack_inter[1] + base
    #
    #                 seg1 = segs[ind1 - base]
    #                 seg2 = segs[ind2 - base]
    #
    #
    #                 x_movement_from_1_to_2, \
    #                 y_movement_from_1_to_2 = self.get_starting_x_y_movement(seg1, seg2)
    #
    #                 total_distance_between_lines += math.sqrt(x_movement_from_1_to_2**2 + y_movement_from_1_to_2**2)
    #
    #
    #                 x_move, y_move, den = self.scale_movement(x_movement_from_1_to_2,
    #                                                      y_movement_from_1_to_2,
    #                                                      len(non_intersections))
    #
    #
    #
    #                 movement[ind1][0] += x_move
    #                 movement[ind1][1] += y_move
    #
    #                 movement[ind2][0] -= x_move
    #                 movement[ind2][1] -= y_move
    #
    #                 denom[ind1] += den
    #                 denom[ind2] += den
    #
    #
    #     #print(f" WHATS RETURNED FROM FUNCTION: {movement}")
    #     return movement, denom, total_events, total_distance_between_lines

    def get_2_non_intersection_list(self, index_of_tree):

        tree = self.tree_list[index_of_tree]
        segs = self.get_tree_segments(tree)
        angle_valid = self.invalid_angles[index_of_tree]

        counter = 0

        potential_intersection_cypher = []
        angular_failing_potential_intersection_cypher = []

        length_normal_fails = 0
        length_angle_failing_fails = 0

        # delt = tree.starting_photo - one_directory.starting_id

        # MAKES INTERSECTIONS TO STORE IN INT_LIST
        for outer_index, outer_seg in enumerate(segs):
            for inner_index, inner_seg in enumerate(segs):
                if outer_index < inner_index:
                    counter += 1
                    inter = outer_seg.intersection(inner_seg)

                    # MEANS IT DOESNT NEED TO INTERSECT
                    if angle_valid[counter - 1] == 0:

                        # IF IT DOES INTERSECT
                        if not inter.is_empty:
                            length_angle_failing_fails += 1
                        # IF DOSNT INTERSECTION
                        else:
                            angular_failing_potential_intersection_cypher.append([outer_index,
                                                                                      inner_index])
                    # MEANS IT SHOULD INTERSECT
                    else:
                        # IF IT DOES INTERSECT
                        if not inter.is_empty:
                            length_normal_fails += 1
                        # IF DOSNT INTERSECTION
                        else:
                            potential_intersection_cypher.append([outer_index,
                                                                      inner_index])

        return potential_intersection_cypher, angular_failing_potential_intersection_cypher, \
                   length_normal_fails, length_angle_failing_fails


    def get_movement_from_polygons(self, use_frag):
        total_fails = 0
        to_dists = 0

        movement, denom = self.make_count_set()

        # For Every Existing Point
        for point_index, point_location in enumerate(self.point_locations):
            # From Every other index, the Point needs to be within the polygon gained by P
            for polygon_index in range(0, len(self.point_locations)):
                #ASSUMING NOT SAME
                if point_index != polygon_index:

                    polygon_this_point_needs_to_be_within = self.get_active_pol(polygon_index, point_index, use_frag)


                    shapely_location = Point(point_location[0], point_location[1])

                    # MEANS POINT ALREADY WITHIN DESIRED
                    # IDEA BRING CLOSER TO CENTERS (TO PREVENT TIP TOUCHING)
                    if polygon_this_point_needs_to_be_within.contains(shapely_location):
                        continue
                    # POINT NOT WITHIN POLYGON
                    # IDEA MOVE TOWARD EACH OTHER
                    else:

                        # Need To Find Closest Point To It, To Then Determine Desired Movement
                        point_that_needs_to_be_within_polygon = shapely_location

                        closest_point_to_this_point, ignore = nearest_points(polygon_this_point_needs_to_be_within,
                                                                             point_that_needs_to_be_within_polygon)

                        # MOVEMENT OF POINT ---> POLYGON
                        x_move = closest_point_to_this_point.x - point_that_needs_to_be_within_polygon.x
                        y_move = closest_point_to_this_point.y - point_that_needs_to_be_within_polygon.y

                        # SCALING
                        if True:
                            val = one_directory.m_jitter

                            if math.sqrt(x_move**2 + y_move**2) < 0.1:
                                val = 0.02

                            # Print NEED TO UPDATE

                            x_move,y_move = self.extend_by_n(x_move, y_move, val)



                            x_move *= 0.5
                            y_move *= 0.5

                        movement[point_index][0] += x_move
                        movement[point_index][1] += y_move

                        movement[polygon_index][0] -= x_move
                        movement[polygon_index][1] -= y_move

                        denom[point_index] += 1
                        denom[polygon_index] += 1

                        total_fails += 1
                        to_dists += math.sqrt(x_move ** 2 + y_move ** 2)

        return movement, denom, total_fails, to_dists

    # RETURNS THE POLYGON OF ST -> ED, EXTENDING FROM LOCATION OF ST
    def get_active_pol(self, st, ed, use_frag):

        pol_rel_zero = self.pure_polygons.get_polygon(st, ed, use_frag)
        # NORMAL

        # MOVING IT RELATIVE TO STARTING
        moved_pol = translate(pol_rel_zero,
                                  xoff=self.point_locations[st][0],
                                  yoff=self.point_locations[st][1])
        return moved_pol


    # ----------TASK SPECIFIC HELPERS:----------------------------
    # ASSISTANCE METHODS  (ASSISTS WITH BELOW)

    def get_starting_x_y_movement(self, seg1, seg2):

        #IDEA, FIND THE AVERAGE
        c1 = list(seg1.coords)
        c2 = list(seg2.coords)

        p1, ig1 = nearest_points(seg2, Point(c1[0][0], c1[0][1]))
        p2, ig2 = nearest_points(seg2, Point(c1[1][0], c1[1][1]))
        p3, ig3 = nearest_points(seg1, Point(c2[0][0], c2[0][1]))
        p4, ig4 = nearest_points(seg1, Point(c2[1][0], c2[1][1]))



        av_x = (p1.x + p2.x + p3.x + p4.x)/4
        av_y = (p1.y + p2.y + p3.y + p4.y)/4

        average_point = Point(av_x, av_y)

        closest_point_on_seg1, ig5 = nearest_points(seg1, average_point)
        closest_point_on_seg2, ig6 = nearest_points(seg2, average_point)

        movement_x_from_1_to_2 = closest_point_on_seg2.x - closest_point_on_seg1.x
        movement_y_from_1_to_2 = closest_point_on_seg2.y - closest_point_on_seg1.y

        return movement_x_from_1_to_2, movement_y_from_1_to_2

    def scale_movement(self, x_move, y_move, total_inter):


        scalar = one_directory.m_dist_exp
        method = one_directory.m_weighting_scheme



        # COMPENSATE FOR DIST_EXP
        if True:
            if x_move > 0:
                x_move = math.pow(x_move, scalar)
            else:
                x_move = -1 * math.pow(abs(x_move), scalar)

            if y_move > 0:
                y_move = math.pow(y_move, scalar)
            else:
                y_move = -1 * math.pow(abs(y_move), scalar)



        # CUT IN HALF (THEN ADD BUFFER)
        if True:
            x_move *= 0.5
            y_move *= 0.5

            x_move, y_move = self.extend_by_n(x_move, y_move, one_directory.m_jitter)



        #COMPENSATE FOR WEIGHT
        if True:

            #EVERY INTERSECTION EQUAL (NO DENOM REQUIRED)
            if method == 0:
                return x_move, y_move, 1

            # MEANS DIVIDED BY NUMBER OF INTERSECTIONS
            elif method == 1:
                v = 1/total_inter
                return x_move/total_inter, y_move/total_inter, v

            #SOME OTHER METHOD I HAVNT YET DEVISES
            else:
                print("OTHER FAIL")






        # COMPENSATE FOR WEIGHT

    def extend_by_n(self, x, y, n):
        length = math.sqrt(x ** 2 + y ** 2)
        if length == 0:
            return x, y

        scale = n / length
        delta_x = x * scale
        delta_y = y * scale

        #IDEA DELTA WILL BE POSSIBLE, WHEN NEED TO BE POSITIVE, NEGATIVE WHEN NEED
        return x + delta_x, y + delta_y





    # ------- GENERAL HELPER ------------------
    def move_random_along_angle(self, angle, absolute, xy):
        angle = math.radians(angle)
        dx = absolute * math.sin(angle)
        dy = absolute * math.cos(angle)

        return (dx + xy[0], dy + xy[1])

    def move_line_segment(self, linesegment, xy):
        coords_to_add = []
        for coord in list(linesegment.coords):
            coords_to_add.append((coord[0] + xy[0], coord[1] + xy[1]))

        return LineString(coords_to_add)

    def move_point(self, point, x, y):

        return [point[0] + x, point[1] + y]



    # -----PRE SETUP-------

    # Prints All Points On Map
    def absolute_print_map(self):
        fig, ax = plt.subplots()

        for perspective_location in self.lof:
            # BOUND POLYGON POSSIBLE
            ax.fill(*perspective_location.bound.exterior.xy, color=perspective_location.color, alpha=0.1)
            plt.plot(*perspective_location.bound.exterior.xy, color=perspective_location.color)

            # EXACT LOCATION
            loc = perspective_location.centre
            plt.plot(loc[0], loc[1], marker="o", color=perspective_location.color)

            # TEXT
            plt.text(loc[0], loc[1], "ID " + str(perspective_location.frame_id - one_directory.starting_id),
                         fontsize=12, color='red')

        self.absolute_time_filter()

        for perspective_location in self.lof:
            # BOUND POLYGON POSSIBLE
            ax.fill(*perspective_location.bound.exterior.xy, color=perspective_location.color, alpha=0.1)
            plt.plot(*perspective_location.bound.exterior.xy, color=perspective_location.color)

        plt.grid()

    def absolute_time_filter(self):

        for outer_index, outer_frame in enumerate(self.lof):
            # For every frame within
            for inner_index, inner_frame in enumerate(self.lof):
                # Diagonalization to avoid repitition or equality
                if outer_index > inner_index:
                    # Max possible distance appart (time distance)
                    distance = abs(outer_frame.time - inner_frame.time) * one_directory.speed_per_second

                    # Creates buffered Distances extending
                    fo_e = outer_frame.bound.buffer(distance)
                    fi_e = inner_frame.bound.buffer(distance)

                    # The new frame 1 possibilities are the overlap between f1, original, and f2_e
                    outer_frame.bound = outer_frame.bound.intersection(fi_e)
                    # The new frame 2 possibilities are the overlap between f2 original and f1_1

                    inner_frame.bound = inner_frame.bound.intersection(fo_e)




    #----------MAJOR SETUP-------------------------------------------------------------------------

    # MAKES BOXS TO STORE MOVEMENT
    def make_count_set(self):
        movement_total = []
        movement_denom = []
        for index in range(0, len(self.lof)):
            movement_total.append([0, 0])
            movement_denom.append(0)
        return movement_total, movement_denom

    def make_polygon_matrix(self):
        print("FA")

    # Determines A Starting List of valid angles
    def make_angle_list(self, type):

        list_of_valid = []

        for tree in self.tree_list:
            list_of_index_values = []
            # number_failed = 0

            for outer_index in range(0, len(tree.list_of_indexs)):
                for inner_index in range(0, len(tree.list_of_indexs)):
                    if outer_index < inner_index:

                        b = tree.starting_photo - one_directory.starting_id
                        # MAKE SURE ANGLES ARE FAR ENOUGH APART (EVEN 350 - 5)
                        o_f = self.lof[b + outer_index].fragments[tree.list_of_indexs[outer_index]]
                        i_f = self.lof[b + inner_index].fragments[tree.list_of_indexs[inner_index]]

                        diff = abs(o_f.p0_dir - i_f.p0_dir)

                        # Adjust for circular range
                        circular_diff = min(diff, 360 - diff)


                        #MEANING USE INTERSECTION LEVELS
                        if type:
                            if circular_diff < one_directory.m_intersection_angle:
                                list_of_index_values.append(0)
                            else:
                                list_of_index_values.append(1)
                        else:
                            if circular_diff < one_directory.m_line_polygon_angle:
                                list_of_index_values.append(0)
                            else:
                                list_of_index_values.append(1)


            list_of_valid.append(list_of_index_values)

        return list_of_valid



    # Obtains All Photos Within Range (od.sr - od.er
    def make_list_of_photos(self):
        print(five_database.omni_obtain_frames())
        # obtaining all frame from database (can be improved)
        for frame in five_database.omni_obtain_frames():
            # Assuming Id's Start With 0
            self.lof.append(
                updated_frame.updated_frame(frame[0], frame[1],
                                                frame[2], frame[3],
                                                frame[4], frame[5],
                                                frame[6], self))

    def make_location_set(self, use_gps):
        llist = []
        if use_gps:
            print("USE GPS")
            for frame in self.lof:
                llist.append([frame.centre[0], frame.centre[1]])

        else:
            print("NOT GPS")

            decent_set = [[1.9433873732083042, -26.766982917030077], [1.2689582369760206, -25.776477469330036], [0.938155165602309, -24.691225938624637], [0.8797712540650866, -23.12525038427634], [0.465267904427673, -22.83900887268746], [-0.17214104515173625, -21.684300984204967], [-0.732970910746984, -20.7274120436354], [-1.426191239179401, -20.401114712968873], [-1.6713512257863876, -19.61030809079361]]


            llist = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
            llist = [[0,-5],[0,-10],[0,-15],[0,-20],[0,-25],[0,-30],[0,-35],[0,-40],[0,-45]]

            # llist = [[2.176204848528288, -30.269433742677485],
            #          [1.6162415864112725, -30.101127452701682],
            #          [1.272161235631625, -28.633138246167643],
            #          [1.203664142252774, -27.050094829752993],
            #          [0.81517636933629655, -27.0823884300533265], [0.3440677247347613, -25.64846319438394], [-0.2753815709718493, -24.604516140070693], [-0.9572161477538085, -24.305891456769753], [-1.2770858238900997, -23.06253648411148]]


            #llist = [[0,0], [30,0], [60,0], [90,0], [120,0], [150,0], [180,0], [210,0], [240,0]]


            # llist = [[0.86, -3.631], [0.691, -5.431], [-0.028, -2.858],
            #          [0, 0], [-1.064, 0.936], [-2.339, 2.519],
            #          [-3.114, 4.318], [-4.307, 4.719], [-3.465, 4.703]]

            # llist = [[1.138022957624074, -4.205986082070967], [0.37965695476842765, -3.102224036189324],
            #  [0.02225257766736161, -1.9308545732620073], [0.0, 0.0], [-0.6187090176248619, 0.5071092410796912],
            #  [-1.2677323652744148, 1.8266589395921815], [-2.0425061796969253, 3.0485181175184204],
            #  [-2.875754406086907, 3.384544664440446], [-3.250917961394677, 4.737785215367742]]
            #
            #
            # llist = [[2.563, -7.928], [0.691, -5.431], [-0.096, -3.675], [0, 0],
            #         [-1.181, 1.082], [-1.821, 2.523], [-2.78, 3.792], [-4.254, 4.771],
            #         [-5.045, 6.691]]


            # for index, frame in enumerate(self.lof):
            #     llist.append([index*10, index*10])

        return llist

    def make_segment_set(self):
        frag_loc = []
        # Creating According Line Segments // Angles
        for index, photo in enumerate(self.lof):

            row_list = []
            angle_list = []

            # Location To Start From
            starting_location = self.point_locations[index]

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

            frag_loc.append(row_list)
        return frag_loc

    # Given f1, f2, and end_range, creates tree objects
    # MAKES A SET OF TREES
    def make_trees(self, frame1, frame2, range_end):
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

            frame = self.lof[later_index_values - one_directory.starting_id]

            for later_index_fragment in range(0, len(frame.fragments)):
                if not later_index_fragment in curr_ind_list:
                    tree = fixed_point()
                    val = tree.create_and_cascade(later_index_values, later_index_fragment)
                    master_tree_list.append(tree)

        return master_tree_list