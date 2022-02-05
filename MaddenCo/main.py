from file_parser import FileParser

if __name__ == '__main__':
    file_parser = FileParser("./MaddenCo/20220106.txt")
    file_parser.parse_text()
    print("done")
