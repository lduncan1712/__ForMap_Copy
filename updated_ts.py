import math
import time
from random import random

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

from eleven_connection import eleven_connection
from five_database import five_database
import numpy as np
from scipy.spatial import ConvexHull
from shapely import affinity

from fixed_point import fixed_point


class ten_segments:

    def __init__(self, lof):
        self.lof = lof

        self.formal_list = []


    # Using All Techniques, Creates List Of Polygons
    # Relative To (0,0) index 0
    #Using All Techniques, Creates Relative List
    def create_formal_list(self, list_of):

        print("CREATING FORMAL LIST")
        print(f"    GIVEN {list_of} ")

        self.lof = list_of

        # CREATE A LIST OF SIMPLE POLYGONS  (USES SIMPLE, CREATE_DIRECT_POLYGONS-->CREATE_SIMPLE_RELATIVE
        for outer_index in range(0, len(self.lof)):
            row = []
            for inner_index in range(0, len(self.lof)):
                if inner_index > outer_index:
                    polygon = self.create_direct_polygon(self.lof[outer_index], self.lof[inner_index], False, False,
                                                         True, True, False)
                    row.append(polygon)
                else:
                    row.append(0)
            self.formal_list.append(row)

        # Create A List Of Complex Using Simples
        for outer_index in range(0, len(self.lof) - 1):
            for inner_index in range(0, len(self.lof) - 1):
                if inner_index > outer_index:
                    print(f" {outer_index}  {inner_index}")
                    polygon = self.create_direct_polygon(self.lof[outer_index], self.lof[inner_index], True, False,
                                                         True, True, False)
                    self.formal_list[outer_index][inner_index] = polygon



        updated_rel_f1 = self.create_cascaded_polygons(self.lof[0], True)
        #
        index = 1;
        for x in updated_rel_f1:
            self.formal_list[0][index] = x
            index += 1

        print("AREA AFTER CASCADE")
        sum = 1
        for x in range(1, 5):
            print(f"  {x}  {self.formal_list[0][x].area}")
            sum += self.formal_list[0][x].area
        print(f"          ((({sum}")

        for outer_index in range(0, len(self.lof) - 1):
            for inner_index in range(0, len(self.lof) - 1):
                if inner_index > outer_index:
                    polygon = self.create_direct_polygon(self.lof[outer_index], self.lof[inner_index], True, False,
                                                         True, True, False)
                    self.formal_list[outer_index][inner_index] = polygon
        #
        print("AREAS AFTER COMPLEX 3:")
        sym = 0
        for x in range(1, 5):
            print(f" {self.formal_list[0][x].area}")
            sum += self.formal_list[0][x].area
        print(f"          ((({sum}")



    # N/A
    def create_permanent_reference_list(self, starting_index, ending_index):
        fd = five_database()

        permanent_indexs = fd.translate_entire_photo(starting_index, ending_index)

        list_of_permanent = []
        index_list = []
        # ARBITRARY
        for x in range(0, 10):
            list_of_permanent.append([])

        for connection in permanent_indexs:
            list_of_permanent[connection[0]].append(connection[0])
            index_list.append(connection[0])

        for photo_index in range(starting_index + 1, ending_index + 1):
            for tree_index in index_list:
                new_index = fd.get_tree_later_multiple(starting_index, tree_index, photo_index)
                list_of_permanent[tree_index].append(new_index)

        return index_list, list_of_permanent


    # IDEA, IF SOMETHING EXISTS AS STARTING AND END, OTHERS ARE CONNECTED
    def get_connecting_perspectives(self, perspections, length):

        list_to_add = []

        for index in range(0, length):
            start = []
            end = []
            for perspective in perspections:
                # INDEX, ______
                if perspective[0] == index:
                    end.append(perspective[1])

                # _____, INDEX
                elif perspective[1] == index:
                    start.append(perspective[0])
                else:
                    continue

            if len(start) != 0 and len(end) != 0:

                for start_option in start:
                    for end_option in end:

                        val = (start_option, end_option)

                        if val in perspections:
                            continue
                        else:
                            list_to_add.append(val)

        for val in list_to_add:
            perspections.append(val)

        return perspections





    # Gives The User Choice Between 2 Methods of Polygon Creation
    def create_direct_polygon(self, frame1, frame2, extreme, testing, height, width, delta):

        # If wanting to use simple
        if not extreme:
            print("DOING SIMPLE")
            return self.create_simple_relative_polygon(frame1, frame2, height, width, delta)

        # using complicated
        else:
            # print("DOING COMPLICATED")
            # REQUIRES PREVIOUS ALREADY MADE  (HWD useless)
            return self.create_complex_relative_polygon(frame1, frame2, height, width)


    #Using Simple Lines, Creates Relative Polygon
    def create_simple_relative_polygon(self, frame1, frame2, height, width, delta):
        l = []
        print(f"SIMPLE - RELATIVE  {frame1.frame_id} {frame2.frame_id} ")

        # Creating A List of Intersections (INDEXES IN F1---> F2)
        if frame1.frame_id > frame2.frame_id:
            # print("       SWAPPING")
            m = five_database().translate_entire_photo(frame2.frame_id, frame1.frame_id)
            for sublist in m:
                l.append((sublist[1], sublist[0]))

        else:
            l = five_database().translate_entire_photo(frame1.frame_id, frame2.frame_id)

        print(f"- List Of Connections: {l}")
        # Creates a shape, using previous bounds, and overlapping_connections
        proper_intersections = self.create_polygon_of_possibility(frame1, frame2, l)

        # Creates a shape, using rational requirements
        # rational_polygon = self.create_polygon_of_rationality(frame1, frame2, proper_intersections, l, height, width, delta)

        rational_polygon = proper_intersections.buffer(0.1)

        # Returns The Shape, But Buffered
        return rational_polygon.buffer(0).simplify(0.01)

    #Given 3 Frames, creates 1->3, using 1->2->3
    def create_simple_distant_polygon(self, starting_frame, intermediate_frame, endpoint_frame, height, width, testing):
        st_id = starting_frame.frame_id - one_directory.starting_id
        i_id = intermediate_frame.frame_id - one_directory.starting_id
        e_id = endpoint_frame.frame_id - one_directory.starting_id

        # GET 1-->2
        if starting_frame.frame_id < intermediate_frame.frame_id:
            a = self.formal_list[st_id][i_id]
        else:
            a = self.reflect_polygon(self.formal_list[i_id][st_id])

        # GET 2-->3
        if intermediate_frame.frame_id < endpoint_frame.frame_id:
            b = self.formal_list[i_id][e_id]
        else:
            b = self.reflect_polygon(self.formal_list[e_id][i_id])

        # b extending from a

        # print("INDIVIDIALS:")
        # print(a)
        # print(b)
        c = self.build_shape_relative_to_shape(a, b)

        return c

    # KEEP
    # Given 2 Frames, Creates Frame Using 1->2 and 1->3->2 and 1->4->2
    # Only Does Single Length Tho


    #Creates Final Using, Relative Values FOR ALL 3WAY
    def create_complex_relative_polygon(self, frame1, frame2, height, width):
        # print(f"CREATING COMPLEX_RELATIVE_POLYGON {frame1.frame_id} {frame2.frame_id}")

        # First obtain the range to use
        f1_range = (frame1.polygons_below, frame1.polygons_above)
        f2_range = (frame2.polygons_below, frame2.polygons_above)
        # Its intersection is the overlap valuable

        intersected_range = self.intersection_of_relative_ranges(f1_range, f2_range)

        # If no intersection
        if intersected_range == None:
            print("IS THIS EVEN POSSIBLE")


        # Some intersection
        else:
            intersected_polygon = 0

            for frame_index in range(intersected_range[0] - one_directory.starting_id,
                                     intersected_range[1] + 1 - one_directory.starting_id):

                # Nothing to do
                if frame_index == frame1.frame_id - one_directory.starting_id:
                    continue

                # Can create direct polygon
                elif frame_index == frame2.frame_id - one_directory.starting_id:

                    if frame2.frame_id > frame1.frame_id:
                        c = self.formal_list[frame1.frame_id - one_directory.starting_id][
                            frame2.frame_id - one_directory.starting_id]
                    else:
                        c = self.reflect_polygon(self.formal_list[frame2.frame_id - one_directory.starting_id][
                                                     frame1.frame_id - one_directory.starting_id])

                    if intersected_polygon == 0:
                        intersected_polygon = c
                    else:
                        intersected_polygon = intersected_polygon.intersection(c)

                # Need to go multiple
                else:
                    c = self.create_simple_distant_polygon(frame1, self.lof[frame_index], frame2, height, width, False)
                    if intersected_polygon == 0:
                        intersected_polygon = c
                    else:
                        intersected_polygon = intersected_polygon.intersection(c)

            return intersected_polygon

    # KEEP
    def create_polygon_of_possibility(self, frame1, frame2, connections):

        polygons_to_rationalize = []

        # print("TRYING BOUNDS")
        # print(frame1.bound)
        # print(frame2.bound)

        # creates a polygon that frame2 must be within
        final, a, b = self.build_shape_using_intital_bounds(frame1, frame2, frame1.bound, frame2.bound, (0, 0))

        # obtains a list of all relationships that need to be upheld
        l = connections
        # Creates List Of Polygons That Need To Be Intersection
        for ind, match in enumerate(l):
            f1_index = match[0]
            f2_index = match[1]

            f1 = frame1.fragments[f1_index]
            f2 = frame2.fragments[f2_index]

            # distance between max and min
            l1 = f1.max_dist
            s1 = f1.min_dist
            l2 = f2.max_dist
            s2 = f2.min_dist
            print(f"{f1.width_d}  {f2.width_d}")
            print(f" {l1} {s1} {l2} {s2}")

            # corrasponding points
            ss = self.reverse_engineer_position(f1, f2, s1, s2, frame1)
            sl = self.reverse_engineer_position(f1, f2, s1, l2, frame2)
            ls = self.reverse_engineer_position(f1, f2, l1, s2, frame2)
            ll = self.reverse_engineer_position(f1, f2, l1, l2, frame1)
            # if ind == 0:
            #     color="red"
            # elif ind == 1:
            #     color="orange"
            # else:
            #     color="yellow"
            #
            poly = Polygon((ss, sl, ll, ls))
            # g,h = poly.exterior.xy
            # self.plot_perspective.plot(g,h, color=color, marker="*")

            # x,y = poly.exterior.xy
            # self.plot_perspective.plot(x, y, marker="o", color='orange')

            polygons_to_rationalize.append(poly)

        # makes a refined polygon
        for polygon in polygons_to_rationalize:
            final = final.intersection(polygon)

        return final

    # KEEP
    # Returns a polygon with vertices on outside no more then n mether appart
    def complicate(self, polygon):
        # Extract exterior ring from polygon
        exterior = polygon.exterior

        # Create list to hold new exterior ring coordinates
        new_coords = []

        # Iterate over pairs of adjacent coordinates in exterior ring
        for i in range(len(exterior.coords) - 1):
            start = Point(exterior.coords[i])
            end = Point(exterior.coords[i + 1])

            # Add the start point to the new exterior ring
            new_coords.append(start)

            # Compute distance between start and end points
            dist = start.distance(end)

            # If distance is greater than 0.1m, add new points to the line
            if dist > 0.1:
                num_points = int(dist / 0.1) + 1
                increment = 1 / num_points  # REPLACE1 WITH DIST

                # Add new points along the line
                for j in range(1, num_points):
                    fraction = j * increment
                    new_point = exterior.interpolate(fraction, normalized=True)
                    new_coords.append(new_point)

            # Add the end point to the new exterior ring
            new_coords.append(end)

        # Create new exterior ring and polygon from new coordinates
        new_exterior = LineString(new_coords)
        new_polygon = Polygon(new_exterior, polygon.interiors)

        return new_polygon

    # NOT SURE
    def create_polygon_of_rationality(self, frame1, frame2, possibility, list_of_connections, height, width, delta):
        origin = (0, 0)

        final_list_of_indexs = []

        frag1 = frame1.fragments[list_of_connections[0][0]]
        frag2 = frame2.fragments[list_of_connections[0][1]]

        f1_total = frag1.max_dist - frag1.min_dist
        f2_total = frag2.max_dist - frag2.min_dist

        # CREATE DISTINCT PERSPECTIVE LISTS
        distinct_perspective_list_one = []
        distinct_perspective_list_two = []

        for x in list_of_connections:
            if x[0] != -1 and x[1] != -1:
                distinct_perspective_list_one.append(x[0])
                distinct_perspective_list_two.append(x[1])
        print(f"  FRAMES:  {frame1.frame_id}  {frame2.frame_id}")

        relevant_perspectives_one = self.assess_useful_perspectives_from_connections(frame1.frame_id,
                                                                                     distinct_perspective_list_one)
        relevant_perspectives_two = self.assess_useful_perspectives_from_connections(frame2.frame_id,
                                                                                     distinct_perspective_list_two)

        # Goes Through Every 10 Cm, To Identify If a point should be within
        for one_index in range(1, int(f1_total * 10) - 1):
            fr1_dist = frag1.min_dist + one_index * 0.1
            key_interception_point = frame1.move_random_along_angle(frag1.base_dir, fr1_dist, origin)

            row_of_indexes = []

            for two_index in range(1, int(f2_total * 10) - 1):
                fr2_dist = frag2.min_dist + two_index * 0.1
                key_frame2_point = frame1.move_random_along_angle(
                    (frag2.base_dir + 180) % 360, fr2_dist,
                    key_interception_point)

                if not possibility.contains(Point(key_frame2_point[0], key_frame2_point[1])):
                    continue
                else:

                    val = self.efficiency_test(height, width, delta, list_of_connections, frame1, frame2,
                                               key_frame2_point, relevant_perspectives_one, relevant_perspectives_two)
                    # print("A")
                    if not val == False:
                        row_of_indexes.append(val)

            if len(row_of_indexes) > 0:
                final_list_of_indexs.append(row_of_indexes)

        # If Too Few Points Are Determined Within
        if len(final_list_of_indexs) < 1:
            print("        POLYGON OF RATIONALITY FAILED  (NOT ENOUGH INDEXES)")
        else:

            # Create A Polygon That Takes The Outside Indexes
            v = self.minimum_bounding_polygon(final_list_of_indexs)
            p = Polygon(v)

            # If It Needs To Be Convex Hulled (to Remove Overlap)
            if not p.is_valid:

                p = p.convex_hull
                if not p.is_valid:
                    print("      NOT VALID - TRIED TO FIX FAILED")

            return p.buffer(0.1)

    # NOT SURE
    def create_cascaded_polygons(self, frame1, use_complicated):
        # Range of polygons in front of
        f1_range = (frame1.frame_id, frame1.polygons_above)

        # Cache To Hold Relative Polygons
        cache = []

        # Forward Cleaning
        for index in range(f1_range[0] + 1, f1_range[1] + 1):

            previous_value = index - f1_range[0] - 2

            # Means first after f1
            if len(cache) == 0:
                # a = self.create_direct_polygon(frame1, self.lof[index], use_complicated, False, True, True)
                a = self.formal_list[frame1.frame_id - one_directory.starting_id][index - one_directory.starting_id]
                cache.append(a)


            # Means needs to rationalize more
            else:
                # The previous polygon starting point
                previous_polygon = cache[previous_value]

                # short_direct = self.create_direct_polygon(self.lof[index - 1], self.lof[index], use_complicated, False, True, True)
                short_direct = self.formal_list[index - 1 - one_directory.starting_id][
                    index - one_directory.starting_id]

                applied_direct = self.build_shape_relative_to_shape(previous_polygon, short_direct)

                # Now must rational, direct from all before
                intersection = applied_direct

                # Rationalizes Previous
                for iterated in range(f1_range[0], index - 1):

                    # long_direct = self.create_direct_polygon(self.lof[iterated], self.lof[index], use_complicated, False, True, True)
                    long_direct = self.formal_list[iterated - one_directory.starting_id][
                        index - one_directory.starting_id]

                    # If this is the line from the origin to poly, starting at correct place
                    if iterated == f1_range[0]:
                        intersection = intersection.intersection(long_direct)
                    else:
                        to_iterate_around = cache[iterated - f1_range[0] - 1]

                        direct_possibilities = self.build_shape_relative_to_shape(to_iterate_around, long_direct)

                        intersection = intersection.intersection(direct_possibilities)

                cache.append(intersection)


        return cache

    #KEEP

    def smooth_edges(self, points):
        # Convert the list of points to a numpy array
        points = np.array(points)

        # Compute the convex hull of the points
        hull = ConvexHull(points)

        # Return the vertices of the convex hull as a list of tuples
        vertices = [(points[vertex, 0], points[vertex, 1]) for vertex in hull.vertices]

        if not Polygon(vertices).is_valid:
            print("SMOOTHING RESULTS IN NOT VALID POLYGON")

        return vertices

    # Takes The Total Points Found Within, and Creates A Polygon, Using Those on the outside
    # KEEP
    def minimum_bounding_polygon(self, points):

        new_semi_trimmed_edges = []

        # Obtain first, and last in list

        for row in points:
            new_semi_trimmed_edges.append(row[0])

        for row in points:
            if len(row) > 1:
                new_semi_trimmed_edges.append(row[len(row) - 1])

        new_semi_trimmed_edges = list(set(new_semi_trimmed_edges))

        # Convert the list of points to a numpy array
        points = np.array(new_semi_trimmed_edges)

        # Compute the convex hull of the points
        hull = ConvexHull(points)

        # Return the vertices of the convex hull as a list of tuples
        vertices = [(points[vertex, 0], points[vertex, 1]) for vertex in hull.vertices]

        return vertices

    #NOT SURE
    # Returns the perspectives, that only feature 2 trees included
    def assess_useful_perspectives_from_connections(self, id, list_of_connection):

        list_of_perspective_to_keep = []

        perspectives = five_database().get_perspectives(id)
        # print(f" RAW PERSPECTIVES {perspectives}")
        # print(f" RAW CONNECTIONS {list_of_connection}")

        for perspective in perspectives:

            if perspective[0] in list_of_connection and perspective[1] in list_of_connection:
                list_of_perspective_to_keep.append(perspective)
        # print(f" FILTERED PERSPECTIVES {list_of_perspective_to_keep}------------------------------------")
        return list_of_perspective_to_keep




    #KEEP
    def reverse_engineer_position(self, frag1, frag2, dist1, dist2, frame):
        key_interception_point = frame.move_random_along_angle(frag1.base_dir, dist1, (0, 0))

        key_frame2_point = frame.move_random_along_angle((frag2.base_dir + 180) % 360, dist2, key_interception_point)

        return key_frame2_point

        # determines whether an intersection is blacklisted


    # MAYBE
    def efficiency_get_intersection_point(self, frag1, frag2, loc_1, loc_2):

        hor_angle = frag1.base_dir
        start_point = frag1.parent.move_random_along_angle(hor_angle, frag1.min_dist, loc_1)
        end_point = frag1.parent.move_random_along_angle(hor_angle, frag1.max_dist, loc_1)
        seg1 = LineString([start_point, end_point])
        # print(seg1)

        hor_angle = frag2.base_dir
        start_point = frag2.parent.move_random_along_angle(hor_angle, frag2.min_dist, loc_2)
        end_point = frag2.parent.move_random_along_angle(hor_angle, frag2.max_dist, loc_2)
        seg2 = LineString([start_point, end_point])
        # print(seg2)

        if seg2.intersects(seg1):
            # print("GOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOo")

            sect = seg1.intersection(seg2)
            return (sect.x, sect.y)
        else:
            # print("DOESNT INTERSECT")
            return True








    #MAYBE
    def effic_is_blacklisted(self, ind1, ind2):
        if self.system_blacklist[ind1][ind2] == 0:
            return True
        else:
            return False



    #KEEP  (UNIQUE)))))

    # Creates A Polygon Representing POV (for a frame, at a position)
    def create_perspective_polygons(self, frame, position):

        furthest, closest = frame.obtain_furthest_and_closest_position()

        starting_angle, ending_angle = frame.left_range, frame.right_range

        close1 = frame.move_random_along_angle(starting_angle, closest, position)
        close2 = frame.move_random_along_angle(starting_angle + frame.width / 2, closest, position)
        close3 = frame.move_random_along_angle(ending_angle, closest, position)

        far1 = frame.move_random_along_angle(starting_angle, furthest, position)
        far2 = frame.move_random_along_angle(starting_angle + frame.width / 2, furthest, position)
        far3 = frame.move_random_along_angle(ending_angle, furthest, position)

        return Polygon([far1, far2, far3, close3, close2, close1])



    # KEEP
    # Given a shape, and anouther shape relative to 0, create a polygon, of shape 2 extending from shape1
    def build_shape_relative_to_shape(self, shape1, shape2):

        if len(shape1.exterior.coords) == 1:
            translated_shape = self.translate_polygon(shape2, shape1.exterior.coords[0][0],
                                                      shape1.exterior.coords[0][0])
            return translated_shape
        else:
            current_shape = 0
            # Complicate
            shape1 = self.complicate(shape1)

            s1_vertices = list(shape1.exterior.coords)

            for vertice in s1_vertices:
                translated_shape = self.translate_polygon(shape2, vertice[0], vertice[1])
                if not translated_shape.is_valid:
                    print("TRANSLATED NOT VALUD")

                if current_shape == 0:
                    current_shape = translated_shape
                else:
                    current_shape = current_shape.union(translated_shape).convex_hull
            return current_shape

    # KEEP
    def build_shape_using_intital_bounds(self, frame1, frame2, frame1_bound, frame2_bound, sp):
        current_shape = 0

        # For Every Edge Of Frame1
        frame1_vertices = list(frame1.bound.exterior.coords)  # USED TO BE LISTED

        for vertice in frame1_vertices:
            # Make a shape that represents f2, extending from a point
            translated_2_shape = self.translate_polygon(frame2_bound, sp[0] - 1 * vertice[0], sp[1] - 1 * vertice[1])

            if current_shape == 0:
                current_shape = translated_2_shape
            else:
                current_shape = current_shape.union(translated_2_shape)

        current_shape = Polygon(list(current_shape.exterior.coords))

        # create a bound based on time
        t_dist = (1 + abs(frame1.time - frame2.time)) * one_directory.speed

        time_constrained_shape = Point(sp[0], sp[0]).buffer(t_dist)

        final_constrained = current_shape.intersection(time_constrained_shape)

        return final_constrained, time_constrained_shape, current_shape

    # KEEP
    def translate_polygon(self, polygon, x_offset, y_offset):
        # Create a new list to hold the translated vertices
        translated_vertices = []

        # Iterate over the vertices of the polygon and adjust their coordinates
        for ps in list(polygon.exterior.coords):
            x, y = ps[0], ps[1]
            translated_x = x + x_offset
            translated_y = y + y_offset
            translated_vertices.append((translated_x, translated_y))

        # Create a new polygon object with the translated vertices
        translated_polygon = Polygon(translated_vertices)

        return translated_polygon

    #KEEP
    def reflect_polygon(self, polygon):
        reflected = []

        for vertice in list(polygon.exterior.coords):
            reflected.append((-1 * vertice[0], -1 * vertice[1]))

        return Polygon(reflected)

        return reflected_polygon


    #NOT SURE
    # Returns the combo with the lowest deviation for every size
    def obtain_best_comb(self, lcombo, intersections):

        list_weight = []
        list_actual = []

        # THEIR LENGTH ARE THE NUMBER OF ROWS
        for x in range(0, len(intersections)):
            list_weight.append(100)
            list_actual.append([])

        for combo in lcombo:
            sum = 0
            total = 0

            for row, column in enumerate(combo):
                if column != -1:
                    sum += abs(1 - intersections[row][column][11])
                    total += 1

            if total == 0:
                continue
            else:
                av = sum / total

                if list_weight[total - 1] > av:
                    list_weight[total - 1] = av
                    list_actual[total - 1] = combo
        return list_actual, list_weight






    #MAYBE
    # Obtains the difference between 2 angles
    def difference_between_angles(self, a1, a2):
        if a1 > a2:
            c1 = min(a1 - a2, abs(360 - a1 + a2))
        else:
            c1 = min(a2 - a1, abs(360 - a2 + a1))
        return c1






    #USEFU:
    @staticmethod
    def distance(xy1, xy2):
        return math.sqrt((xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2)

    def deg(self, degree):
        return (360 - degree + 90) % 360

    def direction(self, p1, p2):
        x_d = p2[0] - p1[0]
        y_d = p2[1] - p1[1]
        return self.deg(math.degrees(math.atan2(y_d, x_d))), math.sqrt(x_d ** 2 + y_d ** 2)

