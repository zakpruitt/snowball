import pandas as pd


class ExcelWriter:
    def __init__(self):
        self.writer = pd.ExcelWriter("output.xlsx",
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

    def create_format(self, format_name, bg_color, font, font_size, align, border):
        format = self.workbook.add_format(
            {'bg_color': bg_color, 'font': font, 'font_size': font_size, 'align': align,
             'border': border})
        self.formats[format_name] = format

    def format_headers_sf(self, sheet_name, dataframe, buffer, format):
        worksheet = self.writer.sheets[sheet_name]
        for col_num, value in enumerate(dataframe.columns.values):
            worksheet.write(0, col_num + buffer, value, self.formats[format])

    def format_headers_af(self, sheet_name, dataframe, buffer, format1, format2):
        worksheet = self.writer.sheets[sheet_name]
        for col_num, value in enumerate(dataframe.columns.values):
            if col_num % 2 == 0:
                worksheet.write(0, col_num + buffer, value,
                                self.formats[format1])
            else:
                worksheet.write(0, col_num + buffer, value,
                                self.formats[format2])

    def format_columns_sf(self, sheet_name, dataframe, spacing, format):
        worksheet = self.writer.sheets[sheet_name]
        for col in range(0, len(dataframe.columns)):
            worksheet.set_column(col, col, spacing, self.formats[format])

    def format_columns_af(self, sheet_name, dataframe, buffer, spacing, format1, format2):
        worksheet = self.writer.sheets[sheet_name]
        for col in range(0, len(dataframe.columns)):
            if col % 2 == 0:
                worksheet.set_column(col, col + buffer, spacing, self.formats[format1])
            else:
                worksheet.set_column(col, col + buffer, spacing, self.formats[format2])
