import pandas as pd
from file_parser import FileParser
from excel_writer import ExcelWriter
from datetime import date

# def generate_excel_file(*dataframes, *sheet_names):
#     # create dataframes
#     columns = ['Date Created', 'Sup Code', 'Sub Dept', 'Email', 'Employee #',
#                'Support #', 'Last User', 'Original User', 'Time Last Changed']
#     info_df = pd.DataFrame(information, columns=columns)
#     count_df = pd.DataFrame(count)

#     # create excel writer
#     excel_writer = ExcelWriter("output")

#     # create sheets
#     today = date.today()
#     formatted_date = today.strftime("%d/%m/%Y")
#     excel_writer.create_and_write_new_sheet("", info_df)

#     # XLSX writer objects
#     writer = pd.ExcelWriter("output.xlsx",
#                             engine='xlsxwriter',
#                             options={'strings_to_numbers': True})
#     info_df.to_excel(writer, sheet_name='MaddenCo Data {Date}', index=False)
#     count_df.to_excel(writer, sheet_name='MaddenCo Counts {Date}', index=True)
#     workbook = writer.book
#     info_worksheet = writer.sheets['MaddenCo Data {Date}']
#     count_worksheet = writer.sheets['MaddenCo Counts {Date}']

#     # formats
#
#     yellow_header_format = workbook.add_format(
#         {'bg_color': '#FFC000', 'font': 'Calibri Light', 'font_size': '12', 'align': 'center',
#          'border': 1})
#     blue_format = workbook.add_format(
#         {'bg_color': '#DDEBF7', 'font': 'Calibri Light', 'font_size': '12', 'align': 'center',
#          'border': 1})
#     yellow_format = workbook.add_format(
#         {'bg_color': '#FFF2CC', 'font': 'Calibri Light', 'font_size': '12', 'align': 'center',
#          'border': 1})

#     # set info column headers
#     for col_num, value in enumerate(info_df.columns.values):
#         if col_num % 2 == 0:
#             info_worksheet.write(0, col_num, value, blue_header_format)
#         else:
#             info_worksheet.write(0, col_num, value, yellow_header_format)

#     # set info columns
#     for col in range(0, 9):
#         if col % 2 == 0:
#             info_worksheet.set_column(col, col, 25, blue_format)
#         else:
#             info_worksheet.set_column(col, col, 25, yellow_format)

#     # set count column headers
#     for col_num, value in enumerate(count_df.columns.values):
#         if col_num % 2 == 0:
#             count_worksheet.write(0, col_num + 1, value, blue_header_format)
#         else:
#             count_worksheet.write(0, col_num + 1, value, yellow_header_format)

#     for col_num, value in enumerate(count_df.index.values):
#         count_worksheet.write(0, col_num + 1, value, blue_header_format)

#     count_worksheet.write(0, 0, "Employee #", blue_header_format)
#     for row in range(0, 4):
#         value = count_df.index.values[row]
#         count_worksheet.write(row + 1, 0, value, blue_header_format)

#     for col in range(0, len(count_df.columns) + 1):
#         count_worksheet.set_column(col, col, 25, blue_format)

#     writer.save()


if __name__ == '__main__':
    # parse text file(s)
    file_parser = FileParser("./MaddenCo/20220106.txt")
    file_parser.parse_text()

    # create excel_writer object and dataframes
    excel_writer = ExcelWriter()
    columns = ['Date Created', 'Sup Code', 'Sub Dept', 'Email', 'Employee #',
               'Support #', 'Last User', 'Original User', 'Time Last Changed']
    info_df = pd.DataFrame(file_parser.line_information, columns=columns)
    count_df = pd.DataFrame(file_parser.count_information)

    # create and write new sheets
    today = date.today()
    formatted_date = today.strftime("%m-%d-%Y")
    excel_writer.create_and_write_new_sheet(
        f"MaddenCo Data {formatted_date}", info_df)
    excel_writer.create_and_write_new_sheet(
        f"MaddenCo Count {formatted_date}", count_df, True)

    # create formats
    excel_writer.create_format(
        "blue_header_format", '#5B9BD5', 'Calibri Light', '12', 'center', 1)
    excel_writer.create_format(
        "yellow_header_format", '#FFC000', 'Calibri Light', '12', 'center', 1)
    excel_writer.create_format(
        "blue_format", '#DDEBF7', 'Calibri Light', '12', 'center', 1)
    excel_writer.create_format(
        "yellow_format", '#FFF2CC', 'Calibri Light', '12', 'center', 1)
    excel_writer.create_format(
        "cyan_header_format", "#4BACC6", 'Calibri Light', '12', 'center', 1)
    excel_writer.create_format(
        "orange_header_format", "#F79646", 'Calibri Light', '12', 'center', 1)
    excel_writer.create_format(
        "cyan_format", "#DAEEF3", 'Calibri Light', '12', 'center', 1)
    excel_writer.create_format(
        "orange_format", "#FDE9D9", 'Calibri Light', '12', 'center', 1)

    # format sheets
    excel_writer.format_headers_af(
        f"MaddenCo Data {formatted_date}", info_df, 0, "blue_header_format", "yellow_header_format")
    excel_writer.format_columns_af(
        f"MaddenCo Data {formatted_date}", info_df, 0, 25, "blue_format", "yellow_format")
    excel_writer.format_headers_af(
        f"MaddenCo Count {formatted_date}", count_df, 1, "cyan_header_format", "orange_header_format")
    excel_writer.format_columns_af(
        f"MaddenCo Count {formatted_date}", count_df, 1, 25, "cyan_format", "orange_format")
    
    # save
    excel_writer.writer.save()
    print("done")
