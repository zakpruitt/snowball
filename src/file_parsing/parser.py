import re
from models.call import Call

class Parser:
    def __init__(self):
        self.calls_db = Call()
        self.emp_flag = None
        self.email_flag = False
        self.sub_dept_flag = False

    def parse_text(self, file):
        with open(file, 'r+', encoding="utf-16") as f:
            for line in f.readlines():
                if re.search("(^\s|^[0-9]{8})", line):
                    if line.startswith(" "):
                        # line with count/email, etc
                        self.email_flag = False
                    else:
                        # since line is valid, parse it.
                        self.__parse_line(line)

    def __parse_line(self, line):
        # check if line is valid
        line_array = line.split()
        if line_array[1] == "W" or line_array[1] == "N":
            return "INVALID"

        call = self.__build_call(line_array)
        self.calls_db.insert(call)


    def __build_call(self, line_array):
        symbols = ['H', 'S', 'E']

        # build tuple with placeholder values
        call_array = ["" for x in range(9)]
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

        # hydrate call with actual values
        call_array[0] = line_array[length - 4]
        call_array[1] = line_array[0]
        call_array[2] = line_array[1]
        call_array[3] = self.sub_dept_flag
        call_array[4] = self.email_flag
        call_array[5] = self.emp_flag
        call_array[6] = line_array[length - 3]
        call_array[7] = line_array[length - 2]
        call_array[8] = line_array[length - 1]

        call = tuple(call_array) 
        print(call)
        return call
