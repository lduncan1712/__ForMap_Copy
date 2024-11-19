import psycopg2

import master



class new_tracking:
    def __init__(self):


        self.list_of_points = []
        self.list_of_boxs = []
        self.list_of_colors = []

        self.list_of_length_since_error = []

        self.list_starting_major = []

        self.indexs_of_majors = []

        self.previous_indexs = []

        self.index = 0
        self.absolute_index = []








    def update_list(self, points, boxs, colors, major, major_number, vid_vis):

        list_of_previous_indexs = []
        len_prev = len(self.list_of_points)
        for index in range(0, len(self.list_of_points)):

            list_of_previous_indexs.append(len_prev - 1 - index)
        #print("PREVIOUS TO BE ITERATED")
        #print(list_of_previous_indexs)

        list_of_current_indexs = []
        len_curr = len(points)
        for index in range(0, len(points)):
            list_of_current_indexs.append(index)



        #MATCH ALL CURRENT WITH PREVIOUS
        for current_index in range(0, len(points)):

            this_color = colors[current_index]
            this_point = points[current_index]
            this_box = boxs[current_index]

            #MATCH ALL POSSIBLE
            #print(" COLORS???")
            #print(self.list_of_colors)
            for previous_index, previous_color in enumerate(self.list_of_colors):

                #IF SAME COLOR, MEANING THIS IS THE ONE
                if new_tracking.compare_color(previous_color, this_color):
                    #UPDATES POINTS, BOXS, TIME SINCE ERROR
                    self.list_of_points[previous_index].append(this_point)
                    self.list_of_boxs[previous_index].append(this_box)
                    self.list_of_length_since_error[previous_index] = 0

                    self.previous_indexs.append(-1)
                    self.absolute_index.append(self.index)
                    self.index+=1


                    #print(f" REMOVING PREVIOUS: {list_of_previous_indexs}  {previous_index}")
                    list_of_previous_indexs.remove(previous_index)
                    list_of_current_indexs.remove(current_index)

                    #SETS MAJOR ALLOCATION
                    if major:

                        #IF FIRST MAJOR, DEFINE IT AS SO
                        if self.list_starting_major[previous_index] == -1:
                            self.list_starting_major[previous_index] = major_number

                        #EITHER WAY, ADD TO LIST OF INDEXS WITH MAJORS
                        self.indexs_of_majors[previous_index].append(len(self.list_of_points[previous_index]) - 1)


                    break


        indexs_to_delete = []
         #ADD FAIL TO PREVIOUS NOT MATCHED
        for previous_failed_index in list_of_previous_indexs:

            #UPDATE POINTS AS FAILED
            self.list_of_points[previous_failed_index].append(None)
            self.list_of_boxs[previous_failed_index].append(None)
            #INCREASE TIME SINCE FAIL
            self.list_of_length_since_error[previous_failed_index] += 1


            #IF MAJOR NEED TO ADD STILL
            if major:
                self.indexs_of_majors[previous_failed_index].append(len(self.indexs_of_majors[previous_failed_index]) - 1)
                if self.list_starting_major[previous_failed_index] == -1:
                    self.list_starting_major[previous_failed_index] = major_number


            #REMOVE IF NECESSARY
            if self.list_of_length_since_error[previous_failed_index] >= master.time_before_remove:
                vid_vis.remove_value(self.list_of_colors[previous_failed_index])

                indexs_to_delete.append(previous_failed_index)


        #ADD NEW CURRENTS NOT DEALT WITH
        for current_failed_index in list_of_current_indexs:
            self.list_of_points.append([points[current_failed_index]])
            self.list_of_boxs.append([boxs[current_failed_index]])

            self.list_of_colors.append(colors[current_failed_index])
            self.list_of_length_since_error.append(0)
            self.previous_indexs.append(-1)

            self.absolute_index.append(self.index)
            self.index += 1


            if major:
                self.list_starting_major.append(major_number)
                self.indexs_of_majors.append([0])
            else:
                self.list_starting_major.append(-1)
                self.indexs_of_majors.append([])

        if len(indexs_to_delete) > 1:
            #print(f" DELETING: {indexs_to_delete}")
            for previous_to_remove in indexs_to_delete:
                #print(f" BEFORE REMOVING: ")

                del self.list_of_points[previous_to_remove]
                del self.list_starting_major[previous_to_remove]
                del self.list_of_boxs[previous_to_remove]
                del self.list_of_length_since_error[previous_to_remove]
                del self.indexs_of_majors[previous_to_remove]
                del self.list_of_colors[previous_to_remove]
                del self.absolute_index[previous_to_remove]
                del self.previous_indexs[previous_to_remove]


    def update_for_connections(self, indexs):

        for index_index, in_list in enumerate(indexs):

            self.previous_indexs[in_list] = index_index






    @staticmethod
    def compare_color(color1, color2):
        return color1[0] == color2[0] and color1[1] == color2[1] and color1[2] == color2[2]

    def confirm_uniqueness(self, colors_sorted_left_right):
        for outer_index, outer_object in enumerate(self.list):
            for inner_index, inner_object in enumerate(self.list):
                if outer_index > inner_index:
                    if self.compare_color(outer_object.color, inner_object.color):
                        print("OVERLAP ZZZ")
                        print(colors_sorted_left_right)