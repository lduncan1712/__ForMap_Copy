import math

from matplotlib import pyplot as plt
from shapely.geometry import Polygon, Point, LineString, GeometryCollection
from shapely.affinity import translate

import one_directory
from five_database import five_database

import warnings

# Ignore specific category of warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)


class updated_polygons:

    def __init__(self, list_of_photos, trust_location, trust_time, do_complex):
        simple_list = []

        self.list_of_photos = list_of_photos

        self.trust_location = trust_location
        self.trust_time = trust_time

        self.db = five_database()

        print("MAKING POLYGON:")
        #BASIC BY GPS / TIME / CONNS
        self.create_simple_list()


        # starting_size = self.obtain_sizes()
        #
        #
        # while(True):
        #
        #     self.create_medium_list()
        #
        #     new_size = self.obtain_sizes()
        #     print(f"DO: {starting_size} {new_size}")
        #     if round(new_size) == round(starting_size):
        #         break
        #     else:
        #
        #         starting_size = new_size


        if do_complex:

            self.create_medium_list()


            self.create_min()

            self.create_medium_list()





        # starting_size = self.obtain_sizes()
        #
        # while (True):
        #     print("DO:")
        #     self.create_medium_list()
        #
        #     new_size = self.obtain_sizes()
        #
        #     if round(new_size) == round(starting_size):
        #         break
        #     else:
        #
        #         starting_size = new_size

        self.smallest_index = self.obtain_row_sizes()



    def obtain_row_sizes(self):
        lowest_row = 0.5
        lowest_total = math.inf

        for start in range(0, len(self.list_of_photos)):
            this_total = 0

            for index in range(0, len(self.list_of_photos)):

                if start > index:
                    this_total += self.polygons[index][start].area
                elif start < index:
                    this_total += self.polygons[start][index].area
                else:
                    continue

            if this_total < lowest_total:
                lowest_row = start
                lowest_total = this_total

        return lowest_row



    def obtain_sizes(self):
        tott = 0
        to_print = []
        for start in range(0, len(self.list_of_photos)):
            row_tot = 0
            row = []
            for end in range(0, len(self.list_of_photos)):
                if end > start:
                    row.append(self.polygons[start][end].area)
                    tott += self.polygons[start][end].area
                    row_tot += self.polygons[start][end].area
                else:
                    row.append("A")
            #to_print.append(row)

        return tott


    #CREATE SIMPLE LOCATIONS (LINES + gs + time)
    def create_simple_list(self):
        list_of = []
        for starting_index in range(0, len(self.list_of_photos)):
            row = []
            for ending_index in range(0, len(self.list_of_photos)):

                if ending_index > starting_index:
                    row.append(self.create_basis(self.list_of_photos[starting_index],
                                                 self.list_of_photos[ending_index],
                                                 self.trust_location,
                                                 self.trust_time))
                else:
                    row.append(0)
            list_of.append(row)

        self.polygons = list_of



    #USES ALL Between
    def create_medium_list(self):

        total_ignores = []
        moves_this_turn = []

        for index in range(0, len(self.list_of_photos)):
            total_ignores.append(False)
            moves_this_turn.append(1)


        total_iterations_avoided = 0


        while(True):

            area_starting = 0
            area_ending = 0

            #TESTING ENDING CONDITION
            if True:
                tot = 0
                for val in moves_this_turn:
                    tot += val
                if tot == 0:
                    break


            #UPDATING CASES
            new = []
            for index, val in enumerate(moves_this_turn):
                if val == 0:
                    total_ignores[index] = True
                new.append(0)
            moves_this_turn = new





            #IF ONE CHANGED THIS ROUND MAKE TRUE
            for start in range(0, len(self.list_of_photos)):
                for end in range(start + 1, len(self.list_of_photos)):
                    if total_ignores[start] == True and total_ignores[end] == True:
                        total_iterations_avoided += 1

                        continue
                    else:
                        st = self.polygons[start][end].area
                        #a = len(list(self.polygons[start][end].exterior.coords))

                        area_starting += st



                        self.polygons[start][end] = self.create_medium_3(start, end, len(self.list_of_photos))

                        ne = self.polygons[start][end].area
                        #b = len(list(self.polygons[start][end].exterior.coords))

                        area_ending += ne

                        if abs(st - ne) < one_directory.area_tolerance:
                            continue
                        else:
                            moves_this_turn[start] += 1
                            moves_this_turn[end] += 1



            print(f"M: AFTER {moves_this_turn} IT_AVOIDED: {total_iterations_avoided} ST_AREA: {area_starting} (({area_starting - area_ending}))")
            total_iterations_avoided = 0





        # for start in range(0, len(self.list_of_photos)):
        #     for end in range(start + 1, len(self.list_of_photos)):
        #         st = len(list(self.polygons[start][end].exterior.coords))
        #         self.polygons[start][end] = self.create_medium_3(start, end, len(self.list_of_photos))
        #         ne = len(list(self.polygons[start][end].exterior.coords))


    def create_indexed_complex_list(self, index):
        print("FA")

    def create_complex_list(self):
        cache_for_relative = []

        for index in range(1, len(self.list_of_photos)):
            #print(f"INDEX {index}")

            #MEANS FIRST AFTER
            if len(cache_for_relative) == 0:
                first_direct = self.polygons[0][1]
                cache_for_relative.append(first_direct)

            #NEED TO RATIONALE ALL
            else:
                #WHERE WE START FROM
                previous_polygon = cache_for_relative[-1]


                #THE VALUE OF THE PREVIOUS DIRECTED TOWARD NEXT
                #Since List Starts At 1
                short_direct = self.polygons[index - 1][index]

                #THE (index - 1) applied to the index
                applied_direct = self.build_extending_polygon(previous_polygon, short_direct)

                intersection = applied_direct

                for every_prev in range(0, index):


                    long_direct = self.polygons[every_prev][index]

                    #MEANS THIS IS A DIRECT LINE TO ORIGIN
                    if every_prev == 0:
                        intersection = intersection.intersection(long_direct)

                    else:
                        to_iterate_around = cache_for_relative[every_prev - 1]

                        direct_possibility = self.build_extending_polygon(to_iterate_around,
                                                                          long_direct)
                        intersection = intersection.intersection(direct_possibility)
                    #print(f"   {every_prev} {index}    ")

                cache_for_relative.append(intersection)


        for index, value in enumerate(cache_for_relative):
            self.polygons[0][index + 1] = value

    def get_method(self, index1, index2):
        if index1 < index2:
            return self.polygons[index1][index2]
        else:
            return self.reverse_polygon(self.polygons[index2][index1])



    #Returns the basic polygon that satisfies all, and all bool
    def create_basis(self, photo1, photo2, trust_location, trust_time):
        list_of_connections = self.db.translate_entire_photo(photo1.frame_id,
                                                             photo2.frame_id)
        possible = 0

        #fig, ax = plt.subplots()

        #MAKES POSSIBLE USING INTERSECTION OF LINES
        for connection in list_of_connections:
            f1_index = connection[0]
            f2_index = connection[1]

            f1 = photo1.fragments[f1_index]
            f2 = photo2.fragments[f2_index]

            # distance between max and min
            l1 = f1.max_dist
            s1 = f1.min_dist
            l2 = f2.max_dist
            s2 = f2.min_dist

            # ranges = 5
            #
            # union = 0
            #
            # for one_diff in range(0, 3):
            #     for two_diff in range(0, 3):
            #
            #         print(f"   ABC {one_diff}  {two_diff}")
            #
            #         a1 = f1.p0_dir - ranges + one_diff*ranges
            #         a2 = (f2.p0_dir - ranges + two_diff*ranges + 180) % 360
            #
            #         ss = self.reverse_position((0, 0), s1, a1, s2, a2)
            #         sl = self.reverse_position((0, 0), s1, a1, l2, a2)
            #         ls = self.reverse_position((0, 0), l1, a1, s2, a2)
            #         ll = self.reverse_position((0, 0), l1, a1, l2, a2)
            #
            #         poly = Polygon((ss, sl, ll, ls))  # .buffer(0.5)
            #
            #         x,y = poly.exterior.xy
            #         if one_diff == 1 and two_diff == 1:
            #             plt.plot(x,y,marker="*")
            #         else:
            #             plt.plot(x,y,)
            #
            #
            #
            #         if union == 0:
            #             union = poly
            #         else:
            #             union = union.union(poly)
            #
            # x,y = union.convex_hull.exterior.xy
            #
            # plt.plot(x,y, marker="o", color="black")




            a1 = f1.p0_dir
            a2 = (f2.p0_dir + 180) % 360

            ss = self.reverse_position((0,0), s1, a1, s2, a2)
            sl = self.reverse_position((0,0), s1, a1, l2, a2)
            ls = self.reverse_position((0,0), l1, a1, s2, a2)
            ll = self.reverse_position((0,0), l1, a1, l2, a2)

            poly = Polygon((ss, sl, ll, ls)) #.buffer(0.5)

            if possible == 0:
                possible = poly
            else:
                possible = possible.intersection(poly)

        #MAKES TIME MEASURES
        if trust_time or possible == 0:


            possible_distance = one_directory.speed*\
                                (abs(photo2.time - photo1.time) + 1)
            poly = Point(0,0).buffer(possible_distance)

            if possible == 0:
                possible = poly
            else:
                possible = possible.intersection(poly)





        #MAKES DISTANCE MEASURES
        if trust_location:
            poly = self.build_relative_bound(photo1.bound, photo2.bound)
            possible = possible.intersection(poly)



        #MEANS NO CONNECTION AND GPS AND TIME
        return possible.convex_hull


    #0         5
    def create_medium_3(self, photo1, photo2, max):
        #IDEA for every number between that connects them
        total = 0

        #ASSUMING EVERY END IS COMING FROM DIRECT POLYGON, DIRECTS SHOULD ALL BE SIMPLE

        starting_point = self.polygons[photo1][photo2]
        #print(f"STARTING VERTICES: {len(list(starting_point.exterior.coords))}")


        for index in range(0, max):

            #IF EQUALS 1
            if index == photo1:
                continue
            #EQUALS 2
            elif index == photo2:
                continue

            #NOT 1 OR 2
            else:


                #MEANS  P1 --> INDEX (FORWARD)
                if photo1 < index:
                    p1_to_index = self.polygons[photo1][index]
                else:
                    p1_to_index = self.reverse_polygon(self.polygons[index][photo1])

                total+=len(list(p1_to_index.exterior.coords))

                # MEANS INDEX --> P2 (FORWARD)
                if index < photo2:
                    to_be_extended = self.polygons[index][photo2]
                    next_step = self.build_extending_polygon(p1_to_index,
                                                             to_be_extended).simplify(0.01)
                else:
                    to_be_extended = self.reverse_polygon(self.polygons[photo2][index])
                    next_step = self.build_extending_polygon(p1_to_index,
                                                             to_be_extended).simplify(0.01)
                total+=len(list(to_be_extended.exterior.coords))
                total+=len(list(next_step.exterior.coords))

                #print(f" {len(list(p1_to_index.exterior.coords))}  {len(list(to_be_extended.exterior.coords))}")



                starting_point = starting_point.intersection(next_step).simplify(0.01) #.convex_hull
                total+=len(list(starting_point.exterior.coords))
        # x,y = starting_point.exterior.xy
        # plt.fill(x,y, color="black")

        #print(f" FULL MEDIUM 3: {len(list(starting_point.exterior.coords))}")
        total+=len(list(starting_point.exterior.coords))
        print(f" TOTAL: {total}")
        return starting_point.simplify(0.01)

    def create_min(self):
        starting_area = 0
        ending_area = 0

        for start in range(0, len(self.list_of_photos)):
            for end in range(start + 1, len(self.list_of_photos)):


                # fig, ax = plt.subplots()

                previous = self.polygons[start][end]

                starting_area += previous.area

                #x,y = previous.exterior.xy
                #plt.plot(x,y,color="red")

                dist = (end - start)*one_directory.min_speed
                to_remove = Point(0,0).buffer(dist)

                #x,y = to_remove.exterior.xy
                #plt.plot(x,y,color="green")

                new = previous.difference(to_remove)

                # if True:
                #
                #     #print(F" BB {new} {start} {end}")

                self.polygons[start][end] = new

                ending_area += new.area

                #plt.title(f" {start} {end}")

        print(f"MID:          ST_AREA: {starting_area}   (({starting_area - ending_area}))")



    # def rainbow_colors(self, index):
    #     if index == 1:
    #         return
    #     elif index == 2:
    #
    #     elif index == 2:


    def reverse_polygon(self, polygon):
        coords = []

        for soc in list(polygon.exterior.coords):
            coords.append((soc[0]*-1, soc[1]*-1))

        return Polygon(coords)

    #GIVEN A FIXED LOCATION BASICALLY EXTENDS ONE FROM THE OTHER
    def build_extending_polygon(self, to_extend_from, origin_0_extendable):
        ending = 0

        starting_shape = to_extend_from

        for vertice in list(starting_shape.exterior.coords):
            translated = self.build_translated_polygon(origin_0_extendable, vertice[0], vertice[1])

            if ending == 0:
                ending = translated
            else:

                ending = ending.union(translated).convex_hull

        return ending


    #Given 2 GPS bounds, create polygon of all relative positions given B1 at origin
    def build_relative_bound(self, shape1, shape2):
        current_shape = 0

        # For Every Edge Of Frame1
        frame1_vertices = list(shape1.exterior.coords)  # USED TO BE LISTED

        for vertice in frame1_vertices:
            # Make a shape that represents f2, extending from a point
            translated_2_shape = self.build_translated_polygon(shape2, -1 * vertice[0], -1 * vertice[1])

            if current_shape == 0:
                current_shape = translated_2_shape
            else:
                current_shape = current_shape.union(translated_2_shape)

        current_shape = Polygon(list(current_shape.exterior.coords))

        return current_shape





    #Creates A Shape Whose Edges Have A Point Every 0.1m
    def build_complicated_shape(self, shape):
        #print(shape)
        # Extract exterior ring from polygon
        exterior = shape.exterior

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
        new_polygon = Polygon(new_exterior, shape.interiors)

        return new_polygon

    #Moves A Polygon by given x,y
    def build_translated_polygon(self, shape, x, y):
        translated_polygon = translate(shape, xoff=x, yoff=y)
        return translated_polygon

    #Moves Given Angle
    def move_random_along_angle(self, angle, absolute, xy):
        angle = math.radians(angle)
        dx = absolute * math.sin(angle)
        dy = absolute * math.cos(angle)

        return (dx + xy[0], dy + xy[1])


