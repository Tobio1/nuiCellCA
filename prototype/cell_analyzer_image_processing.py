

import cv
import cell_analyzer_objects


#############################################################################
#MODIFY DEFINES BELOW
#############################################################################

THRESHOLD_VALUE = 81
MAX_THRESHOLD_IMAGE_VALUE = 255

ERODER_PATTERN_SIZE = 2
DILATE_PATTERN_SIZE = 2


#THRESHOLD_TYPE = cv.CV_THRESH_BINARY
#THRESHOLD_TYPE = cv.CV_THRESH_BINARY_INV
THRESHOLD_TYPE = cv.CV_THRESH_OTSU
#THRESHOLD_TYPE = cv.CV_THRESH_TOZERO
#THRESHOLD_TYPE = cv.CV_THRESH_TOZERO_INV
#THRESHOLD_TYPE = cv.CV_THRESH_TRUNC

#cv.CV_THRESH_BINARY      cv.CV_THRESH_OTSU        cv.CV_THRESH_TRUNC
#cv.CV_THRESH_BINARY_INV  cv.CV_THRESH_TOZERO
#cv.CV_THRESH_MASK        cv.CV_THRESH_TOZERO_INV

#############################################################################



class CellAnalyzerImageProcessing(object):


    def load_image(self, image_path, image_type):
        try:
            return cv.LoadImageM(image_path, image_type)
        except:
            print '[!] cant load image!'
            sys.exit(2)


    def load_image_color(self, image_path):
        print '[i] load color image'
        return self.load_image(image_path, cv.CV_LOAD_IMAGE_COLOR)


    def load_image_gray(self, image_path):
        print '[i] load gray image'
        return self.load_image(image_path, cv.CV_LOAD_IMAGE_GRAYSCALE)


    def filter_image_erode(self, threshold_image):
        print '[i] erode filter'
        erode_threshold_image = cv.CreateImage(cv.GetSize(threshold_image), cv.IPL_DEPTH_8U, cv.CV_8UC1)
        cv.Erode(threshold_image, erode_threshold_image, None, ERODER_PATTERN_SIZE)
        return erode_threshold_image


    def filter_image_dilate(self, threshold_image):
        print '[i] dilate filter'
        dilate_threshold_image = cv.CreateImage(cv.GetSize(threshold_image), cv.IPL_DEPTH_8U, cv.CV_8UC1)
        cv.Dilate(threshold_image, dilate_threshold_image, None, DILATE_PATTERN_SIZE)
        return dilate_threshold_image


    def calc_threshold_image(self, src_gray_image):
        print '[i] calc threshold image'
        threshold_image = cv.CreateImage(cv.GetSize(src_gray_image), cv.IPL_DEPTH_8U, cv.CV_8UC1)

        #Threshold(src, dst, threshold, maxValue, thresholdType) -> None
        cv.Threshold(src_gray_image, threshold_image, THRESHOLD_VALUE, MAX_THRESHOLD_IMAGE_VALUE, THRESHOLD_TYPE)
        return threshold_image


    def calc_horizontal_histogram(self, threshold_image):
        print '[i] calc horizontal histogram'
        horizontal_histogram_image = cv.CreateMat(threshold_image.height, threshold_image.width, cv.CV_8UC1)
        hist_array = numpy.zeros(threshold_image.width)

        #calculate histogram
        for height in range(0, threshold_image.height):
            for width in range(0, threshold_image.width):
                if cv.Get2D(threshold_image, height, width)[0] == MAX_THRESHOLD_IMAGE_VALUE:
                    hist_array[width] += 1

        #create histogram image
        cv.SetZero(horizontal_histogram_image)
        for width in range(0, horizontal_histogram_image.width):
            for i in range(int(hist_array[width])):
                cv.Set2D(horizontal_histogram_image, horizontal_histogram_image.height - i -1, width, MAX_THRESHOLD_IMAGE_VALUE)

        arraySum = 0
        for i in range(len(hist_array)):
            arraySum += hist_array[i]

        return (horizontal_histogram_image, hist_array)


    def __find_neighbors(self, height, width, threshold_image, cell_mark_map, cell_object):

        if (cv.Get2D(threshold_image, height, width)[0] == MAX_THRESHOLD_IMAGE_VALUE):
            cell_mark_map[height][width] = 1
            cell_object.add_point(cell_analyzer_objects.CellAnalyzerPoint(height, width))
        else:
            return

        #down
        if (height < (threshold_image.height - 1) and cell_mark_map[height + 1][width] == 0):
            self.__find_neighbors(height + 1, width, threshold_image, cell_mark_map, cell_object)

        #right
        if (width < (threshold_image.width - 1) and cell_mark_map[height][width + 1] == 0):
            self.__find_neighbors(height, width + 1, threshold_image, cell_mark_map, cell_object)

        #up
        if (height > 0 and cell_mark_map[height - 1][width] == 0):
            self.__find_neighbors(height - 1, width, threshold_image, cell_mark_map, cell_object)



    def find_cells_neighbor_alg(self, threshold_image):
        print '[i] try to find cells in image (neighbor alg)'

        cell_object_list = []
        #cell_mark_map = numpy.zeros((threshold_image.height,threshold_image.width))
        cell_mark_map =  [[0 for width in range(threshold_image.width)] for height in range(threshold_image.height)]

        for width in range(0, threshold_image.width):
            for height in range(0, threshold_image.height):
                if cell_mark_map[height][width] == 1:
                    #print "continue, already marked in object!"
                    continue

                cell_object = cell_analyzer_objects.CellAnalyzerObject()
                self.__find_neighbors(height, width, threshold_image, cell_mark_map, cell_object)


                if (cell_object.get_nr_of_points()):
                    #print "-> found object with %d points!" % cell_object.get_nr_of_points()

                    cell_object_list.append(cell_object)

        return cell_object_list


    def mark_cells_in_image(self, cell_list, color_image, color):
        print '[i] mark objects in image'

        for cell in cell_list:
            for point_index in range(cell.get_nr_of_points()):
                point = cell.get_point_by_index(point_index)
                cv.Set2D(color_image, point.y, point.x, color)


    def mark_emphasis_in_image(self, cell_list, color_image, color):
        print '[i] mark emphasis in image'

        for cell in cell_list:
            emphasis = cell.get_emphasis()
            cv.Set2D(color_image, emphasis.y, emphasis.x, color)


    def draw_cell_bounding_box_in_image(self, cell_list, color_image, color):
        print '[i] draw bounding box for each cell in image'

        for cell in cell_list:
            x_pos, y_pos, width, height = cell.get_bounding_box()

            #horizontal bounding box lines
            for width_index in range(x_pos, x_pos + width):
                cv.Set2D(color_image, y_pos, width_index, color)
                cv.Set2D(color_image, y_pos + height, width_index, color)

            #vertical bounding box lines
            for height_index in range(y_pos, y_pos + height):
                cv.Set2D(color_image, height_index, x_pos, color)
                cv.Set2D(color_image, height_index, x_pos + width, color)
