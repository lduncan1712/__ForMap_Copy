import math
from random import random
import numpy as np
import torch
from torchvision.ops import box_convert, box_area

from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.data import MetadataCatalog
from detectron2.utils.video_visualizer import VideoVisualizer
from detectron2.utils.visualizer import ColorMode, Visualizer
from detectron2 import model_zoo
from detectron2.layers import interpolate
import os
import imutils
from scipy import ndimage
from shapely.geometry import Point, Polygon
from shapely.geometry import Polygon
import cv2

import master
import one_directory
#import two_frame
#from five_database import five_database
from new_detection_db import new_detection_db
from new_detection_photo import new_detection_photo
from new_tracking import new_tracking
#from ten_segments import ten_segments
#from tracking import tracker


class new_detection:


    #REQUIRED SETUP FOR DETECTION
    def set_up(self, model_to_use):
        cfg = get_cfg()
        cfg.INPUT.MASK_FORMAT = "polygons"  # ??
        cfg.MODEL.DEVICE = "cpu"

        # self.cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/faster_rcnn_R_101_FPN_3x.yaml"))
        # self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Detection/faster_rcnn_R_101_FPN_3x.yaml")

        cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
        cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")

        cfg.merge_from_file(model_zoo.get_config_file("COCO-Keypoints/keypoint_rcnn_X_101_32x8d_FPN_3x.yaml"))
        cfg.MODEL.WEIGHTS = os.path.join("./model", model_to_use)
        cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = one_directory.error_tolerance
        cfg.MODEL.ROI_KEYPOINT_HEAD.NUM_KEYPOINTS = 5
        global predictor
        predictor = DefaultPredictor(cfg)

        global tree_metadata
        tree_metadata = MetadataCatalog.get("my_tree_dataset").set(thing_classes=["Tree"],
                                                                   keypoint_names=["kpCP", "kpL", "kpR", "AX1", "AX2"])


    @staticmethod
    #REQUIRES WORK
    # GETS RANGES WITH BLACK
    def frames_between_black(link):
        distance = []
        between = []
        # assume start is pre
        vcap = cv2.VideoCapture(link)

        position = 0;
        time_since_black = 0;
        number_of_black = 0

        b = 0
        w = 0
        t = 0

        prev_was_black = False
        pos1 = 0
        pos2 = 0
        current_pos = 0

        while (vcap.isOpened()):
            ret, frame = vcap.read()
            # if frame is read correctly ret is True
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break

            # BLACK
            if cv2.mean(frame)[0] < 40:

                # Continue Black
                if prev_was_black:
                    b += 1
                # Starting Black
                else:
                    b += 1
                    pos1 = t
                    prev_was_black = True
            # WHITE
            else:
                # MEANS END OF SNAP
                if prev_was_black:
                    pos2 = t
                    distance.append((pos1, pos2 - 1))
                    prev_was_black = False
                    w += 1

                # Continuing White
                else:
                    w += 1
            t += 1

        return distance


    def begin_work(self, use_photos, photo_directory_name, video):

        # CREATE PHOTO LIST
        if use_photos:

            #BASIC PHOTOS
            # angles_of_roll, down, direction,   and names
            if True:
                self.roll = []
                self.down = []
                self.direction = []
                self.names = []




                index = master.starting_id

                for name in os.listdir(photo_directory_name):
                    #print("PHOTO")
                    detection_photo = new_detection_photo(photo_directory_name + "\\" + name, index)
                    self.roll.append(detection_photo.roll)
                    self.down.append(detection_photo.tilt)
                    self.direction.append(detection_photo.gps_direction)
                    self.names.append(detection_photo.path)
                    index+=1

                self.list_of_between_black = new_detection.frames_between_black(video)


                del self.list_of_between_black[0]



                self.detection_with_photos(video)


        #NO PHOTOS
        else:
            print("NO PHOTO DEFINED")


    def detection_with_photos(self, video):
        tree_metadata = MetadataCatalog.get("my_tree_dataset").set(thing_classes=["Tree"],
                                                                   keypoint_names=["kpCP", "kpL", "kpR", "AX1",
                                                                                   "AX2"])
        #NESTED SETUP
        if True:
            # Format at Video
            vcap = cv2.VideoCapture(video)
            vid_vis = VideoVisualizer(metadata=tree_metadata)

            # Obtain Info
            w = int(vcap.get(cv2.CAP_PROP_FRAME_WIDTH))
            h = int(vcap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            #print(f"VIDEO {w} {h}")

            fps = int(vcap.get(cv2.CAP_PROP_FPS))
            n_frames = int(vcap.get(cv2.CAP_PROP_FRAME_COUNT))

            #print(fps)
            #print(n_frames)

        #BEGINING VIDEO
        if True:
            frame_index = 0
            major_index = 0

            self.tracker = new_tracking()
            self.db = new_detection_db()
            self.db.setup_tracker(self.tracker)
            while(vcap.isOpened()):
                ret, frame = vcap.read()

                #print(type(frame))

                if not ret:
                    print("CANT RECIEVE, ENDING")
                    break


                assess, angle, tilt, change, main = self.determine_everything_using_index(frame_index, major_index)

                #MEANING ITS VALUABLE
                if assess:

                    if main:
                        frame_to_apply = cv2.imread(self.names[major_index])
                    else:

                        frame_to_apply = frame


                        to_get_to = self.list_of_between_black[major_index][0]
                        came_from = self.list_of_between_black[major_index - 1][1]


                        total_frames_between =  to_get_to - came_from





                        frame_to_apply = cv2.resize(frame, (master.photo_x, master.photo_y))
                        #SCALE MABYBE???




                    #print(frame.shape)

                    image_with_pred, kp, b, c, h, w = self.apply_detection(frame_to_apply, angle, vid_vis)
                    #print("DOING SINGLE ITERATION")

                    self.tracker.update_list(kp, b, c, main, major_index, vid_vis)

                    if main:
                        print("DOING MAJOR")
                        indexs_impacted = self.db.send_to_database(tilt, angle, w, h, major_index)

                        self.tracker.update_for_connections(indexs_impacted)





                    image_with_pred = image_with_pred.get_image()

                    cv2.circle(image_with_pred,
                               (0, 0),
                               10,
                               (255, 1, 1),
                               -1)

                    for corner in self.get_corners(w, h, angle):
                        cv2.circle(image_with_pred,
                                   (int(corner[0]), int(corner[1])),
                                   10,
                                   (255, 1, 1),
                                   -1)

                    #image_with_pred = self.print_on_image(image_with_pred, main)


                    for pt in vid_vis._old_instances:
                        if pt.ttl == 8:
                            cv2.putText(image_with_pred,
                                    f"{pt.absolute_index}!!!!!!!!",
                                    (int(pt.key_points[0][0]), int(pt.key_points[0][1])),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    2,
                                    (0, 0, 0),
                                    2,
                                    cv2.LINE_AA)




                    cv2.imwrite("C:\\Users\\ldunc\\Downloads\\" + "HIGH!" + str(frame_index) + str(main) + ".jpg", image_with_pred)




                #MEANING WE CHANGE THE MAJOR
                if change:
                    major_index +=1

                    if major_index == len(self.names):
                        return


                frame_index+=1
                #NOW UPDATE LIST

    def print_on_image(self, image_with_pred, major):

        for index in range(0, len(self.tracker.list_of_colors)):

            last_point = self.tracker.list_of_points[index][-1]

            if last_point is None:
                continue


            color = self.tracker.list_of_colors[index]
            ab_index = self.tracker.absolute_index[index]
            #print(color)

            length_of_existance = len(self.tracker.list_of_points[index])

            if major:
                size = 2
            else:
                size = 1

            cv2.circle(image_with_pred,
                       (int(last_point[0][0]), int(last_point[0][1])),
                       size*10,
                       (int(255*color[0]), int(255*color[1]), int(255*color[2])),
                        -1)


            cv2.putText(image_with_pred,
                         f"{ab_index} {length_of_existance}",
                         (int(last_point[0][0]), int(last_point[0][1])),
                         cv2.FONT_HERSHEY_SIMPLEX,
                         size,
                         (0,0,0),
                         2,
                         cv2.LINE_AA)
        return image_with_pred






        #PRINT IDS OF TREES:

        #PRINT PREVIOUS POINTS OF TREES??

        #PRINT COLORS OF PREVIOUS TREES??

        #PRINT TIME SINCE DISAPEARANCE???






    def apply_detection(self, frame, angle_change, vid_vis):
        tilted_image = ndimage.rotate(frame, angle_change,
                                      mode='constant', cval=600)
        height, width, shape = tilted_image.shape
        #print(f" {width} {height}")


        predictions = predictor(tilted_image)
        predictions["instances"].remove("scores")
        #predictions["instances"].remove("title")


        index_within_predictions_to_keep = self.omni_corner_filter(width, height, angle_change, predictions)

        predictions_within_corners = predictions["instances"][index_within_predictions_to_keep]

        image_with_pred, c = vid_vis.draw_instance_predictions(tilted_image,
                                                                    predictions_within_corners.to("cpu"))


        kp = predictions_within_corners._fields['pred_keypoints'].numpy()
        b = predictions_within_corners._fields['pred_boxes'].tensor.numpy()

        # kp, b, c = self.sort_by_left_right(keypoints, boxes, colors)
        #
        # print(kp)
        #
        # kp, b, c = self.filter_further_suggestions(kp, b, c)
        #
        #
        # #kp, c, b = self.tracker.omni_clean_list_for_duplicates(c, kp,b)
        #



        #self.tracker.confirm_uniqueness(c)


        return image_with_pred, kp, b, c, height, width


    def get_corners(self, x, y, roll):

        angle = math.radians(abs(roll))
        #print(f" {roll} {angle}")
        p1 = int((y * math.sin(angle)))  # + RS
        p2 = int((x * math.cos(angle)))  # + LS
        p3 = int((math.cos(angle) * y))  # + Bott
        p4 = int((math.sin(angle) * x))  # + Top
        #print(f" {x} {y}")
        #print(f" {p1} {p2} {p3} {p4}")

        if roll >= 0:
            # Left,    TOP,        Right,       Bottom
            old_corners = [(0, p4), (p2, 0), (x, p3), (p1, y)]
        else:
            # Bottom                 Right,              Top,           Left
            old_corners = [(x - p1, y), (x, p4), (p1, 0), (0, y - p4)]
                                                    ###################

            #print(f" {x} {p1}    {y}     {x} {p4}     {x} - {p2}  0      0 {p3}")

        #print(old_corners)
        return old_corners





    #RETURNS WHETHER TO ASSESS
    #ANGLE
    #CHANGE MAJOR

    def filter_further_suggestions(self, points, boxs, colors):
        new_points = []
        new_boxes = []
        new_colors = []

        for index in range(0, len(points)):

            p_o = points[index]

            if p_o[1][0] == p_o[2][0]:
                continue
            else:
                new_points.append(p_o)
                new_boxes.append(boxs[index])
                new_colors.append(colors[index])

        return new_points, new_boxes, new_colors

    def determine_everything_using_index(self, index, major):

        #MEANS BEFORE
        if major == 0 and self.list_of_between_black[major][0] > index:
            print(f"{major} {index} BEFORE")
            return False, None, None, False, False


        #MEANS THE FIRST ONE (TO DO)
        if self.list_of_between_black[major][0] == index:
            print(f"{major} {index}  FIRST BLACK MAJOR {major}")
            return True, self.roll[major], self.down[major], False, True


        #MEANS LAST IN BLACK (CHANGE DO NOTHING)
        if self.list_of_between_black[major][1] == index:
            print(f"{major} {index}  FIRST BLACK MAJOR {major}")
            return False, None, None, True, False



        #IF OTHERWISE IN BETWEEN (DO NOTHING)
        if self.list_of_between_black[major][0] <= index <= self.list_of_between_black[major][1]:
            #print(f"{major} {index}    B")
            return False, None, None, False, False

        #MEANS ITS IN RANGE BEFORE BLACK (THIS SHOULDNT HAPPEN IF 0, meaning major n-1 is possible
        else:

            #IF WRONG INDEX
            if index % master.n_th_frames != 0:
                return False, None, None, False, False
            else:

                start = self.roll[major - 1]

                angle_to_change = self.roll[major] - self.roll[major - 1]

                time_to_change_it = self.list_of_between_black[major][0] - \
                                    self.list_of_between_black[major - 1][1]

                what_fraction_were_in = index - self.list_of_between_black[major - 1][1]


                angle = start + (angle_to_change*(what_fraction_were_in/time_to_change_it))

                print(f" {major} {index}   NORMAL: ")
                return True, angle, None, False, False

    def sort_by_left_right(self, list1, list2, list3):
        #INDEX
        sorted_index = sorted(range(len(list1)), key=lambda k: list1[k][0][0])
        print(sorted_index)


        sorted_list1 = [list1[i] for i in sorted_index]
        sorted_list2 = [list2[i] for i in sorted_index]
        sorted_list3 = [list3[i] for i in sorted_index]
        return sorted_list1, sorted_list2, sorted_list3

    def omni_corner_filter(self, x, y, roll, predictions):

        # Calculate Corners (OLD CORNERS):
        if True:
            old_corners = self.get_corners(x,y,roll)

            #print(old_corners)

        # Create Polygon Representing Old (Polygon)

        #print(f" OLD CORNERS (SHOULD BE IN ORDER) {old_corners}")

        polygon = Polygon(old_corners)

        index_list_to_keep = []

        for index, tree in enumerate(predictions["instances"]._fields['pred_keypoints'].numpy()):
            required_remaining = 1
            #print("TREE")
            for index_in, key_point in enumerate(tree):
                shapely_point = Point(key_point[0], key_point[1])

                if not polygon.contains(shapely_point):
                    required_remaining -= 1
                    #print(f"REMOVING {shapely_point}")

            if required_remaining >= 0:
                index_list_to_keep.append(index)
                #print("KEEPING")
                #print(f" KEEPING {index}")
            # else:
            #     print(f"REMOVING INDEX {index}")

        return torch.tensor(index_list_to_keep, dtype=torch.long)





























    @staticmethod
    def detection_without_photos():
        print("DETECTION WITHOUT PHOTOS")

