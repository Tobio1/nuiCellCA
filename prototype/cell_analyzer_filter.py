
#############################################################################
#MODIFY DEFINES BELOW
#############################################################################

#filter defines
MINIMAL_NR_OF_POINTS_PER_CELL_FILTER_VALUE = 7
MAXIMAL_NR_OF_POINTS_PER_CELL_FILTER_VALUE = 42
MINIMAL_DEVIATION_OF_CELL_ASPECT_RATIO_IN_PERCENT = 30

#############################################################################



class CellAnalyzerFilter(object):

    def filter_cells_shape(self, possible_cell_list):
        print '[i] filter cells by shape (circle)'

        filtered_cell_list = []
        rejected_cell_list = []
        for possible_cell in possible_cell_list:
            x_pos, y_pos, width, height = possible_cell.get_bounding_box()

            if ((width - height) < 0):
                ratio = float(width) / height
            else:
                ratio = float(height) / width

            if ((100 - ratio * 100) < MINIMAL_DEVIATION_OF_CELL_ASPECT_RATIO_IN_PERCENT):
                filtered_cell_list.append(possible_cell)
            else:
                rejected_cell_list.append(possible_cell)

        print ' -> nr of dropped cells by size shape filter (%s percent cell aspect ratio deviation): %d' % (MINIMAL_DEVIATION_OF_CELL_ASPECT_RATIO_IN_PERCENT, len(rejected_cell_list))
        return (filtered_cell_list, rejected_cell_list)


    def filter_cells_size(self, possible_cell_list):
        print '[i] filter cells by size'

        filtered_cell_list = []
        rejected_cell_list = []
        for possible_cell in possible_cell_list:

            #check minimal size
            if (possible_cell.get_nr_of_points() < MINIMAL_NR_OF_POINTS_PER_CELL_FILTER_VALUE):
                rejected_cell_list.append(possible_cell)
                continue

            #check maximal size
            if (possible_cell.get_nr_of_points() > MAXIMAL_NR_OF_POINTS_PER_CELL_FILTER_VALUE):
                rejected_cell_list.append(possible_cell)
                continue

            filtered_cell_list.append(possible_cell)


        print ' -> nr of dropped cells by size filter: %d' % (len(possible_cell_list) - len(filtered_cell_list))
        return (filtered_cell_list, rejected_cell_list)
