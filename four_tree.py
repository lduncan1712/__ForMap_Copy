import math

import cv2
import numpy as np

import one_directory


class four_tree:
    def __init__(self, frame, keypoints, box, id):
        self.angle = None
        self.bottom_starting_y = None

        self.super_frame = frame
        self.kp = keypoints
        self.box = box
        self.id = id







        # NEED CALCULATION FOR WHERE BOTTOM BOX IS IN RELATION TO INSIDE FRAME


        if not one_directory.det_testing:

            self.set_tree_measurements()



    #Makes a Rectangle to be applied on visualization, with optional horizontal error bounds
    def quad_segmentation(self, additional_error, top, bottom, slope):

        top = self.point_list[top]
        bottom = self.point_list[bottom]

        #hor_width = math.sqrt(  (self.abs_w*self.abs_w)  / ( (self.slope_list[slope])*(self.slope_list[slope]) + 1 )) / 2

        hor_width = self.abs_w / 2



        #hor width = SQRT(abw^2 / (s^2 + 1),,,,   slope of normal way

        # USE SQUARE TOPS INSTEAD OF NEW
        tr = (int(top[0] + hor_width), int(top[1]))
        tl = (int(top[0] - hor_width), int(top[1]))
        bl = (int(bottom[0] + hor_width), int(bottom[1]))
        br = (int(bottom[0] - hor_width), int(bottom[1]))
        corners = np.array([tl, tr, bl, br])

        return corners

    def set_tree_measurements(self):
        kp = self.kp
        box = self.box

        #WITHIN FRAME, ABSOLUTE DIMENSIONS
        self.abs_h = int(math.hypot(kp[4][0] - kp[0][0], kp[4][1] - kp[0][1]))
        self.abs_w = math.hypot(kp[1][0] - kp[2][0], kp[1][1] - kp[2][1])



        #PIXEL SLOPE (AMOUNT OF X MOVE FOR EVERY Y CHANGE)
        s0 = -1*(((kp[4][0] - kp[0][0])/self.super_frame.x)*self.super_frame.HAOV)       /   (((kp[4][1] - kp[0][1])/self.super_frame.y)*self.super_frame.VAOV)     #ALL
        s2 =  -1*(((kp[4][0] - kp[3][0])/self.super_frame.x)*self.super_frame.HAOV)         /       (((kp[4][1] - kp[3][1])/self.super_frame.y)*self.super_frame.VAOV)    #TOP
        s1 = -1*(((kp[3][0] - kp[0][0])/self.super_frame.x)*self.super_frame.HAOV)          /     (((kp[3][1] - kp[0][1])/self.super_frame.y)*self.super_frame.VAOV)     #BOTTOM
        self.slope_list = [s0, s1, s2]


        #ADD NEW SLOPE FOR NEW_TOP AND BOTTOM?????

        p0 = (int(kp[3][0]), int(kp[3][1]))  #Centre

        p2 = (int(kp[4][0]), int(kp[4][1]))  #Top
        p1 = (int(kp[0][0]), int(kp[0][1]))  #Bottom
        self.point_list = [p0, p1, p2]


        #POINTS LEVEL WITH BOX, AT THE X THE SLOPE SAYS THEY SHOULD BE

        self.top = (self.obtain_x_coord(box[1],    2           ), int(box[1]))
        self.bottom = (self.obtain_x_coord(box[3],   1           ), int(box[3]))


        self.point_list.append(self.top)        #TOP
        self.point_list.append(self.bottom)     #BOTTOM

        self.exists_beyond_frame(0)




    def obtain_x_coord(self, y, slope):
        change = y - self.point_list[slope][1]
        return int(self.point_list[slope][0] - change*self.slope_list[slope]*self.super_frame.VAOV/self.super_frame.HAOV)





    def exists_beyond_frame(self, tolerance):

        hor_width = self.abs_w

        #IF OUTSIDE SAFE TO SAY, GOES BEYOND

        #TOP EXTENDS IF THEKEYPOINT


        #TOP WORKS
        self.top_extension = not (self.super_frame.distance_from_frame_vertical((self.point_list[3][0] + hor_width, self.point_list[3][1]), True) >= (-1)*tolerance and
                             self.super_frame.distance_from_frame_vertical((self.point_list[3][0] - hor_width, self.point_list[3][1]), True) >= (-1)*tolerance)


        #BOTTOM IS EXTENDED IF

        self.bottom_extension = (self.super_frame.distance_from_frame_vertical((self.point_list[4][0] + hor_width, self.point_list[4][1]), False) <= tolerance or
                                self.super_frame.distance_from_frame_vertical((self.point_list[4][0] - hor_width, self.point_list[4][1]), False) <= tolerance)





















