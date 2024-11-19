import os

#import three_image_det
#from eigth_simple_frame import eight_simple_frame
from final_mover import final_mover                       #############
from five_database import five_database
from master import master
from new_detection import new_detection
from pure_mover import pure_mover
from purism_everything import purism_everything
from six_plots import six_plots

#from two_frame import two_frame
from updated_visualizer import updated_visualizer



directory_name = "C:\\Users\\ldunc\\OneDrive\\Documents\\pycharm-workspace\\ForestMapping\\Tests\\Test 19\\Photos"
video_name = "C:\\Users\\ldunc\\OneDrive\\Documents\\pycharm-workspace\\ForestMapping\\Tests\\Test 19\\JMZAE1363.MOV"

ratio_of_pixels = 2.8933

starting_id = 6793000
ending_id = 6770010

horizontal_angle_of_view = 108
vertical_angle_of_view = 85

every_nth_frame = 3
behind_number = 4



#-------------------------------------------
#True: positions locations randomly, False: uses GPS
initial_location_random = True

#Number Of Movement Iterations Done
movement_iteration = 1000



#SETTINGS THAT SEEM TO WORK:: 09/10  9:50

                                     # 10:54 (POLY, OD, PM)




p_max_speed = 2
p_area_tolerance = 0.8

p_min_degree_width_to_start_cutting = 1
p_min_radius = 0.0 #(if not above, 0)
p_max_radius = 0.5


#SMALLEST ANGLE TO BE USED TO MAKE POLYGON
# ANGLE FOR ANGLES TO BE PUSHED TOGETHER
m_line_polygon_angle = 0

#SMALLEST ANGLE TO BE USED TO MAKE INTERSECTION
m_intersection_angle = 10

#Method Of Weighting
# 0 = Every Intersection Equal
# 1 = Every Tree Equal
m_weighting_scheme = 0










#------------------------------
#Smallest Angle For Use Of Intersection
m_angle_intersection = 10

#SMALL ANGLE OF USE OF LINES
m_angle_lines = 0

m_error_fraction = 0.5  #0.5 is all








#PERHAPS SYSTEM, WHEN BIG (REAL CLOSE), CAN BE CLOSER





#Distance Exponent
m_dist_exp = 0.9



m_jitter = 0.1

m_multiplier = 1

#IF NONE LOCKED = -1
# ELSE:  whichever index
m_have_locked_index = -1


#WITH THIS UPDATE:
#09-07- 7:38



# 0, with original  00, 11, || 00, 11   == 32 (RANDOM)
#                   1   0      1   0    == BAD (WHY?????)

#MOVING ONLY HALF   Y              N



# 0, with original dumb cypher gives 24/35 (GOOD)


# 0, with select 2                    0.9/6  (BAD)
# 0, with random 2                     3/14 (BAD)
# 0, with all 4,                       3/16 (BAD)
# 1, with all 4,                       4/19 (BAD)



#--------------------------------------

















speed =  10  #2              #10
min_speed = 0.1  #0.9      #0.5

#minimum change required to remake
area_tolerance = 0.8

#angle appart 2 segs must be to be considered valid
angle_variety = 10


#minimum number of segments to be considered
minimum_number_of_segs = 2

#minimum weight (at larger distances)
distance_exponent = 0.9

wiggle_distance = 0.1

automatic_placement = False     #F

#ONLY VALID WHEN ABOVE IS FALSE (when true places starting location as specficied)
care_about_initial_position = False   #F


# 0 (means every intersection equal)
# 1 (means every tree equal)
# 2 (means linear scale)
method_of_tree_weighting = 0

care_about_complex = True   #T

#IMPORTANT VALUE OF TREES (DETECTED?????????)
error_tolerance = 0.4

iterations_to_do = 1








speed_per_second = 2







class one_directory:

    def __init__(self, d_name, video_location):

        #RUNS CREATING FROM VIDEO
        ###m = master()


        #a = five_database()
        #
        #
        #
        #     v = [19.186541971201112, 22.106952572469623, 22.80044908285558, 25.47760242643329, 19.930671285397164, 16.710368949959513, 8.108281081838177, 18.346107422200202, 26.21586806981379, 14.585681952140515, 22.322212691517503, 15.752783181594896, 15.266484051642744, 22.348234740772256, 17.744755648242954, 23.671221415303137, 23.566071338395304, 15.520383256091172, 19.10020038588924, 25.526952004682638]
        #     tot = 0
        #     for x in v:
        #         tot += x
        #
        #     print(tot/len(v))
        #
        #
        #
        #up = updated_visualizer()
        #pm = pure_mover()
        #
        #fm = final_mover()
        #
        pe = purism_everything();





        # id = starting_id
        # dir_id = 1
        # add = False;
        #
        # nd = new_detection.begin_work(True, d_name, video_location)
        #
        #
        #
        #
        #
        #
        #
        # if add == True:
        #     #Creates Skeleton Frames of Key Points, AND ANGLES
        #     angles_of_roll = []
        #     angles_of_down = []
        #     angles_of_direction = []
        #     names = []
        #
        #     for name in os.listdir(directory_name):
        #         tf = two_frame(directory_name + '\\', name, id, dir_id, True)
        #         print(f"PHOTO ID:  {id}")
        #         # print(tf.roll)
        #         # print(tf.tilt)
        #         #ID NUMBER TO BE ID FOR FRAME
        #         angles_of_roll.append(tf.roll)
        #         angles_of_down.append(tf.tilt)
        #         angles_of_direction.append(tf.gps_direction)
        #         names.append(name)
        #         id+=1
        #
        #     #Creaters
        #     list = three_image_det.three_image_det.frames_between_black(video_name)
        #     print(f"BREAKDOWN OF WORK: {list}")
        #     print(f"BREAKDOWN OF ROLL: {angles_of_roll}")
        #     print(f"BREAKDOWN OF TILT: {angles_of_down}")
        #     print(f"BREAKDOWN OF DIRECTION: {angles_of_direction}")
        #
        #
        #     three_image_det.three_image_det.omni_create_video_predictions(video_name, list,  angles_of_roll, names, angles_of_down, angles_of_direction)
        #
        # else:
        #     
        #
        #




