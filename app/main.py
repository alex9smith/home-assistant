# Contains the main structure of the Flask app
from flask import Flask, Response, request, render_template
from functions import *
from variables import *

import json

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World"

## API Routes

## Shopping List

@app.route('/api/v1/shoppinglist')
def api_show_shopping_list():
    status_code = 200
    response = {}

    try:
        response = {
            'status': 'Success',
            'items': get_all_shopping_list_items()
        }

    except Exception as e:
        status_code = 500
        response = {
            'status': 'Error',
            'details': str(e)
        }

    return Response(json.dumps(response), mimetype='application/json', status = status_code)

@app.route('/api/v1/shoppinglist/<id>', methods = ['GET', 'PUT', 'DELETE'])
def api_manage_shopping_list(id):

    status_code = 200
    response = {}

    try:

        if request.method == 'GET':
            # search the list for an item
            item = search_shopping_list_for_item(id)
            if item:
                response = {
                    'status': 'Success',
                    'items': item
                }

            else:
                raise FileNotFoundError('No item found with that ID')

        elif request.method == 'PUT':
            # add a new item to the list
            item = add_item_to_shopping_list(id)
            response = {
                'status': 'Success',
                'items': item
            }

        elif request.method == 'DELETE':
            # delete an item from the list

            deleted = delete_item_from_shopping_list(id)
            if deleted:
                response = {
                    'status': 'Success',
                    'id': id
                }

            else:
                raise FileNotFoundError('No item found with that ID')
        
    except Exception as e:
        status_code = 500
        response = {
            'status': 'Error',
            'details': str(e)
        }

    return Response(json.dumps(response), mimetype='application/json', status = status_code)

## Storage 

@app.route('/api/v1/storage')
def api_show_stored_items():

    status_code = 200
    response = {}

    try:
        response = {
            'status': 'Success',
            'items': get_all_stored_items()
        }

    except Exception as e:
        status_code = 500
        response = {
            'status': 'Error',
            'details': str(e)
        }

    return Response(json.dumps(response), mimetype='application/json', status = status_code)

@app.route('/api/v1/storage/<id>', methods = ['GET', 'PUT', 'DELETE'])
def api_manage_storage(id):
    # ID here can either be the name or the Mongo ID of name|location
    # Need to handle this in each method where it's relevant

    status_code = 200
    response = {}

    try:

        if request.method == 'GET':
            # Search for the item
            if is_valid_storage_id(id):
                response = {
                    'status': 'Success',
                    'items': search_stored_items_by_id(id)
                }

            else:
                response = {
                    'status': 'Success',
                    'items': search_stored_items_by_name(id)
                }

        elif request.method == 'PUT':
            # Add the item
            if is_valid_storage_id(id):

                name, location = id.split('~')
                response = {
                    'status': 'Success',
                    'items': add_item_to_storage(name, location)
                }
            else:
                raise NameError('The provided ID is not valid. Name and location are both reqiured.')

        elif request.method == 'DELETE':
            # Delete the item
            if is_valid_storage_id(id):

                deleted = delete_from_storage_by_id(id)       
                if deleted:
                    response = {
                        'status': 'Success',
                        'items': deleted
                    }
                else:
                    raise FileNotFoundError('No item found with that ID') 

            else:
                deleted = delete_from_storage_by_name(id)       
                if deleted:
                    if len(deleted) == 1:
                        response = {
                            'status': 'Success',
                            'items': deleted
                        }
                    else:
                        raise FileExistsError('Multiple items with that name were found. Please specify a location as well')
                else:
                    raise FileNotFoundError('No item found with that ID')    

    except Exception as e:

        status_code = 500
        response = {
            'status': 'Error',
            'details': str(e)
        }

    return Response(json.dumps(response), mimetype='application/json', status = status_code)

@app.route('/api/v1/storage/locations')
def api_list_locations():
    status_code = 200
    response = {}

    try:
        response = {
            'status': 'Success',
            'locations': get_all_storage_locations()
        }

    except Exception as e:
        status_code = 500
        response = {
            'status': 'Error',
            'details': str(e)
        }

    return Response(json.dumps(response), mimetype='application/json', status = status_code)

@app.route('/api/v1/storage/locations/<location>')
def api_list_items_in_location(location):
    status_code = 200
    response = {}

    try:
        response = {
            'status': 'Success',
            'items': get_items_stored_in_location(location)
        }

    except Exception as e:
        status_code = 500
        response = {
            'status': 'Error',
            'details': str(e)
        }

    return Response(json.dumps(response), mimetype='application/json', status = status_code)
        
## Webpage routes

@app.route('/shoppinglist')
def render_shopping_list():
    return render_template('shopping-list.html', title = 'Shopping List', scripts = ['/static/js/shopping-list.js'])

@app.route('/storage')
def render_storage():
    return 'Coming soon!'