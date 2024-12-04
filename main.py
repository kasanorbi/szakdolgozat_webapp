from flask import Flask
from flask_cors import CORS
from model.models import setup_database
from controller.bill_controller import bill
from controller.components_controller import components
from controller.customers_controller import customers
from controller.scan_controller import scan
from controller.statistics_controller import statistics
from wia_scan import *


app = Flask(__name__)

app.register_blueprint(bill, url_prefix='/')
app.register_blueprint(components, url_prefix='/')
app.register_blueprint(customers, url_prefix='/')
app.register_blueprint(scan, url_prefix='/')
app.register_blueprint(statistics, url_prefix='/')

CORS(app, resources={r'/*': {'origins': '*'}})


if __name__ == '__main__':
     setup_database()
     app.run(debug=True)
