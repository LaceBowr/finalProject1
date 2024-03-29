from flask import Flask, jsonify, request, Response
from flask_cors import CORS, cross_origin
from base64 import b64encode
import argparse
import mysql.connector
import boto3
import json
import os
from botocore.exceptions import ClientError

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

siteadminusername = ''
siteadminpassword = ''
dbusername = ''
dbpassword = ''

def get_db_connection():
    db_connection = mysql.connector.connect(
        host = "mysql-database-2.cvg0q2icw2th.us-east-2.rds.amazonaws.com",
        user = dbusername,
        password = dbpassword,
        db = "radical_wreckage_schema"
    )
    return db_connection

def init_db_creds_from_secretsmanager(secret_name, region_name):

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secrets_dict = json.loads(get_secret_value_response['SecretString'])
    return secrets_dict['username'], secrets_dict['password']

def perform_sql_select_return_as_list_of_tuples(select_query): 
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(select_query)
    results = cursor.fetchall()
    result_list = []
    for row in results:
        result_list.append((row[0],row[1]))
    cursor.close()
    db.close()
    return result_list

def perform_sql_delete_query(query_str):
    rval = True
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute(query_str)
        db.commit()
        cursor.close()
        db.close()
    except:
        rval = False
    return rval

def perform_sql_select_return_as_list(select_query): 
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(select_query)
    results = cursor.fetchall()
    result_list = []
    for row in results:
        result_list.append(row[0])
    cursor.close()
    db.close()
    return result_list

def perform_sql_insert_query(insert_statement):
    rval = False
    try: 
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute(insert_statement)
        db.commit()
        cursor.close()
        db.close()
        rval = True
    except mysql.connector.Error as e:
        print(f"Error inserting value: {e}")
    return rval

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
    db.close()
    return result_list

# Function to validate basic authentication credentials
def authenticate(username, password):
    #print(f'comparing {siteadminusername} to {username} and {siteadminpassword} to {password}', )
    if siteadminusername == username and siteadminpassword == password:
        return True
    return False

@app.route('/add_car_makes', methods=['POST'])
@cross_origin()
def add_new_make():
    
    auth = request.authorization
    if not auth or not authenticate(auth.username, auth.password):
        return Response('Unauthorized', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

    if not request.is_json:
        print("Not valid json")
        return jsonify ({"result": False, "desc": "Invalid data"})
    #Start here
    make_name = request.json.get("make_name")
    print(f"Requested to insert make name {make_name}")
    query_str = f'insert into makes(make_name) values("{make_name}");'
    #End here -- all the different code for the add car function will 
    #be between these line.  You get car data out of the json and create 
    # your sql query string and then let it be executed below exactly the
    # same as the and_new_make function.
    rval = perform_sql_insert_query(query_str)
    rval = jsonify ({"result": rval})
    print("Add car make result:", rval)
    return rval

@app.route('/add_car_data', methods=['POST'])
@cross_origin()
def add_new_car():

    auth = request.authorization
    if not auth or not authenticate(auth.username, auth.password):
        return Response('Unauthorized', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

    if not request.is_json:
        print("Not valid json")
        return jsonify ({"result": False, "desc": "Invalid data"})
    #print("Got a request to add a new car", request.json)
    #Start here
    #enter all variable names here to make the insert 
    color = request.json.get("color")
    year = request.json.get("year")
    driver_side_image = request.json.get("driver_side_image")
    passenger_side_image = request.json.get("passenger_side_image")
    rear_view_image = request.json.get("rear_view_image")
    front_view_image = request.json.get("front_view_image")
    cost = 0
    try:
        cost = int(request.json.get("cost"))
    except:
        print(f"Cost value: '{request.json.get('cost')}' could not be converted to integer value, it will be inserted as 0")
    sold = 0
    try:
        sold = int(request.json.get("sold"))
    except:
        print(f"sold value: '{request.json.get('sold')}' could not be converted to integer value, it will be inserted as 0")
      
    make_name = request.json.get("make_name")
    makes_id = perform_sql_select_return_as_list( f"select id from makes where make_name= '{make_name}';")
    print(f'Requested to insert make id {makes_id}')
    model = request.json.get("model")
    query_str = f"insert into cars (color, year, driver_side_image, passenger_side_image, rear_view_image, front_view_image, cost, sold, makes_id, model) values ('{color}', {year}, '{driver_side_image}', '{passenger_side_image}', '{rear_view_image}', '{front_view_image}', {cost}, {sold}, {makes_id[0]}, '{model}');"
    print(f"Inserting into db with querystr {query_str}")
    rval = perform_sql_insert_query(query_str)
    rval = jsonify ({"result": rval})
    print("Add car data result:", rval)
    return rval

@app.route('/car/makes', methods=['GET'])
@cross_origin()
def get_cars():
    query_str = 'select distinct make_name from cars join makes on cars.makes_id=makes.id;'   
    result_list = perform_sql_select_return_as_list(query_str)
    return jsonify(result_list)  

@app.route('/car/<make>/<model>', methods=['GET'])
@cross_origin()
def get_cars_by_make_and_model(make, model):
    query_str = f'select year,cars.id from cars join makes on cars.makes_id=makes.id where make_name="{make}" and model="{model}" order by year asc;'
    result_list = perform_sql_select_return_as_list_of_tuples(query_str)
    print(result_list)
    return jsonify(result_list) 

@app.route('/car/delete/<carid>', methods=['GET'])
@cross_origin()
def delete_car_by_id(carid):

    auth = request.authorization
    if not auth or not authenticate(auth.username, auth.password):
        return Response('Unauthorized', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

    print("Entering delete car by id")
    print("Exiting early from delete because we don't want to really delete anything yet")
    return jsonify([])
    query_str = f'delete from cars where id={carid};'
    print(query_str)
    rval = perform_sql_delete_query(query_str)
    result = [{
        'success': rval
    }]
    print(result)
    return jsonify(result)

@app.route('/car/<car_id>', methods=['GET'])
@cross_origin()
def get_cars_by_id(car_id):
    query_str = f'select driver_side_image, passenger_side_image, rear_view_image, front_view_image from cars where id={car_id} limit 1;'
    images = perform_sql_image_query(query_str)
    print("Images:", images)
    car_data = [{
        'make': "",
        'images': images,
        'model': "",
        'year': 0,
        'color': '',
        'mileage': 0,
        'notes': ''
    }]
    return jsonify(car_data)

@app.route('/car/<make>/<model>/<year>', methods=['GET'])
@cross_origin()
def get_cars_by_make_and_model_and_year(make, model, year):
    query_str = f'select driver_side_image, passenger_side_image, rear_view_image, front_view_image  from cars join makes on cars.makes_id=makes.id where make_name="{make}" and model="{model}" and year={year} limit 1;'
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

@app.route('/healthcheck', methods=['GET'])
@cross_origin()
def healthcheck():
    return '', 200 

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

def main():
    # Init db creds as globals up front
    global dbusername
    global dbpassword
    dbusername, dbpassword = init_db_creds_from_secretsmanager("dbadminSecret", "us-east-2")
    global siteadminpassword
    global siteadminusername
    siteadminusername, siteadminpassword = init_db_creds_from_secretsmanager("SiteAddDeleteCreds", "us-east-2")
    args = parse_args()
    # Listen on all network interfaces (0.0.0.0) and the specified port
    app.run(debug=True, host='0.0.0.0', port=args.port)

if __name__ == '__main__':
    main()

