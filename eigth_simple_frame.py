import math

from matplotlib import patches
from shapely.geometry import LineString, Polygon, Point

import nine_fragment
import six_plots
from five_database import five_database
import one_directory



class eight_simple_frame:

    def check_for_an_intersection(self, f1_location, f2_location, f1, f2):


        hor_angle = f1.base_dir
        start_point = self.move_random_along_angle(hor_angle, f1.min_dist, f1_location)
        end_point = self.move_random_along_angle(hor_angle, f1.max_dist, f1_location)

        l1 = LineString([start_point, end_point])

        hor_angle = f2.base_dir
        start_point = self.move_random_along_angle(hor_angle, f2.min_dist, f2_location)
        end_point = self.move_random_along_angle(hor_angle, f2.max_dist, f2_location)

        l2 = LineString([start_point, end_point])

        return l1.intersects(l2)










    def __init__(self, frame_id, x, y, left_angle, width, accuracy, time):

        # setting static data
        self.left_range = left_angle % 360
        self.right_range = (left_angle + width) % 360
        self.accuracy = accuracy
        self.frame_id = frame_id
        self.time = time
        self.width = width

        self.total_width_in_frame = 0

        self.width_importance = 0







        # calculates relative position (can be improved)
        x, y = five_database.obtain_relative_position((x,y), six_plots.corner)

        self.centre = (x, y)

        self.bound = Point(x,y).buffer(accuracy)


        self.fragments = []
        self.minimum_angle_of_productivity = -90
        # obtains frames fragments
        self.obtain_fragments_from_db()

        #print(f" FRAME {self.frame_id}  has max, min {self.max}   {self.min}")


        fd = five_database()
        self.polygons_above, self.polygons_below = fd.get_range(self.frame_id)







        self.confirmed = ()
        self.possible = ()
        #obtain



        self.obtain_position_of_confirmed(20)
        self.obtain_position_of_potential(40)

        # ----------------------------------------------------------

        self.clx = self.centre[0]
        self.cly = self.centre[1]
        # --------------------------------------------------




        self.current_angle = 0
        self.current_line_segment = 0
        self.temp_position = ()





        self.list_confirmed = []
        self.list_overlap = []
        self.list_possible = []
        self.list_of_relative_locks = []




    def single_importance_ratios(self):

        for frg in self.fragments:

            frg.width_importance = frg.width_d / self.total_width_in_frame


    def obtain_furthest_and_closest_position(self):
        furthest = 0
        closest = 1000
        for frg in self.fragments:

            if frg.max_dist > furthest:
                furthest = frg.max_dist
            if frg.min_dist < closest:
                closest = frg.min_dist
        return furthest,closest




    # Obtains all fragments from frame (can be improved: minimum angle
    def obtain_fragments_from_db(self):

        self.minimum_angle_of_productivity = -90
        all_bottoms_found = True
        current_lowest = 90

        for frg in five_database.obtain_fragments(self.frame_id):
            f = nine_fragment.nine_fragment(frg[0], self.frame_id, frg[1], frg[2], frg[3], frg[4],
                                                frg[5], frg[6], frg[7], frg[8], frg[9],
                                                frg[10], frg[11], frg[12], self)
            self.fragments.append(f)
            #CONTINUES BELOW BOTTOM RANGE

            self.total_width_in_frame = self.total_width_in_frame + frg[11]




            #If one continues
            if frg[3] == True:
                all_bottoms_found = False;
            #SETTING BOTTOM TO BE LOWEST KNOWN
            else:
                current_lowest = min(current_lowest, frg[1])

    #ANGLE IS HEIGHT
    def make_line_segments(self, angle):

        for fragment in self.fragments:
            p = fragment.get_point_in_direction_rel(fragment.get_direction_at_angle(angle), fragment.max_dist)

            fragment.linestring = LineString([(self.clx, self.cly), p])


    def make_set_line_segments(self, xy, ver_angle, use_bottom):

        for fragment in self.fragments:

            if use_bottom:
                hor_angle = fragment.get_direction_at_angle(fragment.base_d)
                start_point = self.move_random_along_angle(hor_angle, fragment.min_dist, xy)
                end_point = self.move_random_along_angle(hor_angle, fragment.max_dist, xy)


            fragment.current_line_segment = LineString([start_point, end_point])





        # UNCHANGED FOR ANGLE, NEEDS TO BE CHANGES WHEN MOVE POSITION


    def deg(self, degree):
        return 360 - degree + 90
    #BASE ON OVERLAP OF SHAPES, LIMIT DISTANCE AS WELL

    #MOVES ALONG ANGLE (TOWARD IF >0) at specified fraction of accuracy
    def move_along_angle(self, angle, fractional_change_toward):
        angle = math.radians(angle)
        dx = 2*self.accuracy*fractional_change_toward*math.sin(angle)
        dy = 2*self.accuracy*fractional_change_toward*math.cos(angle)
        pot_x = self.clx + dx
        pot_y = self.cly + dy

        # IF CAN BE MOVED

        self.clx = pot_x
        self.cly = pot_y


        return 2
        # IF HALF FOUND MAKE IT TRUE


    def move_random_along_angle(self, angle, absolute, xy):
        angle = math.radians(angle)
        dx = absolute * math.sin(angle)
        dy = absolute * math.cos(angle)

        return (dx + xy[0], dy + xy[1])








    def obtain_position_of_confirmed(self, distance):
        middle = (self.left_range + self.right_range) / 2

        self.reset_to_centre()
        self.move_along_angle(self.left_range, 0.5)
        p1_1_x = self.clx
        p1_1_y = self.cly
        self.move_along_angle(self.right_range, 100)
        p1_2_x = self.clx
        p1_2_y = self.cly
        self.reset_to_centre()
        self.move_along_angle(self.right_range, 0.5)
        p2_1_x = self.clx
        p2_1_y = self.cly
        self.move_along_angle(self.left_range, 100)
        p2_2_x = self.clx
        p2_2_y = self.cly
        self.reset_to_centre()
        l1 = LineString([(p1_1_x,p1_1_y ), (p1_2_x, p1_2_y)])
        l2 = LineString([(p2_1_x, p2_1_y), (p2_2_x, p2_2_y)])
        intersection = l1.intersection(l2)
        self.confirmed = (intersection.x, intersection.y)

        self.confirmed = Polygon([self.confirmed,
                                 self.move_random_along_angle(self.left_range, distance, self.confirmed),

                                 self.move_random_along_angle((self.left_range + middle) / 2, distance,
                                                              self.confirmed),

                                 self.move_random_along_angle(middle, distance, self.confirmed),
                                 self.move_random_along_angle((middle + self.right_range) / 2, distance,
                                                              self.confirmed),

                                 self.move_random_along_angle(self.right_range, distance, self.confirmed)])



    def obtain_position_of_potential(self, distance):
        middle_angle = (self.left_range + self.right_range) / 2

        self.reset_to_centre()
        self.move_along_angle((self.left_range + self.right_range)/2, -0.5)

        self.possible = (self.clx, self.cly)
        self.possible = Polygon([self.possible,
                                  self.move_random_along_angle(self.left_range, distance, self.possible),


                                 self.move_random_along_angle((self.left_range + middle_angle) / 2, distance,
                                                              self.possible),


                                  self.move_random_along_angle(middle_angle, distance, self.possible),
                                 self.move_random_along_angle((middle_angle + self.right_range) / 2, distance,
                                                              self.possible),

                                  self.move_random_along_angle(self.right_range, distance, self.possible)])

        self.reset_to_centre()






    def distance(self, xy1, xy2):
        return math.sqrt( (xy1[0] - xy2[0])**2 + (xy1[1] -xy2[1])**2 )


    def max_distance(self, t1, t2):
        # THE MAXIMUM 2 POINTS CAN BE AWAY FROM EACH OTHER
        return (1 + abs(t1 - t2)) * one_directory.tech_3_unit*10





    #RETURNS TRUE, IF POINT IS WITHIN CIRCLE
    def within_circle(self, x, y, multipler):
        return (x - self.x)*(x - self.x) + (y - self.y)*(y - self.y) < self.accuracy*self.accuracy*multipler


    def reset_to_centre(self):
        self.clx = self.centre[0]
        self.cly = self.centre[1]








