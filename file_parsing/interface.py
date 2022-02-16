from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from file_parsing.file_input import FileInput
from file_parsing.parser import Parser
from file_parsing.excel_writer import ExcelWriter
from datetime import date
import pandas as pd

class Snowball:

    def __init__(self):
        self.inputFiles = FileInput()

        self.winWidth = 800
        self.winHeight = 200

        self.root = Tk()
        self.root.title('Snowball - File Parser')
        self.root.minsize(width=self.winWidth, height=self.winHeight)
        self.root.grid_columnconfigure(0, weight=1)

        self.inputFrame = ttk.Frame(self.root, padding="3 3 12 12")
        self.inputFrame.grid(column=0, row=0, sticky=(N, W, E, S))
        self.inputFrame.grid_columnconfigure(1, weight=1)

        self.controlFrame = ttk.Frame(self.root, padding="3 3 12 12")
        self.controlFrame.grid(column=0, row=1, sticky=(N, S, E, W))
        self.controlFrame.grid_columnconfigure(0, weight=1)
        self.controlFrame.grid_columnconfigure(1, weight=1)

        ttk.Label(self.inputFrame, text="All File Selected:").grid(
            column=0, row=0)
        self.allFileEntryText = StringVar()
        self.allFileEntry = Entry(self.inputFrame, textvariable=self.allFileEntryText).grid(
            column=1, row=0, sticky=(W, E))
        self.allFileButton = Button(self.inputFrame, text="Select \"All\" File",
                                    command=self.fetchAllFile).grid(column=2, row=0, sticky=(W, E))

        ttk.Label(self.inputFrame, text="Standard File Selected:").grid(
            column=0, row=1)
        self.standardFileEntryText = StringVar()
        self.standardFileEntry = Entry(self.inputFrame, textvariable=self.standardFileEntryText).grid(
            column=1, row=1, sticky=(W, E))
        self.standardFileButton = Button(self.inputFrame, text="Select Standard File",
                                         command=self.fetchStandardFile).grid(column=2, row=1, sticky=(W, E))

        Label(self.inputFrame, text="Out File Selected:").grid(column=0, row=2)
        self.outFileEntryText = StringVar()
        self.outFileEntry = Entry(self.inputFrame, textvariable=self.outFileEntryText).grid(
            column=1, row=2, sticky=(W, E))
        self.outFileButton = Button(self.inputFrame, text="Select Out File",
                                    command=self.fetchOutputFile).grid(column=2, row=2, sticky=(W, E))

        for child in self.inputFrame.winfo_children():
            child.grid_configure(padx=5, pady=5)

        Button(self.controlFrame, text="Parse Files",
               command=self.startParse).grid(column=0, row=0)
        Button(self.controlFrame, text="Close",
               command=self.close).grid(column=1, row=0)

        self.root.mainloop()

    def fetchAllFile(self):
        file = filedialog.askopenfilename()
        self.inputFiles.setAllFile(file)
        self.allFileEntryText.set(file)

    def fetchStandardFile(self):
        file = filedialog.askopenfilename()
        self.inputFiles.setAllFile(file)
        self.standardFileEntryText.set(file)

    def fetchOutputFile(self):
        file = filedialog.askopenfilename()
        self.inputFiles.setOutputFile(file)
        self.outFileEntryText.set(file)
    
    def startParse(self):
        # parse text file(s)
        file_parser = Parser(self.allFileEntryText.get())
        file_parser.parse_text()

        # create excel_writer object and dataframes
        excel_writer = ExcelWriter(self.outFileEntryText.get())
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
        excel_writer.format_row_index(
            f"MaddenCo Count {formatted_date}", count_df, "cyan_header_format")

        # save
        excel_writer.writer.save()
        print("Done!")

    def close(self):
        print("Clean up and Close")

