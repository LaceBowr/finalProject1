from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from base64 import b64encode
import argparse
import mysql.connector
import os

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

db_connection = None

def get_db_connection():
    global db_connection
    if db_connection is None:
        # TODO get your actual db connection string    
        db_connection = mysql.connector.connect(
            host = "10.70.1.211",
            user = "serviceaccount",
            password = "test1234",
            db = "radical_wreckage_schema"
        )
    return db_connection

def perform_sql_select_return_as_list(select_query): 
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(select_query)
    results = cursor.fetchall()
    result_list = []
    for row in results:
        result_list.append(row[0])
    cursor.close()
    return result_list

# For images we are selecting 4 items, so this function return 4 items
def perform_sql_image_query(select_query): 
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(select_query)
    row = cursor.fetchone()
    result_list = []
    result_list.append(row[0])
    result_list.append(row[1])
    result_list.append(row[2])
    result_list.append(row[3])
    cursor.close()
    return result_list

@app.route('/car/makes', methods=['GET'])
@cross_origin()
def get_cars():
    query_str = 'select distinct make_name from cars join makes on cars.makes_id=makes.id;'   
    result_list = perform_sql_select_return_as_list(query_str)
    return jsonify(result_list)  

@app.route('/car/<make>/<model>', methods=['GET'])
@cross_origin()
def get_cars_by_make_and_model(make, model):
    query_str = f'select year from cars join makes on cars.makes_id=makes.id where make_name="{make}" and model="{model}" order by year asc;'
    result_list = perform_sql_select_return_as_list(query_str)
    return jsonify(result_list) 

@app.route('/car/<make>/<model>/<year>', methods=['GET'])
@cross_origin()
def get_cars_by_make_and_model_and_year(make, model, year):
    query_str = f'select driver_side_image, passenger_side_image, rear_view_image, front_view_image  from cars join makes on cars.makes_id=makes.id where make_name="{make}" and model="{model}" and year={year};'
    images = perform_sql_image_query(query_str)
    print("Images:", images)
    car_data = [{
        'make': make,
        'images': images,
        'model': model,
        'year': year,
        'color': '',
        'mileage': 0,
        'notes': ''
    }]
    return jsonify(car_data)

@app.route('/car/models/<make>/<year>')
@cross_origin()
def get_car_year(makes_id, make_name, year):
    yearstr = f'select * from cars join makes on cars.makes_id="{makes_id}" where makes make_name="{make_name}" and year="{year}" order by year asc;'
    result_list = perform_sql_select_return_as_list(yearstr)
    return jsonify(result_list)

@app.route('/car/models/<make>')
@cross_origin()
def get_car_models(make):
    querystr = f'select distinct model from cars join makes on cars.makes_id=makes.id where makes.make_name="{make}" order by model asc;'
    result_list = perform_sql_select_return_as_list(querystr)
    return jsonify(result_list)  

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
        image_type = "png"
        if not os.path.exists(image_path):
            image_path = f'images/{imagename}.jpg'
            if not os.path.exists(image_path):
                image_path = f'images/{imagename}.jpeg'
            image_type = "jepg"
        # Read the image file
        with open(image_path, "rb") as image_file:
            # Convert the image to base64
            base64_data = b64encode(image_file.read()).decode('utf-8')

        # Create a JSON response with the base64 data
        json_response = {
            "success": True,
            "message": "Image converted to base64 successfully",
            "base64_data": base64_data,
            "image_type": image_type 
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
