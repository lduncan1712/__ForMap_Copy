import math

from matplotlib import pyplot as plt
from shapely.affinity import translate
from shapely.geometry import Point, Polygon, GeometryCollection

import one_directory
from five_database import five_database


class pure_polygon:

    def __init__(self, lof):
        self.lof = lof
        self.db = five_database()

        self.create_simple_polygons()

        #print(self.polygons)
        self.create_medium_polygon(use_fragment=False)
        self.create_medium_polygon(use_fragment=True)


        self.canvas()



    def get_overlap(self, index, locations, intersects, total_intersects, use_fragments):

        intersection = 0

        for out_i in range(0, len(locations)):
            po = locations[out_i]

            # EXTENDED
            for in_i in range(0, len(locations)):
                if out_i != in_i:

                    if in_i == index:


                        pol = self.get_polygon(out_i, in_i, use_fragments)
                        moved = self.build_translated_polygon(pol, po[0], po[1])

                        if intersection == 0:
                            intersection = moved
                        else:
                            intersection = intersection.intersection(moved)
        return intersection



    def create_simple_polygons(self):
        list_to_make = []
        fractional_list_to_make = []
        starting_id = self.lof[0].frame_id
        for outer_index in range(0, len(self.lof)):
            row_to_make = []
            fractional_row_to_make = []
            for inner_index in range(0, len(self.lof)):

                if inner_index > outer_index:

                    distance = (self.lof[inner_index].time - self.lof[outer_index].time)*one_directory.p_max_speed

                    intersecting_polygon = Point(0,0).buffer(distance)
                    fractional_intersection_polygon = Point(0,0).buffer(distance)



                    connections = self.db.translate_entire_photo(starting_id + outer_index,
                                                                 starting_id + inner_index)
                    #print(f" POL: {outer_index}  {inner_index} ")
                    for connection in connections:
                        f1_index = connection[0]
                        f2_index = connection[1]

                        f1 = self.lof[outer_index].fragments[f1_index]
                        f2 = self.lof[inner_index].fragments[f2_index]

                        #CHECK FOR ANGLE
                        if True:

                            diff = abs(f1.p0_dir - f2.p0_dir)
                            # Adjust for circular range
                            circular_diff = min(diff, 360 - diff)

                            #IF TOO SMALL
                            if circular_diff < one_directory.m_line_polygon_angle:
                                continue

                        l1 = f1.max_dist
                        s1 = f1.min_dist
                        l2 = f2.max_dist
                        s2 = f2.min_dist

                        a1 = f1.p0_dir
                        a2 = (f2.p0_dir + 180) % 360

                        ss = self.reverse_position((0, 0), s1, a1, s2, a2)
                        sl = self.reverse_position((0, 0), s1, a1, l2, a2)
                        ls = self.reverse_position((0, 0), l1, a1, s2, a2)
                        ll = self.reverse_position((0, 0), l1, a1, l2, a2)

                        poly = Polygon((ss, sl, ll, ls))

                        # x,y = poly.exterior.xy
                        # plt.plot(x,y,marker="o",color="blue")

                        segment_fractional = Polygon()
                        #SEGMENT OPTIONALLY
                        error = one_directory.m_error_fraction
                        percent_error = 0.05
                        if error != 0.5:

                            for percent in range(0, 101):
                                #EVERY _ PERCENT
                                if percent % 5 != 0:
                                    continue
                                else:

                                    fraction = percent/100

                                    #ASSUMING LINE ONE IS FRACTION DOWN ITS LINE
                                    #LINE 2 MUST BE WITHIN
                                    # line2max, line2min, line1min, line1max
                                    if True:

                                        if fraction + error > 1:
                                            line2max = 1
                                        else:
                                            line2max = fraction + error

                                        if fraction - error < 0:
                                            line2min = 0
                                        else:
                                            line2min = fraction - error




                                        if fraction + percent_error > 1:
                                            line1max = 1
                                        else:
                                            line1max = fraction + percent_error



                                        if fraction - percent_error < 0:
                                            line1min = 0
                                        else:
                                            line1min = fraction - percent_error


                                    top_right = self.reverse_position((0,0), l1*line1max, a1, l2*line2max, a2)
                                    top_left = self.reverse_position((0,0), l1*line1max, a1, l2*line2min, a2)
                                    bottom_left = self.reverse_position((0,0), l1*line1min, a1, l2*line2min, a2)
                                    bottom_right = self.reverse_position((0,0), l1*line1min, a1, l2*line2max, a2)

                                    assembly_line_poly = Polygon([top_right, top_left, bottom_left, bottom_right])


                                    segment_fractional = segment_fractional.union(assembly_line_poly)

                        else:
                            segment_fractional = poly


                        fractional_intersection_polygon = fractional_intersection_polygon.intersection(segment_fractional)
                        intersecting_polygon = intersecting_polygon.intersection(poly)
                        #print(f"AFTER {connection}  AREA: {intersecting_polygon.area}")


                    # x,y = fractional_intersection_polygon.convex_hull.exterior.xy
                    # plt.fill(x,y,color="red")
                    row_to_make.append(intersecting_polygon)
                    fractional_row_to_make.append(fractional_intersection_polygon.convex_hull)
                else:
                    row_to_make.append(0)
                    fractional_row_to_make.append(0)

            list_to_make.append(row_to_make)
            fractional_list_to_make.append(fractional_row_to_make)

        self.polygons = list_to_make
        self.fractional_polygons = fractional_list_to_make
        #plt.show()

    def canvas(self):
        fig, ax = plt.subplots()

        for outer in range(0, len(self.polygons)):
            for inner in range(0, len(self.polygons)):
                if inner > outer:
                    #print("STARTING CANVAS")
                    polygon = self.build_translated_polygon(self.polygons[outer][inner], 30*outer, -30*inner)


                    #print(f"11  {polygon.area}")

                    #print(f" {inner} {outer}   {polygon}")
                    if isinstance(polygon, GeometryCollection):
                        for geom in polygon.geoms:
                            x, y = geom.exterior.xy
                            plt.plot(x, y, marker="o")
                    else:
                        x, y = polygon.exterior.xy
                        plt.plot(x, y, marker="o")



                    plt.plot(30*outer, -30*inner, marker="o",color="black")
                    plt.text(30*outer, -30*inner, f"{outer} {inner}")



                    polygon = self.build_translated_polygon(self.fractional_polygons[outer][inner], 30 * outer, -30 * inner)
                    #print(f"22 {polygon.area}")

                    if isinstance(polygon, GeometryCollection):
                        for geom in polygon.geoms:
                            x, y = geom.exterior.xy
                            plt.plot(x, y, marker="o")
                    # else:
                    #     x, y = polygon.exterior.xy
                    #     plt.plot(x, y, marker="o")


                    # x, y = polygon.exterior.xy
                    # plt.plot(x, y, marker="*")
                    plt.plot(30 * outer, -30 * inner, color="green")
                    plt.text(30 * outer, -30 * inner, f"{outer} {inner}")




        #plt.show()


    def create_medium_polygon(self, use_fragment):
        total_ignores = []
        moves_this_turn = []

        for index in range(0, len(self.lof)):
            total_ignores.append(False)
            moves_this_turn.append(1)

        total_iterations_avoided = 0

        while (True):

            area_starting = 0
            area_ending = 0

            # TESTING ENDING CONDITION
            if True:
                tot = 0
                for val in moves_this_turn:
                    tot += val
                if tot == 0:
                    break

            # UPDATING CASES
            new = []
            for index, val in enumerate(moves_this_turn):
                if val == 0:
                    total_ignores[index] = True
                new.append(0)
            moves_this_turn = new

            # IF ONE CHANGED THIS ROUND MAKE TRUE
            for start in range(0, len(self.polygons)):
                for end in range(start + 1, len(self.polygons)):
                    if total_ignores[start] == True and total_ignores[end] == True:
                        total_iterations_avoided += 1
                        continue
                    else:
                        if use_fragment:

                            st = self.fractional_polygons[start][end].area
                            self.fractional_polygons[start][end] = self.create_medium_3(start, end, use_fragment=True)
                            ne = self.fractional_polygons[start][end].area

                        else:
                            st = self.polygons[start][end].area
                            self.polygons[start][end] = self.create_medium_3(start, end, use_fragment=False)
                            ne = self.polygons[start][end].area

                        area_starting += st

                        if abs(st - ne) < one_directory.p_area_tolerance:
                            continue
                        else:
                            moves_this_turn[start] += 1
                            moves_this_turn[end] += 1

            print(
                f"M: AFTER {moves_this_turn} IT_AVOIDED: {total_iterations_avoided} ST_AREA: {area_starting} (({area_starting - area_ending}))")
            total_iterations_avoided = 0

    def get_polygon(self, index1, index2, use_fragment):

        if not use_fragment:
            if index1 < index2:
                return self.polygons[index1][index2]
            else:
                return self.reverse_polygon(self.polygons[index2][index1])
        else:
            if index1 < index2:
                return self.fractional_polygons[index1][index2]
            else:
                return self.reverse_polygon(self.fractional_polygons[index2][index1])






    def reverse_polygon(self, polygon):
        coords = []

        for soc in list(polygon.exterior.coords):
            coords.append((soc[0]*-1, soc[1]*-1))

        return Polygon(coords)

    def create_medium_3(self, photo1, photo2, use_fragment):
        #IDEA for every number between that connects them
        total = 0

        if use_fragment:
            starting_point = self.fractional_polygons[photo1][photo2]
        else:
            starting_point = self.polygons[photo1][photo2]



        for index in range(0, len(self.lof)):

            #IF EQUALS 1
            if index == photo1:
                continue
            #EQUALS 2
            elif index == photo2:
                continue

            #NOT 1 OR 2
            else:

                if use_fragment:
                    p1_to_index = self.get_polygon(photo1, index, use_fragment=True)
                    to_be_extended = self.get_polygon(index, photo2,use_fragment=True)

                    next_step = self.build_extending_polygon(p1_to_index,
                                                             to_be_extended)
                else:
                    p1_to_index = self.get_polygon(photo1, index, use_fragment=False)
                    to_be_extended = self.get_polygon(index, photo2, use_fragment=False)

                    next_step = self.build_extending_polygon(p1_to_index,
                                                             to_be_extended)
                print(p1_to_index)
                print(to_be_extended)
                print(next_step)


                total+=len(list(p1_to_index.exterior.coords))
                starting_point = starting_point.intersection(next_step)


        #print(f" FULL MEDIUM 3: {len(list(starting_point.exterior.coords))}")
        total+=len(list(starting_point.exterior.coords))
        return starting_point.convex_hull





    def build_extending_polygon(self, to_extend_from, origin_0_extendable):
        ending = 0

        starting_shape = to_extend_from

        for vertice in list(starting_shape.exterior.coords):
            translated = self.build_translated_polygon(origin_0_extendable, vertice[0], vertice[1])

            if ending == 0:
                ending = translated
            else:
                ending = ending.union(translated)

        return ending.convex_hull #.simplify(0.01)

    def build_translated_polygon(self, shape, x, y):
        translated_polygon = translate(shape, xoff=x, yoff=y)
        return translated_polygon

    # given angles and distances, move forward using one dir, then extend using next
    def reverse_position(self, start, distance1, angle1, distance2, angle2):
        middle_position = self.move_random_along_angle(angle1, distance1, start)
        end_position = self.move_random_along_angle(angle2, distance2, middle_position)
        return end_position



    # Moves Given Angle
    def move_random_along_angle(self, angle, absolute, xy):
        angle = math.radians(angle)
        dx = absolute * math.sin(angle)
        dy = absolute * math.cos(angle)

        return (dx + xy[0], dy + xy[1])