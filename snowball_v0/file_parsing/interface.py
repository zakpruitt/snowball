from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from file_parsing.file_input import FileInput
from parser import Parser
from file_parsing.excel_writer import ExcelWriter
import sys
import traceback
from datetime import date, datetime
import pandas as pd
import xlwings as xw
from utility import get_file_date, get_date_time


class Snowball:
    def __init__(self):
        self.inputFiles = FileInput()

        self.winWidth = 800
        self.winHeight = 200

        # initialize root
        self.root = Tk()
        self.root.title('Snowball - File Parser')
        self.root.minsize(width=self.winWidth, height=self.winHeight)
        self.root.grid_columnconfigure(0, weight=1)

        # define frame for input lines
        self.inputFrame = ttk.Frame(self.root, padding="3 3 12 12")
        self.inputFrame.grid(column=0, row=0, sticky=(N, W, E, S))
        self.inputFrame.grid_columnconfigure(1, weight=1)

        # define frame for parse and cancel buttons
        self.controlFrame = ttk.Frame(self.root, padding="3 3 12 12")
        self.controlFrame.grid(column=0, row=1, sticky=(N, S, E, W))
        self.controlFrame.grid_columnconfigure(0, weight=1)
        self.controlFrame.grid_columnconfigure(1, weight=1)

        # create All File controls
        ttk.Label(self.inputFrame, text="All File Selected:").grid(
            column=0, row=0)
        self.allFileEntryText = StringVar()
        self.allFileEntry = Entry(self.inputFrame, textvariable=self.allFileEntryText).grid(
            column=1, row=0, sticky=(W, E))
        self.allFileButton = Button(self.inputFrame, text="Select All File",
                                    command=self.fetchAllFile).grid(column=2, row=0, sticky=(W, E))

        # create daily file controls
        ttk.Label(self.inputFrame, text="Daily File Selected:").grid(
            column=0, row=1)
        self.dailyFileEntryText = StringVar()
        self.dailyFileEntry = Entry(self.inputFrame, textvariable=self.dailyFileEntryText).grid(
            column=1, row=1, sticky=(W, E))
        self.dailyFileButton = Button(self.inputFrame, text="Select Daily File",
                                      command=self.fetchDailyFile).grid(column=2, row=1, sticky=(W, E))

        # create output file controls
        Label(self.inputFrame, text="Out File Selected:").grid(column=0, row=2)
        self.outFileEntryText = StringVar()
        self.outFileEntry = Entry(self.inputFrame, textvariable=self.outFileEntryText).grid(
            column=1, row=2, sticky=(W, E))
        self.outFileButton = Button(self.inputFrame, text="Select Out File",
                                    command=self.fetchOutputFile).grid(column=2, row=2, sticky=(W, E))

        for child in self.inputFrame.winfo_children():
            child.grid_configure(padx=5, pady=5)

        Button(self.controlFrame,
               text="Parse Files",
               command=self.startParse,
               height=3,
               width=20,
               bg='violet',
               fg='white').grid(column=0, row=0, padx=2, sticky=(W, E))

        Button(self.controlFrame, 
                text="Close",
               command=self.root.destroy,
               height=3,
               width=20,
               bg='violet',
               fg='white').grid(column=1, row=0, padx=2, sticky=(W, E))

        self.root.mainloop()

    def fetchAllFile(self):
        file = filedialog.askopenfilename()
        self.inputFiles.setAllFile(file)
        self.allFileEntryText.set(file)

    def fetchDailyFile(self):
        file = filedialog.askopenfilename()
        self.inputFiles.setAllFile(file)
        self.dailyFileEntryText.set(file)

    def fetchOutputFile(self):
        file = filedialog.askopenfilename()
        self.inputFiles.setOutputFile(file)
        self.outFileEntryText.set(file)

    def startParse(self):
        try:
            # parse text file(s)
            all_parser = Parser(self.allFileEntryText.get())
            all_parser.parse_text()
            daily_parser = Parser(self.dailyFileEntryText.get())
            daily_parser.parse_text()

            # check date
            formatted_date = None
            if get_file_date(self.allFileEntryText.get()) == get_file_date(self.dailyFileEntryText.get()):
                formatted_date = get_file_date(self.dailyFileEntryText.get())
            else:
                raise Exception("All and Daily files are not from the same day.")

            # create excel_writer object and dataframes
            excel_writer = ExcelWriter(
                f"./generated/output {formatted_date}.xlsx")
            columns = ['Date Created', 'Sup Code', 'Sub Dept', 'Email', 'Employee #',
                       'Support #', 'Last User', 'Original User', 'Time Last Changed']
            all_df = pd.DataFrame(all_parser.line_information, columns=columns)
            daily_df = pd.DataFrame(daily_parser.line_information, columns=columns)
            all_count_df = pd.DataFrame(all_parser.count_information)
            daily_count_df = pd.DataFrame(daily_parser.count_information)

            # create total count df
            total_count_info = all_parser.count_information
            for key in daily_parser.count_information.keys():
                if key not in total_count_info:
                    total_count_info[key] = daily_parser.count_information[key]
                else:
                    for sub_key in daily_parser.count_information[key].keys():
                        total_count_info[key][sub_key] += daily_parser.count_information[key][sub_key]
            count_df = pd.DataFrame(total_count_info)

            # create and write new sheets
            excel_writer.create_and_write_new_sheet(
                f"MaddenCo Daily Data {formatted_date}", daily_df)
            excel_writer.create_and_write_new_sheet(
                f"MaddenCo All Data {formatted_date}", all_df)
            excel_writer.create_and_write_new_sheet(
                f"MaddenCo Daily Count {formatted_date}", daily_count_df, True)
            excel_writer.create_and_write_new_sheet(
                f"MaddenCo All Count {formatted_date}", all_count_df, True)
            excel_writer.create_and_write_new_sheet(
                f"MaddenCo Total Count {formatted_date}", count_df, True)

            excel_writer.create_formats("./config/excel_formats.json")

            # format sheets
            excel_writer.format_headers_af(
                f"MaddenCo Daily Data {formatted_date}", all_df, 0, "blue_header_format", "yellow_header_format")
            excel_writer.format_columns_af(
                f"MaddenCo Daily Data {formatted_date}", all_df, 0, 25, "blue_format", "yellow_format")

            excel_writer.format_headers_af(
                f"MaddenCo All Data {formatted_date}", all_df, 0, "blue_header_format", "yellow_header_format")
            excel_writer.format_columns_af(
                f"MaddenCo All Data {formatted_date}", all_df, 0, 25, "blue_format", "yellow_format")

            excel_writer.format_headers_af(
                f"MaddenCo Daily Count {formatted_date}", daily_count_df, 1, "cyan_header_format", "orange_header_format")
            excel_writer.format_columns_af(
                f"MaddenCo Daily Count {formatted_date}", daily_count_df, 1, 25, "cyan_format", "orange_format")
            excel_writer.format_row_index(
                f"MaddenCo Daily Count {formatted_date}", daily_count_df, "cyan_header_format")

            excel_writer.format_headers_af(
                f"MaddenCo All Count {formatted_date}", all_count_df, 1, "cyan_header_format", "orange_header_format")
            excel_writer.format_columns_af(
                f"MaddenCo All Count {formatted_date}", all_count_df, 1, 25, "cyan_format", "orange_format")
            excel_writer.format_row_index(
                f"MaddenCo All Count {formatted_date}", all_count_df, "cyan_header_format")

            excel_writer.format_headers_af(
                f"MaddenCo Total Count {formatted_date}", count_df, 1, "cyan_header_format", "orange_header_format")
            excel_writer.format_columns_af(
                f"MaddenCo Total Count {formatted_date}", count_df, 1, 25, "cyan_format", "orange_format")
            excel_writer.format_row_index(
                f"MaddenCo Total Count {formatted_date}", count_df, "cyan_header_format")

            # save
            excel_writer.writer.save()
            xw.Book(f"./generated/output {formatted_date}.xlsx")
            messagebox.showinfo(title="Complete", message="Parsing was successful!")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            messagebox.showerror("Error", e)
            with open("error_log.txt", "a") as f:
                f.write(f"{get_date_time()} on file {get_file_date(self.allFileEntryText.get())} on line {traceback.format_exc()} - {e} | {exc_type} | {exc_obj} | {exc_tb} \n\n\n")
