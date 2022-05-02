import os
from flask import Flask
from utility import create_dependencies
from routes.home_routes import home_bp
from routes.parse_routes import parse_bp
from routes.sheets_routes import sheets_bp
from routes.visualize_routes import visualize_bp
from routes.data_routes import data_bp
from routes.settings_routes import settings_bp

app = Flask(__name__)
app.register_blueprint(home_bp)
app.register_blueprint(parse_bp)
app.register_blueprint(sheets_bp)
app.register_blueprint(visualize_bp)
app.register_blueprint(data_bp)
app.register_blueprint(settings_bp)

if __name__ == '__main__':
    create_dependencies(os.path)
    app.run(debug=False)
