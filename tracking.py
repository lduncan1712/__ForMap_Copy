from shapely.geometry import Point, Polygon
import math
import one_directory
import three_image_det
from five_database import five_database
from tracker_object import tracker_object


class tracker:

    def __init__(self):

        # List of Trees
        self.list = []



    def obtain_indexs_of_overlap(self, colors):
        list_of_overlaps = []

        for index, color in enumerate(colors):
            for inner_index, inner_color in enumerate(colors):
                if index < inner_index:
                    if self.compare_color(color, inner_color):
                        val = [index, inner_index]
                        list_of_overlaps.append(val)


    #REMOVE ALL COLORS INDEXS BEFORE (USING KNOWLEDGE OF SAME)





    def omni_clean_list_for_duplicates(self, colors, points, boxes):
        list_of_colors = []
        list_of_indexs = []

        for index, color in enumerate(colors):

            used = False

            for inner_index, inner_color in enumerate(list_of_colors):
                if self.compare_color(color, inner_color):
                    used = True
                    list_of_indexs[inner_index].append(index)
                    break
            if used == False:
                list_of_indexs.append([index])
                list_of_colors.append(color)


        all_unique = True

        for list_of_ind in list_of_indexs:
            if len(list_of_ind) != 1:
                all_unique = False
                break


        if all_unique:
            return points, colors, boxes

        else:
            list_of_indexs_to_return = []
            list_of_colors_to_return = list_of_colors
            list_of_boxes_to_return = []
            for indexs_maybe_plur in list_of_indexs:

                if len(indexs_maybe_plur) > 1:
                    #CHOOSE THE CLOESTED ONE

                    smallest_distance_pixels = 10000
                    smallest_index = -1.5

                    tree = self.omni_obtain_tree_with_given_color(colors[indexs_maybe_plur[0]])
                    last_points = self.obtain_last_point_set_of_tree(tree)

                    for index in indexs_maybe_plur:

                        points_to_compare = points[index]

                        dist = self.obtain_distance_from(last_points, points_to_compare)

                        if dist < smallest_distance_pixels:
                            smallest_distance_pixels = dist
                            smallest_index = index


                    list_of_indexs_to_return.append(points[smallest_index])
                    list_of_boxes_to_return.append(boxes[smallest_index])

                else:
                    list_of_indexs_to_return.append(points[indexs_maybe_plur[0]])
                    list_of_boxes_to_return.append(boxes[indexs_maybe_plur[0]])

            return list_of_indexs_to_return, list_of_colors_to_return, list_of_boxes_to_return



    def obtain_distance_from(self, set1, set2):

        return abs(set1[0][0] - set2[0][0]) + \
                abs(set1[1][0] - set2[1][0]) + \
                abs(set1[2][0] - set2[2][0]) + \
                abs(set1[3][0] - set2[3][0]) + \
                abs(set1[4][0] - set2[4][0])




    def obtain_last_point_set_of_tree(self, tree):
        for reversed_index in range(0, len(tree.list_of_points)):
            value = -1 - reversed_index
            if isinstance(tree.list_of_points[value], int):
                continue
            else:
                return tree.list_of_points[value]



    def omni_obtain_tree_with_given_color(self,color):

        for tree in self.list:
            if self.compare_color(tree.color, color):
                return tree









    def omni_update_list_with_overlap(self, points, boxes, colors, main, vid_vis, overlapping_indexs):
        print("S")


    #WHEN MAIN...COLORS DONT EXIST
    def omni_update_list(self, points, boxes, colors, main, vid_vis):



        list_of_previous_indexs = []
        for index in range(0, len(self.list)):
            index_index = len(self.list) - 1 - index
            list_of_previous_indexs.append(index_index)
        #print(list_of_previous_indexs)

        list_of_current_indexs = []
        for index in range(0, len(points)):
            index_index = len(points) - 1 - index
            list_of_current_indexs.append(index_index)
        #print(list_of_current_indexs)

        #Match ALL CURRENT WITH PREVIOUS (IF NONE -- ALL NEW)
        for current_index in range(0, len(points)):
            if colors == None:
                break
            color_of_this_index = colors[current_index]


            for previous_index, tree in enumerate(self.list):
                if self.compare_color(color_of_this_index, tree.color):

                    tree.update(points[current_index], boxes[current_index], main)
                    #print(f" REMOVING: P: {previous_index} {str(tree.color)} C: {current_index} {str(color_of_this_index)}")
                    list_of_current_indexs.remove(current_index)
                    list_of_previous_indexs.remove(previous_index)

                    print(f"  COL: {tree.color} CONTINUED")

                    #PROBLEM OCCURS WHEN COLOR MATCHS MULTIPLE TIMES
                    #(HENCE REMOVED) BUT THEN ATTEMPTED TO BE REMOVED AGAIN)
                    break



        #FROM HERE, ADD FAIL TO ALL PREVIOUS NOT ENCOUNTERED
        for previous_failed_index in list_of_previous_indexs:
            print(f" PREV {self.list[previous_failed_index].color} FAIL")
            value = self.list[previous_failed_index].update_by_exclusion(main)
            if value == False:
                #print(f"REMOVE7  {self.list[previous_failed_index].color}")
                vid_vis.remove_value(self.list[previous_failed_index].color)
                #print(f" PRELEN = {len(self.list)}")
                self.list.remove(self.list[previous_failed_index])
                #print(f" POSTLEN = {len(self.list)}")
                #print("REMOVE7")



        #FROM HERE, ADD NEW TO ALL CURRENT NOT ENCOUNTERED
        for current_failed_index in list_of_current_indexs:
            print(f" NEW {colors[current_failed_index]} ADDED")

            to = tracker_object(colors[current_failed_index], points[current_failed_index],
                                boxes[current_failed_index], main)
            self.list.append(to)


    def confirm_uniqueness(self, colors_sorted_left_right):
        for outer_index, outer_object in enumerate(self.list):
            for inner_index, inner_object in enumerate(self.list):
                if outer_index > inner_index:
                    if self.compare_color(outer_object.color, inner_object.color):
                        print("OVERLAP ZZZ")
                        print(colors_sorted_left_right)



    #IDEA RETURNS ALL POINTS, AND SEPERATE LIST (SORTED) of COLORS OF FRAMES
    def obtain_main_trees(self):

        list_of_points = []
        list_of_boxes = []
        list_of_colors = []

        #print(f" LEN OF LIST {len(self.list)}")
        #Adds Relevant Points
        for tree in self.list:
            #print(str(tree))

            #CONVERT TO ALSO RETURN BOXES
            val_or_none, box_or_none = tree.major_assessment()

            if val_or_none == False:
                #print("TREE FAILED")
                continue
            else:
                #print("TREE SUCCEEDED")
                #ADD BOXES
                list_of_points.append(val_or_none)
                list_of_colors.append(tree.color)
                list_of_boxes.append(box_or_none)

        #Sorts by left right
        sorted_points, sorted_boxs, sorted_colors = self.sort_by_left_right(list_of_points, list_of_boxes, list_of_colors)

        return sorted_points, sorted_boxs, sorted_colors


    def sort_by_left_right(self, list1, list2, list3):
        # INDEX
        sorted_index = sorted(range(len(list1)), key=lambda k: list1[k][0][0])

        sorted_list1 = [list1[i] for i in sorted_index]
        sorted_list2 = [list2[i] for i in sorted_index]
        sorted_list3 = [list3[i] for i in sorted_index]

        return sorted_list1, sorted_list2, sorted_list3








    @staticmethod
    def compare_color(color1, color2):
        return color1[0] == color2[0] and color1[1] == color2[1] and color1[2] == color2[2]

    def compare_color(self, color1, color2):
        return color1[0] == color2[0] and color1[1] == color2[1] and color1[2] == color2[2]

    #Create A List Whose Indexs are trees in previous
    # Assigning Colors Accordingly
    #Assign A Threshold
    def omni_create_major(self, points, boxs, colors):
        print("A")






    #Changes Values In New Order
    def omni_update_major(self):
        print("B")

    #Used After Match Minor
    def omni_match_major(self):
        print("C")

    #Updates Tree Locations And Stuff
    def omni_match_minor(self):
        print("D")



























    def compare(self, point_lists, bounding_boxs):

        print("GGG")





    #SHRINK ALL POINTS TO ACCORDANCE
    def convert_points(self, tree_points):
        for y in range(0, len(tree_points)):
            for x in range(0, 5):
                tree_points[y][x][0] /= one_directory.ratio_of_pixels
                tree_points[y][x][1] /= one_directory.ratio_of_pixels

        return tree_points

    #SHRINKS ALL BOXES TO ACCORDANCE
    def convert_boxes(self, borders):
        #print(borders)

        for y in range(0, len(borders)):
            for x in range(0, 4):
                borders[y][x] /= one_directory.ratio_of_pixels

        return borders

    #CREATES FIRST MAJOR (NO IMPACT FROM PREVIOUS)
    def create_major(self, point_lists, bounding_boxs):

        #HOLDS POINTS OF PREVIOUS TRACKED
        self.list = []
        self.peaks = []

        #HOLDS INFORMATION ABOUT WHICH IT INTERSECTED
        self.appearance = []
        self.disapearance = []

        #HOLDS INFORMATION ABOUT BASE POINTS (TO TRACK CHANGE)
        self.base_points = []

        self.starting_length = len(point_lists)


        for index, lop in enumerate(point_lists):

            #ADDS POINTS TO LIST
            self.list.append(lop)
            #ADDS UPDATED PEAK
            self.peaks.append(bounding_boxs[index][3])

            #ADDS DIRECTION (FOR LATER)
            self.base_points.append([[(lop[1][0], lop[2][0])]])
            self.base_points[index].append([])

            self.appearance.append(-1)
            self.disapearance.append(-1)





    #CREATES A NEXT MAJOR, (REQUIRES A DICTIONARY OF OVERLAP)
    def create_subsequent_major(self, points_list, bounding_boxes, dictionary, searchable):

        # print("DICTIONARY")
        # print(dictionary)
        # print(points_list)
        #
        # print("OLD MAJOR-----------------")
        # print(self.list)
        # print(self.appearance)
        #CREATE MAJOR AS NORMAL, THEN SIMPLY CHANGE THE APPEARANCE, AND POINTS FIELDS
        stored_appearance = self.appearance
        stored_points = self.base_points

        self.create_major(points_list, bounding_boxes)


        for match in dictionary:


            if stored_appearance[match[0]] != -1:
                self.appearance[match[1]] = searchable[stored_appearance[match[0]]]

            self.base_points[match[1]] = stored_points[match[0]]
            self.base_points[match[1]].append([])

        # print("NEW MAJOR-----------------")
        # print(self.list)
        # print(self.appearance)



    #DEAL WITH PERSPECTIVES (not required
    # def create_major_perspective(self, current_photo, searchable_matchs):
    #
    #     #REMOVES REFERENCES MADE TO POINTS THAT STARTED AND ENDED
    #     for stored_id, stored in enumerate(self.list):
    #
    #         # Ended, and existed within only
    #         if len(stored) == 1 and len(self.base_points[stored_id]) == 1:
    #             # Since No Meaning Can Be Obtained From This, Remove All References To It
    #             for index, start in enumerate(self.appearance):
    #                 if start == stored_id:
    #                     self.appearance[index] == -1
    #             for index, end in enumerate(self.disapearance):
    #                 if start == stored_id:
    #                     self.disapearance[index] == -1
    #
    #
    #
    #             #This Doesnt Need To Carry Forward
    #
    #         #Ended, and existed before
    #
    #
    #     #LATER WILL REMOVE REFERENCES TO FRAMES THAT DISAPEAR THIS TURN
    #
    #     #print(searchable_matchs)
    #
    #     #FOR EVERY TREE
    #     for stored_id, stored in enumerate(self.list):
    #         #ITS APPEARANCE ID
    #         came_before = self.appearance[stored_id]
    #
    #         #IF ALIVE AND NO PREVIOUS, DO NOTHING
    #         if came_before == -1 and len(stored) != 1:
    #             #print("CASE 2")
    #             continue
    #
    #         #IF JUST DIED AND NO DISAPEARANCE, DO NOTHING
    #         if self.disapearance[stored_id] == -1 and len(stored) == 1:
    #             #print("CASE 3")
    #             continue
    #
    #
    #
    #         #CURRENTLY EXISTS
    #         if len(stored) != 1:
    #             #KNOW PREVIOUS STILL CURRENTLY EXISTS
    #             if len(self.list[came_before]) != 1:
    #
    #                 # AT THIS POINT, I KNOW CURRENT EXISTS
    #                 # AT THIS POINT, I KNOW PREVIOUS EXISTS (NOT -1)
    #
    #                 f1_points = self.base_points[stored_id]
    #                 f2_points = self.base_points[came_before]
    #
    #                 f1_final_index = len(f1_points) - 1
    #                 f2_final_index = len(f2_points) - 1
    #
    #                 # F1 STARTS, F2 STARTS:
    #                 if len(self.base_points[stored_id]) == 1 and len(self.base_points[came_before]) == 1:
    #
    #                     val = self.determine_continuance_forward(f1_points[f1_final_index],
    #                                                              f2_points[f2_final_index],
    #                                                              None,
    #                                                              None,
    #                                                              one_directory.pixels_in_ninety)
    #
    #
    #
    #                 # F1 START, F2 DOESNT START
    #                 elif len(self.base_points[stored_id]) == 1 and len(self.base_points[came_before]) != 1:
    #
    #                     val = self.determine_continuance_forward(f1_points[f1_final_index],
    #                                                              f2_points[f2_final_index],
    #                                                              None,
    #                                                              f2_points[f2_final_index - 1][
    #                                                                  len(f2_points[f2_final_index - 1]) - 1],
    #                                                              one_directory.pixels_in_ninety)
    #
    #
    #
    #
    #                 # F1 DOESNT START, F2 DOESNT START
    #                 elif len(self.base_points[stored_id]) != 1 and len(self.base_points[came_before]) != 1:
    #
    #                     val = self.determine_continuance_forward(f1_points[f1_final_index],
    #                                                              f2_points[f2_final_index],
    #                                                              f1_points[f1_final_index - 1][
    #                                                                  len(f1_points[f1_final_index - 1]) - 1],
    #                                                              f2_points[f2_final_index - 1][
    #                                                                  len(f2_points[f2_final_index - 1]) - 1],
    #                                                              one_directory.pixels_in_ninety)
    #                 # IMPOSSIBLE????
    #                 else:
    #                     print("IMPOSSIBLLES")
    #
    #                 # MEANS NO LONGER CONTINUED
    #                 if val == False:
    #                     print(f"   {stored_id} DIDNT MAINTAIN POSITION")
    #
    #                     # CAN REMOVE THE APPEARANCE VALUE
    #                     self.list[stored_id] = -1
    #
    #                 else:
    #                     if searchable_matchs[came_before] == -1 or -1 == searchable_matchs[stored_id]:
    #                         print("NEGATIVE ONE CASE")
    #                         continue
    #
    #                     print(f"   {stored_id} DID MAINTAIN POSITION  SHOULD BE APPLYING")
    #
    #                     # UPLOAD AS NORMAL
    #                     print(
    #                         f" APPLY PREEE (INFRONTTTTTTTTTTTTTT)  {current_photo + one_directory.starting_id}    {searchable_matchs[came_before]}    {searchable_matchs[stored_id]}")
    #
    #                     five_database.apply_perspectives(current_photo + one_directory.starting_id,
    #                                                      searchable_matchs[came_before], searchable_matchs[stored_id])
    #
    #
    #
    #
    #             #PREVIOUS DOESNT EXIST
    #             else:
    #                 self.appearance[stored_id] = -1
    #                 #no conclusions
    #                 continue
    #
    #         #DOESNT CURRENTLY EXIST
    #         else:
    #
    #             #MEANS DISAPEARED BEHIND SOMETHING
    #             if self.disapearance[stored_id] != -1:
    #                 print("-----START---")
    #                 print(f" ATTEMPTING PERSEPCTIVE  {self.disapearance[stored_id]}   {stored_id}")
    #                 val = self.determine_continuance_backward(current_photo + one_directory.starting_id - 1,
    #                                                           self.disapearance[stored_id],
    #                                                           stored_id,
    #                                                           self.base_points[self.disapearance[stored_id]],
    #                                                           self.base_points[stored_id],
    #                                                           2000)
    #                 print("END---------")
    #
    #
    #
    #
    #
    #                 self.disapearance[stored_id] == -1
    #
    #
    #             #MEANS DISAPEARED OUT OF NOWHERE
    #             else:
    #                 #print("DOESNT CURRENTLY EXIST AND DISAPEARED BEHIND NOTHING")
    #                 continue
    #




    #DETERMINES FORWARD (CHECKS FOR ALWAYS INCREASING)
    def determine_continuance_forward(self, pl1, pl2, pp1, pp2, maximum):

        previous_width_min = 0
        previous_width_max = 0

        #Means Both Existed Before (LISTS ARE SAME LENGTH)
        if pp1 != None and pp2 != None:

            minn, maxx = self.angle_between_points(pp1, pp2)

            previous_width_min = minn
            previous_width_max = maxx

            #For Every Point
            for index in range(0, len(pl1)):

                value_min, value_max = self.angle_between_points(pl1[index], pl2[index])

                #TOO SMALL OF ANGLE,                OR        TOO LARGE
                if (value_max < previous_width_min) or (value_min > maximum):
                    return False
                else:
                    previous_width_max = value_max
                    previous_width_min = value_min

            return True

        #Means Both Appeared Within This Frame (LISTS LIKELY ARENT SAME LENGTH)
        elif pp1 == None and pp2 == None:

            smallest = min(len(pl1), len(pl2))
            difference = max(len(pl1), len(pl2)) - smallest

            #L1 IS LARGER
            if len(pl1) > len(pl2):

                for index in range(0, len(pl2)):

                    value_min, value_max = self.angle_between_points(pl1[index + difference], pl2[index])

                    if (value_max < previous_width_min) or (value_min > maximum):
                        return False
                    else:
                        previous_width_max = value_max
                        previous_width_min = value_min
                return True

            #L2 IS LARGER
            else:

                for index in range(0, len(pl1)):

                    value_min, value_max = self.angle_between_points(pl1[index], pl2[index + difference])

                    if (value_max < previous_width_min) or (value_min > maximum):
                        return False
                    else:
                        previous_width_max = value_max
                        previous_width_min = value_min
                return True

        #Means 1 Is New, P is older
        elif pp1 == None and pp2 != None:


            difference = len(pl2) - len(pl1)

            for index in range(0, len(pl1)):
                value_min, value_max = self.angle_between_points(pl1[index], pl2[index + difference])

                if (value_max < previous_width_min) or (value_min > maximum):
                    return False
                else:
                    previous_width_max = value_max
                    previous_width_min = value_min
            return True

        #Means 1 is OLD, 2 is NEW
        else:

            difference = len(pl1) - len(pl2)

            for index in range(0, len(pp2)):
                value_min, value_max = self.angle_between_points(pl1[index + difference], pl2[index])

                if (value_max < previous_width_min) or (value_min > maximum):
                    return False
                else:
                    previous_width_max = value_max
                    previous_width_min = value_min
            return True

    # DETERMINES BACKWARDS
    def determine_continuance_backward(self, photo_index, front_index, back_index, front_list, back_list, size):
        fdb = five_database()

        if len(front_list) == 1 or len(back_list) == 1:
            return False
        else:
            minimum_angle = 0
            current_index = photo_index

            f_len = len(front_list)
            b_len = len(back_list)

            overlapping_range = min(f_len, b_len)

            #INDEXES FROM LAST
            for super_index in range(1, overlapping_range):

                inner_f = front_list[-1*super_index]
                inner_b = back_list[-1*super_index]

                inner_overlap_length = min(len(inner_f), len(inner_b))

                for sub_index in range(1, inner_overlap_length):

                    inner_point_f = inner_f[-1*sub_index]
                    inner_point_b = inner_b[-1*sub_index]

                    pixel_min, pixel_max = self.angle_between_points(inner_point_f, inner_point_b)

                    #NEEDS TO BE INCREASING
                    if pixel_max < minimum_angle or pixel_min > size:
                        print("FAILED")
                        return False
                    else:
                        minimum_angle = pixel_min
                        print("PASSED")



                new_front_index = fdb.get_tree_later_multiple(photo_index, front_index, current_index)
                new_back_index = fdb.get_tree_later_multiple(photo_index, back_index, current_index)



                exists = fdb.check_for_perspectives(current_index, new_front_index, new_back_index)
                if not exists:
                    print(f"APPLYING (PREEEEEEEEEEEEEEEEEE) {current_index} {new_front_index} {new_back_index}")
                    five_database.apply_perspectives(current_index, new_front_index, new_back_index)
                current_index -= 1









    #Returns the x_pixels between p1, p2
    def angle_between_points(self, p1, p2):
        #Want the largest possible angle between

        x_diff_max = max( abs(p1[0] - p2[1]), abs(p2[0] - p1[1]))


        x_diff_min = min(abs(p1[0] - p2[1]), abs(p2[0]) - abs(p1[1]))

        return x_diff_min, x_diff_max

    #COMPARES MINOR

    #Updates:
        #Tolerance For Temporary Lack Of Detection
        #Updated VM Matching
        #Idea That Cant Disapear For No Reason Unless Near Edge
    def updated_compare_minor(self, points_lists, bounding_boxs):
        print("ZA")



    def compare_minor(self, points_lists, bounding_boxs):
        #List of indexes that intersect with indexed previous/current
        previous_intersection = []
        current_intersection = []
        #LIST OF ALL THAT LOOSELY OVERLAP
        previous_potentials = [[] for _ in range(len(self.list))]

        previous_normal_potentials = [[] for _ in range(len(self.list))]
        current_potentials = [[] for _ in range(len(points_lists))]
        #List of shapes that make up all polygons
        prev_shapes = []
        current_shapes = []

        list_to_change = []

        # CREATE LIST THAT TELLS US WHICH CURRENT HAVNT BEEN USED (CAME FROM SIDE/BEHIND)
        list_of_current_not_dealt_with = []
        list_of_previous_not_dealt_with = []
        for ind, curr in enumerate(points_lists):
            list_of_current_not_dealt_with.append(ind)

        for ind, prev in enumerate(self.list):
            if len(prev) != 1:
                list_of_previous_not_dealt_with.append(ind)

        #Make a list of indexes, each representing the PREVIOUS TREE
        for i in range(0, len(self.list)):
            previous_intersection.append([])
            if len(self.list[i]) != 1:
                ls, polygon = three_image_det.three_image_det.create_outline_polygon(self.list[i],
                                                                                     self.peaks[i] + 30,
                                                                                     self.list[i][4][1] - 30, 1.5)
                prev_shapes.append(polygon)
            else:
                prev_shapes.append([])

        # Make a list of indexes, each representing EACH CURRENT TREE
        for i in range(0, len(points_lists)):
            current_intersection.append([])

            ls, polygon = three_image_det.three_image_det.create_outline_polygon(points_lists[i],
                                                                                 bounding_boxs[i][3] + 30,
                                                                                 bounding_boxs[i][1] - 30,
                                                                                 1.5)
            current_shapes.append(polygon)

        #Make Intersections
        for previous_index, previous_point in enumerate(self.list):
            if len(previous_point) == 1:
                continue

            for current_index, current_point in enumerate(points_lists):

                #IF OUTER POLYGONS DONT INTERSECT, EASILY NO
                if not prev_shapes[previous_index].intersects(current_shapes[current_index]):
                    continue
                else:
                    current_potentials[current_index].append(previous_index)
                    previous_normal_potentials[previous_index].append(current_index)

                    #IF PREVIOUS POINTS ARE WITHIN CURRENT SHAPE
                    b1 = current_shapes[current_index].contains(Point(previous_point[0][0], previous_point[0][1]))
                    b2 = current_shapes[current_index].contains(Point(previous_point[1]))
                    b3 = current_shapes[current_index].contains(Point(previous_point[2]))
                    m1 = current_shapes[current_index].contains(Point(previous_point[3]))
                    t1 = current_shapes[current_index].contains(Point(previous_point[4]))




                    #IF CURRENT POINTS ARE WITHIN PREVIOUS SHAPE:
                    pb1 = prev_shapes[previous_index].contains(Point(current_point[0]))
                    pb2 = prev_shapes[previous_index].contains(Point(current_point[1]))
                    pb3 = prev_shapes[previous_index].contains(Point(current_point[2]))
                    pm1 = prev_shapes[previous_index].contains(Point(current_point[3]))
                    pt1 = prev_shapes[previous_index].contains(Point(current_point[4]))




                    #If at least 2 of previous base, and 1 of previous other, are within
                    if (((b1 + b2 + b3) >= 2) and (m1 + t1) >= 1) and (((pb1 + pb2 + pb3) >= 2) and ((pm1 + pt1) >= 1)):

                        current_intersection[current_index].append(previous_index)
                        previous_intersection[previous_index].append(current_index)
                        #print("PASSED TEST")

         #MAKE POTENTIAL INTERSECTIONS:
        for previous_to_match in range(0, len(self.list)):
             #IGNORE
             if len(self.list[previous_to_match]) == 1:
                 continue
            #MEANS THIS IS A VALID PREVIOUS
             else:
                 for previous_to_try in range(0, len(self.list)):
                    if len(self.list[previous_to_try]) == 1 or previous_to_match == previous_to_try:
                        continue
                    else:
                        if prev_shapes[previous_to_try].intersects(prev_shapes[previous_to_match]):
                            previous_potentials[previous_to_match].append(previous_to_try)






        #------------------------------------------------------
        #DETERMINES WHAT TO DO WITH EVERY PREVIOUS/CURRENT
        for prev_index, prev_point in enumerate(self.list):

            if len(prev_point) == 1:
                #print(f" {prev_index} _______________")
                continue
            else:

                #Meaning No Current Point Adheres To This Old, (BEHIND TREE) ---------------------------------------------------------------------------------------
                if len(previous_intersection[prev_index]) == 0:
                    #print(f" {prev_index} ---> _______ ")
                    continue

                # 1 To 1
                elif (len(previous_intersection[prev_index]) == 1) and \
                        (len(current_intersection[previous_intersection[prev_index][0]]) == 1):
                    #print(f" {prev_index} -> {previous_intersection[prev_index][0]}")

                    list_to_change.append([prev_index, previous_intersection[prev_index][0]])

                    list_of_current_not_dealt_with.remove(previous_intersection[prev_index][0])
                    list_of_previous_not_dealt_with.remove(prev_index)

                #Case where a single current tree intersects 2 previous (USUALLY BECAUSE ONE PREVIOUS GOES BEHIND ANOUTHER)

                #Case where this previous, matches with a Current, who overlaps multiple previous
                #Need to figure out if this PREVIOUS (one of many, deserves to get the current  ----------------------------------------------------------------------------------------
                elif len(current_intersection[previous_intersection[prev_index][0]]) > 1:


                    previous_lowest_distance = 10000000
                    previous_lowest_distance_index = -1

                    #The Single Current, that overlaps multiple previous
                    c = points_lists[previous_intersection[prev_index][0]]           #----------------


                    #For every previous that it intersects
                    for index, value in enumerate(current_intersection[previous_intersection[prev_index][0]]):

                        #Making the previous
                        p = self.list[value]

                        #Finding the distance of this previous
                        total_dist = self.distance(c[0], p[0]) + \
                                     self.distance(c[1], p[1]) + \
                                     self.distance(c[2], p[2])

                        if total_dist < previous_lowest_distance:
                            previous_lowest_distance = total_dist
                            previous_lowest_distance_index = value

                    #IF THIS IS THE LOWEST:
                    if previous_lowest_distance_index == prev_index:
                       # print(f" {prev_index} -> {previous_intersection[prev_index][0]}")

                        #CANT UPDATE CUZ IT MIGHT MESS UP NEXT TIME
                        list_to_change.append([prev_index, previous_intersection[prev_index][0]])

                        print(f" REMOVING FROM CURRENT: {previous_intersection[prev_index][0]}")


                        #ERROR
                        print(f" REMOVING FROM PREVIOUS {prev_index} ")

                       # ERROR
                        #list_of_current_not_dealt_with.remove(previous_intersection[prev_index][0])
                        #list_of_previous_not_dealt_with.remove(prev_index)




                #Case where a single Previous tree intersects 2 current (USUALLY COMING OUT FROM BEHIND
                elif len(previous_intersection[prev_index]) > 1:

                    current_lowest_distance = 10000000000
                    current_lowest_distance_index = -1

                    p = self.list[prev_index]
                    for index, value in enumerate(previous_intersection[prev_index]):

                        c = points_lists[value]

                        total_dist = self.distance(c[0], p[0]) + \
                                    self.distance(c[1], p[1]) + \
                                    self.distance(c[2], p[2])

                        if total_dist < current_lowest_distance:
                            current_lowest_distance = total_dist
                            current_lowest_distance_index = value

                   # print(f" {prev_index} -> {current_lowest_distance_index}")

                    #CANT UPDATE CUZ IT WILL MESS UP NEXTTIME
                    list_to_change.append([prev_index, current_lowest_distance_index])

                    list_of_previous_not_dealt_with.remove(prev_index)
                    list_of_current_not_dealt_with.remove(current_lowest_distance_index)

                else:
                    print("SHOULD NEVER DEAL WITH THIS"
                          "---------------------------"
                          "------------------------"
                          "-------------------"
                          "---------------"
                          "-----------"
                          "-------"
                          "----"
                          "--"
                          "-")

        #----------------------------------------------------




        #FILTERS LIST OF POTENTIAL INTERSECTIONS
        new_previous_potentials = []
        for index, values in enumerate(previous_potentials):

            outer_list = []
            for value in values:
                if value in list_of_previous_not_dealt_with:
                    continue
                else:
                    outer_list.append(value)
            new_previous_potentials.append(outer_list)

        previous_potentials = new_previous_potentials







        #VIRGIN MARRY-----------------------------------------------

        previous_to_remove_after = []
        current_to_remove_after = []

        #FOR EVERY LOST PREVIOUS
        for previous_potential_virgin_mary in list_of_previous_not_dealt_with:

            list_of_valid = []

            #Find Number Of Currents With No Home That Touch It
            for current_value in previous_normal_potentials[previous_potential_virgin_mary]:
                if current_value not in list_of_current_not_dealt_with:
                    continue
                else:
                    list_of_valid.append(current_value)


            #If No Possible Unused Touch, Continue
            if len(list_of_valid) == 0:
                continue

            #If One Does
            elif len(list_of_valid) == 1:

                inner_list_of_valid = []

                #Check Whether Current This One ONly Touchs One Previous Without Home
                for previous_value in current_potentials[list_of_valid[0]]:
                    if previous_value not in list_of_previous_not_dealt_with:
                        continue
                    else:
                        inner_list_of_valid.append(previous_value)

                if len(inner_list_of_valid) == 1:
                    list_to_change.append([previous_potential_virgin_mary, list_of_valid[0]])
                    previous_to_remove_after.append(previous_potential_virgin_mary)
                    current_to_remove_after.append(list_of_valid[0])


        for x in previous_to_remove_after:
            list_of_previous_not_dealt_with.remove(x)

        for y in current_to_remove_after:
            list_of_current_not_dealt_with.remove(y)

        #-----VM END--------------------------------





        list_to_add = []

        #NEW TREES ADDED (REMOVE PREVIOUS THAT ARE MATCHED???)
        for current_left_over_index in list_of_current_not_dealt_with:

            #LIKELY APPEARED FROM EDGE
            if len(current_potentials[current_left_over_index]) == 0:
                #print(f" ...  --> {current_left_over_index}  (NONE) ")
                #Make a New Point
                self.list.append(points_lists[current_left_over_index])
                #Make A New Peak
                self.peaks.append(bounding_boxs[current_left_over_index][3])

                # Width Points

                self.base_points.append([[(points_lists[current_left_over_index][1][0],
                                          points_lists[current_left_over_index][2][0])]])
                #NEW APPEARANCE/DISSAPEARANCE
                self.appearance.append(-1)
                self.disapearance.append(-1)

                print(f"   CURRENT: {current_left_over_index} ({len(self.list) - 1} APPEARS WITH NO MATCH")

            #MEANS THIS CAME FROM TOUCHING ONE (LIKELY BEHIND THAT)
            elif len(current_potentials[current_left_over_index]) == 1:
                #print(f" ... --> {current_left_over_index} ({current_potentials[current_left_over_index][0]})")



                #Make Shape
                self.list.append(points_lists[current_left_over_index])

                # Make A New Peak
                self.peaks.append(bounding_boxs[current_left_over_index][3])

                # Width Points

                self.base_points.append([[(points_lists[current_left_over_index][1][0],
                                          points_lists[current_left_over_index][2][0])]])


                #IF THE VALUE IT WAS SUPPOSED TO APPEAR BEHIND DISAPEARS THIS TURN
                if current_potentials[current_left_over_index][0] in list_of_previous_not_dealt_with:
                    self.appearance.append(-1)
                    self.disapearance.append(-1)
                else:
                    # NEW APPEARANCE/DISSAPEARANCE
                    self.appearance.append(current_potentials[current_left_over_index][0])
                    self.disapearance.append(-1)



                print(f"   CURRENT: {current_left_over_index} ({len(self.list) - 1} APPEARS BEHIND PREV {current_potentials[current_left_over_index]}")

            #MEANS THIS NEW TREE TOUCHS MULTIPLE
            # (SO CHOOSEING BEST)
            else:
                lowest_relative_to_new = -1000
                index_lowest_relative = -1
                #For all the PREV it intersected with
                for current_possible_index in current_potentials[current_left_over_index]:

                    if current_possible_index in list_of_previous_not_dealt_with:
                        continue

                    difference = self.list[current_possible_index][0][1] - points_lists[current_left_over_index][0][1]

                    if difference > lowest_relative_to_new:
                        lowest_relative_to_new = difference
                        index_lowest_relative = current_possible_index

                #print(
                #    f"  ... --> {current_left_over_index} ({index_lowest_relative})")

                self.list.append(points_lists[current_left_over_index])

                # Make A New Peak
                self.peaks.append(bounding_boxs[current_left_over_index][3])

                # Width Points
                self.base_points.append([[(points_lists[current_left_over_index][1][0],
                                          points_lists[current_left_over_index][2][0])]])
                # NEW APPEARANCE/DISSAPEARANCE

                if index_lowest_relative != -1:

                    self.appearance.append(index_lowest_relative)
                    self.disapearance.append(-1)
                else:
                    self.appearance.append(index_lowest_relative)
                    self.disapearance.append(-1)

                print(f"   CURRENT: {current_left_over_index} ({len(self.list) - 1} APPEARS BEHIND PREV (({index_lowest_relative})))  {current_potentials[current_left_over_index]}")

        #MEANS PREVIOUS DISAPEARS
        for previous_left_over_index in list_of_previous_not_dealt_with:


            #If this previous touchs no current, LIKELY MEANS WENT BEHIND EDGE
            if len(previous_potentials[previous_left_over_index]) == 0:

                self.list[previous_left_over_index] = [1]

                print(f"  PREVIOUS: {previous_left_over_index} DISSAPEARS BEHIND NONE ")
                continue




            # MEANS THIS CAME FROM TOUCHING ONE (LIKELY BEHIND THAT)
            elif len(previous_potentials[previous_left_over_index]) == 1:
                #print(f" {previous_left_over_index} --> ....  ({previous_potentials[previous_left_over_index][0]})")

                self.list[previous_left_over_index] = [1]
                self.disapearance[previous_left_over_index] = previous_potentials[previous_left_over_index][0]

                print(f"  PREVIOUS: {previous_left_over_index} DISSAPEARS BEHIND {previous_potentials[previous_left_over_index]} ")



            #MEANS THIS CAME FROM TOUCING MULTIPLE, CHOOSE WHICH
            else:
                lowest_relative_to_new = -1000
                index_lowest_relative = -1

                for previous_possible_index in previous_potentials[previous_left_over_index]:

                    # Subtract, (SINCE WHEN CPI front, MORE, SHOULD BE BIGGEEST
                    difference = self.list[previous_possible_index][0][1] - self.list[previous_left_over_index][0][1]

                    if difference > lowest_relative_to_new:
                        lowest_relative_to_new = difference
                        index_lowest_relative = previous_possible_index


                print(
                    f"  PREVIOUS {previous_left_over_index} DISAPEARS BEHIND (({index_lowest_relative}))) {previous_potentials[previous_left_over_index]})")

                self.list[previous_left_over_index] = [1]
                self.disapearance[previous_left_over_index] = index_lowest_relative



        #FOR CURRENT MATCHES:
        for list_index in list_to_change:

            print(f"   CONTINUED:  {list_index}")

            #Moves Points
            self.list[list_index[0]] = points_lists[list_index[1]]
            #Peak
            self.peaks[list_index[0]] = bounding_boxs[list_index[1]][3]

            #Width Points
            wp = (points_lists[list_index[1]][1][0], points_lists[list_index[1]][2][0])

            #               FOR THIS POINTS,   THE LAST INDEX,
            self.base_points[list_index[0]][len(self.base_points[list_index[0]]) - 1].append(wp)


        lll = []
        for id, x in enumerate(self.list):
            if len(x) == 1:

                lll.append(-1)

            else:
                lll.append(4)


        # print(f" DIS   {self.disapearance}")
        # print(f" APP  {self.appearance}")
        # print(f" POINTS     {lll}")




    def distance(self, xy1, xy2):
        return math.sqrt( (xy1[0] - xy2[0])**2 + (xy1[1] -xy2[1])**2 )



    #DEAL WITH ALL CONNECTION STUFF
    def create_major_list(self, points, fd, f1, f2):
        matchs = []
        filtered_matchs = []
        searchable_matchs = []

        for x in range(0, len(self.list)):
            searchable_matchs.append(-1)

        #FOR EVERY VALUE IN LIST
        for index, match in enumerate(self.list):
            #IF THIS LIST VALUE IS EMPTY,
            if len(match) == 1:
                continue
            #OTHERWISE
            else:
                #COMPARE TO EVERY CURRENT POINT
                for inner_index, point in enumerate(points):
                    #AND IF ITS THE SAME, ADD TO LIST
                    if point[0][0] == match[0][0] and point[0][1] == match[0][1]:
                        matchs.append([index, inner_index])
                        searchable_matchs[index] = inner_index

                        if index < self.starting_length:
                            filtered_matchs.append([index, inner_index])
        #ONLY UPLOADING THE ONES FROM PREVIOUS
        fd.upload_connection(filtered_matchs, f1, f2)

        #RETURNING ALL
        return matchs, searchable_matchs


    #IDEA, THE INDEX HOLDS THE NUMBER IN THE NEXT FRAME
    def create_searchable_dict(self, points):

        list = []
        for x in range(0, len(self.list)):
            list.append(-1)


        for value in self.list:
            if len(value) == 1:
                continue
            else:
                for index, inner in enumerate(points):

                    if value[0][0] == inner[0][0] and value[0][1] == inner[0][1]:
                        list[value] = index

        return list




