from report_parser import Parser
from flask import Blueprint, request, render_template, redirect
from utility import create_temp_files

parse_bp = Blueprint('parse', __name__, url_prefix='/parse',
                  template_folder='templates')


@parse_bp.route('/',  methods=["GET", "POST"])
def parse():
    if request.method == "GET":
        return render_template('parse.html')
    else:
        method = request.form['method']
        parser = Parser()

        if method == "single":
            daily = request.files['formFileDaily']
            all = request.files['formFileAll']
            create_temp_files(daily, all)
            parser.parse_text("./data/temp/" + daily.filename)
            parser.parse_text("./data/temp/" + all.filename)
        elif method == "multiple":
            files = request.files.getlist('formFileMultiple')
            for file in files:
                create_temp_files(file)
                parser.parse_text("./data/temp/" + file.filename)

        return redirect('/sheets')
