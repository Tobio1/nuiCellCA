

class CellAnalyzerLogger(object):


    def __init__(self, log_file_name):
        self.log_file_name = log_file_name
        self.open_logfile(self.log_file_name)


    def __del__(self):
        self.close_logfile()


    def write_log_file_detailed(self, possible_cell_list, filtered_cell_list):
        self.write_log_file_header()
        self.write_log_file_analyzer_facts(len(possible_cell_list), len(filtered_cell_list))
        self.write_detailed_cell_object_list_to_log_file(filtered_cell_list)
        self.write_log_file_footer()
        self.close_logfile()


    def write_log_file_simple(self, filtered_cell_list):
        self.write_simple_cell_object_list_to_log_file(filtered_cell_list)


    def open_logfile(self, log_file_name):
        self.log_file = open(log_file_name, 'w')


    def close_logfile(self):
        self.log_file.close()


    def append_line_to_log_file(self, log_line):
        self.log_file.write(log_line + '\n')


    def write_log_file_banner(self, banner_string):
        self.log_file.write('\n*******************************************************\n')
        self.log_file.write('* %s\n' % (banner_string))
        self.log_file.write('*******************************************************\n')


    def write_log_file_heading(self, heading_string):
        self.log_file.write('\n== %s ==\n' % (heading_string))


    def write_log_file_header(self):
        self.write_log_file_banner('hello from logger')


    def write_log_file_footer(self):
        self.write_log_file_banner('done!')


    def write_log_file_analyzer_facts(self, nr_of_elements_found_in_image, nr_of_interesing_elements_found_in_image):
        self.write_log_file_heading('analyzer facts')
        self.append_line_to_log_file(' * nr of cells in image:\t%d' % (nr_of_elements_found_in_image));
        self.append_line_to_log_file(' * nr of interesting cells in image:\t%d' % (nr_of_interesing_elements_found_in_image));
        self.append_line_to_log_file(' * nr of filtered cells:\t%d' % (nr_of_elements_found_in_image - nr_of_interesing_elements_found_in_image));

        ##TODO: add this stuff to the facts
        #file name 
        #used filters
        #used image filter functions (config)
        #used threshold alg...
        #date
        #script revision


    def write_detailed_cell_object_list_to_log_file(self, cell_object_list):

        cell_index = 1
        for cell in cell_object_list:
            self.write_log_file_heading('details for cell nr %d' % cell_index)

            #cell.get_bounding_box()

            self.append_line_to_log_file(' * nr of points: %d' % cell.get_nr_of_points());

            x_min, x_max = cell.get_point_x_min_max()
            self.append_line_to_log_file(' * x position limits - min: %d, max: %d' % (x_min, x_max));
            y_min, y_max = cell.get_point_y_min_max()
            self.append_line_to_log_file(' * y position limits - min: %d, max: %d' % (y_min, y_max));

            point = cell.get_emphasis()
            self.append_line_to_log_file(' * emphasis point - x: %d, y: %d' % (point.x, point.y));

            self.append_line_to_log_file('cell point list:');
            for cell_point_index in range(0, cell.get_nr_of_points()):
                point = cell.get_point_by_index(cell_point_index)
                self.append_line_to_log_file(' * point - x: %d, y: %d' % (point.x, point.y));

            cell_index += 1


    def write_simple_cell_object_list_to_log_file(self, cell_object_list):
        """write simple log entries: cell_id nr_of_points emph_x emph_y
        """
        cell_index = 1
        for cell in cell_object_list:
            emphasis = cell.get_emphasis()
            self.append_line_to_log_file(('%d %d %d %d' % (cell_index, cell.get_nr_of_points(), emphasis.x, emphasis.y)));

            cell_index += 1
