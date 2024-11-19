from random import random
import matplotlib.colors as colors

from shapely.geometry import Point


from five_database import five_database


class fixed_point:


    def get_color(self):
        x = int(20*random()) + 1

        if x == 1:
            return 'red'
        elif x == 2:
            return 'blue'
        elif x == 3:
            return 'green'
        elif x == 4:
            return 'orange'
        elif x == 5:
            return 'purple'
        elif x == 6:
            return 'yellow'
        elif x == 7:
            return 'cyan'
        elif x == 8:
            return 'magenta'
        elif x == 9:
            return 'lime'
        elif x == 10:
            return 'pink'
        elif x == 11:
            return 'brown'
        elif x == 12:
            return 'teal'
        elif x == 13:
            return 'navy'
        elif x == 14:
            return 'olive'
        elif x == 15:
            return 'maroon'
        elif x == 16:
            return 'gold'
        elif x == 17:
            return 'indigo'
        elif x == 18:
            return 'gray'
        elif x == 19:
            return 'black'
        elif x == 20:
            return 'white'
        else:
            return None






    def __init__(self):
        #Holds Whether This is Permanent
        self.permanent = False

        #Holds Finished?
        self.finished = False


        #Holds The Photo of Start
        self.starting_photo = -1

        #Holds A List of Indexs
        self.list_of_indexs = []

        self.list_of_data = []

        #IF LENGTH IS ONE, LINE

        self.point = -1


        self.color = self.get_color()

    def __str__(self):
        return f"P: {self.point} F: {self.starting_photo}  START: {self.starting_photo} IND: {self.list_of_indexs} DATA: {self.list_of_data}"


    #ASSUMING ONLY FORWARD NEEDED
    def create_and_cascade(self, photo, fragment):
        fd = five_database()

        self.starting_photo = photo

        #Obtaining the range of photo, assuming previous ties dont exist
        # val_range = fd.get_range(photo)
        #
        # val_range = (val_range[1], val_range[0])



        for every_index in range(photo, photo + 10):
            v = fd.get_tree_later_multiple(photo, fragment, every_index)
            if v != -1:
                self.list_of_indexs.append(v)


        #print(f" {val_range}___ {str(self)}")


        return len(self.list_of_indexs)










