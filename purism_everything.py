# This Class Defines Movement Using Relative Angles
# Defined by movement within relative frame,
# measured as movement relative to centre
# with starting being either 0 or users choise of frame
from matplotlib import pyplot as plt

import one_directory
import updated_frame
from five_database import five_database
from fixed_point import fixed_point


class purism_everything:


    def __init__(self):
        self.lof = []

        #Default To First Angle
        # Obtain Corner:
        self.corners = five_database.omni_obtain_plot_baseline(1, 100)

        print(f" CORNERS: {self.corners}")

        print("CONS:")
        print(five_database().translate_entire_photo(one_directory.starting_id + 0,
                                                     one_directory.starting_id + 2))

        # Sets Up List
        self.make_list_of_photos()

        self.tree_list = self.make_trees(self.lof[0], self.lof[1],
                                           len(self.lof) - 1)

        self.compare_angle_evaluation()

        self.absolute_print_map()

        plt.show()





    # STARTING STUFF_-------------------------------------------------------------------
        # Given f1, f2, and end_range, creates tree objects
        # MAKES A SET OF TREES
    def make_trees(self, frame1, frame2, range_end):
        master_tree_list = []
        fd = five_database()

        # Create Simple First
        # (Trees That Appear In First)
        for first_index_values in range(0, len(frame1.fragments)):
            tree = fixed_point()
            val = tree.create_and_cascade(frame1.frame_id, first_index_values)
            master_tree_list.append(tree)

        # Create Complex Later
        # (Trees Thats Appear Later, but arnt already covered)
        for later_index_values in range(frame2.frame_id, range_end + 1):

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
                    val = tree.create_and_cascade(later_index_values, later_index_fragment)
                    master_tree_list.append(tree)

        return master_tree_list

    def compare_angle_evaluation(self):


        for outer_index, outer_frame in enumerate(self.lof):
            for inner_index, inner_frame in  enumerate(self.lof):
                if inner_index > outer_index:

                    print(f"  FRAMES: {outer_index}  {inner_index}  "
                          f"DIFF: {outer_frame.get_angle_relative(inner_frame.middle_average, outer_frame.middle_average)}")

                    connections = five_database().translate_entire_photo(outer_frame.frame_id, inner_frame.frame_id)

                    for connection in connections:
                        f1 = outer_frame.fragments[connection[0]]
                        f2 = inner_frame.fragments[connection[1]]

                        o_relative = 1

                        diff = outer_frame.get_angle_relative(f1.average_angle, f2.average_angle)

                        print(f" {connection}     {f1.p0_dir} {f2.p0_dir}           {f1.width} {f2.width}")






    # Obtains All Photos Within Range (od.sr - od.er
    def make_list_of_photos(self):
        print(five_database.omni_obtain_frames())
        # obtaining all frame from database (can be improved)
        for frame in five_database.omni_obtain_frames():
            # Assuming Id's Start With 0
            self.lof.append(
                updated_frame.updated_frame(frame[0], frame[1],
                                                frame[2], frame[3],
                                                frame[4], frame[5],
                                                frame[6], self))

    # Prints All Points On Map
    def absolute_print_map(self):
        fig, ax = plt.subplots()

        for perspective_location in self.lof:
            # BOUND POLYGON POSSIBLE
            ax.fill(*perspective_location.bound.exterior.xy, color=perspective_location.color, alpha=0.1)
            plt.plot(*perspective_location.bound.exterior.xy, color=perspective_location.color)

            # EXACT LOCATION
            loc = perspective_location.centre
            plt.plot(loc[0], loc[1], marker="o", color=perspective_location.color)

            # TEXT
            plt.text(loc[0], loc[1], "ID " + str(perspective_location.frame_id - one_directory.starting_id),
                             fontsize=12, color='red')

            self.absolute_time_filter()

            for perspective_location in self.lof:
                # BOUND POLYGON POSSIBLE
                ax.fill(*perspective_location.bound.exterior.xy, color=perspective_location.color, alpha=0.1)
                plt.plot(*perspective_location.bound.exterior.xy, color=perspective_location.color)

            plt.grid()

    def absolute_time_filter(self):

        for outer_index, outer_frame in enumerate(self.lof):
            # For every frame within
            for inner_index, inner_frame in enumerate(self.lof):
                    # Diagonalization to avoid repitition or equality
                    if outer_index > inner_index:
                        # Max possible distance appart (time distance)
                        distance = abs(outer_frame.time - inner_frame.time) * one_directory.speed_per_second

                        # Creates buffered Distances extending
                        fo_e = outer_frame.bound.buffer(distance)
                        fi_e = inner_frame.bound.buffer(distance)

                        # The new frame 1 possibilities are the overlap between f1, original, and f2_e
                        outer_frame.bound = outer_frame.bound.intersection(fi_e)
                        # The new frame 2 possibilities are the overlap between f2 original and f1_1

                        inner_frame.bound = inner_frame.bound.intersection(fo_e)


