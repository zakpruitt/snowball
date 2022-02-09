import string


class FileInput:
    allFilePath = ''
    standardFilePath = ''
    outputFilePath = ''

    def setAllFile(self, filePath):
        self.allFilePath = filePath
    def setStandardFile(self, filePath):
        self.standardFilePath = filePath
    def setOutputFile(self, filePath):
        self.outputFilePath = filePath

    def getAllFile(self):
        return self.allFilePath
    def getStandardFile(self):
        return self.standardFilePath
    def getOutputFile(self):
        return self.outputFilePath

