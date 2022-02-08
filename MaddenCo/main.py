import pandas as pd
from file_parser import FileParser


def generate_excel_file(data):
    # create dataframe
    columns = ['Date Created', 'Sup Code', 'Sub Dept', 'Email', 'Employee #',
               'Support #', 'Last User', 'Original User', 'Time Last Changed']
    df = pd.DataFrame(data, columns=columns)

    # XLSX writer objects
    writer = pd.ExcelWriter("output.xlsx",
                            engine='xlsxwriter',
                            options={'strings_to_numbers': True})
    df.to_excel(writer, sheet_name='MaddenCo Data {Date}', index=False)
    workbook = writer.book
    worksheet = writer.sheets['MaddenCo Data {Date}']

    # formats
    red_format = workbook.add_format(
        {'bg_color': 'white', 'font': 'Calibri Light', 'font_size': '12', 'align': 'center'})
    green_format = workbook.add_format({'bg_color': 'black'})

    # set columns
    worksheet.set_column(0, 8, 20, red_format)
    worksheet.set_column(9, 10, 20, green_format)

    writer.save()
    print(df)


if __name__ == '__main__':
    file_parser = FileParser("./MaddenCo/20220106.txt")
    data = file_parser.parse_text()
    generate_excel_file(data)
    print("done")
