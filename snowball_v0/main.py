import os
from file_parsing.interface import Snowball
from utility import create_dependencies

if __name__ == '__main__':
    create_dependencies(os.path)
    app = Snowball()
