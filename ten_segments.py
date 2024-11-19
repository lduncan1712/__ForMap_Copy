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



    def create_formal_list(self, list_of):

        print("CREATING FORMAL LIST")
        print(f"    GIVEN {list_of} ")

        self.lof = list_of



        #CREATE A LIST OF SIMPLE POLYGONS  (USES SIMPLE, CREATE_DIRECT_POLYGONS-->CREATE_SIMPLE_RELATIVE
        for outer_index in range(0, len(self.lof)):
            row = []
            for inner_index in range(0, len(self.lof)):
                if inner_index > outer_index:
                    polygon = self.create_direct_polygon(self.lof[outer_index], self.lof[inner_index], False, False, True, True, False)
                    row.append(polygon)
                else:
                    row.append(0)
            self.formal_list.append(row)


        print("AREAS AFTER SIMPLE 1")
        sum = 1
        # for x in range(1, 6):
        #     print(f"  {x}  {self.formal_list[0][x].area}")
        #     sum+= self.formal_list[0][x].area
        # print(f"          ((((({sum}")

        for x in range(0, 6):
            a = []
            for y in range(0,6):
                if self.formal_list[x][y] != 0:
                    a.append(self.formal_list[x][y].area)
                else:
                    a.append(0)
            print(a)



        for x in self.formal_list:
            print(x)
            for y in x:
                print(type(y))



        #Create A List Of Complex Using Simples
        for outer_index in range(0, len(self.lof) - 1):
            for inner_index in range(0, len(self.lof) - 1):
                if inner_index > outer_index:
                    print(f" {outer_index}  {inner_index}")
                    polygon = self.create_direct_polygon(self.lof[outer_index], self.lof[inner_index], True, False, True, True, False)
                    self.formal_list[outer_index][inner_index] = polygon

        print("AREAS AFTER COMPLEX 1")
        sum = 1
        for x in range(1, 5):
            print(f"  {x}  {self.formal_list[0][x].area}")
            sum += self.formal_list[0][x].area
        print(f"          (((((({sum}")


        print("DOING CASCADE 1")
        updated_rel_f1 = self.create_cascaded_polygons(self.lof[0], True)
        #
        index = 1;
        for x in updated_rel_f1:
            self.formal_list[0][index] = x
            index+=1

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





    #Creates A List of
    def create_permanent_reference_list(self, starting_index, ending_index):
        fd = five_database()


        permanent_indexs = fd.translate_entire_photo(starting_index, ending_index)

        list_of_permanent = []
        index_list = []
        #ARBITRARY
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











    #IDEA
    #Starting From 0 At Origin, Try Every Point In 0->1,  given 2 connections, you will have 2 intersection points, from which next frame must fit into

    def omni_filter(self, base_line_id, applied_id):

        fd = five_database()

        i_baseline = base_line_id - one_directory.starting_id
        i_applied = applied_id - one_directory.starting_id

        frame1 = self.lof[i_baseline]
        frame2 = self.lof[i_applied]

        #Range of photos
        range_of_frames = fd.get_range(base_line_id)
        range_of_frames = (range_of_frames[1], range_of_frames[0])

        print(f"   START: {base_line_id}  {applied_id} {range_of_frames}")


        #Permanent Connections
        permanent_indexs, permanent_chart = self.create_permanent_reference_list(base_line_id, range_of_frames[1])

        #Polygons Of Iteration (and Corners)
        ptit = self.formal_list[i_baseline][i_applied]
        min_x, min_y, max_x, max_y = ptit.bounds

        base_line_to_applied_connections = fd.translate_entire_photo(base_line_id, applied_id)

        single_connection_1 = []
        single_connection_2 = []

        for connection in base_line_to_applied_connections:
            single_connection_1.append(connection[0])
            single_connection_2.append(connection[1])

        master_tree_list = []
        
        #BUILD OUT TREE LIST
        if True:
            
            #Create Simple First
            for first_index_values in range(0, len(self.frame1.fragments)):
                tree = fixed_point()
                tree.create_and_cascade(self.frame1.frame_id, first_index_values)
                master_tree_list.append(tree)

            #For Every After
            for later_index_values in range(self.frame2.frame_id, range_of_frames[1] + 1):

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
                        tree.create_and_cascade(later_index_values, later_index_fragment)
                        master_tree_list.append(tree)





        testing = False

        for x in range(0, int((max_x - min_x)*20) + 1):
            for y in range(0, int((max_y - min_y)*20) + 1):

                point = (min_x + 0.05*x, min_y + 0.05*y)
                shapely_point = Point(point[0], point[1])

                print("A")

                if testing:
                    if 0.95 < point[0] < 1.0 and 1.05 < point[1] < 1.1:
                        print("THIS")
                    else:
                        continue


                location_of_photos = []
                location_of_photos.append(Point(0,0))
                location_of_photos.append(shapely_point)

                location_of_trees = []

                updated_perspective_polygons = []

                failure = False
                #If 1 Position in 1 polygon
                if ptit.contains(shapely_point):

                    #REMOVE PREVIOS LIST POINTS
                    for pointss in master_tree_list:
                        pointss.point = -1
                        pointss.list_of_data = []

                    #Creates All Points (0 -> 1)
                    if True:

                        #GO THROUGH ALL CONNECTED
                        for connection in base_line_to_applied_connections:
                            frag1 = frame1.fragments[connection[0]]
                            frag2 = frame2.fragments[connection[1]]

                            # Obtain Point of intersection
                            intersection_point = self.efficiency_get_intersection_point(frag1, frag2, (0, 0), point)

                            #No intersection
                            if intersection_point == True:
                                failure = True

                                # FAILURE #2
                                # REQUIRED INTERSECTIONS BETWEEN 0 --> 1 DONT HAPPEN
                                self.plot_perspective.plot(point[0], point[1], marker="*", color="orange")

                                break

                            #This Tree Does Intersect
                            else:
                                shapely_point = Point(intersection_point[0], intersection_point[1])

                                for tree in master_tree_list:

                                    if tree.starting_photo == frame1.frame_id and tree.list_of_indexs[0] == connection[0]:
                                        tree.point = shapely_point
                                        break

                        if failure:
                            continue
                        #KNOWN TO BE VALID RANGE

                    #Changes Polygon
                    if True:
                        updated_perspective_polygons.append(-1)
                        updated_perspective_polygons.append(-1)

                        for future_index in range(i_baseline + 2, range_of_frames[1] + 1 - one_directory.starting_id):

                            previous_zero_to_future = self.formal_list[i_baseline][future_index]
                            previous_one_to_future = self.translate_polygon(
                                self.formal_list[i_applied][future_index],
                                    point[0], point[1])

                            overlap = previous_zero_to_future.intersection(previous_one_to_future)

                            if overlap.is_empty:
                                # FAILURE #3
                                # POLYGON 0 -> 1 INTERSECTION FAILS
                                self.plot_perspective.plot(point[0], point[1], marker="*", color="yellow")
                                failure = True
                                break
                            else:
                                updated_perspective_polygons.append(overlap)
                        if failure:
                            continue

                    #DownWard Traversal
                    for further_frame in range(base_line_id + 2 - one_directory.starting_id, range_of_frames[1] + 1 - one_directory.starting_id):

                        #Use First 2 Main To Get A Location
                        if True:
                            #Creates Obtained_permanent_1/2
                            for tree in master_tree_list:


                                if tree.starting_photo == base_line_id:
                                    if tree.list_of_indexs[0] == permanent_indexs[0]:
                                        rpo = tree

                                    elif tree.list_of_indexs[0] == permanent_indexs[1]:
                                        rpt = tree

                                    else:
                                        continue

                            corr_id_1 = fd.get_tree_later_multiple(rpo.starting_photo,
                                                                   rpo.list_of_indexs[0],
                                                                   further_frame + one_directory.starting_id)
                            corr_id_2 = fd.get_tree_later_multiple(rpt.starting_photo,
                                                                   rpt.list_of_indexs[0],
                                                                   further_frame + one_directory.starting_id)

                            frag1 = self.lof[further_frame].fragments[corr_id_1]
                            frag2 = self.lof[further_frame].fragments[corr_id_2]

                            location1 = rpo.point
                            location2 = rpt.point

                            location1 = (location1.x, location1.y)
                            location2 = (location2.x, location2.y)



                            coords_1 = [location1, self.frame1.move_random_along_angle(
                                (frag1.base_dir + 180) % 360, frag1.max_dist, location1)]
                            coords_2 = [location2, self.frame1.move_random_along_angle(
                                (frag2.base_dir + 180) % 360, frag2.max_dist, location2)]

                            # Making into linestrings
                            line_extending_from_first = LineString(coords_1)
                            line_extending_from_second = LineString(coords_2)

                            if testing:
                                aa,bb = line_extending_from_first.xy
                                cc,dd = line_extending_from_second.xy
                                self.plot_perspective.plot(aa,bb,color=rpo.color)
                                self.plot_perspective.plot(cc,dd,color=rpt.color)

                            next_point = line_extending_from_first.intersection(line_extending_from_second)

                            if next_point.is_empty:
                                # FAILURE #4
                                # POLYGON 0 -> N (first 2) INTERSECTION FAILS
                                self.plot_perspective.plot(point[0], point[1], marker="*", color="green")
                                failure = True
                                print("GREEN")
                                break
                            else:
                                location_of_photos.append(next_point)

                        #Determines If Location Within Acceptable
                        if True:
                            if not updated_perspective_polygons[further_frame].contains(next_point):
                                # FAILURE #5
                                # POLYGON Nth Frame Location out of polygon FAILS
                                self.plot_perspective.plot(point[0], point[1], marker="*", color="blue")
                                failure = True
                                break


                        #Redefined Forward Polygons
                        if True:
                            for further_index in range(further_frame + 1,
                                                       range_of_frames[1] + 1 - one_directory.starting_id):
                                old = updated_perspective_polygons[further_index]
                                new = self.translate_polygon(self.formal_list[further_frame][further_index], next_point.x, next_point.y)

                                overlap = old.intersection(new)

                                if overlap.is_empty:
                                    # FAILURE #6
                                    # REDEFINING POLYGON 1-->N Fails
                                    self.plot_perspective.plot(point[0], point[1], marker="*", color="indigo")
                                    failure = True
                                    break
                                else:
                                    updated_perspective_polygons[further_index] = overlap
                            if failure:
                                continue

                    if failure:
                        continue
                    else:



                        #Make Tree Locations (FILTER IMPOSSIBLE)
                        if True:

                            for tree in master_tree_list:

                                #LINESEGMENT
                                if len(tree.list_of_indexs) == 1:

                                    continue
                                #POINT
                                else:

                                    #Take First 2 And
                                    fi = tree.starting_photo - one_directory.starting_id
                                    location1 = location_of_photos[fi]
                                    location2 = location_of_photos[fi + 1]

                                    index_1 = tree.list_of_indexs[0]
                                    index_2 = tree.list_of_indexs[1]

                                    frag1 = self.lof[fi].fragments[index_1]
                                    frag2 = self.lof[fi + 1].fragments[index_2]

                                    location1 = (location1.x, location1.y)
                                    location2 = (location2.x, location2.y)



                                    coords_1 = [location1, self.frame1.move_random_along_angle(
                                        frag1.base_dir, frag1.max_dist, location1)]
                                    coords_2 = [location2, self.frame1.move_random_along_angle(
                                        frag2.base_dir, frag2.max_dist, location2)]

                                    # Making into linestrings
                                    ls_1 = LineString(coords_1)
                                    ls_2 = LineString(coords_2)

                                    a,b = ls_1.xy
                                    c,d = ls_2.xy

                                    if testing:


                                        if len(tree.list_of_indexs) != 1:
                                            self.plot_perspective.plot(a,b,color=tree.color)
                                            self.plot_perspective.plot(c,d,color=tree.color)

                                    tree_point = ls_1.intersection(ls_2)

                                    # if testing:
                                    #     if len(tree.list_of_indexs) != 2:
                                    #         self.plot_perspective.plot(tree_point.x, tree_point.y, marker="*", color=tree.color)

                                    #MEANS BASIC INTERSECTION OF FIRST NOT POSSIBLE
                                    if tree_point.is_empty:
                                        failure = True

                                        # FAILURE #7
                                        # POLYGON 0 -> 1 INTERSECTION FAILS
                                        self.plot_perspective.plot(point[0], point[1], marker="*", color="violet")

                                        break

                                    else:
                                        if tree.point != -1:
                                            continue
                                        else:
                                            tree.point = tree_point

                            if failure:
                                continue


                        #FILTER BY BOXES
                        box_width = 0.3
                        if True:
                            #For Every Tree
                            for tree in master_tree_list:
                                number_of_fails = 0
                                #Not Relavent
                                if len(tree.list_of_indexs) <= 2:
                                    continue
                                else:

                                    tree_location = tree.point.buffer(box_width)

                                    for index_in_tree_list in range(2, len(tree.list_of_indexs)):

                                        frag_index = tree.list_of_indexs[index_in_tree_list]
                                        photo_index = index_in_tree_list + tree.starting_photo
                                        photo_actual_index = photo_index - one_directory.starting_id
                                        fragment_object = self.lof[photo_actual_index].fragments[frag_index]
                                        location_of_frame = location_of_photos[photo_actual_index]
                                        shapely_location_of_frame = (location_of_frame.x, location_of_frame.y)

                                        coords = [shapely_location_of_frame,
                                                  self.frame1.move_random_along_angle(fragment_object.base_dir,
                                                                                      fragment_object.max_dist,
                                                                                      shapely_location_of_frame)]
                                        ls = LineString(coords)

                                        if testing:
                                            aaa,bbb = ls.xy
                                            self.plot_perspective.plot(aaa,bbb,color=tree.color)

                                        inter = ls.intersects(tree_location)

                                        if inter:
                                            continue
                                        else:
                                            failure = True
                                            number_of_fails += 1

                                            if testing:
                                                continue
                                            else:
                                                break
                                    if failure:
                                        if number_of_fails == 1:
                                            color = "purple"
                                        else:
                                            color = "gold"

                                        self.plot_perspective.plot(point[0], point[1], color=color, marker="*")
                                        #break
                                        if testing:
                                            aa, bb = tree_location.exterior.xy
                                            self.plot_perspective.plot(aa,bb, color=tree.color)


                            if failure:
                                if not testing:
                                    continue

                        #MAKE SIZE HEIGHT ETC
                        height_error = 0.3
                        if False:
                            for tree in master_tree_list:
                                if len(tree.list_of_indexs) == 1:
                                    continue
                                else:
                                    tree_location = tree.point
                                    tree_location_normal = (tree_location.x, tree_location.y)

                                    for local_index in range(0, len(tree.list_of_indexs)):

                                        frame_index = tree.starting_photo + local_index - one_directory.starting_id
                                        frame = self.lof[frame_index]

                                        fragment_index = tree.list_of_indexs[local_index]
                                        fragment = frame.fragments[fragment_index]

                                        photo_location = location_of_photos[frame_index]
                                        photo_location_normal = (photo_location.x, photo_location.y)

                                        distance = self.distance(tree_location_normal, photo_location_normal)

                                        size = fragment.calculate_rad_at_distance(distance)

                                        height = self.single_height_calculator(fragment, distance, height_error)

                                        data = [distance, height, size]

                                        tree.list_of_data.append(data)


                        # #FILTER BY SIZE, HEIGHT, PERSPECTIVE
                        if True:



                            size_error = 0.324 ##(fraction)
                            #Size Pretty Simple (DIRECT FROM ALL)
                            if False:
                                for tree in master_tree_list:

                                    if len(tree.list_of_indexs) > 1:
                                        overlap = (0, 1)

                                        #INCORPORATE MORE ERROR, FOR SMALLER SIZE,  LIKE PIXEL ERROR< OR FRACTION

                                        for data in tree.list_of_data:
                                            size = data[2]
                                            size_range = (size*(1 - size_error), size*(1 + size_error))

                                            new_intersection = self.single_intersection_of_range(size_range, overlap)

                                            if new_intersection != None:
                                                overlap = new_intersection
                                            else:
                                                self.plot_perspective.plot(point[0], point[1], marker="*", color="red")
                                                failure = True
                                                break

                                        if failure:
                                            break

                                if failure:
                                    continue

                            #PERSPECTIVES
                            if False:


                                for photo_index in range(0, len(location_of_photos)):

                                    all_perspectives = fd.get_perspectives(photo_index + one_directory.starting_id)

                                    all_perspectives = self.get_connecting_perspectives(all_perspectives, len(self.lof[photo_index].fragments))

                                    #TO BE MEANINGFUL (BOTH NEED TO EXIST)
                                    for perspective in all_perspectives:
                                        front = None
                                        back = None

                                        for tree in master_tree_list:

                                            #TREE EXISTS IN RIGHT PHOTO
                                            if tree.starting_photo <= photo_index + one_directory.starting_id < tree.starting_photo + len(tree.list_of_indexs):

                                                index_in_tree = photo_index + one_directory.starting_id - tree.starting_photo

                                                if len(tree.list_of_indexs) < 2:
                                                    continue

                                                if tree.list_of_indexs[index_in_tree] == perspective[0]:
                                                    front = tree
                                                elif tree.list_of_indexs[index_in_tree] == perspective[1]:
                                                    back = tree
                                                else:
                                                    if back != None and front != None:
                                                        break
                                                    else:
                                                        continue

                                        #DISTANCE FROM PHOTO TO TREE
                                        if front != None and back != None:



                                            photo_location = location_of_photos[photo_index]
                                            photo_location = (photo_location.x, photo_location.y)

                                            close_location = (front.point.x, front.point.y)
                                            far_location = (back.point.x, back.point.y)

                                            close_distance = self.distance(photo_location, close_location)

                                            far_distance = self.distance(photo_location, far_location)

                                            if close_distance > far_distance:
                                                failure = True

                                                # FAILURE #8
                                                # POLYGON 0 -> 1 INTERSECTION FAILS
                                                self.plot_perspective.plot(point[0], point[1], marker="*", color="grey")


                                                # print(f"FAIL - PERSPECTIVE: {photo_index} {perspective}")
                                                # for photo in location_of_photos:
                                                #     self.plot_perspective.plot(photo.x, photo.y, color="grey", marker="o")
                                                # break

                                    if failure:
                                        break
                                if failure:
                                    continue





                        if failure:
                            if not testing:
                                continue

                        print(f"SUCCESS: {point}")
                        self.plot_perspective.plot(point[0], point[1], marker="o", color="black")

                        # #print("SHOULD BE PRINTING")
                        # for index, point in enumerate(location_of_photos):

                            #self.plot_perspective.plot(point.x, point.y, marker="*", color=self.color_by_id(index))

                        for tree in master_tree_list:
                            if tree.point != -1:
                                a = len(tree.list_of_indexs)
                                if a == 2:
                                    color = "red"
                                elif a == 3:
                                    color = "orange"
                                elif a == 4:
                                    color = "yellow"
                                else:
                                    color = "green"
                                self.plot_perspective.plot(tree.point.x, tree.point.y, marker="*", color=color)

                        for loc in location_of_photos:

                            self.plot_perspective.plot(loc.x, loc.y, marker="*", color="black")

                else:
                    #FAILURE #1
                    #NOT CONTAINED WITHIN SHAPE
                    #self.plot_perspective.plot(shapely_point.x, shapely_point.y, marker="*", color="red")

                    print("RED FAIR")




    #IDEA, IF SOMETHING EXISTS AS STARTING AND END, OTHERS ARE CONNECTED
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













    def single_intersection_of_range(self, range1, range2):
        sorted_range1 = sorted(range1)
        sorted_range2 = sorted(range2)

        # Check for intersection
        intersection_start = max(sorted_range1[0], sorted_range2[0])
        intersection_end = min(sorted_range1[1], sorted_range2[1])

        # Return intersection or None
        if intersection_start <= intersection_end:
            return (intersection_start, intersection_end)
        else:
            return None




    def two_connection_cascade_first(self, base_line, applied, list_of_connections, range_above_at_least):
        #Converting To List Index
        base_line-=one_directory.starting_id
        applied-=one_directory.starting_id

        # Obtains Corners Of Polygon
        ptit = self.formal_list[base_line][applied]
        min_x, min_y, max_x, max_y = ptit.bounds

        # A List of Permanent Indexes (Compared TO Baseline), and the ID of these for every index
        index_list, list_of_permanent = self.create_permanent_reference_list(base_line + one_directory.starting_id, range_above_at_least[1])

        #List Of Temporary (0,1)
        list_of_first_connection = five_database().translate_entire_photo(base_line + one_directory.starting_id, applied + one_directory.starting_id)

        frame1 = self.lof[base_line]
        frame2 = self.lof[applied]

        width_tolerated = 0.15





        print(list_of_permanent)
        for x in range(0, int((max_x - min_x)*10) + 1):
            print("CHANING COLUMNS====================================================================")
            for y in range(0, int((max_y - min_y)*10) + 1):

                point = (min_x + 0.1*x, min_y + 0.1*y)

                location_set = []
                location_set.append(Point(0,0))
                location_set.append(Point(point[0],point[1]))

                location_of_photos = []


                testing = False

                if testing:


                    if not (1.4 < point[0] and point[0] < 1.5 and point[1] > -0.5 and -0.4 > point[1]):
                        continue
                    else:
                        print("b")


                failure = False

                # If point is in FRAME 1 BOUND
                if ptit.contains(Point(point[0], point[1])):
                    print(f"POINT {point} INIT:")


                    # Creates Baseline points (all chronic???? // location_of_frame_1_indexs)
                    if True:

                        location_of_frame_1_indexs = []


                        for xx in range(0,10):
                            location_of_frame_1_indexs.append(-1)


                        location_of_trees = []

                        #Fills List
                        for connection in list_of_connections:
                            f1 = frame1.fragments[connection[0]]
                            f2 = frame2.fragments[connection[1]]

                            #Obtain Point of intersection
                            intersection_point = self.efficiency_get_intersection_point(f1, f2, (0, 0), point)




                            if testing:

                                if connection[0] == index_list[0] or connection[0] == index_list[1]:
                                    color = "yellow"
                                else:
                                    color = "black"
                                self.plot_perspective.plot(intersection_point[0], intersection_point[1], color=color, marker="o")

                            #MEANS NO INTERSECTION EXISTS
                            if intersection_point == True:
                                failure = True
                                break
                            #AN INTERSECTION EXISTS
                            else:

                                tree = fixed_point()

                                dist_1 = self.distance((0,0),
                                                       (intersection_point[0], intersection_point[1]))
                                dist_2 = self.distance(point,
                                                       (intersection_point[0], intersection_point[1]))

                                height_1, height_2 = self.simplified_obtain_absolute_height(f1, f2, dist_1, dist_2, 0.3)

                                width_1 = f1.calculate_rad_at_distance(dist_1)
                                width_2 = f2.calculate_rad_at_distance(dist_2)

                                data_package_1 = [dist_1, height_1, width_1]
                                data_package_2 = [dist_2, height_2, width_2]

                                #MEANS ITS ONE OF THE PERMANENT
                                if connection[0] in index_list:
                                    #MEANS ITS ONE OF THE DEFINING POINTS
                                    if connection[0] == index_list[0] or \
                                        connection[0] == index_list[1]:


                                        tree.initalize_as_point(True,
                                                                False,
                                                                intersection_point,
                                                                frame1.frame_id,
                                                                frag1.frag_id,
                                                                data_package_1,
                                                                data_package_2)

                                    #NOT DEFINING POINT
                                    else:
                                        tree.initalize_as_point(True,
                                                                True,
                                                                intersection_point,
                                                                frame1.frame_id,
                                                                frag1.frag_id,
                                                                data_package_1,
                                                                data_package_2)

                                        #NOT PERMANENT
                                #NOT PERMANENT
                                else:
                                    tree.initalize_as_point(False,
                                                            True,
                                                            intersection_point,
                                                            frame1.frame_id,
                                                            frag1.frag_id,
                                                            data_package_1,
                                                            data_package_2)





                                    #If No Intersection Exist
                            if intersection_point == True:
                                failure = True
                                break;
                            #Intersections Do Exist
                            else:
                                #print(f"  MAKING INITIAL POINT:  {connection[0]} -> {connection[1]}  {intersection_point}")
                                location_of_frame_1_indexs[connection[0]] = intersection_point

                        if failure:
                            continue


                    # Updates Polygons For Future Frames (all future // updated_polygons_relative_to_one)
                    if True:
                        updated_polygons_relative_to_one = []
                        # For the Zero Index (first?)
                        updated_polygons_relative_to_one.append(-1)
                        # For the One Index (next?)
                        updated_polygons_relative_to_one.append(-1)

                        # For All Other Indexes
                        for future_index in range(base_line + 2, range_above_at_least[1] + 1 - one_directory.starting_id):

                            previous_zero_to_future = self.formal_list[base_line][future_index]
                            previous_one_to_future_extending_from_point = \
                                self.translate_polygon(self.formal_list[applied][future_index], point[0], point[1])

                            overlap = previous_zero_to_future.intersection(previous_one_to_future_extending_from_point)

                            if testing:

                                xxx,yyy = overlap.exterior.xy
                                self.plot_perspective.plot(xxx,yyy, color=self.color_by_id(future_index))

                            if overlap.is_empty:
                                print("       FAIL2")
                                self.plot_perspective.plot(point[0], point[1], color="yellow", marker="o")
                                failure = True
                                break
                            else:
                                #print(f"      UPDATING POLYGON {base_line} --> {future_index}")
                                updated_polygons_relative_to_one.append(overlap)

                        # No intersection between polygons
                        if failure:
                            continue


                    #Begins To Traverse Downwards
                    for further_frame in range(base_line + 2, range_above_at_least[1] + 1 - one_directory.starting_id):

                        #Use First Two Intersections to get a location (next_point)
                        if True:
                            # Gives Me Tree Id in Further_frame of first two
                            first_comparison_index = list_of_permanent[index_list[0]][further_frame]
                            second_comparison_index = list_of_permanent[index_list[1]][further_frame]

                            # Identifying these Fragments
                            frag1 = self.lof[further_frame].fragments[first_comparison_index]
                            frag2 = self.lof[further_frame].fragments[second_comparison_index]

                            #Determining Points These Extend From
                            point1 = location_of_frame_1_indexs[index_list[0]]
                            point2 = location_of_frame_1_indexs[index_list[1]]

                            #Creating Line From Them
                            coords_1 = [point1, self.frame1.move_random_along_angle(
                                                                       (frag1.base_dir + 180) % 360, frag1.max_dist, point1)]
                            coords_2 = [point2, self.frame1.move_random_along_angle(
                                                                        (frag2.base_dir + 180) % 360, frag2.max_dist, point2)]
                            #Making into linestrings
                            line_extending_from_first = LineString(coords_1)
                            line_extending_from_second = LineString(coords_2)

                            if testing:

                                a,b = line_extending_from_first.xy
                                self.plot_perspective.plot(a,b, color = "red")
                                a, b = line_extending_from_second.xy
                                self.plot_perspective.plot(a, b, color="red")


                            #Taking Its intersection
                            next_point = line_extending_from_first.intersection(line_extending_from_second)

                            location_set.append(next_point)


                            if next_point.is_empty:
                                failure = True
                                break

                        # Determines If Next_point in correct range
                        if True:

                            if not updated_polygons_relative_to_one[further_frame].contains(next_point):
                                failure = True
                                break

                        # Determines If All Other ( CHRONIC / TEMP ) Connections Adhere (???????????????????????)

                        # Determine Size, Height, And Perspective (???????????????)


                        #Redefines Forward Polygons Using Newly known position
                        if True:
                            for further_index in range(further_frame + 1, range_above_at_least[1] + 1 - one_directory.starting_id):

                                #The Previously Known Value (defined using above / first)
                                old = updated_polygons_relative_to_one[further_index]

                                #the further_frame (at point) extended to in front
                                new = \
                                    self.translate_polygon(self.formal_list[further_frame][further_index], next_point.x, next_point.y)

                                #Their Intersection Are Valuable
                                overlap = old.intersection(new)

                                if overlap.is_empty:
                                    failure = True
                                    break
                                else:
                                    updated_polygons_relative_to_one[further_index] = overlap







                    if failure:
                        continue
                    else:
                        self.plot_perspective.plot(point[0], point[1], color="black", marker="o")

                        # print(location_of_frame_1_indexs)
                        for index, point in enumerate(location_set):
                            if index > 0 and index < 5:
                                print(f"{self.color_by_id(index)}")
                                self.plot_perspective.plot(point.x, point.y, color=self.color_by_id(index), marker="o")

                #else:
                    #print("  LOCATION FAILS POLYGONS")
                    #self.plot_perspective.plot(point[0], point[1], color="red", marker="o")

    def single_height_calculator(self, fragment, distance, tolerance):
        av_h1 = distance * math.tan(math.radians(fragment.base_d))

        lower = av_h1 - tolerance
        upper = av_h1 + tolerance

        return (lower, upper)







































    #OPTIONALLY CREATE POLYGON USING COMPLEX/SIMPLE
    def create_direct_polygon(self, frame1, frame2, extreme, testing, height, width, delta ):

        #If wanting to use simple
        if not extreme:
            print("DOING SIMPLE")
            return self.create_simple_relative_polygon(frame1, frame2, height, width, delta)

        #using complicated
        else:
            #print("DOING COMPLICATED")
            #REQUIRES PREVIOUS ALREADY MADE  (HWD useless)
            return self.create_complex_relative_polygon(frame1, frame2, height, width)






    def solve_system_two_vector(self, frame1, frame2):
        frame1.make_set_line_segments((0,0), 0, True)

        #Basis Setup
        if True:

            fig, ax = plt.subplots(2,4)
            fig2, ax2 = plt.subplots()
            hills = fig2.add_subplot(111, projection='3d')
            self.frame1 = frame1
            self.frame2 = frame2
            self.frame1.single_importance_ratios()
            self.frame2.single_importance_ratios()
            self.plot_perspective =      ax[0,0]
            self.plot_lines =                ax[0,1]
            self.plot_dots =                  ax[1,0]
            self.plot_chart =                ax[0,3]
            self.board =                     ax[0,2]
            self.waves =                     ax[1,1]
            self.test = ax[1,2]
            self.test2 = ax[1,3]
            self.hills = hills

            self.current_position = 0;
            self.intersection_array = 0;
            self.frame2.possible = 0;

            self.r_i = []
            self.r_b = []
            self.r_h = []

            # TotalWidth1, TotalWidth2, TotalSumRatios, TotalIntersections,          #Num Blacklist
            self.solve_attempt_macros = [0, 0, 0, 0, 0]

            self.frame1_cmap = colors.LinearSegmentedColormap.from_list('f1_map', [(0, frame1.color_to_use), (1, 'black')])
            self.frame2_cmap = colors.LinearSegmentedColormap.from_list('f2_map', [(0, 'grey'), (1, frame2.color_to_use)])

        #Creating Blacklist
        self.system_blacklist = self.solve_system_permanent_blacklist()

        #Creates Boundary
        self.final, time, just = self.build_shape_using_intital_bounds(self.frame1, self.frame2, self.frame1.bound, self.frame2.bound, (0, 0))


        #Visualizes Bounds
        if True:
            #Applies Permanent Components
            self.solve_system_permanant_components(self.final)

            x, y = just.exterior.xy
            self.plot_perspective.plot(x, y, color='red')

            # TIME EXTENT
            x, y = time.exterior.xy
            self.plot_perspective.plot(x, y, color='grey')

            # INTERSECTION
            x, y = self.final.exterior.xy
            self.plot_perspective.plot(x, y, color='green')

        l = five_database().translate_entire_photo(frame1.frame_id, frame2.frame_id)


        ec = eleven_connection(self, frame1, frame2, self.final, l, self.lof)

    #SIMPLE RELATIVE:
    #Given 2 Frames, Creates Shape Using Direct Possibilities
    def create_simple_relative_polygon(self, frame1, frame2, height, width, delta):
        l = []
        print(f"SIMPLE - RELATIVE  {frame1.frame_id} {frame2.frame_id} ")

        # Creating A List of Intersections (INDEXES IN F1---> F2)
        if frame1.frame_id > frame2.frame_id:
            #print("       SWAPPING")
            m = five_database().translate_entire_photo(frame2.frame_id, frame1.frame_id)
            for sublist in m:
                l.append((sublist[1], sublist[0]))

        else:
            l = five_database().translate_entire_photo(frame1.frame_id, frame2.frame_id)

        print(f"- List Of Connections: {l}")
        # Creates a shape, using previous bounds, and overlapping_connections
        proper_intersections = self.create_polygon_of_possibility(frame1, frame2, l)

        # Creates a shape, using rational requirements
        #rational_polygon = self.create_polygon_of_rationality(frame1, frame2, proper_intersections, l, height, width, delta)

        rational_polygon = proper_intersections.buffer(0.1)

        #Returns The Shape, But Buffered
        return rational_polygon.buffer(0).simplify(0.01)


    #(INTERMEDIATE)
    #Given 3 Frames, Creates Shape 3, Created By 1->2->3
    def create_simple_distant_polygon(self, starting_frame, intermediate_frame, endpoint_frame, height, width, testing):
        st_id = starting_frame.frame_id - one_directory.starting_id
        i_id = intermediate_frame.frame_id - one_directory.starting_id
        e_id = endpoint_frame.frame_id - one_directory.starting_id



        #GET 1-->2
        if starting_frame.frame_id < intermediate_frame.frame_id:
            a = self.formal_list[st_id][i_id]
        else:
            a = self.reflect_polygon(self.formal_list[i_id][st_id])


        #GET 2-->3
        if intermediate_frame.frame_id < endpoint_frame.frame_id:
            b = self.formal_list[i_id][e_id]
        else:
            b = self.reflect_polygon(self.formal_list[e_id][i_id])

        # b extending from a

        # print("INDIVIDIALS:")
        # print(a)
        # print(b)
        c = self.build_shape_relative_to_shape(a,b)

        return c



    # COMPLEX RELATIVE
    # Given 2 Frames, Creates Frame Using 1->2 and 1->3->2 and 1->4->2
    #Only Does Single Length Tho
    def create_complex_relative_polygon(self, frame1, frame2, height, width):
        #print(f"CREATING COMPLEX_RELATIVE_POLYGON {frame1.frame_id} {frame2.frame_id}")

        # First obtain the range to use
        f1_range = (frame1.polygons_below, frame1.polygons_above)
        f2_range = (frame2.polygons_below, frame2.polygons_above)
        #Its intersection is the overlap valuable

        intersected_range = self.intersection_of_relative_ranges(f1_range, f2_range)

        #If no intersection
        if intersected_range == None:
            print("IS THIS EVEN POSSIBLE")


        #Some intersection
        else:
            intersected_polygon = 0

            for frame_index in range(intersected_range[0] - one_directory.starting_id, intersected_range[1] + 1 - one_directory.starting_id):

                # Nothing to do
                if frame_index == frame1.frame_id - one_directory.starting_id:
                    continue

                # Can create direct polygon
                elif frame_index == frame2.frame_id - one_directory.starting_id:

                    if frame2.frame_id > frame1.frame_id:
                        c = self.formal_list[frame1.frame_id - one_directory.starting_id][frame2.frame_id - one_directory.starting_id]
                    else:
                        c = self.reflect_polygon(self.formal_list[frame2.frame_id - one_directory.starting_id][frame1.frame_id - one_directory.starting_id])

                    if intersected_polygon == 0:
                        intersected_polygon = c
                    else:
                        intersected_polygon = intersected_polygon.intersection(c)

                #Need to go multiple
                else:
                    c = self.create_simple_distant_polygon(frame1, self.lof[frame_index], frame2, height, width, False)

                    if intersected_polygon == 0:
                        intersected_polygon = c
                    else:
                        intersected_polygon = intersected_polygon.intersection(c)

            return intersected_polygon

    #creates a polygon that represents all points, relative to frame1 at (0,0) that adhere to connections
    def create_polygon_of_possibility(self, frame1, frame2, connections):

        polygons_to_rationalize = []

        #print("TRYING BOUNDS")
        #print(frame1.bound)
        #print(frame2.bound)

        #creates a polygon that frame2 must be within
        final, a, b = self.build_shape_using_intital_bounds(frame1, frame2, frame1.bound, frame2.bound, (0, 0))


        #obtains a list of all relationships that need to be upheld
        l = connections
        #Creates List Of Polygons That Need To Be Intersection
        for ind, match in enumerate(l):
            f1_index = match[0]
            f2_index = match[1]

            f1 = frame1.fragments[f1_index]
            f2 = frame2.fragments[f2_index]



            #distance between max and min
            l1 = f1.max_dist
            s1 = f1.min_dist
            l2 = f2.max_dist
            s2 = f2.min_dist
            print(f"{f1.width_d}  {f2.width_d}")
            print(f" {l1} {s1} {l2} {s2}")

            #corrasponding points
            ss = self.reverse_engineer_position(f1, f2, s1, s2, frame1 )
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


        #makes a refined polygon
        for polygon in polygons_to_rationalize:
            final = final.intersection(polygon)

        return final

    #Returns a polygon with vertices on outside no more then n mether appart
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
                increment = 1 / num_points                 #REPLACE1 WITH DIST

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


    #creates a polygon that represents all points, relative to frame1, at (0,0) that
    # PASS:   Height,  Width,  Difference???
    def create_polygon_of_rationality(self, frame1, frame2, possibility, list_of_connections, height, width, delta):
        origin = (0,0)

        final_list_of_indexs = []

        frag1 = frame1.fragments[list_of_connections[0][0]]
        frag2 = frame2.fragments[list_of_connections[0][1]]

        f1_total = frag1.max_dist - frag1.min_dist
        f2_total = frag2.max_dist - frag2.min_dist

        #CREATE DISTINCT PERSPECTIVE LISTS
        distinct_perspective_list_one = []
        distinct_perspective_list_two = []


        for x in list_of_connections:
            if x[0] != -1 and x[1] != -1:
                distinct_perspective_list_one.append(x[0])
                distinct_perspective_list_two.append(x[1])
        print(f"  FRAMES:  {frame1.frame_id}  {frame2.frame_id}")

        relevant_perspectives_one = self.assess_useful_perspectives_from_connections(frame1.frame_id, distinct_perspective_list_one)
        relevant_perspectives_two = self.assess_useful_perspectives_from_connections(frame2.frame_id, distinct_perspective_list_two)


        #Goes Through Every 10 Cm, To Identify If a point should be within
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

                    val = self.efficiency_test(height, width, delta, list_of_connections, frame1, frame2, key_frame2_point, relevant_perspectives_one, relevant_perspectives_two)
                    #print("A")
                    if not val == False:
                        row_of_indexes.append(val)




            if len(row_of_indexes) > 0:
                final_list_of_indexs.append(row_of_indexes)

        # If Too Few Points Are Determined Within
        if len(final_list_of_indexs) < 1:
            print("        POLYGON OF RATIONALITY FAILED  (NOT ENOUGH INDEXES)")
        else:


            #Create A Polygon That Takes The Outside Indexes
            v = self.minimum_bounding_polygon(final_list_of_indexs)
            p = Polygon(v)

            #If It Needs To Be Convex Hulled (to Remove Overlap)
            if not p.is_valid:

                p = p.convex_hull
                if not p.is_valid:
                    print("      NOT VALID - TRIED TO FIX FAILED")

            return p.buffer(0.1)




    #ONLY APPLIES FORWARD
    #IDEA, HAVE MULTIPLE LOCKED POINTS

    #NOT READY!!!!!!!!!!!!!!!!!!!!!!!!!
    def create_cascade_of_points(self, frame, locked_points_ids, locked_point_locations):

        all_poss = (frame.frame_id, frame.polygons_above + 1)

        cache_of_previous_points = []

        for value in range(all_poss[0], all_poss[1]):

            #ONE OF LOCKED POINTS
            if value in locked_points_ids:
                index = locked_points_ids.index(value)
                cache_of_previous_points.append(locked_point_locations[index])

            #A Polygon To Be Positioned On
            else:

                #If previous was a point
                if locked_points_ids.index(value - 1) != -1:
                    index = locked_points_ids.index(value - 1)
                    short_direct = self.formal_list[value - 1][value]
                    applied_direct = self.translate_polygon(short_direct, locked_point_locations[index][0], locked_point_locations[index][1])
                #Previous was a polygon
                else:
                    previous = cache_of_previous_points[len(cache_of_previous_points) - 1]
                    short_direct - self.formal_list[value - 1][value]
                    applied_direct = self.build_shape_relative_to_shape(previous, short_direct)


            #Then need to rationalize this with all points and polygons before
            #since previous already rationalized
            index_in_cache = -1
            for need_to_rationalize in range(all_poss[0], index - 1):
                #Means its a point
                if locked_points_ids.index(need_to_rationalize) != -1:
                    index =  locked_points_ids.index(need_to_rationalize)
                    long_direct = self.formal_list[need_to_rationalize][value]
                    point_to_start_around = locked_point_locations[index]

                    moved_possibilities = self.translate_polygon(long_direct, point_to_start_around[0], point_to_start_around[1])

                    applied_direct = applied_direct.intersection(moved_possibilities)


                    #Means its a polygon
                else:
                    long_direct = self.formal_list[need_to_rationalize][value]
                    polygon_to_start_around = cache_of_previous_points[index_in_cache]

                    moved_possibilities = self.build_shape_relative_to_shape(polygon_to_start_around, long_direct)

                    applied_direct = applied_direct.intersection(moved_possibilities)



                index_in_cache+=1
                # x, y = applied_direct.exterior.xy
                # self.plot_perspective.plot(x,y,color="black")

            cache_of_previous_points.append(applied_direct)





    #Define
    def create_cascaded_polygons(self, frame1, use_complicated):
        #Range of polygons in front of
        f1_range = (frame1.frame_id, frame1.polygons_above)

        #Cache To Hold Relative Polygons
        cache = []


        #Forward Cleaning
        for index in range(f1_range[0] + 1, f1_range[1] + 1):

            previous_value = index - f1_range[0] - 2

            #Means first after f1
            if len(cache) == 0:
                #a = self.create_direct_polygon(frame1, self.lof[index], use_complicated, False, True, True)
                a = self.formal_list[frame1.frame_id - one_directory.starting_id][index - one_directory.starting_id]
                cache.append(a)


            #Means needs to rationalize more
            else:
                #The previous polygon starting point
                previous_polygon = cache[previous_value]

                #short_direct = self.create_direct_polygon(self.lof[index - 1], self.lof[index], use_complicated, False, True, True)
                short_direct = self.formal_list[index - 1 - one_directory.starting_id][index - one_directory.starting_id]

                applied_direct = self.build_shape_relative_to_shape(previous_polygon, short_direct)


                #Now must rational, direct from all before
                intersection = applied_direct



                #Rationalizes Previous
                for iterated in range(f1_range[0], index - 1):

                    #long_direct = self.create_direct_polygon(self.lof[iterated], self.lof[index], use_complicated, False, True, True)
                    long_direct = self.formal_list[iterated - one_directory.starting_id][index - one_directory.starting_id]


                    #If this is the line from the origin to poly, starting at correct place
                    if iterated == f1_range[0]:
                        intersection = intersection.intersection(long_direct)
                    else:
                        to_iterate_around = cache[iterated - f1_range[0] - 1]

                        direct_possibilities = self.build_shape_relative_to_shape(to_iterate_around, long_direct)

                        intersection = intersection.intersection(direct_possibilities)

                cache.append(intersection)

        id = 1
        # for lal in cache:
        #     x, y = lal.exterior.xy
        #
        #     if id == 1:
        #         color = "orange"
        #     elif id == 2:
        #         color = "red"
        #     elif id == 3:
        #         color = "purple"
        #     else:
        #         color = "black"
        #     id += 1
        #
        #     self.plot_perspective.plot(x, y, color=color)

        return cache


    def color_by_id(self, id):
        if id == 1:
            color = "orange"
        elif id == 2:
            color = "red"
        elif id == 3:
            color = "purple"
        else:
            color = "black"
        return color

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



    #Takes The Total Points Found Within, and Creates A Polygon, Using Those on the outside
    def minimum_bounding_polygon(self, points):

        new_semi_trimmed_edges = []

        #Obtain first, and last in list

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




    #Returns the perspectives, that only feature 2 trees included
    def assess_useful_perspectives_from_connections(self, id, list_of_connection):

        list_of_perspective_to_keep = []

        perspectives = five_database().get_perspectives(id)
        #print(f" RAW PERSPECTIVES {perspectives}")
        #print(f" RAW CONNECTIONS {list_of_connection}")

        for perspective in perspectives:

            if perspective[0] in list_of_connection and perspective[1] in list_of_connection:
                list_of_perspective_to_keep.append(perspective)
        #print(f" FILTERED PERSPECTIVES {list_of_perspective_to_keep}------------------------------------")
        return list_of_perspective_to_keep


    #Determines Using the chosen Tests, whether this point is valid
    def efficiency_test(self, height, size, delta, connections, frame1, frame2, location, list_of_valid_perspectives_1, list_of_valid_perspectives_2):

        #Relative Cameras
        valid_intersection_height = (-1,1)

        #Fraction of Size
        valid_size_differential = 0.4

        #Height relative to camera that base needs to be
        valid_absolute_height = (-4, 0)

        #Exact distance of height, error can be within
        valid_height_error = 0.3

        distance_cache_photo_1 = []
        distance_cache_photo_2 = []

        #CAN BE CHANGED TO UPPER LIMIT OF TREES
        for x in range(0, 20):
            distance_cache_photo_1.append(-1)
            distance_cache_photo_2.append(-1)

        all_too_close = True
        all_too_far = True

        for connection in connections:

            #Define the fragment
            f1 = frame1.fragments[connection[0]]
            f2 = frame2.fragments[connection[1]]

            #Get point where intersects
            intersection_point = self.efficiency_get_intersection_point(f1, f2, (0, 0), location)

            #Get distances to intersection
            d1 = self.distance((0,0), intersection_point)
            d2 = self.distance(location, intersection_point)

            #Put in cache
            distance_cache_photo_1[connection[0]] = d1
            distance_cache_photo_2[connection[1]] = d2





            if height:

                #Obtains the possible height of this CONNECTIONs intersection
                intersection_height, absolute_p1, absolute_p2 = self.efficiency_height_differences(f1,f2, d1, d2, intersection_point, valid_height_error)

                valid_intersection_height = self.intersection_of_relative_ranges(valid_intersection_height, intersection_height)

                # if no intersection can be made between valid point, and required height difference
                if valid_intersection_height == None:
                    #print("FAILING H2")
                    return False

                if (absolute_p1[0] > valid_absolute_height[1]) or \
                        (absolute_p1[1] < valid_absolute_height[0]) or \
                            (absolute_p2[0] > valid_absolute_height[1]) or \
                                (absolute_p2[1] < valid_absolute_height[0]):
                    #print("FAILING H3")
                    return False


            if size:

                #ADD CASE FOR COVERAGE???
                should_be_width1 = round(f1.calculate_rad_at_distance(d1), 5)
                should_be_width2 = round(f2.calculate_rad_at_distance(d2), 5)
                ratio = round(should_be_width1 / should_be_width2, 5)

                if not ((1 - valid_size_differential)**2 <= ratio) and (ratio <= (1 + valid_size_differential)**2):
                    #print("FAILING S1")
                    return False
                #print(ratio)

                #RATIO IS LARGER, THEN HALF SIZE DIFFERENTIAL
                if ((1 + valid_size_differential/1.5)**2 <= ratio):
                    all_too_far = False
                #RATIO IS LESS THEN HALF SIZE DIFFERENTIAL
                elif ((1 - valid_size_differential/1.5)**2 >= ratio):
                    all_too_close = False
                else:
                    all_too_close = False
                    all_too_far = False



        if delta:

            for valid_perspective_1 in list_of_valid_perspectives_1:
                #DISTANCE OF IN FRONT MUST BE LESS OR EQUAL
                if distance_cache_photo_1[valid_perspective_1[0]] <= distance_cache_photo_1[valid_perspective_1[1]]:
                    continue
                else:
                    self.plot_perspective.plot(location[0], location[1], marker="o", color="red")
                    print("FAILING DELTA")
                    return False

            for valid_perspective_2 in list_of_valid_perspectives_2:
                if distance_cache_photo_2[valid_perspective_2[0]] <= distance_cache_photo_2[valid_perspective_2[1]]:
                    continue
                else:
                    print("FAILING DELTA")
                    self.plot_perspective.plot(location[0], location[1], marker="o", color="red")
                    return False






        #CASE FOR CONSISTANT SIZE OVERLAP?,  USELESS
        if len(connections) > 1 and size:
            if all_too_far or all_too_close:
                #print("AA")
                #self.plot_perspective.plot(location[0], location[1], marker="*", color="blue")
                return False






        #ADDD SOMETHING ABOUT IF ALL ARE CONSISTANTLY ABOVE (LARGER, TALLER),  THEN PROBABLY BETTER OUT THERE???

        # if all_too_far:
        #
        #
        # elif all_too_close:
        #     self.plot_perspective.plot(location[0], location[1], marker="*", color="grey")
        # else:
        #     print("LOL")

        return location
















    def reverse_engineer_position(self, frag1, frag2, dist1, dist2, frame):
        key_interception_point = frame.move_random_along_angle(frag1.base_dir, dist1, (0,0))

        key_frame2_point = frame.move_random_along_angle((frag2.base_dir + 180) % 360, dist2, key_interception_point)

        return key_frame2_point




        # determines whether an intersection is blacklisted


    #Obtains the intersection point of 2 frags at given locations
    def efficiency_get_intersection_point(self, frag1, frag2, loc_1, loc_2):

        hor_angle = frag1.base_dir
        start_point = frag1.parent.move_random_along_angle(hor_angle, frag1.min_dist, loc_1)
        end_point = frag1.parent.move_random_along_angle(hor_angle, frag1.max_dist, loc_1)
        seg1 = LineString([start_point, end_point])
        #print(seg1)

        hor_angle = frag2.base_dir
        start_point = frag2.parent.move_random_along_angle(hor_angle, frag2.min_dist, loc_2)
        end_point = frag2.parent.move_random_along_angle(hor_angle, frag2.max_dist, loc_2)
        seg2 = LineString([start_point, end_point])
        #print(seg2)

        if seg2.intersects(seg1):
            #print("GOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOo")

            sect = seg1.intersection(seg2)
            return (sect.x, sect.y)
        else:
            #print("DOESNT INTERSECT")
            return True



    def simplified_obtain_absolute_height(self, frag1, frag2, d1, d2, tolerance):
        av_h1 = d1 * math.tan(math.radians(frag1.base_d))
        av_h2 = d2 * math.tan(math.radians(frag2.base_d))

        max_h1 = av_h1 + tolerance
        min_h1 = av_h1 - tolerance

        max_h2 = av_h2 + tolerance
        min_h2 = av_h2 - tolerance

        return (min_h1, max_h1), (min_h2, max_h2)

    def simplified_obtain_relative_height(self):
        print("FF")


    #Returns the relative height diffrence for a single tree, at a given point
    def efficiency_height_differences(self, frag1, frag2, d1, d2, intersection, tolerance):

        av_h1 = d1 * math.tan(math.radians(frag1.base_d))
        av_h2 = d2 * math.tan(math.radians(frag2.base_d))


        max_h1 = av_h1 + tolerance
        min_h1 = av_h1 - tolerance

        max_h2 = av_h2 + tolerance
        min_h2 = av_h2 - tolerance

        #print(f"H1:  {round(min_h1,2)} {round(max_h1,2)}     H2: {round(min_h2,2)}  {round(max_h2,2)}")





        intersection = self.relative_difference_range_of_point((max_h1, min_h1),
                                                               (max_h2, min_h2))
        #print(f"INTERSECTION:  {round(intersection[0],2)} {round(intersection[1],2)}  ")

        return intersection, (min_h1, max_h1), (min_h2, max_h2)

    # Returns the tolerated Error Angle At Given Distance
    def tolerated_error_bound_at_distance(self, distance, starting_angle):
        a = 20
        b = 1              #WAS 1
        c = 0.5

        angle_dev = a / (distance * b + c * abs(-90 - starting_angle))

        # angle_dev = (1/distance)  * (1/(abs(-90 - starting_angle)))

        # angle_dev = math.pow(abs(starting_angle),1.1)*(math.pow(distance,-0.8))



        return angle_dev

    def relative_difference_range_of_point(self, p1, p2):
        pot1 = p1[0] - p2[1]
        pot2 = p1[1] - p2[0]

        return (min(pot1, pot2), max(pot1, pot2))

    def intersection_of_relative_ranges(self, range1, range2):
        start = max(range1[0], range2[0])
        end = min(range1[1], range2[1])
        if start <= end:
            return (start, end)
        else:
            return None


    def effic_is_blacklisted(self, ind1, ind2):
        if self.system_blacklist[ind1][ind2] == 0:
            return True
        else:
            return False

    # returns a list that forms the blacklist for frame intersections
    def solve_system_permanent_blacklist(self):

        intersection_list = []

        for f1 in self.frame1.fragments:
            f1_row_list = []

            for f2 in self.frame2.fragments:
                diff = self.difference_between_angles(f1.base_dir, f2.base_dir)

                # IF WITHIN DFP from 180
                if 180 - one_directory.dist_from_perfect <= diff <= 180 + one_directory.dist_from_perfect:

                    # IF OPPOSITES AND NOT STRAIGHT

                    if f1.angle_consistant == 1 and f2.angle_consistant == 1:
                        f1_row_list.append(0)
                        self.solve_attempt_macros[3] = self.solve_attempt_macros[3] + 1
                    elif f1.angle_consistant == -1 and f2.angle_consistant == -1:
                        f1_row_list.append(0)
                        self.solve_attempt_macros[3] = self.solve_attempt_macros[3] + 1
                    else:
                        f1_row_list.append(1)

                # EXACT
                elif diff <= 2 * one_directory.dist_from_perfect:

                    # IF ONE IS STRAIGHT (OR NEITHER)
                    if (f1.angle_straight != 1 and f2.angle_straight == 1) or \
                            (f1.angle_straight == 1 and f2.angle_straight != 1) or \
                            (f1.angle_straight != 1 and f2.angle_straight != 1):
                        if f1.angle_consistant == 1 and f2.angle_consistant == -1:
                            f1_row_list.append(0)
                            self.solve_attempt_macros[3] = self.solve_attempt_macros[3] + 1
                        elif f1.angle_consistant == -1 and f2.angle_consistant == 1:
                            f1_row_list.append(0)
                            self.solve_attempt_macros[3] = self.solve_attempt_macros[3] + 1
                        else:
                            f1_row_list.append(1)

                        # CASE WHERE BOTH STRAIGHT, CANT SAY CONCLUSIVELY
                    else:
                        f1_row_list.append(1)
                else:
                    f1_row_list.append(1)
            intersection_list.append(f1_row_list)
        return intersection_list

    #Creates A Polygon Representing POV (for a frame, at a position)
    def create_perspective_polygons(self, frame, position):

        furthest, closest = frame.obtain_furthest_and_closest_position()

        starting_angle, ending_angle = frame.left_range, frame.right_range


        close1 = frame.move_random_along_angle(starting_angle, closest, position)
        close2 = frame.move_random_along_angle(starting_angle + frame.width/2, closest, position)
        close3 = frame.move_random_along_angle(ending_angle, closest, position)

        far1 = frame.move_random_along_angle(starting_angle, furthest, position)
        far2 = frame.move_random_along_angle(starting_angle + frame.width / 2, furthest, position)
        far3 = frame.move_random_along_angle(ending_angle, furthest, position)


        return Polygon([far1, far2, far3, close3, close2, close1])


    # Augments GPS range Using Time Limitations (HOLISTIC)
    def tech_3_pre_clean(self):
        # For every outer frame
        for outer_index, outer_frame in enumerate(self.lof):
            # For every frame within
            for inner_index, inner_frame in enumerate(self.lof):
                #Diagonalization to avoid repitition or equality
                if outer_index > inner_index:



                    #if within a reasonable distance
                    if outer_frame.distance(outer_frame.centre, inner_frame.centre) < 200:
                        # Max possible distance appart (time distance)
                        distance = outer_frame.max_distance(outer_frame.time, inner_frame.time)

                        # Creates buffered Distances extending
                        fo_e = outer_frame.bound.buffer(distance)
                        fi_e = inner_frame.bound.buffer(distance)

                        # The new frame 1 possibilities are the overlap between f1, original, and f2_e
                        outer_frame.bound = outer_frame.bound.intersection(fi_e)
                        # The new frame 2 possibilities are the overlap between f2 original and f1_1



                        inner_frame.bound = inner_frame.bound.intersection(fo_e)

    #Given a shape, and anouther shape relative to 0, create a polygon, of shape 2 extending from shape1
    def build_shape_relative_to_shape(self, shape1, shape2):

        if len(shape1.exterior.coords) == 1:
            translated_shape = self.translate_polygon(shape2, shape1.exterior.coords[0][0], shape1.exterior.coords[0][0])
            return translated_shape
        else:
            current_shape = 0
            #Complicate
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



    #Builds a shape using 2 preconstructed bounds
    def build_shape_using_intital_bounds(self, frame1, frame2, frame1_bound, frame2_bound, sp):
        current_shape = 0


        #For Every Edge Of Frame1
        frame1_vertices = list(frame1.bound.exterior.coords)   #USED TO BE LISTED

        for vertice in frame1_vertices:
            #Make a shape that represents f2, extending from a point
            translated_2_shape = self.translate_polygon(frame2_bound,  sp[0] - 1*vertice[0], sp[1] - 1*vertice[1])

            if current_shape == 0:
                current_shape = translated_2_shape
            else:
                current_shape = current_shape.union(translated_2_shape)

        current_shape = Polygon(list(current_shape.exterior.coords))




        #create a bound based on time
        t_dist =(1 + abs(frame1.time - frame2.time))*one_directory.speed

        time_constrained_shape = Point(sp[0],sp[0]).buffer(t_dist)


        final_constrained = current_shape.intersection(time_constrained_shape)

        return final_constrained, time_constrained_shape, current_shape


    #Moves every point in a polygon by given amount
    def translate_polygon(self, polygon, x_offset, y_offset):
        # Create a new list to hold the translated vertices
        translated_vertices = []

        # Iterate over the vertices of the polygon and adjust their coordinates
        for ps in list(polygon.exterior.coords):
            x,y = ps[0], ps[1]
            translated_x = x + x_offset
            translated_y = y + y_offset
            translated_vertices.append((translated_x, translated_y))

        # Create a new polygon object with the translated vertices
        translated_polygon = Polygon(translated_vertices)

        return translated_polygon


    def reflect_polygon(self, polygon):
        reflected = []

        for vertice in list(polygon.exterior.coords):

            reflected.append((-1*vertice[0], -1*vertice[1]))

        return Polygon(reflected)





        return reflected_polygon




    #Visualizes A Single Solve Attempt
    # (line segements, hills)
    def solve_attempt_visuals(self, to_try, color):
        # MAKE Frame2 Segments (NOT PERMANANT)

        for index, ls in enumerate(self.frame2.fragments):
            x, y = ls.current_line_segment.xy
            a = self.hills.plot(x, y, color=self.frame2_cmap(index / len(self.frame2.fragments)))
            self.r_i.append(a)
            a = self.plot_lines.plot(x, y, color=self.frame2_cmap(index / len(self.frame2.fragments)))
            self.r_i.append(a)

        a = self.plot_lines.plot(to_try[0], to_try[1], marker="o", color=self.frame2.color_to_use)
        self.r_i.append(a)
        a = self.hills.plot(to_try[0], to_try[1], marker="o", color=self.frame2.color_to_use)
        self.r_i.append(a)

        # s1 = self.create_perspective_polygons(self.frame1, (0, 0))
        # s2 = self.create_perspective_polygons(self.frame2, to_try)
        #
        # # poly1x, poly1y = s1.exterior.xy
        # # poly2x, poly2y = s2.exterior.xy
        # #
        # # self.plot_lines.plot(poly1x, poly1y, color='black')
        # # self.plot_lines.plot(poly2x, poly2y, color='black')
        #
        # return s1, s2







    #Returns the combo with the lowest deviation for every size
    def obtain_best_comb(self, lcombo, intersections):

        list_weight = []
        list_actual = []

        #THEIR LENGTH ARE THE NUMBER OF ROWS
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
                av = sum/total

                if list_weight[total - 1] > av:
                    list_weight[total - 1] = av
                    list_actual[total - 1] = combo
        return list_actual, list_weight


    #GENERAL IDEA, FIND ALL POSSIBLE COMBINATIONS, EVEN NOT EXISTANT, THEN FOR EVERY ELEMENT IN SEE IF THEIR REALTIVE HEIGHTS, HOLD UP
    #AND IF SO
    def make_all_possibilities(self, intersections, row, super_list):

        #IF PAST THE LAST ROW
        if row  == len(intersections):
            chain_sub_list.append(super_list)
            return

        #OTHERWISE
        new_row = row + 1


        #COMPARING ALL POSSIBLE ROWS
        for col_index, box in enumerate(intersections[row]):
            #IF USED ALREADY, OR INVLAID
            if box[0] != 1 or col_index in super_list:
                continue
            else:

                list = super_list.copy()
                list.append(col_index)
                self.make_all_possibilities(intersections, new_row, list)







        list = super_list.copy()
        list.append(-1)
        self.make_all_possibilities(intersections, new_row, list)


    #FIlters situations where COMBO HEIGHTS ARE IMPOSSIBLE
    def combo_filter_by_height(self, intersections, chain_list):

        updated = []

        for combo in chain_list:
            #print(f"{combo}---------------------------------------")


            #BASIC IDEA, TAKE INTERSECTION OF ALL RANGES, AND IF ITS ZERO BY END, IMPOSSIBLE

            current_intersection = (-10000, 10000)
            to_add = True
            for row, column in enumerate(combo):


                if column == -1 or intersections[row][column][0] != 1:
                    continue

                box = intersections[row][column]
                (max, av, min) = self.maximum_minimum_difference_between_points(box[7], box[8])

                current_intersection = self.get_intersection( current_intersection[0], current_intersection[1], min, max)
                #print("GETTING")

                if current_intersection == None:
                    to_add = False
                    break;

            if to_add:

                #print(f"CI: {combo}")
                updated.append(combo)

        return updated


    #Intersection between heights
    def get_intersection(self, x1, x2, y1, y2):
        #print(f"GETTING RANGE        {round(x1,2)}  {round(x2,2)}     {round(y1,2)}  {round(y2,2)}")
        if x1 <= y2 and y1 <= x2:
            # Calculate the intersection
            a = max(x1, y1)
            b = min(x2, y2)
            #print(f"OVERLAP    {a}   {b} ")
            return (a, b)
        else:
            # No intersection
            return None






    def visualize_hills_in_board(self, intersections):
        for ind_1, row in enumerate(intersections):

            a =  self.test.plot( (10*ind_1, 10*ind_1) , (-1, 1), color='grey')
            self.r_h.append(a)
            a = self.test2.plot((10*ind_1, 10*ind_1),  (-1, 1), color='grey')
            self.r_h.append(a)
            a =self.plot_chart.plot((10*ind_1, 10*ind_1) , (-1, 1), color='grey')
            self.r_h.append(a)

            for ind_2, point in enumerate(row):
                pos_x = (ind_1*10 + 1.4*ind_2)
                if point[0] == 1:


                    probability = 1 / self.obtain_how_many_in_row_column(intersections, ind_1, ind_2)

                    prob_1 = 1/ self.num_row(intersections, ind_1)
                    prob_2 = 1/self.num_column(intersections, ind_2)



                    a =self.test.plot(pos_x, probability, color='black', marker='o')
                    self.r_h.append(a)
                    a =self.test.plot(pos_x, prob_1, color='red', marker='o')
                    self.r_h.append(a)



                    a =self.test.plot(pos_x, point[7][0], color='lightblue', marker='o')
                    self.r_h.append(a)
                    a =self.test.plot(pos_x, point[7][1], color='blue', marker='o')
                    self.r_h.append(a)
                    a =self.test.plot(pos_x, point[7][2], color='grey', marker='o')
                    self.r_h.append(a)

                    #F2
                    a =self.test2.plot(pos_x, probability, color='black', marker='o')
                    self.r_h.append(a)


                    a =self.test2.plot(pos_x, point[8][0], color='lightblue', marker='o')
                    self.r_h.append(a)
                    a =self.test2.plot(pos_x, point[8][1], color='blue', marker='o')
                    self.r_h.append(a)
                    a =self.test2.plot(pos_x, point[8][2], color='grey', marker='o')
                    self.r_h.append(a)


                    a =self.test2.plot(pos_x, prob_2, color='red', marker='o')
                    self.r_h.append(a)





                    # self.plot_chart.plot((pos_x - 0.02, pos_x - 0.02, pos_x - 0.02), (point[7][0], point[7][1], point[7][2]), color='black', marker="o")
                    # self.plot_chart.plot((pos_x + 0.02, pos_x + 0.02, pos_x + 0.02), (point[8][0], point[8][1], point[8][2]), color='red', marker="o")
                    #

                    a =self.plot_chart.plot(pos_x, probability, color='black', marker='o')
                    self.r_h.append(a)

                    (max, av, min) = self.maximum_minimum_difference_between_points(point[7], point[8])

                    #print(f"MAX: {max}   MIN: {min}                {point[7]}  {point[8]}")

                    a =self.plot_chart.plot((pos_x, pos_x, pos_x),
                                         (max, av, min), color='purple', marker="o")
                    self.r_h.append(a)


    def maximum_minimum_difference_between_points(self, p1, p2):
        pot1 = p1[0] - p2[2]
        pot2 = p1[2] - p2[0]
        av = p1[1] - p2[1]

        return (pot1, av, pot2)


    #Number of intersections in EACH ROW/COLUMN
    def num_row(self, intersections, row):
        total_row = 0
        for box in intersections[row]:
            if box[0] == 1:
                total_row = total_row + 1
        return total_row

    def num_column(self, intersections, column):
        total_column = 0
        for row in range(0, len(intersections)):
            if intersections[row][column][0] == 1:
                total_column = total_column + 1
        return total_column



    #Obtains number of possible to get PROBABILITY OF THIS BEING RIGHT
    def obtain_how_many_in_row_column(self, intersections, row, column):
        total_row = self.num_row(intersections, row)
        total_column = self.num_column(intersections, column)

        #print(f" RC: {row} {column}   {total_row} {total_column}")


        if total_row == 1 and total_column == 1:
            # assume this is a row that is filled (even if some arnt)
            possibilities = 1
        elif total_row == 1 or total_column == 1:
            possibilities = total_row * total_column #* marco_metric
        else:
            possibilities = 1 + (total_row - 1) * (total_column - 1) #* marco_metric

        return possibilities








    #Obtains the difference between 2 angles
    def difference_between_angles(self, a1, a2):
        if a1 > a2:
            c1 = min(a1 - a2, abs(360 - a1 + a2))
        else:
            c1 = min(a2 - a1, abs(360 - a2 + a1))
        return c1




    #VISUALIZES THE INTERSECTIONS WITHIN LINES (COLOR DEPENDING)
    def visualize_intersections(self, intersections):

        for index_1, single_1 in enumerate(intersections):

            for index_2, box in enumerate(intersections[index_1]):

                if box[0] == 0 or box[0] == -1:
                    continue

                if box[0] == 4:
                    color="red"
                elif box[0] == 2:
                    color="orange"
                else:
                    color="green"


                # if (index_1 == 0 and index_2 == 0) or \
                #         (index_1 == 1 and index_2 == 3) or \
                #     (index_1 == 2 and index_2 == 2) or \
                #     (index_1 == 3 and index_2 == 4) or \
                #     (index_1 == 4 and index_2 == 1):
                #     color='blue'
                #     a = self.plot_lines.plot(box[1][0], box[1][1], marker="o", color=color)
                #     self.r_i.append(a)





                a = self.plot_lines.plot(box[1][0], box[1][1], marker="o", color=color)
                self.r_i.append(a)



    #Manual Correctness for a position
    def obtain_in_a_is_n_th(self, inter, num, val):

        max_row = self.test_max_count(inter)
        if max_row == 0:
            return False
        else:
            if inter[max_row - 1][num] == val:
                return True
            else:
                return False;







    #VISUALIZES HILLS
    def visualize_hills(self, intersections):
        minx = 1000
        maxx = -1000
        miny = 1000
        maxy = -1000
        for index_1, single_1 in enumerate(intersections):

            for index_2, box in enumerate(single_1):
                if not box[0] == 1:
                    continue



                # if bigger then current y max
                if box[1][1] > maxy:
                    maxy = box[1][1]
                # if less then current y min
                if box[1][1] < miny:
                    miny = box[1][1]

                # if more then current x max
                if box[1][0] > maxx:
                    maxx = box[1][0]
                # if less then current x min
                if box[1][0] < minx:
                    minx = box[1][0]
        if minx != maxx:
            self.hills.set_xlim(minx, maxx)
        else:
            self.hills.set_xlim(minx, minx + 10)
        if miny != maxy:
            self.hills.set_ylim(miny, maxy)
        else:
            self.hills.set_ylim(miny, miny + 10)

        colormap = colors.LinearSegmentedColormap.from_list('f1_map', [(0, 'red'), (1, 'green')])
        cmap = plt.cm.get_cmap('RdYlGn', 20)

        for index_1, single_1 in enumerate(intersections):

            for index_2, box in enumerate(single_1):

                if box[0] == 1:
                    # Visualize the max, p1 is relative to camera
                    # self.hills.plot((box[1][0] - 0.02, box[1][0] - 0.02), (box[1][1], box[1][1]), (box[7][0], 0), linewidth='5',
                    #                 color="black")
                    #
                    # # Visualize the min, p1 is relative to camera
                    # self.hills.plot((box[1][0] - 0.02, box[1][0] - 0.02), (box[1][1], box[1][1]), (box[7][2], 0), linewidth='5',
                    #                 color="grey")
                    #
                    # # Visualize the max, p2 is from the camera
                    # self.hills.plot((box[1][0] + 0.02, box[1][0] + 0.02), (box[1][1], box[1][1]), (box[8][0], 0), linewidth='5',
                    #                 color="red")
                    #
                    # # Visualize the min, p2 is from the camera
                    # self.hills.plot((box[1][0] + 0.02, box[1][0] + 0.02), (box[1][1], box[1][1]), (box[8][2], 0), linewidth='5',
                    #                color="orange")

                    # Visualize the maximum and minimum difference
                    #print(f"INTERSECTION   {index_1}  {index_2}")
                    max_diff, av, min_diff = self.maximum_minimum_difference_between_points(box[7], box[8])

                    size = abs(max_diff - min_diff)/20


                    # self.hills.plot((box[1][0], box[1][0]), (box[1][1] + 0.02, box[1][1] + 0.02), (max_diff, 0),
                    #                 linewidth='5', color='lightblue')
                    # self.hills.plot((box[1][0], box[1][0]), (box[1][1] - 0.02, box[1][1] - 0.02), (min_diff, 0),
                    #                 linewidth='5', color='blue')


                    self.hills.plot((box[1][0], box[1][0]), (box[1][1] - 0.02, box[1][1] - 0.02), (box[7][1], 0), color="blue")
                    self.hills.plot((box[1][0], box[1][0]), (box[1][1] + 0.02, box[1][1] + 0.02), (box[8][1], 0), color="yellow")





                    self.hills.plot((box[1][0], box[1][0]), (box[1][1], box[1][1]), (av, 0),
                                    linewidth='5', color=self.color_relative_to_zero(av))

                    x, y = Point(box[1][0], box[1][1]).buffer(size).exterior.xy
                    self.hills.plot(x,y, color="grey")



    #VISUALIZES CHECKER
    def visualize_checker(self, intersections):
        # - PERMENTENT --------------------------------------------------------------

        for row in range(0, len(intersections)):

            possible = self.num_row(intersections, row)



        for column in range(0, len(intersections[0])):

            possible = self.num_column(intersections, column)









        for index_1, row in enumerate(intersections):

            for index_2, box in enumerate(row):

                if box[0] == -1 or box[0] == 0:
                    continue


                if box[0] == 1:
                    a = self.board.fill( (index_2*10 + 5, index_2*10 + 5, index_2*10 - 5, index_2*10 - 5),
                                     (index_1*-10 - 5, index_1*-10 + 5, index_1*-10 + 5, index_1*-10 - 5), color='green', alpha=0.5)
                    self.r_b.append(a)



                reference_square = Polygon(
                    [(index_2 * 10 - 2, index_1 * -10 - 2), (index_2 * 10 - 2, index_1 * -10 + 2),
                     (index_2 * 10 + 2, index_1 * -10 + 2), (index_2 * 10 + 2, index_1 * -10 - 2)])

                # MEANING 1 IS MORE THEN 2
                if box[6] >= 1:
                    inverse = 1 / box[6]

                    color = "black"
                else:
                    inverse = box[6]
                    color = "grey"


                relative = Polygon([
                    (index_2 * 10 - 2, index_1 * -10 - 2), (index_2 * 10 - 2, index_1 * -10 - 2 + inverse * 4),
                    (index_2 * 10 + 2, index_1 * -10 - 2 + inverse * 4), (index_2 * 10 + 2, index_1 * -10 - 2)])
                # MEANING 2 IS MORE
                x, y = reference_square.exterior.xy
                a, b = relative.exterior.xy

                c = self.board.plot(x, y, color="black")
                self.r_b.append(c)
                c = self.board.fill(a, b, color=color)
                self.r_b.append(c)


                #WIDTHS: (TOP LEFT) (3)

                if box[10][0] == 1:
                    color="red"
                else:
                    color="green"

                a = self.board.plot(index_2 * 10 - 3, index_1 * -10 + 3, marker="o", color=color)
                self.r_b.append(a)

                #BASE 1:  (5)---    6, 6+3, 6+7,
                if box[10][1] == 1:
                    color="red"
                else:
                    color="green"

                a = self.board.plot(index_2 * 10 - 1, index_1 * -10 + 3, marker="o", color=color)
                self.r_b.append(a)


                if box[10][2] == 1:
                    color="red"
                else:
                    color="green"

                a = self.board.plot(index_2 * 10 +1 , index_1 * -10 + 3, marker="o", color=color)
                self.r_b.append(a)

    #VISUALIZES STOCK
    def visualize_stock(self,index, intersections):

        for index_1, single_1 in enumerate(intersections):

            for index_2, box in enumerate(intersections[index_1]):

                no_match = 0
                black_list = 0

                #ALL-------------------------
                tier1_matchs = 0
                tier_1_total_width_1 = 0
                tier_1_total_width_2 = 0
                tier1_overall_ratio = 1

                #AFTER BASE ------------------
                tier2_matchs = 0
                tier_2_total_width_1 = 0
                tier_2_total_width_2 = 0
                tier_2_overall_ratio = 1

                #AFTER WIDTH COMPARISON ----------
                tier3_matchs = 0
                tier_3_total_width_1 = 0
                tier_3_total_width_2 = 0
                tier_3_overall_ratio = 1


                #NO Matches
                if box[0] == 0:
                    no_match+=1
                #BlackListed
                elif box[0] == -1:
                    black_list+=1
                #Matches
                else:
                    tier1_matchs+=1
                    tier_1_total_width_1+=box[4]
                    tier_1_total_width_2+=box[5]
                    tier1_overall_ratio+=((box[4] + box[5])/2)

                    if not box[0] == 2 or box[0] == 3:
                        tier2_matchs += 1
                        tier_2_total_width_1 += box[4]
                        tier_2_total_width_2 += box[5]
                        tier_2_overall_ratio += ((box[4] + box[5]) / 2)











        self.waves.plot(index,self.solve_attempt_macros[0], marker="o")         #total width1
        self.waves.plot(index, self.solve_attempt_macros[1], marker = "o")      #total width2
        self.waves.plot(index, self.solve_attempt_macros[2], marker = "o")
        self.waves.plot(index, self.solve_attempt_macros[3], marker = "o")
        self.waves.plot(index, self.solve_attempt_macros[4], marker = "o")

        # IF 0, ELSE USE HEIGHT


    def unvisualize(self):
        for a in self.r_b:
            for b in a:
                b.remove()

        for a in self.r_h:
            for b in a:
                b.remove()

        for a in self.r_i:
            for b in a:
                b.remove()

        self.r_b = []
        self.r_i = []
        self.r_h = []





    def color_relative_to_zero(self, val):
        if val >= 0:
            return "green"
        else:
            return "red"

    #BASIC HELPER --------------------------------------------------------------------------




    #USED TO FRAME HILLS
    def get_furthest_closest_match(self, look_in, transpose, column):

        max = 0
        min = 1000

        if not transpose:

            for index in look_in:

                # if index[0] == -1 or index[0] == 0:
                #     continue
                #
                if index[0] == -1 or index[0] == 0:
                    continue

                #New furthest
                if index[2] > max:
                    max = index[2]

                if index[2] < min:
                    min = index[2]

            return max, min
        else:

            for x in range(0, len(look_in)):

                actual = look_in[x][column]

                if actual[0] == -1 or actual[0] == 0:
                    continue

                #New furthest
                if actual[2] > max:
                    max = actual[2]

                if actual[2] < min:
                    min = actual[2]
            return max, min


    @staticmethod
    def distance(xy1, xy2):
        return math.sqrt( (xy1[0] - xy2[0])**2 + (xy1[1] -xy2[1])**2 )


    #PERMANANT STUFF
    def solve_system_permanant_components(self, final_circle):
        # Ploting circle ranges and 0 circles
        x, y = final_circle.exterior.xy
        # (0,0), BOUND
        self.plot_perspective.plot(x, y)
        self.plot_perspective.plot(0, 0, marker="o", color="black")

        #---------------------------------------------------
        self.hills.plot(x,y)
        self.hills.plot(0,0, marker="o", color="black")
        #----------------------------------------------------


        # (0,1) BOUND + REFERENCE
        self.plot_lines.plot(x, y)
        self.plot_lines.plot(0, 0, marker="o", color="black")






        # -------------------------------------------------------------


        # --------- SETTING CIRCLES
        self.plot_dots.set_xlim(-10, 10 * len(self.frame2.fragments))
        self.plot_dots.set_ylim(-10 * len(self.frame1.fragments), 10)
        self.plot_dots.set_xlabel("nth frame 2")
        self.plot_dots.set_ylabel("nth frame 1")

        for one_y, f1 in enumerate(self.frame1.fragments):

            for one_x, f2 in enumerate(self.frame2.fragments):
                z = (one_x * 10, one_y * -10)

                m2, b2 = f2.half_bowl_angle(True)
                m1, b1 = f1.half_bowl_angle(True)



                #OVERALL (BIGGEST)
                l1 = LineString([z, self.frame1.move_random_along_angle(f1.half_angle(f1.s_o, f1.base_dir), 3, z)])
                x, y = l1.xy
                self.plot_dots.plot(x, y, color="black", linewidth=2)

                l1 = LineString([z, self.frame1.move_random_along_angle(f1.half_angle(f1.s_l, f1.base_dir), 2, z)])
                x, y = l1.xy
                self.plot_dots.plot(x, y, color="grey", linewidth=2.5)

                l1 = LineString([z, self.frame1.move_random_along_angle(f1.half_angle(f1.s_u, f1.base_dir), 1, z)])
                x, y = l1.xy
                self.plot_dots.plot(x, y, color="black", linewidth=3)




                #CAMERA
                l2 = LineString([z, self.frame1.move_random_along_angle((f1.base_dir + 180) % 360, 5, z)])
                x, y = l2.xy
                self.plot_dots.plot(x, y, color="black", linewidth=2.5)








                l3 = LineString([z, self.frame1.move_random_along_angle(f2.half_angle(f2.s_o, f2.base_dir), 3, z)])
                x, y = l3.xy
                self.plot_dots.plot(x, y, color="red", linewidth = 2)

                l3 = LineString([z, self.frame1.move_random_along_angle(f2.half_angle(f2.s_l, f2.base_dir), 2, z)])
                x, y = l3.xy
                self.plot_dots.plot(x, y, color="orange", linewidth=2.5)

                l3 = LineString([z, self.frame1.move_random_along_angle(f2.half_angle(f2.s_u, f2.base_dir), 1, z)])
                x, y = l3.xy
                self.plot_dots.plot(x, y, color="red", linewidth=3)



                #CAMERA DIR
                l4 = LineString([z, self.frame1.move_random_along_angle((f2.base_dir + 180) % 360, 5, z)])
                x, y = l4.xy
                self.plot_dots.plot(x, y, color="red", linewidth=2.5)





                if self.system_blacklist[one_y][one_x] == 0:
                    color="red"
                else:
                    color="green"


                #PERMANENT CIRLCES
                self.plot_dots.plot(10 * one_x, -10 * one_y, marker="o", color=color, )



        max1 = -10 * len(self.frame1.fragments) + 5
        max2 = 10 * len(self.frame2.fragments) - 5

        self.board.set_xlabel("2 Going --> Clockwise")
        self.board.set_ylabel("1 Going <-- Clockwise")
        self.board.set_title("LEFT IS STRAIGHT (g/b)    RIGHT IS SLOPES (g/b/r")

        self.board.set_xlim(-15, max2 + 10)
        self.board.set_ylim(max1 - 10, 15)

        # VERTICAL (SO FLAT LINES)
        for one_y, f1 in enumerate(self.frame1.fragments):
            # LINES
            self.board.plot((-5, max2), (-10 * one_y - 5, -10 * one_y - 5), color="black", linewidth=0.5)


            # COLOURED SEGMENT
            self.board.plot((-5, -5), (-10 * one_y + 5, -10 * one_y - 5),
                            color=self.frame1_cmap(one_y / len(self.frame1.fragments)), linewidth=2.5)

            self.waves.plot((-5, max2), (-10 * one_y - 5, -10 * one_y - 5), color="black", linewidth=0.5)

            # COLOURED SEGMENT
            self.waves.plot((-5, -5), (-10 * one_y + 5, -10 * one_y - 5),
                            color=self.frame1_cmap(one_y / len(self.frame1.fragments)), linewidth=2.5)







            self.board.plot(-10 - 2, -10 * one_y, color=f1.convert_to_color(f1.angle_straight), marker="o")




            #self.board.plot(-10 + 2, -10 * one_y, color=f1.convert_to_color(f1.angle_consistant), marker="o")

            self.board.plot(-10 + 1, -10 * one_y, color=f1.convert_to_color(f1.s_o), marker="o")

            self.board.plot(-10 + 2, -10 * one_y + 1, color=f1.convert_to_color(f1.s_u), marker="o")
            self.board.plot(-10 + 2, -10 * one_y - 1, color=f1.convert_to_color(f1.s_l), marker="o")






        # HORIZONTAL (SO V LINES)
        for one_x, f2 in enumerate(self.frame2.fragments):
            # LINES
            self.board.plot((10 * one_x + 5, 10 * one_x + 5), (5, max1), color="black", linewidth=0.5)
            # COLOURED SEGMENT
            self.board.plot((10 * one_x - 5, 10 * one_x + 5), (5, 5),
                            color=self.frame2_cmap(one_x / len(self.frame2.fragments)), linewidth=2.5)

            self.waves.plot((10 * one_x + 5, 10 * one_x + 5), (5, max1), color="black", linewidth=0.5)
            # COLOURED SEGMENT
            self.waves.plot((10 * one_x - 5, 10 * one_x + 5), (5, 5),
                            color=self.frame2_cmap(one_x / len(self.frame2.fragments)), linewidth=2.5)


            self.board.plot(one_x * 10 - 2, 10, marker="o", color=f2.convert_to_color(f2.angle_straight))


            self.board.plot(one_x * 10 + 1, 10, marker="o", color=f2.convert_to_color(f2.s_o))

            self.board.plot(one_x * 10 + 2, 10 + 1, marker="o", color=f2.convert_to_color(f2.s_u))
            self.board.plot(one_x * 10 + 2, 10 - 1, marker="o", color=f2.convert_to_color(f2.s_l))




        self.frame1.make_set_line_segments((0, 0), 0, True)
        self.plot_lines.set_xlim(-20, 20)
        self.plot_lines.set_ylim(-20, 20)
        for index, ls in enumerate(self.frame1.fragments):
            x, y = ls.current_line_segment.xy

            self.hills.plot(x, y, color=self.frame1_cmap(index / len(self.frame1.fragments)))

            self.plot_lines.plot(x, y, color=self.frame1_cmap(index / len(self.frame1.fragments)))



        for index1, row1 in enumerate(self.system_blacklist):

            for index2, box in enumerate(self.system_blacklist[index1]):

                #MEANS BLACKLISTED
                if box == 0:

                    #UP
                    x1 = ( index2*10 -5, index2*10 + 5)
                    y1 = (index1*-10 - 5, index1*-10 + 5)

                    #DOWN
                    x2 = (index2 * 10 + 5, index2 * 10 - 5)
                    y2 = (index1 * -10 - 5, index1 * -10 + 5)

                    self.board.plot(x1, y1, color="black")
                    self.board.plot(x2, y2, color="black")





    def deg(self, degree):
        return (360 - degree + 90) % 360

    def direction(self, p1, p2):
        x_d = p2[0] - p1[0]
        y_d = p2[1] - p1[1]
        return self.deg(math.degrees(math.atan2(y_d, x_d))), math.sqrt(x_d**2 + y_d**2)

