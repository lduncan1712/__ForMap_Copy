import copy
import math
import random

from shapely.geometry import Point, LineString, Polygon

import one_directory
from five_database import five_database
from fixed_point import fixed_point


class file_thirteen:

    def __init__(self, formal_list_polygon, formal_list_frames):

        #Sets Frames (as given list)
        self.frames = formal_list_frames

        #Sets Polygons Of Frames
        self.polygon_maps = formal_list_polygon

        #Creates The List Of Tree Lines
        self.tree_list = self.create_trees(self.frames[0], self.frames[1], len(self.frames) - 1 + one_directory.starting_id)

        #Creates A List Of Which Trees Exist During Which Frames
        self.ledger = self.ledger_from_trees()

        self.fragments_intersections = []
        self.intersections_positions = []

        self.angle_tolerance = 10

    #Creates Starting fragment_locations - line
                #     angle_change    - direction of angles
                #     angle_deviation - difference from start
    def make_starting_segments(self):
        self.angles_change = []
        # Where Points Are
        self.points_locations = []
        # Where Fragments Are
        self.fragments_locations = []
        #
        self.angle_deviation = []

        #Make Starting Locations (Relative To 0, origin)
        starting_point = self.frames[0].centre
        self.points_locations.append([0, 0])

        # Locate Every Other Point
        for next_photo_index in range(1, len(self.frames)):
            next_location = self.frames[next_photo_index].centre
            # Now Making Location Relative To Polygons
            # next_location = [next_location[0] - starting_point[0],
            #                  next_location[1] - starting_point[1]]
            #
            next_location = [ next_photo_index*30, next_photo_index*30]

            self.points_locations.append(next_location)



            #IF NOT WITHIN (PROBL IMPOSSIBLE TO GET ON RIGHT TRACK??

        # Creating According Line Segments // Angles
        for index, photo in enumerate(self.frames):

            row_list = []
            angle_list = []

            #Location To Start From
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

            self.angles_change.append(angle_list)
            self.angle_deviation.append(0)
            self.fragments_locations.append(row_list)


    def iterate_to_local_optima(self):
        #Create A Distance To Compare Using Starting Fragments
        self.starting_disjoint = self.obtain_point_distance(self.fragments_locations)
        self.starting = self.optain_overall_failure(self.starting_disjoint)


        allow = one_directory.ft_allow_multi_event
        leng = len(self.frames)

        for change_event in range(0, one_directory.ft_num_iterations):

            random_frame = int(random.uniform(0, leng))
            starting_point = self.points_locations[random_frame]
            starting_segments = self.fragments_locations[random_frame]

            if not allow:
                event_id = change_event % 2
            else:
                event_id = change_event % 3
                event_id = 0


            #MOVEMENT
            if event_id == 0:
                x_change = random.uniform(-1*one_directory.ft_dist_range, one_directory.ft_dist_range)
                y_change = random.uniform(-1*one_directory.ft_dist_range, one_directory.ft_dist_range)

                new_segments = self.master_position_change(x_change, y_change, starting_segments)

            #ANGLE
            elif event_id == 1:
                angle_change = random.uniform(-1*one_directory.ft_angle_range,
                                              one_directory.ft_angle_range)

                new_segments = self.master_angle_change(
                                                        angle_change,
                                                        starting_point,
                                                        starting_segments)
                if new_segments == False:
                    continue

            #BOTH
            else:
                #IDEA: move / angle in such a way that you are pointed toward main intersections effectively

                angle_change = random.uniform(-1 * one_directory.ft_angle_range,
                                              one_directory.ft_angle_range)

                change = self.make_multi_event_new_position(random_frame,
                                                                        angle_change,
                                                                        starting_point)
                if change == False:
                    continue

                new_segments = self.master_mult_event_change(angle_change,
                                                             change[0],
                                                             change[1],
                                                             starting_point,
                                                             starting_segments)









                continue

            #FROM HERE WE HAVE A MODIFIED SET OF SEGMENTS (APPLIED ON ONE FRAME)

            copy = self.total_copy()
            copy[random_frame] = new_segments

            attempted_expanded_distances = self.obtain_point_distance(copy)
            #print(f" EXPANDED {attempted_expanded_distances}")

            compacted_distances = self.optain_overall_failure(attempted_expanded_distances)

            #IF CLOSER
            if self.compare_distance_values(self.starting, compacted_distances):
                #print(f"  CLOSER: {change_event}(({event_id}))     {compacted_distances}")

                #FRAGMENTS CHANGE
                self.fragments_locations[random_frame] = new_segments


                #Movement
                if event_id == 0 or event_id == 2:
                    a = self.points_locations[random_frame]
                    self.points_locations[random_frame] = (a[0] + x_change, a[1] + y_change)

                #Angle
                if event_id == 1 or event_id == 2:
                    #Angle Deviation
                    self.angle_deviation[random_frame] += angle_change

                    for specific_angle in self.angles_change[random_frame]:
                        specific_angle += angle_change


                self.starting = compacted_distances
                self.starting_disjoint = attempted_expanded_distances





                #ANGLES CHANGE

                #ANGLE DEVIATION CHANGES

                #STARTING (2) IS REPLACED







        #
        #
        #     #get values from it
        #     distance_values = self.obtain_point_distance(copy)
        #     compacted_distances = self.optain_overall_failure(distance_values)
        #
        #
        #     if self.compare_distance_values(self.starting, compacted_distances):
        #
        #         #FRAGMENTS CHANGE
        #         self.fragments_locations[frame_to_try] = new_segments
        #
        #         #STARTING CHANGES
        #         self.starting = compacted_distances
        #
        #         self.intersections_positions = distance_values
        #
        #         #ANgle
        #         if change_event % 3 == 0:
        #             print(f"ANGLE {self.starting}")
        #             self.angle_deviation[frame_to_try]+=att
        #         #Location
        #         elif change_event % 3 == 1:
        #             print(f"LOCATION {self.starting}")
        #
        #             #POINT
        #             a = self.points_locations[frame_to_try]
        #             self.points_locations[frame_to_try] = (a[0] + x_to_try, a[1] + y_to_try)
        #
        #         else:
        #             print("")
        #
        #
        return self.points_locations, self.tree_list, self.fragments_locations











    #Given The Index of a frame, and a set of new line segments that go within it,
    #returns true if the distance value of the new is closer
    def dvons(self, index, new):
        copy_to_evaluate = self.total_copy()
        copy_to_evaluate[index] = new

        expanded_intersections = self.obtain_point_distance(copy_to_evaluate)

        contracted_intersections = self.optain_overall_failure(expanded_intersections)

        return self.compare_distance_values(self.starting, contracted_intersections)

    #Method that returns a point in a given direction, and distance
    def move_random_along_angle(self, angle, absolute, xy):
        angle = math.radians(angle)
        dx = absolute * math.sin(angle)
        dy = absolute * math.cos(angle)


        return (dx + xy[0], dy + xy[1])

    #Returns a list of linesegments whose ls are rotated, false if impossible
    def master_angle_change(self, angle_change, point_of_origin, current_linesegments):

        list_to_return = []

        for linesegment in current_linesegments:

            new_linesegment = self.change_angle(linesegment, angle_change, point_of_origin)
            list_to_return.append(new_linesegment)

        return list_to_return

    def master_position_change(self, x,y, linesegments):

        list_to_return = []

        for ls in linesegments:

            new_linestring_location = self.translate_linestring_location(ls, x, y)
            list_to_return.append(new_linestring_location)

        #print(list_to_return)

        return list_to_return


    def master_mult_event_change(self, angle, x, y, starting_point, starting_segments):

        angle_modified_segments = self.master_angle_change(angle, starting_point, starting_segments)

        angle_modified_moved = self.master_position_change(x,y, angle_modified_segments)

        return angle_modified_moved




    def make_multi_event_new_position(self, index, angle, starting_location):
        #Choose 2 With Good Length That Are Within this index (preferably with more then 3)
        first_location = 0
        second_location = 0

        first_angle = 0
        second_angle = 0

        for t_index, tree in enumerate(self.tree_list):

            if t_index in self.ledger[index] and len(tree.list_of_indexs) > 2:

                #Finding the frag index at this value
                frag_index = index + one_directory.starting_id - tree.starting_photo
                angle = self.angles_change[index][frag_index]

                if first_location == 0:
                    first_location = t_index

                    #Finding what index this represents at given index
                    first_angle = angle
                elif second_location == 0:
                    second_location = t_index
                    second_angle = angle
                else:
                    break

        #From Here We Have 2 Trees That Occur At The Correct Index
        actual_first_point = self.starting_disjoint[first_location][4]
        actual_second_point = self.starting_disjoint[second_location][4]

        difference = self.make_intersection(starting_location, actual_first_point,
                                            actual_second_point,
                                            first_angle + angle,
                                            second_angle + angle)

        return difference










    def potential_angle_change(self, index, angle, points, lines, angles):
        #Makes New Using Previous
        new_angle = angles[index] + angle

        #If Valid To Do
        if abs(new_angle) < self.angle_tolerance:

            points, new_line_segments = self.turn_point_and_linesegments(index, angle, points, lines)


            new_values = self.obtain_point_distance(new_line_segments)

            consolidated_values = self.optain_overall_failure(new_values)

            #True Meaning Starting Is Closer
            if not self.compare_distance_values(self.starting, consolidated_values):
                #print(f"SECOND NOT BETTER: {self.starting} {consolidated_values} {self.fragments_locations} {self.points_locations}")
                return False

            #Means New Is Closer
            else:
                print(f"SECOND __ BETTER: {self.starting} {consolidated_values} {self.fragments_locations} {self.points_locations}")

                #Set New Starting
                self.starting = consolidated_values

                #Set Angles
                self.angles_change[index] = new_angle

                #Set New LineSegments
                self.fragments_locations[index] = new_line_segments[index]

                return True

        else:
            return False


    #IDEA Given 2 Angle, and starting locations, reverse engineer starting point
    #Used To Achieve Both
    def make_intersection(self, previous, location1tostart, location2tostart, angle1NotYetReversed, angle2NotYetReversed):

        f1_angle = angle1NotYetReversed + 180 % 360
        f2_angle = angle2NotYetReversed + 180 % 360

        p11 = location1tostart
        p12 = self.move_random_along_angle(f1_angle, 100, (location1tostart.x, location1tostart.y))

        set1 = [p11,p12]

        ls1 = LineString(set1)

        p21 = location2tostart
        p22 = self.move_random_along_angle(f2_angle, 100, (location2tostart.x, location2tostart.y))

        set2 = [p21, p22]

        ls2 = LineString(set2)

        location = ls1.intersection(ls2)

        if location.is_empty:
            return False

        else:
            x_difference = location.x - previous[0]
            y_difference = location.y - previous[1]

            return (x_difference, y_difference)



    def change_angle_list(self, index, change):
        for index, fragment in enumerate(self.angles_change[index]):

            self.angles_change[index][index]+=change


    # def potential_location_change(self, index, x, y):
    #
    #     new_location_set, new_line_segments = self.move_point_and_linesegments(index, x, y, self.points_locations, copy.copy(self.fragments_locations))
    #
    #     #IN POLYGON????
    #
    #     new_basic_values = self.obtain_point_distance(new_line_segments)
    #
    #     new_total = self.optain_overall_failure(new_basic_values)
    #
    #     #Starting Keeps
    #     if not self.compare_distance_values(self.starting, new_total):
    #         #print(f"SECOND NOT BETTER: {self.starting} {new_total} {self.fragments_locations} {self.points_locations}")
    #         return False
    #     #Changes
    #     else:
    #         print(f"SECOND __ BETTER: {self.starting} {new_total} {self.fragments_locations} {self.points_locations}")
    #
    #         #Changes Points
    #         self.points_locations[index] = new_location_set[index]
    #
    #         #Changes LineString
    #         self.fragments_locations[index] = new_line_segments[index]
    #
    #         #Starting
    #         self.starting = new_total
    #
    #         #print(f" CHANGING {index}")
    #
    #         return True


    def compare_distance_values(self, first, second):
        #print(f" COMPARING: {first} {second}")

        #PRINT TRUE IF CHANGED (SECOND CLOSER)

        #If First Has Higher Number Completed,
        if first[0] > second[0]:
            return False
        #If Second has Higher Number Completed
        elif first[0] < second[0]:
            return True

        #Same Number Of Completed
        else:
            #If First Has Lower Distance
            if first[1] < second[1]:
                return False

            #Second Has Lower Distance
            elif first[1] > second[1]:
                return True

            else:
                print("SAME CASE")


    #Given f1, f2, and end_range, creates tree objects
    def create_trees(self, frame1, frame2, range_end):
        master_tree_list = []
        fd = five_database()

        # Create Simple First
        #(Trees That Appear In First)
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


    #creates a list holding lists, where all indexs in each index, tell which trees exist during which frames
    def ledger_from_trees(self):

        ledger = []

        #Creates A List For Every Frame
        for photo_index in range(0, len(self.frames)):
            ledger.append([])

        #Adds Tree Indexs, to whatever frames they occur in
        for index, tree in enumerate(self.tree_list):
            for after in range(0, len(tree.list_of_indexs)):
                ledger[after + tree.starting_photo - one_directory.starting_id].append(index)
        return ledger


    def omni_get_ls_per_tree(self, tree, ls):
        list_to_return = []
        starting_index = tree.starting_photo - one_directory.starting_id

        for index, value in enumerate(tree.list_of_indexs):
            list_to_return.append(ls[index + starting_index][value])

        return list_to_return






    def obtain_forces_from_tree(self, segs):
        force_vectors = []
        double_intersection = []

        for oi, ot in enumerate(segs):
            single_intersection = []
            for ii, it in enumerate(segs):
                if ii >= oi:

                    inter_maybe = ot.intersection(it)

                    #INTERSECTION
                    if not inter_maybe.is_empty:
                        single_intersection.append(inter_maybe)
                    #NO INTERSECTION
                    else:
                        single_intersection.append(None)

                        distance_between_lowest = ot.distance(it)





            double_intersection.append(single_intersection)










    def omni_obtain_average(self, segs, it, plt):
        half_weighted = []
        full_weighted = []


        for outer_index, outer_ls in enumerate(segs):
            for inner_index, inner_ls in enumerate(segs):
                if outer_index < inner_index:
                    print(f"OUTER {it}")
                    inter = outer_ls.intersection(inner_ls)

                    #INTERSECTION EXISTS
                    if not inter.is_empty:
                        full_weighted.append(inter)

                        if it == 2:
                            print(f"SHOULD PRINT  {inter.x} {inter.y}")
                            plt.plot(inter.x, inter.y, color="blue", markersize=10)

                    #NO INTERSECTION
                    else:
                        # pol1 = outer_ls.interpolate(outer_ls.project(inner_ls))
                        # pol2 = inner_ls.interpolate(inner_ls.project(outer_ls))

                        point = self.alpha_middle(outer_ls, inner_ls)

                        pol1, pol2 = self.omni_closest_between(outer_ls, inner_ls)
                        #
                        average_x = (pol1.x + pol2.x) / 2
                        average_y = (pol1.y + pol2.y) / 2

                        #
                        half_weighted.append(Point(average_x, average_y))
                        #half_weighted.append(point)

                        # if it == 2:
                        #     print(f"SHOULD PRINT HALF  {average_x} {average_y}")
                        #     plt.plot(average_x,average_y, color="orange")

        super_x = 0
        super_y = 0

        for point in full_weighted:
            super_x+= point.x
            super_y+= point.y


        for point in half_weighted:
            super_x += point.x#*one_directory.ft_weight_of_disjoint
            super_y += point.y#*one_directory.ft_weight_of_disjoint



        div = len(segs) + (len(half_weighted))#*one_directory.ft_weight_of_disjoint)
        super_x /= div
        super_y /= div

        print(f"SO AVERAGE IS: {super_x} {super_y}")

        return super_x, super_y


    def omni_vector_change(self, segment, av):


        print(av.distance(segment))
        closest_point = segment.interpolate(segment.project(av))
        print(f" C {av.x - closest_point.x} {av.y - closest_point.y}")
        return av.x - closest_point.x, av.y - closest_point.y





    def alpha_macro(self):

        starting_segments = self.fragments_locations


        for iteration in range(0, one_directory.ft_iterations):
            print("B")



    def alpha_score(self, ls):
        print("A")

    def alpha_movement(self, ls):
        total_change = []
        total_weight = []

        for index in range(0, len(ls)):
            total_change.append([0, 0])
            total_weight.append(0)

        for tree in self.tree_list:

            if len(tree.list_of_indexs) > 1:
                # The Starting Segments
                set_of_seg = self.omni_get_ls_per_tree(tree, ls)


                list_of_intersections = []
                values_of_disjoint = []

                for outer_index, outer_seg in enumerate(set_of_seg):
                    value_1 = []
                    for inner_index, inner_seg in enumerate(set_of_seg):

                        inter = outer_seg.intersection(inner_seg)

                        # IF THEY INTERSECT
                        if not inter.is_empty:

                            value_1.append(inter)

                        # DONT INTERSECT
                        else:
                            value_1.append(0)

                    list_of_intersections.append(value_1)

    #IDEA: bring all intersections together + disjoint together




    def ep_moving_st(self, ls):
        #HOLDS LOCATION OF ALL INTERSECTIONS (0) OTHERWISE
        loc_intercept = []
        #HOLDS LOCATION OF ALL NON-INTER INTERSECTION
        loc_disjoint = []
        #HOLDS DISTANCES BETWEEN INTERSECTIONS
        distance_both = []



        #Makes Above
        for oi, ols in enumerate(ls):
            row = []
            for ii, ils in enumerate(ls):
                if oi < ii:

                    inter_maybe = ols.intersection(ils)

                    #INTERSECTS
                    if not inter_maybe.is_empty:
                        loc_intercept.append(inter_maybe)
                        distance_both.append(0)

                    else:
                        #NO DIRECT INTERCEPT
                        loc_intercept.append(None)

                        #MAKE A PARTIAL INTERCEPT
                        point_of_intersection = self.alpha_middle(ols, ils)

                        #ADD IT TO DISJOINT
                        loc_disjoint.append(point_of_intersection)

                        #Distance Between Segments Is >0
                        distance_both.append(ols.intersection(ils))


        #FROM HERE WE HAVE A LIST OF ALL INTERSECTIONS, SEMI-INTER...., DISTANCES

        #GOALS: CLOSE AS POSSIBLE INTERSECTION,
        #       CLOSE AS POSSIBLE DISJOINT
        #       ACCEPTABLE WITHIN CERTAIN RANGE


        #STRONG FORCE FOR CLOSER??


        #MOVING POINTS CLOSER TOGETHER











    def final_obtain_forces_on_tree(self, ls):
        intersections_or_lines = []

        for o_index, o_seg in enumerate(ls):
            row = []
            for i_index, i_seg in enumerate(ls):

                inter = o_seg.intersection(i_seg)

                #IF AN INTERSECTION OCCURS
                if not inter.is_empty:
                    row.append(inter)

                #NO INTERSECTION
                else:
                    #MAKE LINE
                    print("FD")





    def final_obtain_average_line(self):

        print("ZA")



    def z_move(self):
        total_moves = []
        for x in range(0, len(self.fragments_locations)):
            total_moves.append([0,0])


        for tree in self.tree_list:
            if len(tree.list_of_indexs) > 4:

                applicable_segments = self.omni_get_ls_per_tree(tree, self.fragments_locations)
                start = tree.starting_photo - one_directory.starting_id

                forces, intersections, total = self.a_forces_for_single_tree(applicable_segments)

                for index, force in enumerate(forces):
                    total_moves[index + start][0] += force[0]/ len(tree.list_of_indexs)
                    total_moves[index + start][1] += force[1] /len(tree.list_of_indexs)

        print(f" MOVES: {total_moves}")
        self.omni_adjust_all_values(total_moves)







    def a_forces_for_single_tree(self, ls):
        forces = []
        for index in range(0, len(ls)):
            forces.append([0,0])

        number_of_total = 0
        number_of_intersection = 0

        for o_index, o_seg in enumerate(ls):
            for i_index, i_seg in enumerate(ls):

                inter = o_seg.intersection(i_seg)

                number_of_total+=1

                #IF AN INTERSECTION OCCURS
                if not inter.is_empty:
                    number_of_intersection += 1
                #NO INTERSECTION
                else:
                    #FIND DISTANCE BETWEEN (AND ACCORDING FORCES)
                    distance = i_seg.distance(o_seg)

                    #FORCE TOTAL OF THIS MOVEMENT
                    force = one_directory.ft_a_c1 * \
                            math.log(10, distance/one_directory.ft_a_c2)

                    #MIDDLE POINT BETWEEN LS (USED FOR DIRECTION ONLY)
                    total_middle = self.alpha_middle(i_seg, o_seg)

                    #FINDING THE POINTS CLOSEST
                    point_on_o = o_seg.interpolate(o_seg.project(total_middle))
                    point_on_i = i_seg.interpolate(i_seg.project(total_middle))

                    #DISTANCE BETWEEN 2 ARTIFICAL CENTRE POINTS
                    exagerated_distance = point_on_i.distance(point_on_o)

                    #SCALAR
                    scaled_force = force/exagerated_distance

                    #DETERMINING FORCES BEING APPLIED
                    ox, oy, ix, iy = self.forces_applied(scaled_force, point_on_o, point_on_i)

                    forces[o_index][0] += ox
                    forces[o_index][1] += oy
                    forces[i_index][0] += ix
                    forces[i_index][1] += iy

        return forces, number_of_intersection, number_of_total







    def forces_applied(self, force_coefficent, po, pi):

        x_o_subtract_i = (po.x - pi.x) / 2
        y_o_subtract_i = (po.y - pi.y) / 2

        o_movement_x = -1* x_o_subtract_i*force_coefficent
        o_movement_y =  -1* y_o_subtract_i*force_coefficent

        i_movement_x = x_o_subtract_i*force_coefficent
        i_movement_y = y_o_subtract_i*force_coefficent

        return o_movement_x, o_movement_y, i_movement_x, i_movement_y



























    #Obtains A "Middle Between 2 Disjoint LS
    def alpha_middle(self, seg1, seg2):
        #IDEA: Average between all 4 corner intersection
        seg1_coords = list(seg1.coords)
        seg2_coords = list(seg2.coords)

        c1 = seg1.interpolate(seg1.project(Point(seg2_coords[0][0], seg2_coords[0][1])))
        c2 = seg1.interpolate(seg1.project(Point(seg2_coords[1][0], seg2_coords[1][1])))
        c3 = seg2.interpolate(seg2.project(Point(seg1_coords[0][0], seg1_coords[0][1])))
        c4 = seg2.interpolate(seg2.project(Point(seg1_coords[1][0], seg1_coords[1][1])))

        av_x = (c1.x + c2.x + c3.x + c4.x) / 4
        av_y = (c1.y + c2.y + c3.y + c4.y) / 4

        return Point(av_x, av_y)






    def alpha_average(self, set_of_seg):
        list_of_intersections = []

        for outer_index, outer_seg in enumerate(set_of_seg):
            value_1 = []
            for inner_index, inner_seg in enumerate(set_of_seg):

                inter = outer_seg.intersection(inner_seg)

                #IF THEY INTERSECT
                if not inter.is_empty:

                   value_1.append(inter)

                # DONT INTERSECT
                else:
                    value_1.append(0)




        x = 0
        y = 0
        for point in list_of_intersections:
            x += point[0]
            y += point[1]

        a = len(list_of_intersections)

        if a > 0:
            x /= a
            y /= a
            return [x, y]
        else:
            None


















    #REVITALIZE USING BETTER
    # - better weighting
    # - better movement for disjoint
    # - option for test
    # - some concept for NEAR parellel lines
    # - APPROPEITE SCALING..
    # FIXING 3 PROBLEM
    def omni_movement_3(self, ls, test, plt):
        total_change = []
        total_weight = []

        for index in range(0, len(ls)):
            total_change.append([0, 0])
            total_weight.append(0)

        for tree in self.tree_list:

            if len(tree.list_of_indexs) > 1:

                #The Starting Segments
                prev_segs = self.omni_get_ls_per_tree(tree, ls)



    def omni_movement_3_inner(self, set_of_seg):
        list_of_intersections = []

        for outer_index, outer_seg in enumerate(set_of_seg):
            for inner_index, inner_seg in enumerate(set_of_seg):

                inter = outer_seg.intersection(inner_seg)

                #IF THEY INTERSECT
                if not inter.is_empty:

                    list_of_intersections.append(inter)

                # DONT INTERSECT
                else:
                    print("FA")


        x = 0
        y = 0
        for point in list_of_intersections:
            x += point[0]
            y += point[1]

        a = len(list_of_intersections)
        if a > 0:
            x /= a
            y /= a

























    #IDEA BRING SEGMENTS INTERSETIONS TOGETHER
    def omni_movement_2(self, ls):


        # Setup lists



        for tree in self.tree_list:

            #DETERMINING WHERE TO MOVE
            if len(tree.list_of_indexs) > 1:
                segments_to_use = self.omni_get_ls_per_tree(tree, ls)










    #GETS MOVEMENT SHOULD OCCUR
    def omni_movement(self, ls, plt, it):

        total_change = []
        total_weight = []

        #Setup lists
        for index in range(0, len(ls)):
            total_change.append([0,0])  #ERROR
            total_weight.append(0)

        #Apply every value to movement
        for tr in self.tree_list:


            #Multiple Values Enough To Use
            if len(tr.list_of_indexs) > 1:

                applicable_segs = self.omni_get_ls_per_tree(tr, ls)
                print(f" ONES SAID TO USE: {applicable_segs}")


                le = len(applicable_segs)

                average = self.omni_obtain_average(applicable_segs, it, plt)
                average = Point(average[0], average[1])
                print(f"AVERAGE:  {average}")

                # if it == 2:
                #
                #     plt.plot(average.x, average.y, marker="*", color="red")
                #
                #     for se in applicable_segs:
                #         a,b = se.xy
                #         plt.plot(a,b, color="red")

                starting = tr.starting_photo - one_directory.starting_id

                for index, single_segment in enumerate(applicable_segs):
                    frame = starting + index

                    location_change_x, location_change_y = self.omni_vector_change(single_segment,
                                                                                   average)
                    print(f" DISTANCE FROM AV:  {location_change_x} {location_change_y}")
                    #MEANS DIVIDE BY LENGTH (EQUAL WEIGHT BY TREE)
                    if one_directory.ft_equal_tree:
                        # print("VAL")
                        # print(total_change[frame][0])
                        # print(location_change_x)
                        total_change[frame][0] += (location_change_x/le)
                        total_change[frame][1] += (location_change_y/le)
                        total_weight[frame] += (1/le)
                    #DONT (WEIGHT BE FRAG)
                    else:
                        total_change[frame][0] += location_change_x
                        total_change[frame][1] += location_change_y
                        total_weight[frame] += 1


                #break

            else:
                continue


        #Apply Changes
        list_to_return = []
        for index, tc in enumerate(total_change):
            if total_weight[index] != 0:
                uv = [tc[0]/total_weight[index], tc[1]/total_weight[index]]
            else:
                uv = tc
            list_to_return.append(uv)

        #Return Desired Change
        return list_to_return


    def omni_adjust_all_values(self, list_of_values_to_change):

        list_to_return = []

        updated_points = []

        for frame_index, fragments in enumerate(self.fragments_locations):
            deltas = list_of_values_to_change[frame_index]
            updated_lines = self.move_point_and_linesegments(deltas[0], deltas[1], fragments)

            prev = self.points_locations[frame_index]
            # print(prev)
            # print(deltas)
            point = [prev[0] + deltas[0], prev[1] + deltas[1]]

            list_to_return.append(updated_lines)
            updated_points.append(point)

        self.fragments_locations = list_to_return
        self.points_locations = updated_points



    def omni_assess_status(self, ls):
        number_of_intersections = 0
        number_of_close = 0
        overall_distance = 0

        #IDEA DETERMINE THE NUMBER OF FRAGMENTS THAT INTERSECT OR ARE CLOSE ENOUGH TOGETHER THAT MATTED
        for tree in self.tree_list:

            if len(tree.list_of_indexs) > 1:

                segs = self.omni_get_ls_per_tree(tree, ls)

                for outer_index, outer_seg in enumerate(segs):
                    for inner_index, inner_seg in enumerate(segs):
                        if inner_index > outer_index:

                            inter = outer_seg.intersection(inner_seg)

                            #MEANS TOUCHS
                            if not inter.is_empty:
                                number_of_intersections += 1

                            #DOESNT TOUCH
                            else:
                                # cp1= outer_seg.interpolate(outer_seg.project(inner_seg))
                                # cp2 = inner_seg.interpolate(inner_seg.project(outer_seg))
                                #
                                cp1, cp2 = self.omni_closest_between(outer_seg, inner_seg)

                                d = cp1.distance(cp2)

                                #TOO MUCH DISTANCE
                                if d > one_directory.ft_distance_acceptable:
                                    overall_distance += d
                                else:
                                    number_of_close += 1

        return [number_of_intersections, number_of_close, overall_distance]

    #IDEA IF DONT INTERSECT LS should intersect at someones ends
    def omni_closest_between(self, ls1, ls2):

        lol1 = 0
        lol2 = 0
        shortest_distance = 10000000


        #USING ENDPOINTS OF LS1
        for ls1_ep in list(ls1.coords):
            ls1_ep = Point(ls1_ep[0], ls1_ep[1])
            cp = ls2.interpolate(ls2.project(ls1_ep))
            #NEW CLOSER
            d = cp.distance(ls1_ep)
            if d < shortest_distance:
                shortest_distance = d
                lol1 = ls1_ep
                lol2 = cp


        #USING ENDPOINTS OF LS2
        for ls2_ep in list(ls2.coords):
            ls2_ep = Point(ls2_ep[0], ls2_ep[1])
            cp = ls1.interpolate(ls1.project(ls2_ep))

            d = cp.distance(ls2_ep)
            if d < shortest_distance:
                shortest_distance = d
                lol1 = cp
                lol2 = ls2_ep

        return lol1, lol2




     #RETURNS TRUE IF FIRST IS BETTER  (int, close, dist)
    def omni_first_is_better(self, values1, values2):

         #IF NUMBER OF INTER + CLOSE IS MORE
         if values1[0] + values1[1] > values2[0] + values2[1]:
             return True
         #IF DISTANCE IS SMALLER
         elif values1[2] < values2[2]:
             return True
         else:
             return False

    def omni_adjust_single_value(self, reco_movement, starting_segs, index):
        deltas = reco_movement[index]
        starting_segs[index] = self.move_point_and_linesegments(deltas[0], deltas[1], starting_segs[index])

        return starting_segs

    def omni_macro(self, plt):
        starting_positions = self.points_locations

        starting_segments = self.fragments_locations
        starting_scoring_data = self.omni_assess_status(starting_segments)





        #For Every Iteration
        for iteration in range(0, one_directory.ft_iterations):

            recommended_movement = self.omni_movement(starting_segments, plt, iteration)
            #print(f"PRE   RECM:  {recommended_movement}")
            recommended_segments = self.omni_adjust_all_values(recommended_movement,
                                                               starting_segments)

            new_score = self.omni_assess_status(recommended_segments)

            #IF OLD BETTER
            if False: #self.omni_first_is_better(starting_scoring_data, new_score):
                print("ITERATION FAILED")
                print(f"     OLD {starting_scoring_data}  "
                      f"     NEW {new_score}")
            #IMPROVEMENT
            else:
                starting_scoring_data = new_score
                starting_segments = recommended_segments
                print(f"IMPROVEMENT?:  {new_score}  {recommended_movement}")

                #print(starting_positions[0][0])
                for index, movement in enumerate(recommended_movement):
                    #print(f" RECOM MOVE: {type(starting_positions[index])}")

                    starting_positions[index][0] += movement[0]
                    starting_positions[index][1] += movement[1]


        return starting_positions, starting_segments, self.tree_list




































    # def omni_attempt(self, ls):
    #     delta_list = []
    #     for index in range(0, len(ls)):
    #         delta_list.append((0,0))
    #
    #
    #     for tree in self.tree_list:
    #         #Means should be actually possible
    #         if len(tree.list_of_indexs) > 1:
    #
    #             starting_frame = tree.starting_photo - one_directory.starting_id
    #
    #             matrix = []
    #
    #             #CREATES MATRIX OF INTERSECTIONS
    #             for outer_index in range(0, len(tree.list_of_indexs)):
    #                 row = []
    #                 # Touching Every Other Fragment
    #                 for inner_index in range(outer_index + 1, len(tree.list_of_indexs)):
    #
    #                     # The indexs needs
    #                     index_1 = tree.list_of_indexs[outer_index]
    #                     index_2 = tree.list_of_indexs[inner_index]
    #
    #                     # getting linesegment from list
    #                     line_segment_1 = ls[outer_index + starting_frame][index_1]
    #                     line_segment_2 = ls[inner_index + starting_frame][index_2]
    #
    #                     # The intersection of this point
    #                     inter = line_segment_1.intersection(line_segment_2)
    #
    #                     # Intersects Clearly
    #                     if not inter.is_empty:
    #                         row.append(inter)
    #                     else:
    #                         row.append(0)
    #                 matrix.append(row)
    #
    #
    #             #NOW HAVE A PYRAMID OF VALUES
    #
    #
    #             #FOR ALL ROWS
    #             for common_row_index, common_row in enumerate(matrix):
    #                 #FOR EVERY INDEX IN THE ROW
    #                 for starting_index, starting_value in enumerate(common_row):
    #                     val1 = common_row[starting_index]
    #                     #SINCE LIST STARTS AFTER FRAME OF COMMON
    #                     f1 = starting_frame + common_row_index + starting_index + 1
    #                     #IF ITS A POINT
    #                     if not val1 == 0:
    #                         for ending_index, ending_value in enumerate(common_row):
    #                             if starting_index < ending_index:
    #                                 val2 = common_row_index[ending_index]
    #                                 f2 = starting_frame + common_row_index + ending_index + 1
    #                                 #IF ITS A POINT TOO
    #                                 if not val2 == 0:
    #
    #                                     #WEIGHT
    #                                     x_diff = val2.x - val1.x
    #                                     y_diff = val2.y - val1.y
    #                                     #WEIGHT
    #
    #                                     delta_list[f1][0] += x_diff
    #                                     delta_list[f1][1] += y_diff
    #
    #                                     delta_list[f2][0] -= x_diff
    #                                     delta_list[f2][1] -= y_diff
    #
    #
    #             #MIX ALL COLUMNS AND ROWS
    #
    #             #FOR EVERY POINT (GOING DOWNWARDS)
    #             for starting_row_index, starting_row_value in enumerate(matrix):
    #                 for starting_column_index, starting_value in enumerate(starting_row_index):
    #                     #MEANS THE INTERSECTION BETWEEN THESE 2 COLUMNS IS A POINT
    #                     if not starting_value == 0:
    #
    #                         f1_a = starting_frame + starting_row_index
    #                         f2_a = f1_a + starting_column_index + 1
    #                         loc_a = starting_value
    #
    #                         #FOR EVERY POINT BELOW IT
    #                         for ending_row_index in range(starting_row_index, len(matrix)):
    #                             for ending_column_index in range(0, len(starting_row_value)):
    #                                 if ending_row_index == starting_row_index and starting_column_index >= ending_column_index:
    #                                     continue
    #                                 else:
    #                                     if not matrix[ending_row_index][ending_column_index] == 0:
    #                                         f1_b = starting_frame + ending_row_index
    #                                         f2_b = f1_b + ending_column_index + 1
    #                                         location_b = matrix[ending_row_index][ending_column_index]
    #
    #                                         #SAME ROW
    #                                         if f1_a == f1_b:
    #                                             v1 = f2_a
    #                                             v2 = f2_b
    #
    #                                         #SAME COLUMN
    #                                         elif f2_a == f2_b:
    #                                             v1 = f1_a
    #                                             v2 = f1_b
    #
    #                                         #NEITHER
    #                                         else:
    #                                             continue
    #
    #                                         #VAL 1 AND VAL 2 INDICATE FRAMES THAT NEED TO BE CHANGED
    #                                         #LOCATION 1 / 2 ARE LOCATIONS OF INTERSECTIONS
    #


    #Given a cache of current line_segments
    #Returns a list of average location and distance
    #LO: (SD, NF, DF)
    def obtain_point_distance(self, line_segments_to_use):
        data_to_return = []

        for tree in self.tree_list:

            intersection_location = []
            number_of_failures = 0
            number_of_success = 0
            distance_of_failure = 0
            distance_of_success = 0

            # If Tree Has Multiple Values
            if len(tree.list_of_indexs) > 1:

                start = tree.starting_photo - one_directory.starting_id

                # print("PRINTABLE")
                # print(f"   LINESEGMENTS: {line_segments_to_use}")

                # For Every Fragment
                for outer_index in range(0, len(tree.list_of_indexs)):
                    # Touching Every Other Fragment
                    for inner_index in range(outer_index + 1, len(tree.list_of_indexs)):

                        # The indexs needs
                        index_1 = tree.list_of_indexs[outer_index]
                        index_2 = tree.list_of_indexs[inner_index]

                        # getting linesegment from list
                        line_segment_1 = line_segments_to_use[outer_index + start][index_1]
                        line_segment_2 = line_segments_to_use[inner_index + start][index_2]

                        # The intersection of this point
                        inter = line_segment_1.intersection(line_segment_2)

                        # Intersects Clearly
                        if not inter.is_empty:

                            # add to list of intersection locations
                            intersection_location.append(inter)

                            # increase number of successes
                            number_of_success += 1

                        # Doesnt Intersect
                        else:

                            # increasing distance of failures
                            distance_of_failure += line_segment_1.distance(line_segment_2)

                            # increasing number of failures
                            number_of_failures += 1

                # Makes Major Point From All Intersections
                super_x = 0
                super_y = 0
                for location in intersection_location:
                    super_x += location.x
                    super_y += location.y

                if len(intersection_location) > 0:
                    super_x /= len(intersection_location)
                    super_y /= len(intersection_location)
                new_average = Point(super_x, super_y)

                # self.ts.ts.plot_perspective.plot(new_average.x, new_average.y, marker="o", color=tree.color)

                distance_lost = 0
                # Creates Distance From It (Using Distance from every point to av)
                for location in intersection_location:

                    unremoved_distance = location.distance(new_average)

                    if unremoved_distance >= one_directory.ft_minimum_diff:
                        unremoved_distance -= one_directory.ft_minimum_diff
                        distance_lost += one_directory.ft_minimum_diff
                    else:
                        distance_lost += unremoved_distance
                        unremoved_distance = 0

                    distance_of_success += unremoved_distance

                data = [number_of_success, distance_of_success, number_of_failures, distance_of_failure, new_average,
                        distance_lost]

                data_to_return.append(data)

            else:
                data_to_return.append([0, 0, 0, 0, 0, 0])

        #print(f" RETURNING {data_to_return}")
        return data_to_return


    #Given Set of point and linesegments, change linesegments
    def turn_point_and_linesegments(self, angle, point, linesegments):

        starting_point = point

        to_change = []
        for line_seg in linesegments:

            new_line_seg = self.change_angle(line_seg, angle, starting_point)
            #print(f"    CS: {new_line_seg}")
            to_change.append(new_line_seg)

        new_set = to_change



        return new_set


    def rotate_point(self, point, angle_degrees, center):
        angle_rad = math.radians(angle_degrees)
        translated_point = (point[0] - center[0], point[1] - center[1])
        rotated_x = translated_point[0] * math.cos(angle_rad) - translated_point[1] * math.sin(angle_rad)
        rotated_y = translated_point[0] * math.sin(angle_rad) + translated_point[1] * math.cos(angle_rad)
        rotated_point = (rotated_x + center[0], rotated_y + center[1])
        return rotated_point


    #Takes Set Of Point Locations, and LineSegments, index, and x,y moves
    def move_point_and_linesegments(self, x, y, fragments_location):

        list_of_segments = []

        for line_segment in fragments_location:

            new_linestring_location = self.translate_linestring_location(line_segment, x, y)
            list_of_segments.append(new_linestring_location)




        return list_of_segments




    def translate_linestring_location(self, linestring, x, y):
        line_of_points = []
        for point_set in list(linestring.coords):
            line_of_points.append((point_set[0] + x, point_set[1] + y))

        return LineString(line_of_points)


    def translate_polygon_location(self, polygon, x, y):
        line_of_points = []
        for point_set in list(polygon.exterior.coords):
            line_of_points.append((point_set[0] + x, point_set[1] + y))

        return Polygon(line_of_points)


    #Returns Data (for each tree)







    def convert_expanded_distances_to_compacted(self, data):
        print("DELETE")


    #RETURNS HOLLISTIC VIEW OF DIST,
    def optain_overall_failure(self, data):
        number_of_total_failures = 0
        number_of_success = 0
        distance_of_total_failures = 0
        distance_of_total_successes = 0

        distance_removed = 0
        for data_set in data:
            #print(f" LIST? {data_set[0]}")
            #print(f" {data_set}")
            #print(data)
            number_of_success += data_set[0]
            number_of_total_failures += data_set[2]
            distance_of_total_failures += data_set[3]
            distance_removed += data_set[5]

            #MAKES DISTANCES ALL WEIGHTED EQUALLY


            #IF DISTANCE AVERAGES
            unweighted_distance = data_set[1]



            #SETS TO EQUAL WEIGHT
            if one_directory.ft_equal_weight:
                if data_set[0] != 0:
                    weight_distance = unweighted_distance / data_set[0]
                else:
                    weight_distance = unweighted_distance
            else:
                weight_distance = unweighted_distance

            distance_of_total_successes += weight_distance


            #ASSUMED DISTANCE IS ALREADY REMOVED MIN




        return [number_of_success, distance_of_total_successes,
                number_of_total_failures, distance_of_total_failures, distance_removed]





    def change_angle(self, linestring, angle, point_of_rotation):

        set_coords = []

        for coord in list(linestring.coords):
            new_coord = self.rotate_point(coord, angle, point_of_rotation)
            set_coords.append(new_coord)

        return LineString(set_coords)

    def total_copy(self):

        new_set_of_segments = []

        for frame in self.fragments_locations:
            row_list = []
            for fragment in frame:
                row_list.append(fragment)
            new_set_of_segments.append(row_list)

        return new_set_of_segments

