import pylab
import numpy


class CellAnalyzerCellStatistics(object):

    def __init__(self, log_path):
        self.log_path = log_path


    def draw_cell_size_distribution_diagram(self, diagram_file_name, cell_list):

        cell_distribution_hashmap = {}
        nr_of_points_list = []
        for cell in cell_list:
            value = cell_distribution_hashmap.get(cell.get_nr_of_points(), 0)
            cell_distribution_hashmap[cell.get_nr_of_points()] = value + 1
            nr_of_points_list.append(cell.get_nr_of_points())

        index_max = cell_distribution_hashmap.keys()[-1] + 3
        index_min = 0

        value_list = []
        for index in range(index_min, index_max):
            value_list.append(cell_distribution_hashmap.get(index, 0))


        median_value = numpy.median(nr_of_points_list)
        print '[i] calculated median value: %f' % median_value

        mean_value =  float(sum(value_list)) / len(value_list)
        print '[i] calculated mean value: %f' % mean_value

        pylab.plot(value_list, 'r',  label='cell size distribution')
        pylab.axvline(x=median_value, label='median')

        pylab.xlabel('cell size [pixel]')
        pylab.ylabel('cell count [cells]')
        pylab.title('cell size distribution')
        pylab.grid(True)
        pylab.legend(loc= 'best')

        pylab.savefig(self.log_path + '/' + diagram_file_name)
        #pylab.show()
