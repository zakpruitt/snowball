
import os
from file_parsing.interface import Snowball

if __name__ == '__main__':
    if not os.path.exists('generated'):
        os.makedirs('generated')
    app = Snowball()
