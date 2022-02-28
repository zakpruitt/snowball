import os
from file_parsing.interface import Snowball
from file_parsing.utility import createDependencies
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

if __name__ == '__main__':
    createDependencies(os.path)
    app.run(debug=True)
    # app = Snowball()