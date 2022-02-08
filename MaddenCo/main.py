import pandas as pd
from file_parser import FileParser


def generate_excel_file(data):
    columns = ['Date Created', 'Sup Code', 'Sub Dept', 'Email', 'Employee #',
               'Support #', 'Last User', 'Original User', 'Time Last Changed']
    df = pd.DataFrame(data, columns=columns)
    writer = pd.ExcelWriter("output.xlsx", engine='xlsxwriter')
    df.to_excel('output.xlsx', index=False)
    print(df)


if __name__ == '__main__':
    file_parser = FileParser("./MaddenCo/20220106.txt")
    data = file_parser.parse_text()
    generate_excel_file(data)
    print("done")
