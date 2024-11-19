import psycopg2
from psycopg2.extras import execute_values

import one_directory

myConn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="password"
)

frame_query = "INSERT INTO photo (id, time, altitude, starting_v_degree, starting_h_degree, v_aov, h_aov, position_accuracy, " \
              "altitude_accuracy, dir_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
tree_query = "INSERT INTO tree (id, par_id, base_degree, peak_degree, " \
             "dividing_degree, peak_continues, base_continues, slope_overall, slope_upper, " \
             "slope_lower, width_degree, width_error, peak_direction, base_direction) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
conn_query = "INSERT INTO connections (p1, p2, t1, t2) VALUES (%s, %s, %s, %s)"
class five_database:

    def setup_connection(self, frame, phase1):
        self.cursor = myConn.cursor()
        self.frame = frame

        if phase1:
            self.upload_frame_to_db(frame.id)
        else:
            self.upload_trees_to_db()


    def omni_upload_connections_to_db(self, first, second, list):

        query = "INSERT INTO connections " \
                "(p1,p2,t1,t2) VALUES (%s, %s, %s, %s)"
        for partial_list in list:

            to_be_given = [first, second, partial_list[0], partial_list[1]]
            self.cursor.execute(query, to_be_given)
        myConn.commit()






    def omni_upload_trees_to_db(self, degree_points, width_points, box_points, frame_id):
        self.cursor = myConn.cursor()

        value = "INSERT INTO tree_perspective " \
                "(frame_id, id," \
                "base_deg, peak_deg," \
                "p0_deg, p0_dir," \
                "p1_deg, p1_dir," \
                "p2_deg, p2_dir," \
                "p3_deg, p3_dir," \
                "p4_deg, p4_dir, width) VALUES " \
                "(%s, %s," \
                "%s, %s," \
                "%s, %s," \
                "%s, %s," \
                "%s, %s," \
                "%s, %s," \
                "%s, %s, %s) "

        for index, degree_point in enumerate(degree_points):
            print("VAL")
            width = width_points[index]
            box = box_points[index]

            data = (frame_id + one_directory.starting_id, index,
                    box[3], box[1],
                    degree_point[0][1], degree_point[0][0],
                    degree_point[1][1], degree_point[1][0],
                    degree_point[2][1], degree_point[2][0],
                    degree_point[3][1], degree_point[3][0],
                    degree_point[4][1], degree_point[4][0],
                    width)
            print(data)

            self.cursor.execute(value, data)
        myConn.commit()









    def upload_trees_to_db(self):
        self.frame.list_of_instances = sorted(self.frame.list_of_instances, key=lambda x: x.point_list[1][0])

        x = 0;
        # adds each tree object
        for tree in self.frame.list_of_instances:
            self.upload_tree_to_db(tree, self.frame.id, x)
            x = x + 1


    def upload_frame_to_db(self, id):


        # location = "POINT(" + self.frame.longitude + " " + self.frame_latitude + ")"

        #id, time, altitude, starting_v_degree, starting_h_degree, v_aov, h_aov, gps_accuracy, altitude_accuracy"



        #id, time, altitude, starting_v_degree, starting_h_degree, v_aov, h_aov, position_accuracy, " \
         #     "altitude_accuracy, dir_id
        values = (id,
                  self.frame.date_time,
                  self.frame.altitude,
                  69,


                  69,
                  self.frame.VAOV,
                  self.frame.HAOV,
                  self.frame.dop,
                  1000,
                  self.frame.directory_id
                  )


        self.cursor.execute(frame_query, values)
        myConn.commit()

        point = f"ST_GeographyFromText('POINT({self.frame.longitude} {self.frame.latitude})')"

        data = [(point,)]

        self.cursor.execute(f"Update photo set position_of_photo = {point} where id = {id}")

        myConn.commit()


    def setup_connection_connection(self):
        self.cursor = myConn.cursor()

    def upload_connection(self, list_of_conns, p1, p2):

        for con in list_of_conns:

            values = (p1 + one_directory.starting_id, p2 + one_directory.starting_id, con[0], con[1])

            self.cursor.execute(conn_query, values)
        myConn.commit()


    def upload_tree_to_db(self, tree, id, tree_id):



        # id, parent_id, base_degree, peak_degree, " \
        #              "
        # dividing_degree, peak_continues, base_continues, slope_overall, slope_upper, " \
        #              "
        # slope_lower, width_degree, width_error
        values = (tree_id,
                  id,
                  tree.super_frame.get_degree_at_y(tree.bottom[1]),
                  tree.super_frame.get_degree_at_y(tree.top[1]),
                  tree.super_frame.get_degree_at_y(tree.point_list[2][1]),
                  tree.top_extension,
                  tree.bottom_extension,
                  float(tree.slope_list[0]),
                  float(tree.slope_list[2]),
                  float(tree.slope_list[1]),
                  (tree.abs_w/tree.super_frame.x)*tree.super_frame.HAOV,
                  69,
                  tree.super_frame.get_degree_at_x(tree.top[0]),
                  tree.super_frame.get_degree_at_x(tree.bottom[0])
                            #peak direction
                            #base direction
                )


        self.cursor.execute(tree_query, values)

        myConn.commit()


    @staticmethod
    def apply_perspectives(frame, front, back):
        cursor = myConn.cursor()
        s = "INSERT INTO perspectives (id_photo, id_front, id_back) VALUES (%s, %s, %s)"
        values = (frame, front, back)
        cursor.execute(s, values)
        myConn.commit()


    def check_for_perspectives(self, f1, f2, f3):
        cursor = myConn.cursor()
        s = "SELECT id_front from perspectives where id_photo = %s and id_front = %s and id_back = %s"
        values = (f1, f2, f3)
        cursor.execute(s, values)
        val = cursor.fetchall()
        if len(val) == 0:
            return False
        else:
            return True


    @staticmethod
    def get_connections(p1, p2):
        cursor = myConn.cursor()
        s = "SELECT t1, t2 from connections where p1 = %s and p2 = %s"
        values = (p1, p2)
        cursor.execute(s, values)
        return cursor.fetchall()


    def get_perspectives(self, id):
        cursor = myConn.cursor()
        s = "SELECT id_front, id_back from perspectives where id_photo = %s"
        values = (id,)
        cursor.execute(s, values)
        return cursor.fetchall()

    #Returns the position in one frame further of a tree
    def get_tree_later_single(self, photo_id, tree_id):
        cursor = myConn.cursor()
        s = "SELECT t2 FROM CONNECTIONS WHERE p1 = %s and p2 = %s and t1 = %s"
        values = (photo_id, photo_id + 1, tree_id)
        #print(f" VALUES {values}")
        cursor.execute(s, values)
        value = cursor.fetchall()

        #RETURNS NO VALUES
        if len(value) == 0:
            return -1
        else:
            return value[0]


    #returns the Tree ID in ending_id corrasponding to starting_id
    #CAN BE REVERSED
    def get_tree_later_multiple(self, starting_id, tree_id, ending_id):

        if starting_id == ending_id:
            return tree_id

        #NORMAL DIRECTION
        if ending_id > starting_id:

            index_to_start = starting_id
            val_to_start = tree_id
            while(index_to_start < ending_id):

                val = self.get_tree_later_single(index_to_start, val_to_start)
                if val == -1:
                    return -1
                else:
                    index_to_start+=1
                    val_to_start = val[0]
            return val_to_start

        #OPPOSITE DIRECTION
        else:
            list_of_ending_values = self.get_trees_at_single_photo(ending_id)
            # print("--------------------------------------------")
            # print(list_of_ending_values)
            #print(list_of_ending_values)
            index_to_start = ending_id
            values_left = len(list_of_ending_values)

            #GO through every
            while(index_to_start < starting_id):
                #Go through every connection
                for ind, value in enumerate(list_of_ending_values):
                    #if not already gone
                    if value != -1:
                        #get the next index
                        val = self.get_tree_later_single(index_to_start, value)
                        #if exists, set to it
                        if val != -1:
                            list_of_ending_values[ind] = val[0]
                        #otherwise, make it to 0
                        else:
                            list_of_ending_values[ind] = -1
                            values_left-=1
                #print(list_of_ending_values)
                index_to_start += 1
                #print(list_of_ending_values)
            #print("----------------------------------")

            #MEANS NONE EXIST
            if values_left == 0:
                return -1
            for ind, val in enumerate(list_of_ending_values):
                if val == tree_id:
                    return ind
            return -1



    #Obtains all the trees id found at in a given photo
    def get_trees_at_single_photo(self, photo_id):
        cursor = myConn.cursor()
        s = "SELECT id FROM tree_perspective WHERE frame_id = %s"
        values = (photo_id,)
        cursor.execute(s, values)

        list = []
        for x in cursor.fetchall():
            list.append(x[0])
        return list

    def translate_entire_photo(self, starting_id, ending_id):

        starting_trees = self.get_trees_at_single_photo(starting_id)
        #print(f" STARTING TREES:  {starting_trees}")
        list = []

        for ind, tree in enumerate(starting_trees):
            val = self.get_tree_later_multiple(starting_id, ind, ending_id)
            if val != -1:
                list.append([ind, val])

        return list


    # def get_range(self, starting_id, index):
    #     fd = five_database
    #
    #     highest_index = starting_id
    #     lowest_index = starting_id
    #
    #     #ATTEMPT ABOVE
    #     print(f" STARTS: {highest_index}")
    #     for above_index in range(starting_id + 1, starting_id + 100):
    #
    #         above_list = self.get_tree_later_multiple(starting_id, above_index)
    #         print(f" {starting_id}  {above_index}   == {above_list}")
    #         if len(above_list) == 0:
    #             break
    #         else:
    #             highest_index = above_index
    #
    #     #ATTEMPT BELOW
    #     for below_index in range(1, 100):
    #
    #         below_list = self.translate_entire_photo(starting_id - below_index, starting_id)
    #         print(f" {starting_id} {below_index} == {below_list}")
    #         if len(below_list) == 0:
    #             break
    #         else:
    #             lowest_index = starting_id - below_index
    #
    #     return highest_index, lowest_index
    #





















    @staticmethod
    def omni_obtain_plot_baseline(id, buffer):
        cursor = myConn.cursor()
        #cursor.execute(f"WITH furthest_west_south AS (SELECT ST_X(position::geometry) as lon, "
                      # f"                                    ST_Y(position::geometry) as lat FROM frame WHERE ST_X(position::geometry) = (SELECT min(ST_X(position::geometry)) FROM frame where directory_id = {id}) AND ST_Y(position::geometry) = (SELECT min(ST_Y(position::geometry)) FROM frame where directory_id = {id})), translated AS (SELECT ST_Transform(ST_Translate(ST_Transform(ST_SetSRID(ST_Point(lon, lat), 4326), 3857), -100, -100), 4326) as new_geom FROM furthest_west_south) SELECT ST_X(new_geom), ST_Y(new_geom) FROM translated;")

        cursor.execute(f"SELECT ST_X(ST_Transform(ST_Translate(ST_Transform(ST_SetSRID(ST_Point((SELECT min(ST_X(position_of_photo::geometry)) from photo where dir_id = {id} and id >= {one_directory.starting_id} and id <= {one_directory.ending_id}), (SELECT min(ST_Y(position_of_photo::geometry)) from photo where dir_id = {id} and id >= {one_directory.starting_id} and id <= {one_directory.ending_id})), 4326), 3857), -{buffer}, -{buffer}), 4326)), " 
                       f"ST_Y(ST_Transform(ST_Translate(ST_Transform(ST_SetSRID(ST_Point((SELECT min(ST_X(position_of_photo::geometry)) from photo where dir_id = {id} and id >= {one_directory.starting_id} and id <= {one_directory.ending_id}), (SELECT min(ST_Y(position_of_photo::geometry)) from photo where dir_id = {id} and id >= {one_directory.starting_id} and id <= {one_directory.ending_id})), 4326), 3857), -{buffer}, -{buffer}), 4326)) as point")
        return cursor.fetchall()[0]






    @staticmethod
    def omni_obtain_fragments(parent_id):
        cursor = myConn.cursor()

        cursor.execute(f" SELECT id, "
                       f"base_deg, "
                       f"peak_deg, "
                       f"p0_deg, "
                       f"p0_dir, "
                       f"p1_deg, "
                       f"p1_dir, "
                       f"p2_deg, "
                       f"p2_dir, "
                       f"p3_deg, "
                       f"p3_dir, "
                       f"p4_deg, "
                       f"p4_dir, "
                       f"width from tree_perspective "
                       f"where frame_id = {parent_id} ")

        return cursor.fetchall()

    #a curated selection of frames based on user...... made later
    @staticmethod
    def omni_obtain_frames():

        cursor = myConn.cursor()
        cursor.execute(f"SELECT id, ST_X(position_of_photo::geometry), ST_Y(position_of_photo::geometry),"
                       f"starting_h_degree, h_aov, position_accuracy, time from photo where id >= {one_directory.starting_id} and id < {one_directory.ending_id} order by id")
        return cursor.fetchall()


    @staticmethod
    def omni_obtain_relative_position(point, baseline):
        cursor = myConn.cursor()
        cursor.execute("SELECT ST_Distance("
                       f"ST_GeomFromText('POINT({baseline[0]} {baseline[1]})', 4326)::geography,"
                       f"ST_GeomFromText('POINT({baseline[0]} {point[1]})', 4326)::geography);")
        y = cursor.fetchone()[0]

        cursor.execute("SELECT ST_Distance("
                       f"ST_GeomFromText('POINT({baseline[0]} {baseline[1]})', 4326)::geography,"
                       f"ST_GeomFromText('POINT({point[0]} {baseline[1]})', 4326)::geography);")
        x = cursor.fetchone()[0]
        return x,y



