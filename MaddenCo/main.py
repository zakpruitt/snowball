import time
import re

def parse_text(file_name):
    with open(file_name, 'r+', encoding="utf-16") as file:
        for line in file.readlines():
            if re.search("(^\s|^20([0-9]{6}))", line):
                print(line)
                time.sleep(0.2)





        
if __name__ == '__main__':
    parse_text('./MaddenCo/20220106.txt')
    print("done")
    