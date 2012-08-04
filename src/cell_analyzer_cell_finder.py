
import cell_analyzer_objects
import cv

import numpy as np
import scipy
import scipy.ndimage as ndimage
import scipy.ndimage.filters as filters
import matplotlib.pyplot as plt



#############################################################################
#MODIFY DEFINES BELOW
#############################################################################

NEIGHBORS_ALG_MAX_THRESHOLD_IMAGE_VALUE = 255

MAXIMA_ALG_THRESHOLD = 150
MAXIMA_ALG_NEIGHBORHOOD_SIZE = 5

#############################################################################



class CellAnalyzerCellFinderDefaultStrategy(object):

    def __init__(self, image):
        self.image = image


    def find_cells(self):
        print '[i] do nothing with image...'
        cell_object_list = []
        return cell_object_list



class CellAnalyzerCellFinderNeighbors(CellAnalyzerCellFinderDefaultStrategy):

    def __init__(self, threshold_image):
        #super(CellAnalyzerCellFinderDefaultStrategy, self).__init__(threshold_image)
        CellAnalyzerCellFinderDefaultStrategy.__init__(self, threshold_image)

    def find_cells(self):
        return self.find_cells_neighbor_alg(self.image)


    def __find_neighbors(self, height, width, threshold_image, cell_mark_map, cell_object):

        if (cv.Get2D(threshold_image, height, width)[0] == NEIGHBORS_ALG_MAX_THRESHOLD_IMAGE_VALUE):
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



#http://stackoverflow.com/questions/9111711/get-coordinates-of-local-maxima-in-2d-array-above-certain-value
class CellAnalyzerCellFinderMaxima(CellAnalyzerCellFinderDefaultStrategy):


    def __init__(self, color_image):
        #super(CellAnalyzerCellFinderDefaultStrategy, self).__init__(self, color_image)
        CellAnalyzerCellFinderDefaultStrategy.__init__(self, color_image)


    def find_cells(self):

        cell_object_list = []

        data = scipy.array(self.image)
        data.reshape(self.image.height, self.image.width, self.image.channels)

        data_max = filters.maximum_filter(data, MAXIMA_ALG_NEIGHBORHOOD_SIZE)
        maxima = (data == data_max)
        data_min = filters.minimum_filter(data, MAXIMA_ALG_NEIGHBORHOOD_SIZE)
        diff = ((data_max - data_min) > MAXIMA_ALG_THRESHOLD)
        maxima[diff == 0] = 0

        labeled, num_objects = ndimage.label(maxima)
        slices = ndimage.find_objects(labeled)
        x, y = [], []

        for dy, dx, crap in slices:
            x_center = (dx.start + dx.stop - 1)/2
            x.append(x_center)
            y_center = (dy.start + dy.stop - 1)/2
            y.append(y_center)

            cell = cell_analyzer_objects.CellAnalyzerObject()
            point = cell_analyzer_objects.CellAnalyzerPoint(y_center, x_center)
            cell.add_point(point)

            #HACK HACK HACK: this is to avoid a division by zero!
            #point = cell_analyzer_objects.CellAnalyzerPoint(y_center + 1, x_center)
            #cell.add_point(point)
            #point = cell_analyzer_objects.CellAnalyzerPoint(y_center - 1, x_center)
            #cell.add_point(point)
            #point = cell_analyzer_objects.CellAnalyzerPoint(y_center, x_center + 1)
            #cell.add_point(point)
            #point = cell_analyzer_objects.CellAnalyzerPoint(y_center, x_center - 1)
            #cell.add_point(point)

            cell_object_list.append(cell)


        #plt.imshow(data)
        #plt.savefig('/tmp/data.png', bbox_inches = 'tight')

        #plt.autoscale(False)
        #plt.plot(x,y, 'ro')
        #plt.savefig('/tmp/result.png', bbox_inches = 'tight')

        #create dummy cell objects with only one pixel
        #for x_element in x:
            #print x

        return cell_object_list


        