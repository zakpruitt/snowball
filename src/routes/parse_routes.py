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
        # create temp files
        daily = request.files['formFileDaily']
        all = request.files['formFileAll']
        create_temp_files(daily, all)

        # parse temp files
        parser = Parser()
        parser.parse_text("./data/temp/" + daily.filename)
        parser.parse_text("./data/temp/" + all.filename)

        return redirect('/sheets')
