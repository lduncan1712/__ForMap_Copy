import psycopg2

import master

myConn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="password"
)

class new_detection_db:

    def __init__(self):

        self.cursor = myConn.cursor()

        self.connection_query = "INSERT INTO connections (p1, p2, t1, t2) VALUES (%s, %s, %s, %s)"

        self.tree_query = "INSERT INTO tree_perspective " \
                "(frame_id, " \
                "id," \
                "base_deg, " \
                "peak_deg," \
                "p0_deg, " \
                "p0_dir," \
                "p1_deg, " \
                "p1_dir," \
                "p2_deg, " \
                "p2_dir," \
                "p3_deg, " \
                "p3_dir," \
                "p4_deg, " \
                "p4_dir, " \
                "width) " \
                "VALUES " \
                "(%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s, %s) "



    def setup_tracker(self, tracker):
        self.tracker = tracker

    def send_to_database(self, starting_vertical, starting_horizontal, x, y, major):

        #DEFINES INDEXS TO MOVE
        ### indexs_placed_in_order
        if True:

            list_indexs_to_print_as_single = []
            points_indexs_to_print_as_single = []

            # GETS INDEXS, AND POINTS
            for index, pointlists in enumerate(self.tracker.list_of_points):

                if pointlists[-1] is None:
                    continue
                else:

                    p_to_change = pointlists[-1]

                    list_indexs_to_print_as_single.append(index)
                    points_indexs_to_print_as_single.append(p_to_change)

            indexs_placed_in_order = self.sorting_by_location(points_indexs_to_print_as_single,
                                                              list_indexs_to_print_as_single)

            # CREATE CONNECTIONS

        #CREATE TREES (+ CONVERT TO DEGREE)
        if True:
            x_2 = x/2
            y_2 = y/2

            for index_of_tree, index_within_list in enumerate(indexs_placed_in_order):
                #print("SOMETHING TO EXECUTE")
                points = self.tracker.list_of_points[index_within_list][-1]
                # TREES
                values = (
                    major + master.starting_id,
                    index_of_tree,
                    69,
                    69,
                    self.convert_vertical_to_angle(starting_vertical, y_2, points[0][1]),
                    self.convert_horizontal_to_angle(starting_horizontal, x_2, points[0][0]),
                    self.convert_vertical_to_angle(starting_vertical, y_2, points[1][1]),
                    self.convert_horizontal_to_angle(starting_horizontal, x_2, points[1][0]),
                    self.convert_vertical_to_angle(starting_vertical, y_2, points[2][1]),
                    self.convert_horizontal_to_angle(starting_horizontal, x_2, points[2][0]),
                    self.convert_vertical_to_angle(starting_vertical, y_2, points[3][1]),
                    self.convert_horizontal_to_angle(starting_horizontal, x_2, points[3][0]),
                    self.convert_vertical_to_angle(starting_vertical, y_2, points[4][1]),
                    self.convert_horizontal_to_angle(starting_horizontal, x_2, points[4][0]),
                    69
                )

                self.cursor.execute(self.tree_query, values)
            myConn.commit()


        #CREATE CONNECTIONS
        if True:
            for index_of_value, index_in_list in enumerate(indexs_placed_in_order):

                prev_index = self.tracker.previous_indexs[index_in_list]
                if prev_index != -1:

                    values = (major - 1 + master.starting_id, major + master.starting_id, prev_index, index_of_value)

                    self.cursor.execute(self.connection_query, values)
            myConn.commit()


        return indexs_placed_in_order

    def sorting_by_location(self, list1, list2):
        sorted_index = sorted(range(len(list1)), key=lambda k: list1[k][0][0])

        # sorted_list1 = [list1[i] for i in sorted_index]
        sorted_list2 = [list2[i] for i in sorted_index]

        return sorted_list2

    #ASSUME MIDDLE IS AT STARTING ANGLE (MASTER APPLIES)
    def convert_vertical_to_angle(self, starting_angle, middle, y):
        return (starting_angle + (y - middle)*master.x_degree_per_pixel) % 360

    #ASSMUE MIDDLE IS AT STARTING ANGLE (MASTER APPLIES)
    def convert_horizontal_to_angle(self, starting_angle, middle, x):
        return (starting_angle + (x - middle)*master.y_degree_per_pixel % 360)


