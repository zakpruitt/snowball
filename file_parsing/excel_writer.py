import pandas as pd
import json

class ExcelWriter:
    def __init__(self, outFile="output.xlsx"):
        self.writer = pd.ExcelWriter(outFile,
                                     engine='xlsxwriter',
                                     engine_kwargs={'options': {'strings_to_numbers': True}})
        self.workbook = self.writer.book
        self.formats = {}

    def create_and_write_new_sheet(self, sheet_name, dataframe, row_labels=False):
        dataframe.to_excel(
            self.writer,
            sheet_name=sheet_name,
            index=row_labels
        )

    def create_formats(self, format_path):
        file = open(format_path)
        format_file_contents=json.load(file)
        for i in format_file_contents["formats"]:
            name = i.pop("name")
            format = self.workbook.add_format(i)
            self.formats[name] = format

    def format_headers_sf(self, sheet_name, dataframe, buffer, format):
        worksheet = self.writer.sheets[sheet_name]
        for col in range(0 + buffer, len(dataframe.columns) + buffer):
            value = dataframe.columns.values[col - buffer]
            worksheet.write(0, col, value,
                            self.formats[format])

    def format_headers_af(self, sheet_name, dataframe, buffer, format1, format2):
        worksheet = self.writer.sheets[sheet_name]
        for col in range(0 + buffer, len(dataframe.columns) + buffer):
            value = dataframe.columns.values[col - buffer]
            if col % 2 == 0:
                worksheet.write(0, col, value,
                                self.formats[format1])
            else:
                worksheet.write(0, col, value,
                                self.formats[format2])

    def format_columns_sf(self, sheet_name, dataframe, buffer, spacing, format):
        worksheet = self.writer.sheets[sheet_name]
        for col in range(0, len(dataframe.columns) + buffer):
            worksheet.set_column(
                col, col, spacing, self.formats[format])

    def format_columns_af(self, sheet_name, dataframe, buffer, spacing, format1, format2):
        worksheet = self.writer.sheets[sheet_name]
        for col in range(0, len(dataframe.columns) + buffer):
            if col % 2 == 0:
                worksheet.set_column(
                    col, col, spacing, self.formats[format1])
            else:
                worksheet.set_column(
                    col, col, spacing, self.formats[format2])

    def format_row_index(self, sheet_name, dataframe, format):
        worksheet = self.writer.sheets[sheet_name]
        for row in range(0, len(dataframe.index)):
            value = dataframe.index.values[row]
            worksheet.write(row + 1, 0, value, self.formats[format])

    
