import time

def parse_text(file_name):
    with open(file_name, 'r+', encoding="utf-16") as file:
        for line in file.readlines():
            if "PAGE" in line:
                print(line)
        
if __name__ == '__main__':
    parse_text('./MaddenCo/20220106.txt')
    print("done")
    