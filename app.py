from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from base64 import b64encode
import argparse
import mysql.connector

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

db_connection = None

def get_db_connection():
    if db_connection is None:
        # TODO get your actual db connection string    
        db_connection = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "Johnisageek#1"
        )
    return db_connection
 
@app.route('/car/makes', methods=['GET'])
@cross_origin()
def get_cars():
    db = get_db_connection()
    db.cursor.execute("select * from get_cars_by_make_and_model() db_connection;")
        # jsonify and return results
    return jsonify(get_cars_by_make_and_model)
    # TODO get the value from the cursor, check for successful execution
    
    #return jsonify(["Chevrolet","GMC", "Saturn", "Ford", "Dodge", "Toyota"])

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
        if model == "Mustang":
            model_years = [1998]
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
        'images': ["mustang_front", "mustang_rear", "mustang_driver", "mustang_passenger"],
        'model': model,
        'year': year,
        'color': 'black',
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
        car_models = ["Windstar", "F-250", "Bronco Top", "Taurus", "Mustang", "Ranchero", "F-250"]
    elif make == "Dodge":
        car_models = ["Intrepid", "Grand Caravan", "Aries"]
    elif make == "Toyota":
        car_models = ["Camry", "Avalon"]
    else:
        car_models = ["no cars (in database) of this make"]
    return jsonify(car_models)

@app.route('/add_car', methods=['POST'])
@cross_origin()
def add_car():
    try:
        # Get JSON data from the request
        data = request.get_json()

        # Extract data members
        make = data['make']
        model = data['model']
        year = data['year']
        notes = data['notes']
        color = data['color']
        car_type = data['type']
        images = data['images']

        # You can perform further processing or validation here

        # Return a response
        response = {
            'status': 'success',
            'message': 'Car added successfully',
            'data': {
                'make': make,
                'model': model,
                'year': year,
                'notes': notes,
                'color': color,
                'type': car_type,
                'images': images
            }
        }
        return jsonify(response)

    except Exception as e:
        # Handle exceptions if any
        response = {
            'status': 'error',
            'message': str(e)
        }
        return jsonify(response)

@app.route('/getimage/<imagename>')
@cross_origin()
def get_image(imagename):
    try:
        image_path = f'images/{imagename}.png'
        # Read the image file
        with open(image_path, "rb") as image_file:
            # Convert the image to base64
            base64_data = b64encode(image_file.read()).decode('utf-8')

        # Create a JSON response with the base64 data
        json_response = {
            "success": True,
            "message": "Image converted to base64 successfully",
            "base64_data": base64_data
        }

    except FileNotFoundError:
        json_response = {
            "success": False,
            "message": "File not found. Please provide a valid file path."
        }
    except Exception as e:
        json_response = {
            "success": False,
            "message": f"An error occurred: {str(e)}"
        }

    return json_response


def parse_args():
    parser = argparse.ArgumentParser(description='Flask App with Port Option')
    parser.add_argument('--port', type=int, default=5000, help='Port number to run the Flask app on')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    # Listen on all network interfaces (0.0.0.0) and the specified port
    app.run(debug=True, host='0.0.0.0', port=args.port)
