from new_detection import new_detection
#import insta360_updated2 as insta


starting_id = 10002400
ttl = 8
directory_name = "C:\\Users\\ldunc\\OneDrive\\Documents\\pycharm-workspace\\ForestMapping\\Tests\\Test 19\\Photos"
video_name = "C:\\Users\\ldunc\\OneDrive\\Documents\\pycharm-workspace\\ForestMapping\\Tests\\Test 19\\JMZAE1363.MOV"
model_to_use = "ResNext-101_fold_01.pth"


n_th_frames = 3
before_starting = 0

x_aov = 108
y_aov = 85

video_x = 1104
video_y = 828

photo_x = 3200
photo_y = 2400

absolute_index = 1

x_degree_per_pixel = x_aov/photo_x
y_degree_per_pixel = y_aov/photo_y

time_required_for_rescaling = 10
total_colors_created = 74
time_before_remove = 8

class master:

    def __init__(self):

        
        nd = new_detection()
        nd.set_up(model_to_use)
        nd.begin_work(True, directory_name, video_name)