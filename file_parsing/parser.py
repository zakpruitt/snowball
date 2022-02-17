import re


class Parser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.emp_flag = None
        self.email_flag = False
        self.sub_dept_flag = False
        # TODO: convert to dict
        self.line_information = []
        self.count_information = {}

    def parse_text(self):
        with open(self.file_path, 'r+', encoding="utf-16") as file:
            for line in file.readlines():
                if re.search("(^\s|^[0-9]{8})", line):
                    if line.startswith(" "):
                        # line with count/email, etc
                        self.email_flag = False
                    else:
                        # line with information
                        information_array = self.__parse_information_line(line)
                        if (information_array != "INVALID"):
                            self.line_information.append(information_array)

    def __parse_information_line(self, line):
        # split line and check if invalid
        line_array = line.split()
        if line_array[1] == "W" or line_array[1] == "N":
            return "INVALID"

        # build information array and update count, then return array to append
        information_array = self.__build_information_array(line.split())
        self.__update_count(information_array)
        return information_array

    def __build_information_array(self, line_array):
        symbols = ['H', 'S', 'E']
        
        # build array with placeholder values
        information_array = ["" for x in range(0, 9)]
        length = len(line_array)

        # check flags
        for element in line_array:
            if element in symbols:
                if self.email_flag == False and element == "E":
                    self.email_flag = True
                else:
                    self.sub_dept_flag = element
            elif len(element) == 3 and element.isdigit():
                self.emp_flag = element

        # build array with actual values
        information_array[0] = line_array[0]
        information_array[1] = line_array[1]
        information_array[2] = self.sub_dept_flag
        information_array[3] = self.email_flag
        information_array[4] = self.emp_flag
        information_array[5] = line_array[length - 4]
        information_array[6] = line_array[length - 3]
        information_array[7] = line_array[length - 2]
        information_array[8] = line_array[length - 1]

        return information_array

    def __update_count(self, information_array):
        # create key in dict if not already created
        employee_number = information_array[4]
        if employee_number not in self.count_information.keys():
            self.count_information[self.emp_flag] = {
                'Total': 0,
                'Immed': 0,
                'Later': 0,
                'Emails': 0
            }

        # update total
        self.count_information[employee_number]['Total'] += 1

        # update immed/later. if not immed, it must be later.
        if information_array[6] == information_array[7]:
            self.count_information[employee_number]['Immed'] += 1
        else:
            self.count_information[employee_number]['Later'] += 1

        # update emails
        if information_array[3] == True:
            self.count_information[employee_number]['Emails'] += 1

    def __str__(self):
        return str(self.line_information)
