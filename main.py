import os
from file_parsing.interface import Snowball
from file_parsing.utility import createDependencies

if __name__ == '__main__':
    createDependencies(os.path)
    app = Snowball()
