import os
from file_parsing.utility import createDependencies
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/parse',  methods=["GET", "POST"])
def parse():
    if request.method == "GET":
        return render_template('parse.html')

if __name__ == '__main__':
    createDependencies(os.path)
    c
    app.run(debug=True)
    # app = Snowball()
