import math

from matplotlib import pyplot as plt
from shapely.affinity import translate
from shapely.geometry import Point, Polygon, GeometryCollection

from five_database import five_database


class final_polygon:

    def __init__(self, final_mover):
        self.lof = final_mover.lof
        self.db = five_database()
        self.fm = final_mover

        #MAKES SIMPLE POLYGONS
        self.create_simple_polygons()

        #PRINTS THEM
        self.canvas(all=False)

        #BUFFER AT ALL????

        #MEDIUM POLYGONS
        self.create_medium_polygon(use_fragment=False)

        #NEEDS SOME WORK-----------------------------------------------------
        #self.create_medium_polygon(use_fragment=True)

        #PRINT THEM
        self.canvas(all=True)

    def create_simple_polygons(self):
        list_to_make = []
        fractional_list_to_make = []

        has_no_connections = []
        starting_id = self.lof[0].frame_id
        for outer_index in range(0, len(self.lof)):
            row_to_make = []
            fractional_row_to_make = []
            has_no_connection_row = []
            for inner_index in range(0, len(self.lof)):

                if inner_index > outer_index:

                    distance = (self.lof[inner_index].time - self.lof[outer_index].time) * \
                               self.fm.polygon_max_speed

                    intersecting_polygon = Point(0, 0).buffer(distance)
                    fractional_intersection_polygon = Point(0, 0).buffer(distance)

                    connections = self.db.translate_entire_photo(starting_id + outer_index,
                                                                 starting_id + inner_index)
                    total_used = 0
                    #CONNECTIONS
                    for connection in connections:
                        f1_index = connection[0]
                        f2_index = connection[1]

                        f1 = self.lof[outer_index].fragments[f1_index]
                        f2 = self.lof[inner_index].fragments[f2_index]

                        # CHECK THAT ANGLE ADHERES TO REQUIREMENTS
                        if True:

                            diff = abs(f1.p0_dir - f2.p0_dir)
                            # Adjust for circular range
                            circular_diff = min(diff, 360 - diff)

                            # IF TOO SMALL
                            if circular_diff < self.fm.polygon_min_difference_angle:
                                continue

                        total_used+=1


                        #Creates Polygon
                        # poly
                        if True:
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

                        #Create SEGMENTED POLYGON
                        # frac_poly
                        if True:
                            frac_poly = Polygon()
                            #Take Several Location CONVEX_HULL rest
                            error = self.fm.segmented_error_allowed
                            percent_error = 0.05
                            for percent in range(0, 101):
                                if percent % 5 == 0:
                                    fraction = percent/100

                                    #assuming LINE1 IS FRACTION ABOVE:
                                    #line2max, line2min, line1min, line1max
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

                                    top_right = self.reverse_position((0, 0), l1 * line1max, a1, l2 * line2max, a2)
                                    top_left = self.reverse_position((0, 0), l1 * line1max, a1, l2 * line2min, a2)
                                    bottom_left = self.reverse_position((0, 0), l1 * line1min, a1, l2 * line2min, a2)
                                    bottom_right = self.reverse_position((0, 0), l1 * line1min, a1, l2 * line2max, a2)

                                    frac_poly_single = Polygon([top_right, top_left, bottom_left, bottom_right])
                                    frac_poly_single = frac_poly.convex_hull
                                frac_poly = frac_poly.union(frac_poly_single)


                        intersecting_polygon = intersecting_polygon.intersection(poly)
                        fractional_intersection_polygon = fractional_intersection_polygon.intersection(frac_poly)

                    has_no_connection_row.append(total_used)

                    if self.fm.polygon_trust_gps:
                        print("INTERSECT BASED ON LOCATION")

                    row_to_make.append(intersecting_polygon)
                    fractional_row_to_make.append(fractional_intersection_polygon)
                else:
                    row_to_make.append(0)
                    fractional_row_to_make.append(0)
                    has_no_connection_row.append(0)

            list_to_make.append(row_to_make)
            fractional_list_to_make.append(fractional_row_to_make)
            has_no_connections.append(has_no_connection_row)

        self.polygons = list_to_make
        self.polygons_f = fractional_list_to_make
        self.has_no_direct_connection = has_no_connections

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

                            st = self.polygons_f[start][end].area
                            self.polygons_f[start][end] = self.create_medium_3(start, end, use_fragment=True)
                            ne = self.polygons_f[start][end].area

                        else:
                            st = self.polygons[start][end].area
                            self.polygons[start][end] = self.create_medium_3(start, end, use_fragment=False)
                            ne = self.polygons[start][end].area
                            print(f"  {start} {end}  {st} --> {ne}")

                        area_starting += st

                        if abs(st - ne) < self.fm.polygon_area_difference:
                            continue
                        else:
                            moves_this_turn[start] += 1
                            moves_this_turn[end] += 1

            print(
                f"M: USING F: {use_fragment}   AFTER {moves_this_turn} IT_AVOIDED: {total_iterations_avoided} ST_AREA: {area_starting} (({area_starting - area_ending}))")
            total_iterations_avoided = 0

    def canvas(self,all):
        fig, ax = plt.subplots()

        for outer in range(0, len(self.polygons)):
            for inner in range(0, len(self.polygons)):
                if inner > outer:

                    has_no_connection = self.has_no_direct_connection[outer][inner]

                    #MEANING NO CONNECTION
                    if has_no_connection == 0 and not all:
                        continue
                    else:


                        #PRINTING NORMAL
                        if True:
                            polygon = self.build_translated_polygon(self.polygons[outer][inner], 30*outer, -30*inner)

                            if isinstance(polygon, GeometryCollection):
                                for geom in polygon.geoms:
                                    x, y = geom.exterior.xy
                                    plt.plot(x, y, marker="o",color="red")
                            else:
                                x, y = polygon.exterior.xy
                                plt.plot(x, y, marker="o", color="green")

                        plt.plot(30*outer, -30*inner, marker="o",color="black")
                        plt.text(30*outer, -30*inner, f"{outer} {inner}")

                        #PRINTING OTHER
                        if False:
                            polygon = self.build_translated_polygon(self.polygons_f[outer][inner], 30 * outer,
                                                                    -30 * inner)


                            if isinstance(polygon, GeometryCollection):
                                for geom in polygon.geoms:
                                    x, y = geom.exterior.xy
                                    plt.plot(x, y, marker="*", color="red")
                            else:
                                x, y = polygon.exterior.xy
                                plt.plot(x, y, marker="*", color="green")




        #plt.show()





    #------------------------------------------------------------
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

    def reverse_polygon(self, polygon):
        coords = []

        for soc in list(polygon.exterior.coords):
            coords.append((soc[0]*-1, soc[1]*-1))

        return Polygon(coords)

    #NEEDS WORK, CURRENTLY USES NOT FRAGMENT
    def get_polygon(self, index1, index2, use_fragment):

        if not use_fragment:
            if index1 < index2:
                return self.polygons[index1][index2]
            else:
                return self.reverse_polygon(self.polygons[index2][index1])
        else:
            if index1 < index2:
                return self.polygons_f[index1][index2]
            else:
                return self.reverse_polygon(self.polygons_f[index2][index1])



    def create_medium_3(self, photo1, photo2, use_fragment):

        #IDEA for every number between that connects them
        total = 0

        if use_fragment:
            starting_point = self.polygons_f[photo1][photo2]
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



                total+=len(list(p1_to_index.exterior.coords))
                starting_point = starting_point.intersection(next_step)


        #print(f" FULL MEDIUM 3: {len(list(starting_point.exterior.coords))}")
        total+=len(list(starting_point.exterior.coords))
        return starting_point.convex_hull


    def build_translated_polygon(self, shape, x, y):
        translated_polygon = translate(shape, xoff=x, yoff=y)
        return translated_polygon

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