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
    blue_header_format = workbook.add_format(
        {'bg_color': '#5B9BD5', 'font': 'Calibri Light', 'font_size': '12', 'align': 'center',
         'border': 1})
    yellow_header_format = workbook.add_format(
        {'bg_color': '#FFC000', 'font': 'Calibri Light', 'font_size': '12', 'align': 'center',
         'border': 1})
    blue_format = workbook.add_format(
        {'bg_color': '#DDEBF7', 'font': 'Calibri Light', 'font_size': '12', 'align': 'center',
         'border': 1})
    yellow_format = workbook.add_format(
        {'bg_color': '#FFF2CC', 'font': 'Calibri Light', 'font_size': '12', 'align': 'center',
         'border': 1})

    # set column headers
    for col_num, value in enumerate(df.columns.values):
        if col_num % 2 == 0:
            worksheet.write(0, col_num, value, blue_header_format)
        else:
            worksheet.write(0, col_num, value, yellow_header_format)

    # set columns
    for col in range(0, 9):
        if col % 2 == 0:
            worksheet.set_column(col, col, 25, blue_format)
        else:
            worksheet.set_column(col, col, 25, yellow_format)

    writer.save()
    print(df)


if __name__ == '__main__':
    file_parser = FileParser("./MaddenCo/20220106.txt")
    data = file_parser.parse_text()
    generate_excel_file(data)
    print("done")
