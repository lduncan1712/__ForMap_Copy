import one_directory


class tracker_object:

    def __init__(self, color, points, boxes, main):
        #Color
        self.color = color
        #Points
        self.list_of_points = []
        self.list_of_boxes = []
        #List Of Indexs That Were Mains
        self.list_of_main = []

        self.length_since_error = 0

        if main:
            self.list_of_main.append(0)

        self.list_of_points.append(points)
        self.list_of_boxes.append(boxes)

    def __str__(self):
        return str(self.color) + " " + str(self.list_of_main) + " " + str(self.list_of_points)

    def update(self, points, boxes, main):

        self.list_of_points.append(points)
        self.list_of_boxes.append(boxes)

        if main:
            self.list_of_main.append(len(self.list_of_points) - 1)

    def update_by_exclusion(self, main):

        self.list_of_points.append(0)
        self.list_of_boxes.append(0)

        self.length_since_error+=1

        if main:
            self.list_of_main.append(len(self.list_of_points) - 1)

        if self.length_since_error >= 8:
            return False
        else:
            return True


    #IDEA: if appears in main, obviously use
    #      if doesnt, if appears before and after reasonably, ... find average

    #DONE 2 OR SO AFTER,
    def major_assessment(self):


        #COULD APPEAR AFTER
        if len(self.list_of_main) == 0:
            print("LACKS A MAIN")
            return False, False


        last_main_index = self.list_of_main[-1]

        last_values = self.list_of_points[last_main_index]
        last_box = self.list_of_boxes[last_main_index]


        #CHANGED FOR NOW... WHEN MAIN RELIABLE RECHANGE

        #If Not Found
        if True:  #not isinstance(last_values, list):
            prev_point = 0
            fut_point = 0

            prev_box = 0
            fut_box = 0
            #print("QUESTIONABLE POINT: 60")
            #print(self.list_of_points)
            #Need Value Just Before
            for previous in range(1, 1 + one_directory.behind_number ):

                previous_index = last_main_index - previous

                #IF POINT SET. VALID
                if not isinstance(self.list_of_points[previous_index], int):
                    prev_point = self.list_of_points[previous_index]
                    prev_box = self.list_of_boxes[previous_index]
                    print("MAKING PREV")
                    break
            #print("LACK THEREOF")
            #Need Values Just Before


            for forward_index in range(last_main_index + 1, last_main_index + 1 + one_directory.behind_number):

                if not isinstance(self.list_of_points[forward_index], int):
                    print("MAKING FUTURE")
                    fut_point = self.list_of_points[forward_index]
                    fut_box = self.list_of_boxes[forward_index]
                    break
            #print("LACK THER")

            #If Both Are Found - ASSUME VALID
            if not isinstance(prev_point, int) and not isinstance(fut_point, int):
                return self.find_average(prev_point, fut_point), self.find_average_box(prev_box, fut_box)
            else:
                return False, False
        # else:
        #     return last_values, last_box


















    def find_average(self, points1, points2):
        print("VAL BEFORE")
        print(points1)
        print(points2)

        points3 = []

        for index in range(0, len(points1)):
            index_3_x = (points1[index][0] + points2[index][0]) / 2
            index_3_y = (points1[index][1] + points2[index][1]) / 2

            values = (index_3_x, index_3_y)

            points3.append(values)

        return points3

    def find_average_box(self, box1, box2):
        box3 = []
        for index in range(0, 4):
            box_index = (box1[index] + box2[index]) / 2
            box3.append(box_index)

        return box3


