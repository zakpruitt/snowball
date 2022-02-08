import re
from turtle import update


class FileParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.emp_flag = None
        self.email_flag = False
        self.sub_dept_flag = False
        self.line_information = []
        self.count_information = {}

    def parse_text(self):
        with open(self.file_path, 'r+', encoding="utf-16") as file:
            for line in file.readlines():
                if re.search("(^\s|^20([0-9]{6}))", line):
                    if line.startswith(" "):
                        # line with count/email, etc
                        self.email_flag = False
                    else:
                        # line with information
                        self.line_information.append(self.__parse_information_line(line))
        return self.line_information

    def __parse_information_line(self, line):
        information_array = self.__build_information_array(line.split())
        self.__update_count(information_array)
        return information_array

    def __build_information_array(self, line_array):
        symbols = ['H', 'S', 'E']

        information_array = ["" for x in range(0, 9)]
        length = len(line_array)

        for element in line_array:
            if element in symbols:
                if self.email_flag == False and element == "E":
                    self.email_flag = True
                else:
                    self.sub_dept_flag = element
            elif len(element) == 3 and element.isdigit():
                self.emp_flag = element

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
        employee_number = information_array[3]
        if employee_number not in self.count_information.keys():
            self.count_information[self.emp_flag] = {
                'total': 0,
                'immed': 0,
                'later': 0,
                'emails': 0
            }
        
        # update total
        self.count_information[employee_number]['total'] += 1
        
        # update immed/later. if not immed, it must be later.
        if information_array[6] == information_array[7]:
            self.count_information[employee_number]['immed'] += 1
        else:
            self.count_information[employee_number]['later'] += 1
        
        # update emails
        if information_array[3] == True:
            self.count_information[employee_number]['emails'] += 1

    def __str__(self):
        return str(self.output)
