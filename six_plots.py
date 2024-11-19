import time
import random

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import eigth_simple_frame
from matplotlib import patches
from shapely import LineString, get_point
from shapely.plotting import plot_line, plot_points
from matplotlib.patches import Wedge

from five_database import five_database
import ten_segments

#corner = five_database.obtain_plot_baseline(1, 200)[0]


class six_plots:

    def __init__(self, directory_id):
        # Directory id to use
        self.directory_id = directory_id
        # Obtaining from database, this directory
        self.set_up_plot(directory_id)

       #
        self.make_plot()

    @staticmethod
    def get_corner():
        return corner

    # completes all required plot set up
    def set_up_plot(self, directory_id):

        self.main_list = []

        # obtaining all frame from database (can be improved)
        for frame in five_database.obtain_frames(directory_id):
            # Assuming Id's Start With 0
            self.main_list.append(
                eigth_simple_frame.eight_simple_frame(frame[0], frame[1], frame[2], frame[3], frame[4], frame[5], frame[6]))

        print("SP: CREATING ALL FRAMES FROM DB (PUTTING IN LIST)")
        print(f"({len(self.main_list)})self.main_list")


    def make_plot(self):
        fig, ax = plt.subplots()

        # Creates intersection list (and possible, impossible)
        self.ts = ten_segments.ten_segments(self.main_list)

        print("CREATES A TS OBJECT (FOR LATER)")




        self.ts.tech_3_pre_clean()

        print("APPLYING A TECHNIQUE 3 PRECLEAN, ON FRAMES IN LIST")



        print("ASSIGNING COLOR TO USE FOR EVERY FRAME")
        print("AND PLOTS CIRLCES ON FIRST PLOT")
        for index, frame in enumerate(self.main_list):
            color = tuple([random.random() for _ in range(3)])

            frame.color_to_use = color
            print(f"     {index}: {color}")


            #plots archeic, confirmed, possible ----------------------------------------------------------- NOT SET FOR PRECLEAN
            ax.fill(*frame.confirmed.exterior.xy, color="green", alpha=0.1)
            ax.fill(*frame.possible.exterior.xy, color='blue', alpha=0.1)

            # creates bounds (where could be)
            plt.plot(*frame.bound.exterior.xy, color=color)
            #creates all main dots
            plt.plot(frame.clx, frame.cly, marker="o", color=color)



        f1, f2, f3,f4 = self.main_list[1], self.main_list[2], self.main_list[0], self.main_list[0]

        print("BEGINING SOLVE 2 SYSTEM (CAN BE CHANGED!!!!!!!!!!)")
        self.ts.solve_system_two_vector(f1, f2)



        plt.grid()
        plt.show()

    def deg(self, degree):
        return 360 - degree + 90
