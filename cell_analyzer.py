#!/usr/bin/env python
# -*- coding: utf-8 -*-


import cv
import sys

import cell_analyzer_logger
import cell_analyzer_cell_filter
import cell_analyzer_cell_finder
import cell_analyzer_image_processing


#############################################################################
#MODIFY DEFINES BELOW
#############################################################################

CELL_ANALYZER_SIMPLE_LOG_FILE_NAME = 'cell_analyzer_simple.log'
CELL_ANALYZER_DETAILED_LOG_FILE_NAME = 'cell_analyzer_detailed.log'

#############################################################################




class CellAnalyzer(object):
    """ class to analyze images and find interesting cells with filtering
    """

    def __init__(self):
        print "[i] hello from cell analyzer object"


    def __del__(self):
        print "[i] bye bye from cell analyzer object"


    def analyze(self, image_path):
        print '[i] process image %s...' % (image_path)

        my_cell_analyzer_image_processing = cell_analyzer_image_processing.CellAnalyzerImageProcessing()

        gray_image = my_cell_analyzer_image_processing.load_image_gray(image_path)
        color_image = my_cell_analyzer_image_processing.load_image_color(image_path)
        threshold_image = my_cell_analyzer_image_processing.calc_threshold_image(gray_image)
        canny_feature_threshold_image = my_cell_analyzer_image_processing.get_canny_feature(threshold_image)
        #horizontal_histogram_image, horizontal_histogram_array = my_cell_analyzer_image_processing.calc_horizontal_histogram(threshold_image)

        erode_threshold_image = my_cell_analyzer_image_processing.get_image_erode(threshold_image)
        #dilate_threshold_image = my_cell_analyzer_image_processing.get_image_dilate(threshold_image)



        #TODO
        #watershed_image, watershed_markers = my_cell_analyzer_image_processing.get_watershed_markers(color_image)


        #change cell finder algorithm here
        #cell_finder = cell_analyzer_cell_finder.CellAnalyzerCellFinderNeighbors(threshold_image)
        #cell_finder = cell_analyzer_cell_finder.CellAnalyzerCellFinderNeighbors(erode_threshold_image)
        cell_finder = cell_analyzer_cell_finder.CellAnalyzerCellFinderMaxima(color_image)

        possible_cell_list = []
        possible_cell_list = cell_finder.find_cells()
        if(len(possible_cell_list) == 0):
            print "[!] no possible cell found in image..."
            #return
        else:
            print "[i] %d possible cells found in image" % len(possible_cell_list)
            for cell in possible_cell_list:
                print " -> nr of points in object: %d" % cell.get_nr_of_points()
                #for point in range(0, obj.get_nr_of_points()):
                    #print "    x: %d | y: %d" % (obj.get_point_by_index(point).x, obj.get_point_by_index(point).y)


        #mark all recognized cells with a bounding box
        my_cell_analyzer_image_processing.draw_cell_bounding_box_in_image(possible_cell_list, color_image, (0, 0, 255))


        #filter cells, clone list for statistics and log
        filtered_cell_list = possible_cell_list[:]

        my_cell_filter = cell_analyzer_cell_filter.CellAnalyzerCellFilter()
        #filtered_cell_list, rejected_cells_by_size_filter_list = my_cell_filter.filter_cells_size(filtered_cell_list)
        #filtered_cell_list, rejected_cells_by_shape_filter_list  = my_cell_filter.filter_cells_shape(filtered_cell_list)


        #mark interesting cells
        my_cell_analyzer_image_processing.mark_cells_in_image(filtered_cell_list, color_image, (255, 0, 0))
        #my_cell_analyzer_image_processing.mark_emphasis_in_image(filtered_cell_list, color_image, (0, 255, 255))


        #write log file
        print '\n\n[i] write log files...'
        cell_analyer_logger_detailed = cell_analyzer_logger.CellAnalyzerLogger(CELL_ANALYZER_DETAILED_LOG_FILE_NAME)
        cell_analyer_logger_detailed.write_log_file_detailed(possible_cell_list, filtered_cell_list)
        cell_analyer_logger_simple = cell_analyzer_logger.CellAnalyzerLogger(CELL_ANALYZER_SIMPLE_LOG_FILE_NAME)
        cell_analyer_logger_simple.write_log_file_simple(filtered_cell_list)


        cv.ShowImage('gray_image', gray_image)
        cv.SaveImage('gray_image.png', gray_image)

        cv.ShowImage('threshold_image', threshold_image);
        cv.SaveImage('threshold_image.png', threshold_image)

        cv.ShowImage('color_image', color_image)
        cv.SaveImage('color_image.png', color_image)

        cv.ShowImage('canny_feature_threshold_image', canny_feature_threshold_image)
        cv.SaveImage('canny_feature_threshold_image.png', canny_feature_threshold_image)

        cv.ShowImage('erode_threshold_image', erode_threshold_image)
        cv.SaveImage('erode_threshold_image.png', erode_threshold_image)


        #cv.ShowImage('horizontal_histogram_image', horizontal_histogram_image);
        #cv.ShowImage('dilate_threshold_image', dilate_threshold_image)


        print '\n\n[i] final report:'
        print ' * %d cells found in image ' % len(possible_cell_list)
        print ' * %d interesting cells found in image (filtered) ' % len(filtered_cell_list)


        print '\n\n[i] press any key to exit...'
        cv.WaitKey(0)



def print_help():
    print '[i] help:'
    print ' * call application with a image name as parameter'
    print ' * %s <path_to_image>\n' % (sys.argv[0])


if __name__ == "__main__":

    if (len(sys.argv) != 2):
        print '[!] give me path to an image to analyze!'
        print_help()
        sys.exit(1)

    image_name = sys.argv[1]

    cell_analyzer = CellAnalyzer()
    cell_analyzer.analyze(image_name)

    sys.exit(0)

