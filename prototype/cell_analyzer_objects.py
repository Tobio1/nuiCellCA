

class CellAnalyzerPoint(object):
    """ simple point class to represent a point in a image
    """

    def __init__(self, y, x):
        self.y = y
        self.x = x


class CellAnalyzerObject(object):
    """ cell class represents a cell in a image
    """

    def __init__(self):
        self.point_list = []


    def add_point(self, point):
        self.point_list.append(point)


    def get_emphasis(self):
        x_min, x_max = self.get_point_x_min_max()
        y_min, y_max = self.get_point_y_min_max()

        emphasis_point = CellAnalyzerPoint(0, 0)
        emphasis_point.x = x_min + (x_max - x_min) / 2
        emphasis_point.y = y_min + (y_max - y_min) / 2

        return emphasis_point


    def get_point_x_min_max(self):
        x_min = 999999999999999999999999999999999999999999999999999999999999999999999999999999;
        x_max = 0;

        for point in self.point_list:
            if(point.x < x_min):
                x_min = point.x
            if(point.x > x_max):
                x_max = point.x
        return (x_min, x_max)


    def get_point_y_min_max(self):
        y_min = 999999999999999999999999999999999999999999999999999999999999999999999999999999;
        y_max = 0;

        for point in self.point_list:
            if(point.y < y_min):
                y_min = point.y
            if(point.y > y_max):
                y_max = point.y
        return (y_min, y_max)


    def get_nr_of_points(self):
        return len(self.point_list)


    def get_point_by_index(self, index):
        return self.point_list[index]


    def get_bounding_box(self):
        x_min, x_max = self.get_point_x_min_max()
        y_min, y_max = self.get_point_y_min_max()

        width = abs(x_min - x_max)
        height = abs(y_min - y_max)

        return (x_min, y_min, width, height)

