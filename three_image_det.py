


#
#
# import math
# from random import random
# #import numpy as np
# import torch
# from torchvision.ops import box_convert, box_area
#
# from detectron2.engine import DefaultPredictor
# from detectron2.config import get_cfg
# from detectron2.data import MetadataCatalog
# from detectron2.utils.video_visualizer import VideoVisualizer
# from detectron2.utils.visualizer import ColorMode, Visualizer
# from detectron2 import model_zoo
# from detectron2.layers import interpolate
# import os
# import imutils
# from scipy import ndimage
# from shapely.geometry import Point, Polygon
# from shapely.geometry import Polygon
#
#
# import cv2
#
#
# import one_directory
# import two_frame
# from five_database import five_database
# from ten_segments import ten_segments
# from tracking import tracker
#
#
# class three_image_det:
#
#
#     @staticmethod
#     def set_up(model_to_use):
#
#         cfg = get_cfg()
#         cfg.INPUT.MASK_FORMAT = "polygons"  # ??
#         cfg.MODEL.DEVICE = "cpu"
#
#         # self.cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/faster_rcnn_R_101_FPN_3x.yaml"))
#         # self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Detection/faster_rcnn_R_101_FPN_3x.yaml")
#
#         cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
#         cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
#
#         cfg.merge_from_file(model_zoo.get_config_file("COCO-Keypoints/keypoint_rcnn_X_101_32x8d_FPN_3x.yaml"))
#         cfg.MODEL.WEIGHTS = os.path.join("./model", model_to_use)
#         cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = one_directory.error_tolerance
#         cfg.MODEL.ROI_KEYPOINT_HEAD.NUM_KEYPOINTS = 5
#         global predictor
#         predictor = DefaultPredictor(cfg)
#
#         global tree_metadata
#         tree_metadata = MetadataCatalog.get("my_tree_dataset").set(thing_classes=["Tree"],
#                                                                    keypoint_names=["kpCP", "kpL", "kpR", "AX1", "AX2"])
#
#
#
#
#
#     @staticmethod
#     def frames_between_black(link):
#         distance = []
#         between = []
#         #assume start is pre
#         vcap = cv2.VideoCapture(link)
#
#         position = 0;
#         time_since_black = 0;
#         number_of_black = 0
#
#         b = 0
#         w = 0
#         t = 0
#
#         prev_was_black = False
#         pos1 = 0
#         pos2 = 0
#         current_pos = 0
#
#
#         while (vcap.isOpened()):
#             ret, frame = vcap.read()
#             # if frame is read correctly ret is True
#             if not ret:
#                 print("Can't receive frame (stream end?). Exiting ...")
#                 break
#
#             #BLACK
#             if cv2.mean(frame)[0] < 40:
#
#                 #Continue Black
#                 if prev_was_black:
#                    b += 1
#                 #Starting Black
#                 else:
#                     b += 1
#                     pos1 = t
#                     prev_was_black = True
#             #WHITE
#             else:
#                 #MEANS END OF SNAP
#                 if prev_was_black:
#                     pos2 = t
#                     distance.append((pos1, pos2 - 1))
#                     prev_was_black = False
#                     w += 1
#
#                 #Continuing White
#                 else:
#                     w += 1
#             t+=1
#
#
#         return distance
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#     @staticmethod
#     def omni_create_video_predictions(link, list, angles, names, down, compass):
#         tree_metadata = MetadataCatalog.get("my_tree_dataset").set(thing_classes=["Tree"],
#                                                                        keypoint_names=["kpCP", "kpL", "kpR", "AX1",
#                                                                                        "AX2"])
#         #The fraction 1/fu of frames not skipped
#         frame_use = 3
#
#         #The number of frames from MAIN, before assessment
#         variance_use = 4
#
#
#
#         #Nested_Setup
#         if True:
#
#             # Format at Video
#             vcap = cv2.VideoCapture(link)
#
#             # Obtain Info
#             w = int(vcap.get(cv2.CAP_PROP_FRAME_WIDTH))
#             h = int(vcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#
#             print(f"VIDEO {w} {h}")
#
#             fps = int(vcap.get(cv2.CAP_PROP_FPS))
#             n_frames = int(vcap.get(cv2.CAP_PROP_FRAME_COUNT))
#
#             print(fps)
#             print(n_frames)
#
#             fd = five_database()
#             fd.setup_connection_connection()
#
#         # Check if camera opened successfully
#         if (vcap.isOpened() == False):
#             print("Error opening video stream or file")
#
#         #More Nested_Setup
#         if True:
#             vid_vis = VideoVisualizer(metadata=tree_metadata)
#
#             nframes = 0
#             nphoto = 0
#             current_angle = 0
#             differential = 0
#
#             applied_already = False
#             current_angle = angles[0]
#
#             time_to_major = -1*one_directory.behind_number
#
#             first_bc = True
#             cached_colors = 0
#
#             last_completed = False
#
#         #Tracking Object
#         global t
#         t = tracker()
#
#         while (vcap.isOpened()):
#             ret, frame = vcap.read()
#
#             # if frame is read correctly ret is True
#             if not ret:
#                 print("Can't receive frame (stream end?). Exiting ...")
#                 break
#
#
#             # Means Within Black (MAIN PHOTO)
#             if not last_completed and (list[nphoto][0] <= nframes) and (nframes <= list[nphoto][1]):
#
#                 # Means Photo Already Assessed
#                 if applied_already:
#                     print(f" {nframes} WITHIN BLACK {nphoto} ALREADY APPLIED")
#                     applied_already = True;
#                 # It needs to be handled
#                 else:
#                     print(f" {nframes} WITHIN BLACK {nphoto} APPLYING")
#                     applied_already = True
#                     time_to_major = one_directory.behind_number
#
#                     path = one_directory.directory_name + '/' + names[nphoto]
#                     roll = angles[nphoto]
#
#                     image, key_points, boxes, colors, h, w = three_image_det.omni_detection(True, path, roll, vid_vis, t)
#
#                     t.confirm_uniqueness(colors)
#
#                     compacted_key_points = t.convert_points(key_points)
#                     compacted_boxes = t.convert_boxes(boxes)
#
#                     t.omni_update_list(compacted_key_points,
#                                        compacted_boxes,
#                                        colors,
#                                        True,
#                                        vid_vis)
#                     a = random()
#                     cv2.imwrite("C:\\Users\\ldunc\\Downloads\\" + "HIGH" + str(a) + ".jpg", image.get_image())
#
#                 # IF THIS IS THE LAST IN THE BLACK RANGE
#                 if nframes == list[nphoto][1]:
#
#                     # IF THIS IS THE LAST FRAME, NO BOTHER NEXT (TAKEN TOKEN 2)
#                     if nphoto + 1 == len(list):
#                         print(f"LAST PHOTO {nframes} {nphoto}")
#                         current_angle = angles[nphoto]
#                         nphoto = nphoto + 1
#                         last_completed = True
#
#                     # NOT THE LAST CAN CALCULATE ANGLE
#                     else:
#                         # print(f"MAJOR PHOTO {nphoto}")
#                         current_angle = angles[nphoto]
#                         differential = (angles[nphoto] - angles[nphoto + 1]) / (
#                                         (0.5 * list[nphoto][0] + 0.5 * list[nphoto][1]) - (
#                                             0.5 * list[nphoto + 1][0] + 0.5 * list[nphoto + 1][1]))
#
#                         applied_already = False;
#                         nphoto = nphoto + 1
#
#             # Within a valid range
#             else:
#
#                 # IF BEFORE FIRST AND MORE THEN 2 AWAY
#                 if nphoto == 0 and nframes < list[nphoto][0] - one_directory.behind_number*one_directory.every_nth_frame - 1:
#                     print(f" {nframes} INTER - TOO FAR BEFORE {nphoto}")
#
#                 #AFTER LAST AND MORE THEN 2 AWAY
#                 elif nphoto == len(list) - 1 and nframes > list[nphoto][1] + one_directory.behind_number*one_directory.every_nth_frame + 1:
#                     print(f" {nframes} INTER - TOO FAR AFTER {nphoto}")
#                     break
#
#                 # Valid To Compare
#                 else:
#
#                     applied_already = False
#                     current_angle += differential
#
#                     # FOR EVERY 5 FRAMES
#                     if nframes % one_directory.every_nth_frame == 0:
#                         print(f" {nframes} INTER USING")
#
#                         time_to_major -= 1
#
#                         image, key_points, boxes, colors, h, w = three_image_det.omni_detection(False, frame,
#                                                                                  current_angle, vid_vis, t)
#                         t.confirm_uniqueness(colors)
#
#                         image = image.get_image()
#
#                         t.omni_update_list(key_points, boxes, colors, False, vid_vis)
#
#
#                         #MEANS DO MAJOR STUFF
#                         if time_to_major == 0:
#                             print("   APPLYING MAJOR STUFF")
#
#                             # #GET LIST OF VALUED
#                             s_points, s_boxs, s_colors = t.obtain_main_trees()
#
#                             for upper_index, set_of_p in enumerate(s_points):
#                                 for index in range(0, 5):
#                                     cv2.circle(image, (int(set_of_p[index][0]), int(set_of_p[index][1])), 10, (255,255,255), -1)
#
#                             height, width = h,w
#                             #CONVERT POINTS INTO DEGREES
#
#                             height_tilt = down[nphoto - 1]
#                             direction_tilt = compass[nphoto - 1]
#
#                             degree_equivalants, degree_equivalants_boxs = three_image_det.omni_convert_pixel_to_degree(s_points, s_boxs,
#                                                                                               height,
#                                                                                               width,
#                                                                                                   height_tilt,
#                                                                                                    direction_tilt)
#
#
#                             #DETERMINE DEGREE DIFFERENCES IN WIDTH
#                             widths_horizontal = three_image_det.omni_convert_widths(degree_equivalants)
#
#
#                             #print("PRE UPLOAD")
#                             fd.omni_upload_trees_to_db(degree_equivalants,
#                                                        widths_horizontal,
#                                                        degree_equivalants_boxs,
#                                                        nphoto - 1)
#
#
#                             #MEANS FIRST MAJOR (NO PREVIOUS)
#                             if first_bc:
#                                 first_bc = False
#                                 print("      FIRST MAJOR")
#
#                                 cached_colors = s_colors
#
#                             else:
#                                 print("      NOT FIRST MAJOR")
#
#                                 previous_colors = cached_colors
#                                 current_colors = s_colors
#
#                                 connection_colors = three_image_det.omni_match_connections(previous_colors,
#                                                                                            current_colors)
#                                 fd.omni_upload_connections_to_db(nphoto - 2 + one_directory.starting_id,
#                                                                  nphoto - 1 + one_directory.starting_id,
#                                                                  connection_colors)
#
#                                 cached_colors = s_colors
#
#                             a = random()
#                             cv2.imwrite("C:\\Users\\ldunc\\Downloads\\" + "MAIN" + str(nframes) + ".jpg",
#                                         image)
#
#                         else:
#
#                             print(f" {nframes} INTER - APPLIED ----- _________ {time_to_major}")
#                             cv2.imwrite("C:\\Users\\ldunc\\Downloads\\" + "A" + str(nframes) + ".jpg",
#                                         image)
#
#
#
#
#                     else:
#                         print(f" {nframes} INTER - NORMAL")
#
#             nframes += 1
#
#             # video.release()
#         vcap.release()
#             # cv2.destroyAllWindows()
#
#     @staticmethod
#     def omni_match_connections(set1, set2):
#
#         matchs_to_return = []
#
#         for index_one, color_one in enumerate(set1):
#
#             for index_two, color_two in enumerate(set2):
#
#                 if three_image_det.compare_colors(color_one, color_two):
#                     matchs_to_return.append([index_one, index_two])
#                     break
#
#         return matchs_to_return
#
#
#
#
#
#     @staticmethod
#     def compare_colors(color1, color2):
#         return color1[0] == color2[0] and color1[1] == color2[1] and color1[2] == color2[2]
#
#     @staticmethod
#     def omni_convert_widths(list_given):
#         list_to_return = []
#
#         for tree_in_degrees in list_given:
#             val1 = tree_in_degrees[2][0]
#             val2 = tree_in_degrees[1][0]
#
#             difference_in_width_degrees = max(val1, val2) - min(val1, val2)
#
#             list_to_return.append(difference_in_width_degrees)
#
#
#
#
#         return list_to_return
#
#     @staticmethod
#     #AOV and TILT DOWN ALREADT FOUND
#     def omni_convert_pixel_to_degree(points, boxs, height_pixels, width_pixels, base_tilt, base_degree):
#         h_aov = one_directory.horizontal_angle_of_view
#         v_aov = one_directory.vertical_angle_of_view
#
#
#         list_to_return = []
#
#         list_of_boxs_to_return = []
#
#         for point_set in points:
#             inner_list = []
#             inner_box_list = []
#             for singular_point in point_set:
#                 s_x = singular_point[0]
#                 s_y = singular_point[1]
#                 degree_of_x = three_image_det.get_degree_at_x(s_x, width_pixels, base_degree, h_aov)
#                 degree_of_y = three_image_det.get_degree_at_y(s_y, height_pixels, base_tilt, v_aov)
#
#                 s_val = [degree_of_x, degree_of_y]
#
#                 inner_list.append(s_val)
#             list_to_return.append(inner_list)
#
#
#         for box_set in boxs:
#
#             inner_box_list = []
#             print(box_set)
#
#             v1 = three_image_det.get_degree_at_x(box_set[0], width_pixels, base_degree, h_aov)
#             v2 = three_image_det.get_degree_at_y(box_set[1], height_pixels, base_tilt, v_aov)
#
#             v3 = three_image_det.get_degree_at_x(box_set[2], width_pixels, base_degree, h_aov)
#             v4 = three_image_det.get_degree_at_y(box_set[3], height_pixels, base_tilt, v_aov)
#
#             inner_box_list = [v1, v2, v3, v4]
#             list_of_boxs_to_return.append(inner_box_list)
#
#
#
#
#
#
#
#
#
#         return list_to_return, list_of_boxs_to_return
#
#
#
#
#     #Returns An Applies Image, As Well as keypoints, boxes, and colors
#     @staticmethod
#     def omni_detection(bool_main, photo, roll, vid_vis, t):
#
#         #Turns To Convertible Formot
#         if True:
#             if bool_main:
#                 image = cv2.imread(photo)
#             #Can Simply Using
#             else:
#                 image = photo
#
#         #Tilting Image
#         tilted_image = ndimage.rotate(image, roll,
#                                       mode='constant', cval=600)
#         height, width, shape = tilted_image.shape
#
#         #Getting Predictions:
#         predictions = predictor(tilted_image)
#
#         #Filtering Trees In Corners
#         keep = three_image_det.omni_corner_filter(width, height, roll, predictions)
#
#         if len(keep) > 0:
#             predictions_filtered = predictions["instances"][keep]
#         else:
#             predictions_filtered = 0
#             print("FAIL DUE TO NO TREES IN FRAME TO APPLY")
#         #IF MAIN - USE OTHER
#
#         if bool_main:
#             #my_visualizer = Visualizer(tilted_image[:, :, ::-1], metadata=MetadataCatalog.get("my_tree_dataset"),
#             #                           instance_mode=ColorMode.SEGMENTATION)
#             #image_with_pred, colors = my_visualizer.draw_instance_predictions(predictions_filtered.to("cpu"))
#
#             image_with_pred, colors = vid_vis.draw_instance_predictions(tilted_image, predictions_filtered.to("cpu"))
#
#             key_points = t.convert_points(predictions_filtered._fields['pred_keypoints'].numpy())
#             boxes = t.convert_boxes(predictions_filtered._fields['pred_boxes'].tensor.numpy())
#         else:
#
#             image_with_pred, colors = vid_vis.draw_instance_predictions(tilted_image, predictions_filtered.to("cpu"))
#
#             key_points = predictions_filtered._fields['pred_keypoints'].numpy()
#             boxes = predictions_filtered._fields['pred_boxes'].tensor.numpy()
#
#         key_points, boxes, colors = three_image_det.filter_further_suggestions(key_points, boxes, colors)
#
#         key_points, colors, boxes = t.omni_clean_list_for_duplicates(colors, key_points, boxes)
#
#         key_points, boxes, colors = three_image_det.sort_by_left_right(key_points, boxes, colors)
#
#
#         return image_with_pred, key_points, boxes, colors, height, width
#
#     @staticmethod
#     def filter_further_suggestions(points, boxs, colors):
#         new_points = []
#         new_boxes = []
#         new_colors = []
#
#         for index in range(0, len(points)):
#
#             p_o = points[index]
#
#             if p_o[1][0] == p_o[2][0]:
#                 continue
#             else:
#                 new_points.append(p_o)
#                 new_boxes.append(boxs[index])
#                 new_colors.append(colors[index])
#
#         return new_points, new_boxes, new_colors
#
#
#     @staticmethod
#     def omni_obtain_angles_new_dimensions(HAOV, VAOV, old_x, old_y, new_x, new_y):
#         return HAOV*(new_x/old_x), VAOV*(new_y/old_y)
#
#     @staticmethod
#     def get_degree_at_y(y_value, y_total, starting_angle, total_angle):
#         print("STARTING Y: ")
#
#
#         angle_per_pixel = total_angle/y_total
#
#         difference = abs(y_value - (y_total/2))
#
#         #MEANS BELOW START
#         if y_value > y_total:
#             return starting_angle - difference*angle_per_pixel
#
#         #ABOVE START
#         else:
#             return starting_angle + difference*angle_per_pixel
#
#
#
#
#
#
#
#
#
#
#
#
#     @staticmethod
#     def get_degree_at_x(x_value, x_total, starting_angle, total_angle):
#         #MEANING RIGHT
#         if x_value >= int(x_total/2):
#             degree = starting_angle + (x_value - x_total/2)*(total_angle/x_total)
#         else:
#             degree = starting_angle - (x_total/2 - x_value)*(total_angle/x_total)
#         return degree % 360
#
#
#
#
#
#
#
#     @staticmethod
#     def omni_calculate_exact_angle_width(middle_angle, aov, total_pixel):
#         print("ABS")
#
#     #Idea Using What We Know About Previous Boundaries
#     #Create A Shape (photo), and can then test if points are within
#     @staticmethod
#     def omni_corner_filter(x, y, roll, predictions):
#
#         #Calculate Corners (OLD CORNERS):
#         if True:
#             angle = math.radians(abs(roll))
#             p1 = int((y * math.sin(angle)))  # + RS
#             p2 = int((x * math.cos(angle)))  # + LS
#             p3 = int((math.cos(angle) * y))  # + Bott
#             p4 = int((math.sin(angle) * x))  # + Top
#
#             if angle <= 0:
#                 # Left,    TOP,        Right,       Bottom
#                 old_corners = [(0, p4), (p2, 0), (x, p3), (p1, y)]
#             else:
#                 # Bottom                 Right,              Top,           Left
#                 old_corners = [(x - p1, y), (x, p4), (x - p2, 0), (0, p3)]
#
#
#         #Create Polygon Representing Old (Polygon)
#
#         print(f" OLD CORNERS (SHOULD BE IN ORDER) {old_corners}")
#
#         polygon = Polygon(old_corners)
#
#         index_list_to_keep = []
#
#
#         for index, tree in enumerate(predictions["instances"]._fields['pred_keypoints'].numpy()):
#             required_remaining = 1
#             for index_in, key_point in enumerate(tree):
#                 shapely_point = Point(key_point[0], key_point[1])
#
#                 if polygon.contains(shapely_point):
#                     print(f" TREE {index} INDEX {index_in} WITHIN")
#                 else:
#                     print(f" TREE {index} INDEX {index_in} WITHIN")
#                     required_remaining-=1
#
#             if required_remaining >= 0:
#                 index_list_to_keep.append(index)
#                 print(f" KEEPING {index}")
#             else:
#                 print(f"REMOVING INDEX {index}")
#
#         return torch.tensor(index_list_to_keep, dtype=torch.long)
#
#     @staticmethod
#     def sort_by_left_right(list1, list2, list3):
#         #INDEX
#         sorted_index = sorted(range(len(list1)), key=lambda k: list1[k][0][0])
#
#         sorted_list1 = [list1[i] for i in sorted_index]
#         sorted_list2 = [list2[i] for i in sorted_index]
#         sorted_list3 = [list3[i] for i in sorted_index]
#         return sorted_list1, sorted_list2, sorted_list3
#
#
#
#
#
#
#
#     @staticmethod
#     def perpendicular_direction(p1, p2):
#         # p1 and p2 are tuples or lists of (x, y) coordinates for the two points
#         x1, y1 = p1
#         x2, y2 = p2
#         # calculate slope of original line segment
#         if x2 - x1 == 0:
#             m = (y2 - y1)/0.01
#             #print("TRICKY CASE")
#         else:
#             m = (y2 - y1) / (x2 - x1)
#         # calculate slope of line perpendicular to original line
#         if m == 0:
#             m = 0.001
#         m_perp = -1 / m
#         # find midpoint of line segment
#         x_mid = (x1 + x2) / 2
#         y_mid = (y1 + y2) / 2
#
#         return (-m_perp, 1)
#
#     @staticmethod
#     def vector_average(vec1, vec2):
#         # Calculate the average vector
#         avg_x = (vec1[0] + vec2[0]) / 2
#         avg_y = (vec1[1] + vec2[1]) / 2
#         return (avg_x, avg_y)
#
#     @staticmethod
#     def find_x_value(ref_point, direction_vector, y_value):
#         # Check if the direction vector is not vertical
#         if direction_vector[1] != 0:
#             # Calculate the slope of the direction vector
#             slope = direction_vector[0] / direction_vector[1]
#             if slope == 0:
#                 slope = 0.001
#             # Calculate the x value at the given y value using the slope-intercept formula
#             x_value = ref_point[0] + (y_value - ref_point[1]) / slope
#         else:
#             # If the direction vector is vertical, the x value is simply the x coordinate of the reference point
#             x_value = ref_point[0]
#         return x_value
#
#     @staticmethod
#     def move_point_in_direction(point, vector, distance):
#         # Calculate the magnitude of the vector
#         magnitude = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
#         if magnitude == 0:
#             magnitude == 0.001
#         # Normalize the vector
#         normalized_vector = (vector[0] / magnitude, vector[1] / magnitude)
#         # Calculate the new point coordinates
#         new_x = point[0] + normalized_vector[0] * distance
#         new_y = point[1] + normalized_vector[1] * distance
#         return (new_x, new_y)
#
#     @staticmethod
#     def create_outline_polygon(points, absolute_base, absolute_top, multiplier):
#
#         width = ten_segments.distance(points[1], points[2])*multiplier
#
#         top_perp = three_image_det.perpendicular_direction((points[4][0], points[4][1]), (points[3][0], points[3][1]))
#         bot_perp = three_image_det.perpendicular_direction((points[3][0], points[3][1]), (points[0][0], points[0][1]))
#
#         av = ((top_perp[0] + bot_perp[0])/2, (top_perp[1] + bot_perp[1])/2)
#
#         top_perp = (-1 * top_perp[1], top_perp[0])
#         bot_perp = (-1 * bot_perp[1], bot_perp[0])
#         av = (-1 * av[1], av[0])
#
#
#
#         bottom_point_to_use = three_image_det.find_x_value(points[0], (-1*bot_perp[0], bot_perp[1]), absolute_base)
#         top_point_to_use = three_image_det.find_x_value(points[4], (-1*top_perp[0], top_perp[1]), absolute_top)
#         mid_point_to_use = points[3]
#
#
#
#
#         tl = three_image_det.move_point_in_direction((top_point_to_use, absolute_top), top_perp, width/2)
#         tr = three_image_det.move_point_in_direction((top_point_to_use,absolute_top), (-1*top_perp[0], -1*top_perp[1]), width / 2)
#
#         al = three_image_det.move_point_in_direction(mid_point_to_use, av, width / 2)
#         ar = three_image_det.move_point_in_direction(mid_point_to_use, (-1 * av[0], -1 * av[1]), width / 2)
#
#         bl = three_image_det.move_point_in_direction((bottom_point_to_use,absolute_base), top_perp, width / 2)
#         br = three_image_det.move_point_in_direction((bottom_point_to_use, absolute_base), (-1 * bot_perp[0], -1 * bot_perp[1]), width / 2)
#
#
#         return (tl, al, bl, br, ar, tr), Polygon([tl, al, bl, br, ar, tr])
#
#
#
#
#
#
#
#
#
#
#
#
#     @staticmethod
#     def create_image_predictions(path, image_frame, roll):
#         image = cv2.imread(path)
#
#
#         image = ndimage.rotate(image, roll, mode='constant', cval=600)
#
#
#         tree_metadata = MetadataCatalog.get("my_tree_dataset")
#         # MetadataCatalog.get("my_tree_dataset").thing_colors = [(0, 0, 0)]
#         # MetadataCatalog.get("my_tree_dataset").thing_classes=["Tree"]
#
#         #Making Predictions
#         t_pred_0 = predictor(image)
#
#
#         # Removing False Tilt Predictions
#         t_pred_1 = t_pred_0["instances"][three_image_det.filtered_list(t_pred_0["instances"]._fields['pred_keypoints'].numpy(), image_frame)]
#
#         # MAKES PreTree Objects
#         image_frame.convert_instances( t_pred_1._fields['pred_keypoints'].numpy(),
#                                        t_pred_1._fields['pred_boxes'].tensor.numpy())
#
#         image_with_pred = three_image_det.apply_predictions_grid(image, t_pred_1, image_frame, tree_metadata)
#
#
#         return t_pred_1._fields['pred_keypoints'].numpy(), t_pred_1._fields['pred_boxes'].tensor.numpy(), image_with_pred
#
#
#
#     @staticmethod
#     def apply_predictions_grid(image, tree_predictions, image_frame, tree_metadata):
#
#         second = tree_predictions
#         print(tree_predictions)
#         print(str(tree_predictions))
#         #
#         # second.remove('pred_boxes')
#         #tree_predictions.remove('pred_boxes')
#         #tree_predictions.remove('scores')
#
#
#         MetadataCatalog.get("my_tree_dataset").thing_colors = [(0, 0, 0)]
#         MetadataCatalog.get("my_tree_dataset").thing_classes = ["Tree"]
#
#         print("WHATS ADDED TO IMAGE:")
#         #print(tree_predictions)
#
#
#         my_visualizer = Visualizer(image[:, :, ::-1], metadata=MetadataCatalog.get("my_tree_dataset"), instance_mode= ColorMode.SEGMENTATION)
#         image_with_pred = my_visualizer.draw_instance_predictions(second.to("cpu"))
#
#         predi = second.to("cpu")
#
#         classes = predi.pred_classes.tolist() if predi.has("pred_classes") else None
#
#
#         if my_visualizer._instance_mode == ColorMode.SEGMENTATION and my_visualizer.metadata.get("thing_colors"):
#             colors = [
#                 my_visualizer._jitter([x / 255 for x in my_visualizer.metadata.thing_colors[c]]) for c in classes
#             ]
#             alpha = 0.8
#         else:
#             colors = None
#             alpha = 0.5
#         print("COLORS TO PRINT:")
#         print(colors)
#
#
#         if not one_directory.det_testing:
#
#
#             image_with_pred = three_image_det.apply_visual_stat(image_with_pred.get_image(), image_frame.list_of_instances, image_frame)
#
#             return image_with_pred
#
#         else:
#             a = random()
#             #cv2.imwrite("C:\\Users\\ldunc\\Downloads\\" + str(a) + ".jpg", image_with_pred.get_image())
#             return
#
#         # cv2.imshow("FinalResult", image_with_pred)
#
#
#         # cv2.waitKey(0)
#
#
#     @staticmethod
#     def apply_visual_stat(image, list, frame):
#         new_image = image
#         cv2.drawContours(new_image, [np.array(frame.old_corners)], 0, (255, 1, 1), 5)
#
#
#         for n in range(0, frame.x):
#             x = n
#             y = frame.get_edge_of_old_box(n, True)
#             cv2.circle(new_image, (int(x),int(y)), 20, (255,255,1), -1)
#             y = frame.get_edge_of_old_box(n, False)
#             cv2.circle(new_image, (int(x), int(y)), 20, (1, 255, 1), -1)
#
#         #cv2.line(new_image, (int(frame.x / 2), 0), (int(frame.x / 2), frame.y), (255,255,255), 5 )
#         # cv2.line(new_image, (0, int(frame.y / 2)), (frame.x, int(frame.y / 2)), (255, 255, 255), 5)
#         #TOP CENTER
#         #cv2.putText(new_image, str(frame.gps_direction), (int(frame.x / 2) - 30, frame.y), cv2.FONT_HERSHEY_SIMPLEX, 5, (255,0,0), 1, cv2.LINE_AA)
#         #cv2.putText(new_image, str(frame.tilt), (0, int(frame.y / 2)) , cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 0, 0), 1,
#                     #cv2.LINE_AA)
#
#         for line in frame.obtain_coordinate_system_line_positions():
#             #VERTICALLY EMPORTANT KEYPOINT
#             if frame.get_degree_at_y(line[1][1]) % 90 == 0:
#                 cv2.line(new_image, line[0], line[1], (0, 0, 0), 5)
#             #HORIZONTALLY IMPORTANT KEYPOINT
#             elif frame.get_degree_at_x(line[0][0]) % 90 == 0:
#                 cv2.line(new_image, line[0], line[1], (0, 0, 0), 5)
#             else:
#                 cv2.line(new_image,  line[0], line[1], (0,0,0), 5)
#
#
#         for tree in list:
#             kp = tree.point_list
#
#             #OVERALL SKELETON (BETWEEN KEYPOINTS)
#             cv2.line(new_image, kp[1], kp[2], (150, 55, 150), 10)
#             #Top SKELETON (BETWEEN HALF, Top Keypoint)
#             cv2.line(new_image, kp[0], kp[1], (150, 55, 150), 10)
#             #Bottom (BETWEEN HALF, Bottom Keypoint)
#             cv2.line(new_image, kp[2], kp[0], (150, 55, 150), 10)
#
#
#
#
#
#             #OVERALL BOX (Between Keypoints)
#             cv2.drawContours(new_image, [tree.quad_segmentation(0, 2, 1, 0)], 0, (255, 1, 1), 3)
#             #TOP RECTANGLE (Between Centre, ABS Top)
#             cv2.drawContours(new_image, [tree.quad_segmentation(0, 3, 0, 2)], 0,  (1, 1 ,255), 3)
#             #BOTTOM (Between Centre, Abs Bottom)
#             cv2.drawContours(new_image, [tree.quad_segmentation(0, 0, 4, 1)], 0, (1, 255, 1), 3)
#
#             if tree.top_extension:
#                 x = (0, 128,0)
#             else:
#                 x = (1,1,250)
#             if tree.bottom_extension:
#                 y = (0, 128, 0)
#             else:
#                 y = (1,1,250)
#
#             # TOP AND BOTTOM MAX POINT (ESTIMATION)
#             cv2.circle(new_image, tree.top, 20, x, -1)  ###########################################
#             cv2.circle(new_image, tree.bottom, 20, y, -1)
#             cv2.line(new_image, (int(tree.top[0] -  tree.abs_w/2), tree.top[1]), (int(tree.top[0] + tree.abs_w/2), tree.top[1]), x, 10)
#             cv2.line(new_image, (int(tree.bottom[0] - tree.abs_w / 2), tree.bottom[1]), (int(tree.bottom[0] + tree.abs_w / 2), tree.bottom[1]), y, 10)
#
#
#
#
#         return new_image
#
#
#
#     #OPTIONAL, ALLOWS OFTEN FLATTENS OUT TOP/BOTTOM,  HOWEVER
#
#
#
#     @staticmethod
#     def filtered_list(boxes, frame):
#
#
#         list = []
#         for x in range(len(boxes)):
#             k3 = boxes[x][3]
#
#             if not one_directory.det_testing:
#
#                 if not frame.is_out_side_of_frame((k3[0], k3[1]), 0):
#                     list.append(x)
#             else:
#                 list.append(x)
#         return torch.tensor(list, dtype=torch.long)
#
#     @staticmethod
#     def filtered_list_static(boxes, x,y, oc, ls, rs, roll):
#         list = []
#         for x in range(len(boxes)):
#             k3 = boxes[x][3]
#
#             if not two_frame.is_out_side_of_frame((k3[0], k3[1]), 0, oc, ls, rs, y, roll):
#                 list.append(x)
#
#
#         return torch.tensor(list, dtype=torch.long)
#
#
#     @staticmethod
#     def get_color(i):
#         if i == 0:
#             color = (1, 1, 1)
#         elif i == 1:
#             color = (1, 1, 255)
#         elif i == 2:
#             color = (1, 255, 1)
#         elif i == 3:
#             color = (1, 255, 255)
#         elif i == 4:
#             color = (255, 1, 1)
#         elif i == 5:
#             color = (255, 1, 255)
#         elif i == 6:
#             color = (255, 255, 1)
#         elif i == 7:
#             color = (255, 255, 255)
#         else:
#             color = (100, 100, 100)
#         return color
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#


