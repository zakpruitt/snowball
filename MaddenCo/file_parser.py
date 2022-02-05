import re


class FileParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.emp_flag = 0
        self.email_flag = False

    def __parse_count_line(line):
        line_elements = line.split()
        # print(line_elements)

    def __parse_information_line(line):
        line_elements = line.split()
        parsed_string = ""
        print(len(line_elements))

    def parse_text(self):
        with open(self.file_path, 'r+', encoding="utf-16") as file:
            for line in file.readlines():
                if re.search("(^\s|^20([0-9]{6}))", line):
                    if line.startswith(" "):
                        # line with count/email, etc
                        self.parse_count_line(line)
                    else:
                        # line with information
                        self.parse_information_line(line)
