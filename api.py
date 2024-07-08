from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.json_util import dumps

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/names"
mongo = PyMongo(app)

@app.route('/')
def home():
  """
    Used to test connection with the API.

    Returns:
        JSON response of 'Hello World!' with status code 200
  """
  return jsonify(message="Hello World!"), 200

### Create ###

@app.route('/create_first_name', methods=['POST'])
def add_name():
  """
    Adds the new first name specified in JSON data into the 'first_names' collection.

    Returns:
      JSON response with success or error message.
      
    Errors:
      - 400 Bad Request if 'name' field is missing in JSON data.
      - 500 Internal Serval Error if database operation fails.
      
    Example JSON Request:
    ```
    {
      "name": "Alice"
    }
    ```
  """
  if request.is_json:
    try:
      data = request.json
      if 'name' in data:
        mongo.db.first_names.insert_one({"name": data["name"].strip()})
        return jsonify(message="Name added successfully"), 201
      else:
        return jsonify(message="Missing 'name' field in JSON data"), 400
    except Exception as e:
      return jsonify(message="Error: {}".format(str(e))), 500
  else:
    return jsonify(message="Request content type must be 'application/json'"), 400
  
### Retrieve ###

@app.route('/first_names', methods=['GET'])
def get_first_names():
  """
  Retrieves all first names in the collection. Allows for alphabetical
  sorting through query parameters.
  
  Query Parameters:
    - alphabetical (optional): If set to "true", returns names in alphabetical order.

  Returns:
    JSON array of first names.
  
  Errors:
    - 500 Internal Server Error if database operation fails.
    
  Example Usage:
    - To retrieve all first names normally:
    ```
    GET /get_first_names
    ```
    
    - To retrieve all first names sorted alphabetically:
    ```
    GET /get_first_names?alphabetical=true
    ```
  """
  # alphabetical query variable sorts the names in alphabetical order
  alphabetical = request.args.get('alphabetical')
  try:
    if alphabetical == "true":
      first_names = mongo.db.first_names.find({}, { "name" : True, "_id" : False }).sort("name", 1)
    else:
      first_names = mongo.db.first_names.find({}, { "name" : True, "_id" : False })

    return dumps(first_names), 200
  except Exception as e:
    return jsonify(message="Error: {}".format(str(e))), 500
 
### Update ###

@app.route('/update_first_name', methods=['PUT'])
def update_first_names():
  """
    Updates the first name specified in JSON data in the collection.

    Returns:
      JSON response with success or error message.
    
    Errors:
      - 400 Bad Request if either 'old_name' or 'new_name' are missing in JSON data
      - 404 Not Found if the name specified by 'old_name' is not found in the database
      - 500 Internal Server Error if database operation fails.
    
    Example JSON Request:
    ```
    {
      "old_name": "Alice",
      "new_name": "Bob"
    }
    ```
  """
  if request.is_json:
    try:
      data = request.json

      if 'new_name' not in data:
        return jsonify(message="Missing 'new_name' field in JSON data"), 400
      if 'old_name' not in data:
        return jsonify(message="Missing 'old_name' field in JSON data"), 400

      result = mongo.db.first_names.update_one(
        { "name": data["old_name"] },
        { '$set': { "name": data["new_name"] }}
      )

      if result.modified_count == 1:
        return jsonify(message="Name updated successfully"), 200
      else:
        return jsonify(message="Name not found"), 404
    except Exception as e:
      return jsonify(message="Error: {}".format(str(e))), 500
  else:
    return jsonify(message="Request content type must be 'application/json'"), 400

### Delete ###

@app.route('/delete_first_name', methods=['DELETE'])
def delete_first_name():
  """
    Deletes the first name specified in JSON data in the collection.

    Returns:
      JSON response with success or error message.

    Errors:
      - 400 Bad Request if 'name' field missing in JSON data.
      - 404 Not Found if first name not found in database.
      - 500 Internal Server Error if database operation fails.
    
    Example JSON Request:
    {
      "name": "Alice"
    }
  """
  if request.is_json:
    try:
      data = request.json
      if 'name' not in data:
        return jsonify(message="Missing 'name' field in JSON data"), 400
      result = mongo.db.first_names.delete_one({ "name": data["name"] })
      if result.deleted_count == 1:
        return jsonify(message="Name deleted successfully"), 200
      else:
        return jsonify(message="Name not found"), 404
    except Exception as e:
      return jsonify(message="Error: {}".format(str(e))), 500
  else:
    return jsonify(message="Request content type must be 'application/json'"), 400


if __name__ == '__main__':
  app.run(debug=True)