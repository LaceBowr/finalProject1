from flask import Flask, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
#CORS(app, origins='http://localhost:8400') 
#CORS(app, resources={r"/api/*": {"origins": "http://localhost:8400"}})
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/car/makes', methods=['GET'])
@cross_origin()
def get_cars():
    return jsonify(["Chevrolet","GMC", "Saturn", "Ford", "Dodge", "Toyota"])

@app.route('/car/<make>/<model>', methods=['GET'])
@cross_origin()
def get_cars_by_make_and_model(make, model):
    model_years = []
    if make == "Chevrolet":
        if model == "Cavalier":
            model_years = [1978, 1997, 2001, 2010]
    elif make == "GMC":
        if model == "k-1500":
            model_years = [1986]
    elif make == "Saturn":
        if model == "Ion":
            model_years = [2004]
    elif make == "Ford":
        if model == "Windstar-LX":
            model_years = [2002]
    elif make == "Dodge":
        if model == "Intrepid":
            model_years = [1994]
    elif make == "Toyota":
        if model == "Avalon":
            model_years = [2000]
    else:
        if model == "":
            model_years = []
    return jsonify(model_years)

@app.route('/car/<make>/<model>/<year>', methods=['GET'])
@cross_origin()
def get_cars_by_make_and_model_and_year(make, model, year):
    car_data = [{
        'make': make,
        'images': ["images\driver-side-image.png", "images\passenger-side-image.png", "images\\front-view-image.png", "images\\rear-view-image.png"],
        'model': model,
        'year': year,
        'color': 'blue',
        'mileage': 99000,
        'notes': ''
    }]
    return jsonify(car_data)


@app.route('/car/models/<make>')
@cross_origin()
def get_car_models(make):
    car_models = []
    if make == "Chevrolet":
        car_models = ["Cabriolet", "Cavalier", "Camero", "Silverado"]
    elif make == "GMC":
        car_models = ["k-1500"]
    elif make == "Saturn":
        car_models = ["Ion", "SL2", "L2"]
    elif make == "Ford":
        car_models = ["Windstar-LX", "F-250", "Bronco Top", "Taurus", "Mustang", "Ranchero", "F-250"]
    elif make == "Dodge":
        car_models = ["Intrepid", "Grand Caravan", "Aries"]
    elif make == "Toyota":
        car_models = ["Camry", "Avalon"]
    else:
        car_models = ["no cars (in database) of this make"]
    return jsonify(car_models)

'''
@app.route('/cars', methods=['GET'])
def get_cars():
    all_cars = {
        'make': 'Chevrolet',
        'model': 'Tahoe',
        'year': 2008,
        'color': 'Black',
        'mileage': 15000;

        'make': 'Dodge',
        'model': 'Grand Caravan',
        'year': 2002,
        'color': 'white',
        'mileage': 25000;

        'make': 'Mecury',
        'model': 'Tracer',
        'year': 1990,
        'color': 'pearl',
        'mileage': 70000
    }
    return jsonify(all_cars)

@app.route('/cars/<make>', methods=['GET'])
def list_of_car_makes_details(make):
    find_makes_list = {
        if make = 'Chevrolet'
            apend.car_data((car_data) in list_of_car_makes)
        elif make = 'GMC'
            apend.car_data((car_data) in list_of_car_makes)
        elif make = 'Saturn'
            apend.car_data((car_data) in list_of_car_makes)
        elif make = 'Ford'
            apend.car_data((car_data) in list_of_car_makes)
        elif make = 'Dodge'
            apend.car_data((car_data) in list_of_car_makes)
        else:
            make = []
            apend.car_data((car_data))
        }
        return (list_of_car_makes_details)
            print((car_data) in find_makes_list)
'''
if __name__ == '__main__':
    app.run(debug=True)
