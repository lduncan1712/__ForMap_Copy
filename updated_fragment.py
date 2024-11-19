import math

import one_directory


class updated_fragment:


    def __init__(self, values):

        self.id = values[0]
        self.base_deg = values[1]
        self.peak_deg = values[2]
        self.p0_deg = values[3]
        self.p0_dir = values[4]
        self.p1_deg = values[5]
        self.p1_dir = values[6]
        self.p2_deg = values[7]
        self.p2_dir = values[8]
        self.p3_deg = values[9]
        self.p3_dir = values[10]
        self.p4_deg = values[11]
        self.p4_dir = values[12]


        self.width = values[13]


        self.average_angle = self.p0_dir



        self.max_dist = self.calculate_distance_at_max_radius(0.5)

        if self.width > one_directory.p_min_degree_width_to_start_cutting:
            self.min_dist = self.calculate_distance_at_max_radius(one_directory.p_min_radius)
        else:
            self.min_dist = self.calculate_distance_at_max_radius(0)

        # print(f"       FRAGMENT:"
        #       f"           ID: {self.id}"
        #       f"           BASE_DEG: {self.base_deg}"
        #       f"           PEAK_DEG: {self.peak_deg}"
        #       f"            P0 - DEG: {self.p0_deg}"
        #       f"            P0 - DIR: {self.p0_dir}"
        #       f"            P4 - DEG: {self.p4_deg}"
        #       f"            P4 - DIR: {self.p4_dir}"
        #       f"            WIDTH: {self.width}"
        #       f"            MAX: {self.max_dist}"
        #       f"            MIN: {self.min_dist}")

    def calculate_distance_at_max_radius(self, radius):
        d = radius / math.tan(math.radians(self.width/2))
        return d