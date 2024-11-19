

from one_directory import one_directory
#from three_image_det import three_image_det
#ID OF DIRECTORY TO PULL FRAME FROM
directory_id = 1

#Location Of Directory To Put in:
location_input_directory = "ddddd"

#Location of Directory To Output
location_output_directory = "eeeeee"




#Trim From Hor Edges (Due to potential minimal view at edges)
error_0 = 0.5    #(Degrees)



# SUB TECHNIQUE ALLOWANCE:
# -----------------------------------------------------------------------------
# Utilize Technique 1 (Base Comparison/Relative)
tech_1 = True
# Tolerated Range Degree
tech_1_unit = 0
# -------------------------------------
# Utilize Technique 2 (Base Comparison/Absolute)
tech_2 = True
# Range Vertical
tech_2_range = (1, 2)
# --------------------------------------------------------------------------
# Utilize Technique 3 (Time/Distance Constraints)
tech_3 = True
# Maximum Meters Per Second
tech_3_unit = 5
# ------------------------------------------------------------------------
# Utilize Technique 4 (Instance Extremity/Maximum)
tech_4 = True
# Maxium Radius
tech_4_unit = 5
# ------------------------------
# Utilize Technique 5 (Instance Extremity/Minimun)
tech_5 = True
# Minimum Radius (Likely Depends on Det)
tech_5_unit = 0.02


# Utilize Technique 6 (Direction Tracking)

# (idea, if trees are directly facing each other, trunk should be opposite directions, or about same magnitude
# (idea, if trees are directly perpendicular 






def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.

    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

    #Begins Taking Photos

    #three_image_det.set_up("ResNext-101_fold_01.pth")  #ResNext-101_fold_01.pth

    #

    #neg_one_reading.extract("OLDOUTPUT/12.jpg", 100, 100)
    print("PASSE D HER")

    #three_image_det.create_video_predictions("VIDEOS/forest_walk_1min.mp4")


    dir = one_directory("C:\\Users\\ldunc\\OneDrive\\Documents\\pycharm-workspace\\ForestMapping\\TestH", \
                        "C:\\Users\\ldunc\\OneDrive\\Documents\\pycharm-workspace\\ForestMapping\\TestHVids\\BQNQE7517.MOV")

    










    # mydir = Directory(1, 'C:/Users/ldunc/OneDrive/Documents/COMSCI STUFF (PREVIOUSLY JUST IN DOCUMENTS)/TP_Resources/TestImages')


    # my_new_frame = Frame("testImages/room2.JPG")


    # my_frame = Frame("img_1")
    # my#_frame.new_x = 964
    # my_frame.new_y = 1161


    # myDet = Image_Detector(model_to_use = "X-101_RGB_60k.pth")
    # myDet.mask_on_image("testImages/img_1.png", my_frame)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
