from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from file_input import FileInput


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
        self.inputFiles.setAllFile(self.allFileEntryText.get())
        self.inputFiles.setStandardFile(self.standardFileEntryText.get())
        self.inputFiles.setOutputFile(self.outFileEntryText.get())
        print(f'All File: {self.inputFiles.getAllFile()} \nStandard File: {self.inputFiles.getStandardFile()} \nOutFile: {self.inputFiles.getOutputFile()}')

    def close(self):
        print("Clean up and Close")


app = Snowball()
