from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from Inputs_Class import InputFiles

class SnowBall:

    def __init__(self):
        self.inputFiles = InputFiles()

        self.winWidth = 400
        self.winHeight = 400

        self.root = Tk()
        self.root.title('Snowball - File Parser')
        self.root.geometry(f'{self.winWidth}x{self.winWidth}')

        self.allFileFrame = Frame()
        Label(master=self.allFileFrame, text="All File Selected:").pack()
        self.allFileLabelText = StringVar()
        self.allFileLabel = Label(master=self.allFileFrame, textvariable=self.allFileLabelText)
        self.allFileButton = Button(master=self.allFileFrame, text="Select \"All\" File", command = self.fetchAllFile)
        

        self.standardFileFrame = Frame()
        Label(master=self.standardFileFrame, text="Standard File Selected:").pack()
        self.standardFileLabelText = StringVar()
        self.standardFileLabel = Label(master=self.standardFileFrame, textvariable=self.standardFileLabelText)
        self.standardFileButton = Button(master=self.standardFileFrame, text="Select Standard File", command = self.fetchStandardFile)

        self.outFileFrame = Frame()
        Label(master=self.outFileFrame, text="Out File Selected:").pack()
        self.outFileLabelText = StringVar()
        self.outFileLabel = Label(master=self.outFileFrame,textvariable=self.outFileLabelText)
        self.outFileButton = Button(master=self.outFileFrame, text="Select Out File", command = self.fetchOutputFile)

        self.controlFrame = Frame()
        Button(master=self.controlFrame, text="Parse Files", command=self.startParse).pack()
        Button(master=self.controlFrame, text="Close", command=self.close).pack()


        
        self.allFileLabel.pack()
        self.allFileButton.pack()
        self.allFileFrame.pack()

        
        self.standardFileLabel.pack()
        self.standardFileButton.pack()
        self.standardFileFrame.pack()

        
        self.outFileLabel.pack()
        self.outFileButton.pack()
        self.outFileFrame.pack()

        self.controlFrame.pack()
        self.root.mainloop()


    def fetchAllFile(self):
        file = filedialog.askopenfilename()
        self.inputFiles.setAllFile(file)
        self.allFileLabelText.set(file)
        
        
    def fetchStandardFile(self):
        file = filedialog.askopenfilename()
        self.inputFiles.setAllFile(file)
        self.standardFileLabelText.set(file)
        
    def fetchOutputFile(self):
        file = filedialog.askopenfilename()
        self.inputFiles.setOutputFile(file)
        self.outFileLabelText.set(file)

    def startParse(self):
        print("Do Stuff")
    
    def close(self):
        print("Clean up and Close")

app=SnowBall()