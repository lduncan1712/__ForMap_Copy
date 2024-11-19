import math
import random

from matplotlib import pyplot as plt
from shapely.affinity import translate, scale
from shapely.geometry import LineString, Point, Polygon
from shapely.ops import nearest_points

import updated_frame
from final_polygon import final_polygon
from five_database import five_database
import one_directory
from fixed_point import fixed_point


class final_mover:

    def __init__(self):

        #Define Variables
        if True:
            #How Far Apart Angles Must Be To Be Used In Simple Polygon
            self.polygon_min_difference_angle = 0
            #Fastest Possible Speed Moved (+1 second too)
            self.polygon_max_speed = 2
            self.polygon_trust_time = False
            self.polygon_trust_gps = False
            self.polygon_area_difference = 0.4


            #REQUIRES LOTS OF WORK STILL------------------------------------------
            self.segmented_use_segmented = False
            #limits on segmented
            self.segmented_error_allowed = 0.5
            #------------------------------------------------------

            self.movement_start_gps = False
            self.movement_start_set = True
            self.movement_start_random = False
            self.movement_box_size = 30   #WHEN ABOVE TRUE





            #The difference in angle required to be intersection
            self.intersection_difference_angle = 10


            #how close not required lines need to be before forces are removed
            self.non_intersection_distance_tolerance = 0.2


            #ASSUME THAT SINCE AVERAGE SEPERATED LINES FORCES ARENT MOST EFFICIENT PATH
            # DONT HAVE TO WORRY ABOUT ONLY EDGING

            #HOW MUCH INTERSECTION MUST HAPPEN TO NOT MORE POLYGON
            # (TO PREVENT SIMPLY TOUCHING EDGES AND NOT ACTUALLY OVERALLPING)
            self.anti_scale_buffer_for_polygons = 0.9

            self.jitter = 0.05




            # ALL TREES EQUAL (0)
            # ALL INTERSECTIONS EQUAL (1)
            self.weighting_scheme = 1

            self.distance_exponent = 1.0





        #Basic Setup (points located at GPS locations)
        if True:
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

        #Creates Polygons + Trees + Angles
        if True:
            self.final_polygon = final_polygon(self)
            print("AFTER")
            #plt.show()

            self.tree_list = self.make_trees(self.lof[0], self.lof[1],
                                             len(self.lof) - 1 + one_directory.starting_id)

            #THIS IS LIST FOR INTERSECTION ANGLES
            self.tree_angle_list = self.make_angle_list()

        #Creates Starting Location For Points (+ segs)
        if True:
            #SETS POINTS
            if self.movement_start_gps:
                locations = []
                for frame in self.lof:
                    locations.append([frame.centre[0], frame.centre[1]])

            elif self.movement_start_random:
                locations = []
                for index in range(0, len(self.lof)):
                    x = random.uniform(0, self.movement_box_size)
                    y = random.uniform(0, self.movement_box_size)
                    locations.append([x,y])
            #USE SET
            else:
                #locations = [[1.0609683501109846, -27.8712070750437], [0.5952320151453749, -27.168411574513126], [0.37304019051562876, -26.449700667926017], [0.34445678654718687, -25.326776369171412], [0.012320414262576905, -25.041739874882772], [-0.29640951453989073, -24.17170751292045], [-0.6024242758308966, -23.39897356626959], [-1.259124517347499, -23.280572237355386], [-1.3657644090842445, -22.458903349036135]]

                self.indexs_to_use = [0,1,2,3,4,5,6,7,8]


                locations = [[0,-5],[0,-10],[0,-15],[0,-20],[0,-25],[0,-30],[0,-35],[0,-40],[0,-45]]

            self.current_locations = locations


            #MAKES SEGMENTS
            fragment_locations = []
            # Creating According Line Segments // Angles
            for index, photo in enumerate(self.lof):

                row_list = []
                angle_list = []

                # Location To Start From
                starting_location = self.current_locations[index]

                for fragment in photo.fragments:
                    close_point = self.move_random_along_angle(fragment.p0_dir,
                                                               fragment.min_dist,
                                                               starting_location)
                    far_point = self.move_random_along_angle(fragment.p0_dir,
                                                             fragment.max_dist,
                                                             starting_location)
                    linestring = LineString([close_point, far_point])

                    row_list.append(linestring)
                    #angle_list.append(fragment.p0_dir)

                fragment_locations.append(row_list)


            self.current_fragment_locations = fragment_locations

        #RANDOM TEST
        if True:
            fig, ax = plt.subplots()

            pol = LineString([(4, 4),(-4, -4)])
            pol2 = LineString([(3,2), (-3,-2)])
            pol3 = LineString([(6, 3), (-4,-3)])
            pol4 = LineString([(-1,-3),(3,4)])
            pol5 = LineString([(-3,-2.5), (4,3)])
            pol6 = LineString([(-5, 5), (25, -25)])

            total = pol.union(pol2).union(pol3).union(pol4).union(pol5).union(pol6).convex_hull



            self.make_exterior_lines(total)
            lines = [pol, pol2, pol3, pol4, pol5, pol6]

            a,b,c,d,segment_to_try = self.lucas_get_start(lines)

            x,y = segment_to_try.xy
            plt.plot(x,y,marker="o", color="black")

            #p1, p2 = self.lucas_use(lines)

            # plt.plot(p1.x, p1.y, marker="*",color="purple")
            # plt.plot(p2.x, p2.y, marker="*", color="orange")



            x,y = total.exterior.xy
            plt.plot(x,y,color="blue")



            x, y = pol.xy
            plt.plot(x, y)
            x, y = pol2.xy
            plt.plot(x, y)
            x, y = pol3.xy
            plt.plot(x, y)
            x,y = pol4.xy
            plt.plot(x,y)
            x,y = pol5.xy
            plt.plot(x,y)
            x,y = pol6.xy
            plt.plot(x,y)

            v = LineString([(5, 2), (5,5)])
            print(f" DOES IT INTERSECTS:  {total.intersection(v)}")

            #x,y = v.xy
            #plt.plot(x,y,marker="*", color="blue")



            #
            # shortest_intersection = self.find_shortest_touching_segment(pol, pol2, pol3)

            for x in range(0, 5):
                poin = self.point_at_fraction_along(pol, x/-4)
                if x == 1:
                    color = "red"
                else:
                    color = "green"
                plt.plot(poin.x, poin.y, color=color, marker="*")


            #plt.plot(x,y,color="green", marker="o")



            #
            # location = Point(13, 7)
            #
            # sup, ignore = nearest_points(pol, location)
            #
            #
            #
            # plt.plot(location.x, location.y, color="green",marker="*")
            #
            # plt.plot(sup.x, sup.y, color="blue",marker="*")
            #
            # x = print(f" CRAZY:  {pol.intersection(sup)}")

        #MOVE INTO POSITION:
        if True:

            for index in range(0, 200):

                line_movement, line_denom, line_events, line_distance = self.line_movement()

                polygon_movement, polygon_denom, polygon_events, polygon_distance = self.polygon_movement()

                intersection_movement, intersection_denom, \
                intersection_events, total_intersections, intersections_distance = self.intersection_movement()


                if index < 100:
                    list_val = [polygon_movement, polygon_denom]


                else:

                    if index % 3 == 0:
                        list_val = [intersection_movement, intersection_denom]
                    elif index % 3 == 1:
                        list_val = [line_movement, line_denom]
                    else:
                        list_val = [polygon_movement, polygon_denom]


                    # else:
                    #     list_val = [intersection_movement, intersection_denom]


                #print(f" POLY EVENTS: {polygon_events} {polygon_distance}")

                #list_val = [polygon_movement, polygon_denom]

                to_use = []
                for index_l in range(0, len(line_movement)):
                    val = [0,0]

                    if list_val[1][index_l]!= 0:
                        val[0] = list_val[0][index_l][0]/list_val[1][index_l]
                        val[1] = list_val[0][index_l][1]/list_val[1][index_l]
                    to_use.append(val)

                print(f" {index}::    P: {round(polygon_events, 4)} P_D: {round(polygon_distance, 4)}  "
                      f"L: {round(line_events, 4)}  L_D: {round(line_distance, 4)}"
                      f"I: {round(intersection_events, 4)} I_D: {round(intersections_distance, 4)}  MOVEMENT: {self.sum_movement(to_use)}")


                #NEEDS WORK -------------------
                self.actually_move(to_use, stay_within=False)






        self.end_print()
        plt.show()




    def actual_method(self, lines):

        polygon = self.make_polygon_from_lines(lines)

        exterior_lines = self.make_exterior_lines(polygon)


        for o_i, o_l in enumerate(exterior_lines):
            for i_i, i_l in enumerate(exterior_lines):
                if o_i < i_i:
                    print("ZA")







    def lucas_get_start(self, lines):

        #BASIC IDEA START AT A SINGLE POINT
        polygon = self.make_polygon_from_lines(lines)
        exterior_lines = self.make_exterior_lines(polygon)
        print(exterior_lines)
        largest_lines = len(exterior_lines) - 1

        length = largest_lines + 1

        # STARTING: 3
        # FRACT: 0.8


        #GIVES US TWO STARTING POINTS
        # l1, l2, f1, f2, starting_line
        while(True):


            #ATTEMPTING TO MAKE A FULL CONNECTION FROM THIS RANDOM POINT

            l1 = random.randint(0, len(exterior_lines) - 1)
            #print(random_line_to_start_on)
            f1 = random.randint(1, 4)/5
            #print(fraction)
            p1 = self.point_at_fraction_along(exterior_lines[l1], f1)

            print(f" STARTING: {l1}  FRACT: {f1}")
            #NOW APPLY THIS FORWARD UNTIL WE GET A LOCATION THAT WORKS
            for index in range(0, length):
                print(" GOING:")

                l2 = index + l1

                l2 = exterior_lines[(l2) % length]

                for int_tot in range(1, 4):
                    print(f"    SUBGOING")
                    f2 = int_tot/4

                    exact_location = self.point_at_fraction_along(l2, f2)

                    combining_segment_to_try = LineString([exact_location, p1])

                    is_valid = self.check_if_line_intersects_all_others(combining_segment_to_try, lines)

                    if is_valid:
                        return l1, f1, l2, f2, combining_segment_to_try
                    else:
                        continue





















        #IF WE START LOSING GO BACK








        return self.point_at_fraction_along(exterior_lines[cl], cl_f), self.point_at_fraction_along(exterior_lines[cr], cr_f)


    def lucas_use(self, lines):

        l1, f1, l2, f2, starting_segment = self.lucas_get_start(lines)


        for iteration in range(0, 10):
            print("ZA")

















    def make_exterior_lines(self, polygon):
        segs = []

        list_of_points = list(polygon.exterior.coords)

        for index in range(0, len(list_of_points) - 1):
            p1 = list_of_points[index]
            p2 = list_of_points[index + 1]

            segs.append(LineString([p1, p2]))
        #print(segs)
        return segs

    def make_polygon_from_lines(self, lines):

        new = Polygon()

        for line in lines:
            new = new.union(line)

        return new.convex_hull


    def check_if_line_intersects_all_others(self, line1, others):
        for line in others:

            if not line1.intersects(line):
                return False

        return True



    # def list_of_lines_intersected














    def closest_line(self, polygon, lines_list):

        #IDEA ASSESS EVERY VERTICES COMPARED TO EVERY OTHER

        #ONE FIVTH
        print("ZA")












    def master_line(self, lines):

        #Creating A Polygon (pol // segs)
        if True:
            pol = 0
            for line in lines:
                if pol == 0:
                    pol = line
                else:
                    pol = pol.union(line)
            pol = pol.convex_hull
            segs = self.make_exterior_lines(pol)




        #IF TWO POLYGONS ONLY INTERSECT AT A POINT, THEN KNOW EXACT/ONLY DISTANCE




        #FOR EVERY COMBO
        for o_i, o_s in enumerate(lines):
            for i_i, i_s in enumerate(lines):
                if o_i < i_i:
                    print("ZA")




                #FIND THE BEST IN THIS COMBO


















    def point_at_fraction_along(self, ls, fraction):
        return ls.interpolate(fraction, normalized=True)



    def sum_movement(self, movement):
        total = 0
        for val in movement:
            total += math.sqrt(val[0]**2 + val[1]**2)
        return total

    #IF EQUAL= TREAT EQUAL
    #ELSE:    Scale according to denom sum
    def average_all_lists(self, lists, equal):
        new = []

        length = len(lists)
        #EVERY PHOTO LOCATION
        for index in range(0, len(lists[0])):

            #MEANS FIND AND TAKE AVERAGE
            if equal:
                continue


            #SUM TOT / SUM DENOM
            else:
                continue









    def line_movement(self):
        total_distance = 0
        total_events = 0

        movement_list, denom_list = self.make_count_set()

        for tree_index, tree in enumerate(self.tree_list):

            #SINCE INCLUDE ANY
            if len(tree.list_of_indexs) > 1:

                base_index = tree.starting_photo - one_directory.starting_id

                segments = self.get_tree_segments(tree)


                non_intersections, indexs = self.get_intersections(segments,
                                                                   tree_index,
                                                                    actually_get_intersections=False,
                                                                    only_looking_for_intersection_degree=False
                                                                    )

                for n_index, non_intersection in enumerate(non_intersections):

                    index_to_use_in_movement_1 = non_intersection[0] + base_index
                    index_to_use_in_movement_2 = non_intersection[1] + base_index

                    segment1 = segments[non_intersection[0]]
                    segment2 = segments[non_intersection[1]]


                    #BUFFER DISTANCE NEEDS WORK-----------------------
                    #---
                    #_--
                    one_to_two_x, one_to_two_y = self.sub_line_movement(segment1,segment2, buffer_distance=0)

                    dist = math.sqrt(one_to_two_x**2 + one_to_two_y**2)



                    #NEEDS WORK, DIFFERENT FORCE WHETHER IT SHOULD INTERSECT OR NOT
                    x_to_use, y_to_use, den = self.scale_movement(one_to_two_x,
                                                                  one_to_two_y,
                                                                  len(non_intersections))

                    #print(self.intersection_difference_angle)
                    #ALLOWANCE FOR CLOSE (ASSUMING INTERSECTION NOT NEEDED)
                    if dist < self.non_intersection_distance_tolerance and \
                        self.tree_angle_list[tree_index][n_index] == 0:
                        x_to_use = 0
                        y_to_use = 0
                        den = 0
                        #print("TOLERANCE CASE USED")


                    total_distance += dist
                    total_events += 1


                    movement_list[index_to_use_in_movement_1][0] += x_to_use
                    movement_list[index_to_use_in_movement_1][1] += y_to_use

                    movement_list[index_to_use_in_movement_2][0] -= x_to_use
                    movement_list[index_to_use_in_movement_2][1] -= y_to_use

                    denom_list[index_to_use_in_movement_1] += den
                    denom_list[index_to_use_in_movement_2] += den
        #print(f" DISTANCE BETWEEN:  {total_distance}  {total_events}")
        return movement_list, denom_list, total_events, total_distance

    #RETURNS MOVEMENT BETWEEN 2 DISJOINT LS
    def sub_line_movement(self, seg1, seg2, buffer_distance):

        #BASIC IDEA, FIND 4 END POINTS FIND A CENTRE
        #THEN FIND THE ClOSEST TO EACH SEGMENT

        #USE THIS TO CREATE A VECTOR, AND MAYBE SCALE (SO DISTANCE IS OPTIMAL TO CLOSEST??)

        c1 = list(seg1.coords)
        c2 = list(seg2.coords)

        p1, ig1 = nearest_points(seg2, Point(c1[0][0], c1[0][1]))
        p2, ig2 = nearest_points(seg2, Point(c1[1][0], c1[1][1]))
        p3, ig3 = nearest_points(seg1, Point(c2[0][0], c2[0][1]))
        p4, ig4 = nearest_points(seg1, Point(c2[1][0], c2[1][1]))

        av_x = (p1.x + p2.x + p3.x + p4.x) / 4
        av_y = (p1.y + p2.y + p3.y + p4.y) / 4

        average_point = Point(av_x, av_y)






        closest_point_on_seg1, ig5 = nearest_points(seg1, average_point)
        #print(f" INTERSECTS: {seg1.intersection(closest_point_on_seg1)}")

        closest_point_on_seg2, ig6 = nearest_points(seg2, average_point)
        #print(seg2.contains(closest_point_on_seg2))

        # -----------------------------
        # fig, ax = plt.subplots()
        # x,y = seg1.xy
        # plt.plot(x,y,color="blue")
        # x,y = seg2.xy
        # plt.plot(x,y,color="green")
        #
        # if seg1.intersects(closest_point_on_seg1) or seg2.intersects(closest_point_on_seg2):
        #     marker="o"
        # else:
        #     marker="*"

        # plt.plot(average_point.x, average_point.y, marker=marker, color="black")
        # plt.plot(closest_point_on_seg1.x, closest_point_on_seg1.y, marker=marker, color="black")
        # plt.plot(closest_point_on_seg2.x, closest_point_on_seg2.y, marker=marker, color="black")

        movement_x_from_1_to_2 = closest_point_on_seg2.x - closest_point_on_seg1.x
        movement_y_from_1_to_2 = closest_point_on_seg2.y - closest_point_on_seg1.y

        return movement_x_from_1_to_2, movement_y_from_1_to_2

    def intersection_movement(self):
        total_intersections = 0
        total_events = 0
        total_distance = 0

        movement_list, denom_list = self.make_count_set()


        for t_index, tree in enumerate(self.tree_list):
            if len(tree.list_of_indexs) > 1:

                segments = self.get_tree_segments(tree)

                base_line = tree.starting_photo - one_directory.starting_id

                intersections, cypher, indexs = self.get_intersections(segments,
                                                                t_index,
                                                                actually_get_intersections=True,
                                                                only_looking_for_intersection_degree=True)

                total_intersections += len(intersections)

                event_denom = 0
                for x in range(1, len(intersections)):
                    event_denom += x

                #total_events += event_denom

                for outer_intersection_index, outer_intersection in enumerate(intersections):
                    for inner_intersection_index, inner_intersection in enumerate(intersections):

                        if outer_intersection_index < inner_intersection_index:

                            x_movement_from_outer_to_inner = inner_intersection.x - outer_intersection.x
                            y_movement_from_outer_to_inner = inner_intersection.y - inner_intersection.y

                            db = math.sqrt(x_movement_from_outer_to_inner**2 + y_movement_from_outer_to_inner**2)









                            #total_distance += db

                            #FROM OUTER TO INNER
                            x_move, y_move, scale_denom = self.scale_movement(x_movement_from_outer_to_inner,
                                                                              y_movement_from_outer_to_inner,
                                                                              event_denom)

                            # IF CLOSE ENOUGH:
                            if db < self.non_intersection_distance_tolerance:
                                x_move = 0
                                y_move = 0
                                scale_denom = 0


                            total_events += 1
                            total_distance += db


                            outer_cypher = cypher[outer_intersection_index]
                            inner_cypher = cypher[inner_intersection_index]


                            #THE FIRST OF OUTER
                            movement_list[outer_cypher[0] + base_line][0] += x_move
                            movement_list[outer_cypher[0] + base_line][1] += y_move
                            #SECOND OF OUTER
                            movement_list[outer_cypher[1] + base_line][0] += x_move
                            movement_list[outer_cypher[1] + base_line][1] += y_move

                            # THE FIRST OF INNER
                            movement_list[inner_cypher[0] + base_line][0] -= x_move
                            movement_list[inner_cypher[0] + base_line][1] -= y_move
                            # SECOND OF INNER
                            movement_list[inner_cypher[1] + base_line][0] -= x_move
                            movement_list[inner_cypher[1] + base_line][1] -= y_move


                            denom_list[outer_cypher[0] + base_line] += scale_denom
                            denom_list[outer_cypher[1] + base_line] += scale_denom

                            denom_list[inner_cypher[0] + base_line] += scale_denom
                            denom_list[inner_cypher[1] + base_line] += scale_denom




                            # movement[cypher_one[0] + base_line][0] += x_move
                            # movement[cypher_one[1] + base_line][1] += y_move
                            #
                            # movement[cypher_two[0] + base_line][0] -= x_move
                            # movement[cypher_two[1] + base_line][1] -= y_move

        return movement_list, denom_list, total_events, total_intersections, total_distance


    #IDEA SOMETIMES THE RELATIVE POSITON IS CORRECT, BUT TOO CLOSE OR FAR, IN THIS CASE SCALE THE POINT LOCATIONS
    #UNTIL NO LONGER IN POLYGON ACCEPTANCE
    def scale_current_locations(self):
        print("MAKE THIS METHOD")

    def polygon_movement(self):
        total_events = 0
        total_distances = 0

        movement_list, denom_list = self.make_count_set()

        for point_index, point_location in enumerate(self.current_locations):
            for polygon_index in range(0, len(self.current_locations)):
                if polygon_index != point_index:

                    #NEEDS WORK
                    polygon = self.get_active_pol(polygon_index, point_index, False)


                    shapely_point = Point(point_location[0],
                                          point_location[1])

                    smaller_polygon = scale(polygon, xfact=self.anti_scale_buffer_for_polygons,
                                            yfact=self.anti_scale_buffer_for_polygons)

                    #IF ALREADY WITHIN SMALLER SCALED POLYGON (NO MOVEMENT REQUIRED)
                    if smaller_polygon.contains(shapely_point):
                        continue
                    #NOT WITHIN SO NEED TO MOVE
                    else:

                        closest_point, ignore = nearest_points(smaller_polygon, shapely_point)

                        #GOING FROM POINT ---> POLYGON (INDEX)

                        x_move = closest_point.x - shapely_point.x
                        y_move = closest_point.y - shapely_point.y

                        sd = math.sqrt(x_move**2 + y_move**2)
                        total_distances += sd

                        x_move *= 0.5
                        y_move *= 0.5

                        jitter = sd*0.5

                        x_move, y_move = self.extend_by_n(x_move, y_move, jitter)

                        movement_list[point_index][0] += x_move
                        movement_list[point_index][1] += y_move

                        movement_list[polygon_index][0] -= x_move
                        movement_list[polygon_index][1] -= y_move

                        denom_list[point_index] += 1
                        denom_list[polygon_index] += 1

                        total_events += 1


        return movement_list, denom_list, total_events, total_distances




    #BASIC IDEA,
    #  USING WEIGHTING TO SCALE MOVEMENT
    #  AND DISTANCE EXPONENT
    #  (NEEDS WORK - BUFFER or treat already more as enough)
    def scale_movement(self, x, y, tot):

        scalar_distance = self.distance_exponent
        method = self.weighting_scheme

        #COMPENSATING FOR DISTANCE EXPONENT
        if x > 0:
            x = math.pow(x, scalar_distance)
        else:
            x = -1 * math.pow(abs(x), scalar_distance)

        if y > 0:
            y = math.pow(y, scalar_distance)
        else:
            y = -1 * math.pow(abs(y), scalar_distance)


        #CUT IN HALF
        x *= 0.5
        y *= 0.5

        #ALL TREES EQUAL
        if method == 0:
            return x/tot, y/tot, 1/tot
        #ALL Intersections equal
        elif method == 1:
            return x, y, 1
        else:
            print("third idk yet")



    def actually_move(self, movement, stay_within):
        new_points = []
        new_segments = []

        for p_index, point in enumerate(self.current_locations):
            new_points.append(self.move_point(point, movement[p_index]))


        for s_index, list_of_segments in enumerate(self.current_fragment_locations):
            new_row = []
            for ss_index, segment in enumerate(list_of_segments):
                new_row.append(self.move_line_segment(segment, movement[s_index]))
            new_segments.append(new_row)


        self.current_locations = new_points
        self.current_fragment_locations = new_segments








    def make_count_set(self):
        movement_total = []
        movement_denom = []
        for index in range(0, len(self.lof)):
            movement_total.append([0, 0])
            movement_denom.append(0)
        return movement_total, movement_denom

    def move_line_segment(self, linesegment, xy):
        coords_to_add = []
        for coord in list(linesegment.coords):
            coords_to_add.append((coord[0] + xy[0], coord[1] + xy[1]))

        return LineString(coords_to_add)

    def move_point(self, point, xy):

        return [point[0] + xy[0], point[1] + xy[1]]

        # RETURNS THE POLYGON OF ST -> ED, EXTENDING FROM LOCATION OF ST

    def get_active_pol(self, st, ed, use_frag):

        pol_rel_zero = self.final_polygon.get_polygon(st, ed, False)
        # NORMAL

        # MOVING IT RELATIVE TO STARTING
        moved_pol = translate(pol_rel_zero,
                              xoff=self.current_locations[st][0],
                              yoff=self.current_locations[st][1])
        return moved_pol


    #IF actually get intersections, returns intersections, and dictionary
    #ELSE returns dictionary



    #NEEDS WORK (CURRENTLY RETURNS ALL INTERSECTIONS NOT JUST
    def get_intersections(self, segs, tree_index, actually_get_intersections, only_looking_for_intersection_degree):
        list = []
        cypher = []
        indexs = []


        index = 0
        for outer_seg_index, outer_seg in enumerate(segs):
            for inner_seg_index, inner_seg in enumerate(segs):
                if inner_seg_index > outer_seg_index:

                    inter_maybe = outer_seg.intersection(inner_seg)
                    #print(f" SEGS TO COMPARE:")
                    #print(outer_seg)
                    #print(inner_seg)
                    #print(f" {inter_maybe} {actually_get_intersections}")


                    #IF INTERSECTS AND LOOKING FOR INTERSECTION ADD TO LIST
                    if not inter_maybe.is_empty and \
                            actually_get_intersections:


                        #ONLY LOOKING FOR SPECIFIC AND IT FITS    OR ANYTHING IS ADDED
                        if (only_looking_for_intersection_degree and \
                            self.tree_angle_list[tree_index][index] == 1) or (not only_looking_for_intersection_degree):

                            cypher.append([outer_seg_index, inner_seg_index])
                            list.append(inter_maybe)
                            indexs.append(index)

                    #IF DOESNT AND LOOKING FOR NOT ADD TO LIST
                    if inter_maybe.is_empty and not actually_get_intersections:
                        cypher.append([outer_seg_index, inner_seg_index])
                        indexs.append(index)
                    index += 1



        if actually_get_intersections:
            return list, cypher, indexs
        else:
            return cypher, indexs







    def get_tree_segments(self, tree):
        list_to_return = []
        starting_index = tree.starting_photo - one_directory.starting_id

        for index, value in enumerate(tree.list_of_indexs):
            list_to_return.append(self.current_fragment_locations[index + starting_index][value])

        return list_to_return

    def extend_by_n(self, x, y, n):
        length = math.sqrt(x ** 2 + y ** 2)
        if length == 0:
            return x, y

        scale = n / length
        delta_x = x * scale
        delta_y = y * scale

        #IDEA DELTA WILL BE POSSIBLE, WHEN NEED TO BE POSITIVE, NEGATIVE WHEN NEED
        return x + delta_x, y + delta_y



    #AFTER--------------------------

    def end_print(self):
        fig, ax = plt.subplots()

        #SEGMENTS
        if True:

            for tree in self.tree_list:

                segs = self.get_tree_segments(tree)
                base = tree.starting_photo - one_directory.starting_id
                col = tree.color

                for index, seg in enumerate(segs):

                    if not index + base in self.indexs_to_use:
                        continue
                    else:
                        x,y = seg.xy
                        plt.plot(x,y,color=col)

        #POINTS
        if True:
            for index, point in enumerate(self.current_locations):

                if not index in self.indexs_to_use:
                    continue
                else:
                    plt.plot(point[0], point[1], marker="*")
                    plt.text(point[0], point[1], f"{index}")


        #INTERSECTIONS
        if True:
            for t_index, tree in enumerate(self.tree_list):

                base = tree.starting_photo - one_directory.starting_id

                should_be_length = 0
                for val in self.tree_angle_list[t_index]:
                    should_be_length+=val

                intersections, cypher, index = self.get_intersections(self.get_tree_segments(tree),
                                                       t_index,
                                                       actually_get_intersections=True,
                                                       only_looking_for_intersection_degree=True)

                #print(f" TREE: {t_index}  SHOULD HAVE: {should_be_length}  HAS {len(intersections)}")

                for index, intersection in enumerate(intersections):

                    if not (cypher[index][0] + base in self.indexs_to_use and cypher[index][1] + base in self.indexs_to_use):
                        continue
                    else:

                        val = intersection.buffer(0.10)
                        x,y = val.exterior.xy

                        plt.fill(x, y, color=tree.color)
                        plt.plot(x,y,color="black")

            print(f" FINAL LOCATION: {self.current_locations}")












    #------PRESETUP STUFF---------------------------------
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

    def move_random_along_angle(self, angle, absolute, xy):
        angle = math.radians(angle)
        dx = absolute * math.sin(angle)
        dy = absolute * math.cos(angle)

        return (dx + xy[0], dy + xy[1])

    def make_angle_list(self):

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

                        #
                        if circular_diff < self.intersection_difference_angle:
                            list_of_index_values.append(0)

                        #NEEDS TO INTERSECT == 1
                        else:
                            list_of_index_values.append(1)



            list_of_valid.append(list_of_index_values)

        return list_of_valid

