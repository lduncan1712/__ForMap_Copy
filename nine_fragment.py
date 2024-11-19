import math

from shapely.geometry import Polygon, LineString

import six_plots

from matplotlib import patches




class nine_fragment:
    def __init__(self, id, parent_id, base_d, base_dir, base_c, div_d, peak_d, peak_dir, peak_c, s_o, s_u, s_l, width_d, width_e, parent):
        self.id = id
        self.parent_id = parent_id
        self.parent = parent

        self.current_direction = base_dir
        self.line = 0

        #PERMANANT SHAPE
        self.wedge = 0;

        #PERMANANT DATA
        self.base_d = base_d  #DEGREE AT BASE
        self.base_dir = base_dir
        self.base_c = base_c  #IF BASE CONT
        self.div_d = div_d  #DEG FOR DIVIDE
        self.peak_d = peak_d  #DEG AT PEAK
        self.dir = peak_dir
        self.peak_c = peak_c  #PEAK CONTINUES
        self.s_o = s_o  #SLOPES
        self.s_u = s_u
        self.s_l = s_l
        self.width_d = width_d
        self.width_e = width_e


        self.linestring = 0

        self.max_dist = self.calculate_distance_at_max_radius(0.35)
        self.min_dist = self.calculate_distance_at_max_radius(0.05)



        # WHETHER ALL ON SAME SIDE
        #1 = Positive Const,      0 = Not Const,         Red = Neg Consistant
        self.angle_consistant = self.determine_angle_consistency(0.01)


        #WHETHER WITHIN STRAIGHT UP RANGE
        # Straight = Green (1),        Not = Red (0)
        self.angle_straight = self.determine_overall_straight(0.1)

        # IF ALL WITHIN A CLOSENESS (IF STRAIGHT PROBABLY CLOSE)
        #self.angle_closeness = self.determine_closeness()



    #OBTAINS THE CENTRE VALUE AT GIVEN HEGIHT
    def get_direction_at_angle(self, height):
        #ABOVE HALF, USE TOP POINT AS REFERENCE
        if(height > self.div_d):
            return self.peak_dir + (self.peak_d - height)*self.s_u % 360
        #USE BOTTOM POINT FOR REFERENCE
        else:
            return self.base_dir + (self.base_d - height)*self.s_l % 360

    #basic idea, return a point that will make up line segment, based on



    def get_point_in_direction_rel(self, angle, distance ):
        angle = math.radians(angle)
        dx =   distance * math.sin(angle)
        dy =  distance * math.cos(angle)
        pot_x = self.parent.clx + dx
        pot_y = self.parent.cly + dy
        return (pot_x, pot_y)




    #UNCHANGED FOR ANGLE, NEEDS TO BE CHANGES WHEN MOVE POSITION

    def deg(self, degree):
        return 360 - degree + 90


    def get_distance(self, point):

        return math.sqrt(    (point[0] - self.parent.clx)**2 + (point[1] - self.parent.cly)**2  )


    def get_distance_between_points(self, point1, point2):
        return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

    def calculate_rad_at_distance(self, distance):
        #USING APPROX ANGLE WIDTH
        #AND DESIRED WIDTH, CALCULATE PROBABLE
        r = distance*math.tan(math.radians(self.width_d/2))
        return r



    def calculate_distance_at_max_radius(self, radius):
        d = radius / math.tan(math.radians(self.width_d/2))
        return d

    def half_bowl_angle(self, bool_base_angle):
        if bool_base_angle:
            if self.s_l > 0:
                return (self.base_dir + 90) % 360, self.base_dir
                #print("POSITIVE")
            else:
                return (self.base_dir - 90) % 360, self.base_dir
                #print("NEGATIVE")
        else:
            if self.s_o > 0:
                return (self.base_dir + 90) % 360, self.base_dir
                #print("POSITIVE")
            else:
                return (self.base_dir - 90) % 360, self.base_dir
                #print("NEGATIVE")

    def half_angle(self, angle, start):
        if angle > 0:
            return (start + 90) % 360
        elif angle == 0:
            return start % 360

        else:
            return (start - 90) % 360







    # def get_component_elements(self, angle):
    #     return math.sin(math.radians(angle)), math.cos(math.radians(angle))


    def within_180(self, shifted_1, starting_1, shifted_2, starting_2):

        #IF DISTANCE BETWEEN IS LESS THEN 90 AND

        #LESS THEN 90 between oposite original (only need to check one)

        #DIFFERENCE BETWEEN PRIMES
        if shifted_1 > shifted_2:
            c1 = min(shifted_1 - shifted_2, abs(360 - shifted_1 + shifted_2))
        else:
            c1 = min(shifted_2 - shifted_1, abs(360 - shifted_2 + shifted_1))

        #DIFFERENCE BETWEEN PRIME AND OPPOSING NON
        if shifted_1 > starting_2:
            c2 =  min(shifted_1 - starting_2, abs(360 - shifted_1 + starting_2))
        else:
            c2 = min(starting_2 - shifted_1, abs(360 - starting_2 + shifted_1))



        if c1 <= 90:
            #print(f"PASSED c1: {round(c1,3)}   c2: {round(c2,3)}")
            return True
        else:
            #print(f"FAILED c1: {round(c1,3)}   c2: {round(c2,3)}")
            return False

              #1: Overall, #2: Upper, #3 Lower


    #DETERMINES IF ALL ANGLE GO IN SAME DIRECTION
    def determine_angle_consistency(self, error):

       if self.s_o >= 0 and self.s_l >= 0 and self.s_u >= 0:
           return 1
       elif self.s_o <= 0 and self.s_l <= 0  and self.s_u <= 0:
            return -1
       else:
           return 0



    #DETERMINES HOW CLOSE TOGETHER 3 ARE (EITHER WAY)
    def determine_closeness(self):
        return -1




    #DETERMINES HOW STRAIGHT ANGLE ARE
    def determine_overall_straight(self, n):
        #IF ALL MEASUREMENTS ARE WITHIN N OF BEING VERTICAL
        overall = abs(self.s_o) <= n
        upper = abs(self.s_u) <= n
        lower = abs(self.s_l) <= n

        return overall and upper and lower

    def convert_to_color(self, value):
        if value > 0:
            color = "green"
        elif value == 0:
            color = "black"
        else:
            color = "red"
        return color































