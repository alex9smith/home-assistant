# Contains the common functions and classes

from variables import *
import sys
from pymongo import MongoClient
from datetime import datetime

## Helper functions

def is_valid_storage_id(id):
    # Checks to see if the supplied id is a valid storage id
    # Returns true or false
    if type(id) == str and '|' in id:
        return True

    else:
        return False

## Database interactions

# Shopping List

def get_all_shopping_list_items():
    # Retrieves all items on the shopping list from Mongo
    # Returns a list of dictionaries
    client = MongoClient(host = MONGO_DB_HOST, port = MONGO_DB_PORT, username = MONGO_DB_USER, password = MONGO_DB_PASS, authSource = MONGO_DB_DBASE)
    db = client[MONGO_DB_DBASE]
    collection = db['shoppinglist']
    items = collection.find()
    if items:
        items = [i for i in items]
        client.close()
        return items
    else:
        client.close()
        return []

def add_item_to_shopping_list(id):
    # Takes an item name and adds it to the shopping list collection in Mongo
    # Returns the inserted item
    client = MongoClient(host = MONGO_DB_HOST, port = MONGO_DB_PORT, username = MONGO_DB_USER, password = MONGO_DB_PASS, authSource = MONGO_DB_DBASE)
    db = client[MONGO_DB_DBASE]
    collection = db['shoppinglist']
    item = {
        '_id': str(id).lower().replace(' ', '-'),
        'name': str(id),
        'added': datetime.now().strftime("%s")
    }
    collection.insert_one(item)
    client.close()
    return [item]

def delete_item_from_shopping_list(id):
    # Takes an item ID and deletes it from the shopping list
    # Returns the deleted item or None if not found
    client = MongoClient(host = MONGO_DB_HOST, port = MONGO_DB_PORT, username = MONGO_DB_USER, password = MONGO_DB_PASS, authSource = MONGO_DB_DBASE)
    db = client[MONGO_DB_DBASE]
    collection = db['shoppinglist']
    query = {
        '_id': id
    }
    found = collection.find_one(query)
    if found:
        collection.delete_one(query)
        client.close()
        return [found]
    else:
        client.close()
        return None

def search_shopping_list_for_item(id):
    # Takes an ID and searches the shopping list for that item
    # Returns the first matched item, or None if there are no matches
    client = MongoClient(host = MONGO_DB_HOST, port = MONGO_DB_PORT, username = MONGO_DB_USER, password = MONGO_DB_PASS, authSource = MONGO_DB_DBASE)
    db = client[MONGO_DB_DBASE]
    collection = db['shoppinglist']
    query = {
        '_id': id
    }
    found = collection.find_one(query)
    if found:
        found = [i for i in found]
        client.close()
        return found
    else:
        client.close()
        return None

## Storage

def get_all_stored_items():
    # Connects to the storage Mongo collection and returns a list of all stored items
    client = MongoClient(host = MONGO_DB_HOST, port = MONGO_DB_PORT, username = MONGO_DB_USER, password = MONGO_DB_PASS, authSource = MONGO_DB_DBASE)
    db = client[MONGO_DB_DBASE]
    collection = db['storage']
    items = collection.find()
    if items:
        items = [i for i in items]
        client.close()
        return items
    else:
        client.close()
        return []

def add_item_to_storage(name, location):
    # Takes an item name and location
    # Adds the item to Mongo
    # Returns the added item
    client = MongoClient(host = MONGO_DB_HOST, port = MONGO_DB_PORT, username = MONGO_DB_USER, password = MONGO_DB_PASS, authSource = MONGO_DB_DBASE)
    db = client[MONGO_DB_DBASE]
    collection = db['storage']
    item = {
        '_id': str(name).lower().replace(' ', '-') + '|' + str(location).lower().replace(' ', '-'),
        'name': str(name).lower(),
        'location': str(location),
        'added': datetime.now().strftime("%s")
    }
    collection.insert_one(item)
    client.close()
    return [item]

def search_stored_items_by_name(name):
    # Takes an item name and searches the collection with it
    # returns a list of matched items or None 
    client = MongoClient(host = MONGO_DB_HOST, port = MONGO_DB_PORT, username = MONGO_DB_USER, password = MONGO_DB_PASS, authSource = MONGO_DB_DBASE)
    db = client[MONGO_DB_DBASE]
    collection = db['storage']
    query = {
        'name': name
    }
    found = collection.find(query)
    if found:
        found = [i for i in found]
        client.close()
        return found
    else:
        client.close()
        return None

def search_stored_items_by_id(id):
    # Takes an item ID of the form name|location and searches for it
    # Returns a list containing the matched item or None if no matches
    client = MongoClient(host = MONGO_DB_HOST, port = MONGO_DB_PORT, username = MONGO_DB_USER, password = MONGO_DB_PASS, authSource = MONGO_DB_DBASE)
    db = client[MONGO_DB_DBASE]
    collection = db['storage']
    query = {
        '_id': str(id)
    }
    found = collection.find(query)
    found = [i for i in found]
    if found:
        found = [i for i in found]
        client.close()
        return found
    else:
        client.close()
        return None

def delete_from_storage_by_name(name):
    # Takes an item name and searches the collection for it
    # if a single match is found, deletes the item and returns a list containing the matched items
    # if multiple matches are found, does not delete and returns a list of matched items
    client = MongoClient(host = MONGO_DB_HOST, port = MONGO_DB_PORT, username = MONGO_DB_USER, password = MONGO_DB_PASS, authSource = MONGO_DB_DBASE)
    db = client[MONGO_DB_DBASE]
    collection = db['storage']
    query = {
        'name': {'$regex': '.*' + str(name) + '.*'}
    }
    found = collection.find(query)
    if found == None:
        return None
    else:
        items = [i for i in found]
        if len(items) == 1:
            collection.delete_one(query)
        return items

def delete_from_storage_by_id(id):
    # Takes an item ID and searches the collection for it
    # if a match is found, deletes the item and returns a list containing the matched item
    client = MongoClient(host = MONGO_DB_HOST, port = MONGO_DB_PORT, username = MONGO_DB_USER, password = MONGO_DB_PASS, authSource = MONGO_DB_DBASE)
    db = client[MONGO_DB_DBASE]
    collection = db['storage']
    query = {
        '_id': str(id)
    }
    found = collection.find_one(query)
    if found == None:
        client.close()
        return None
    else:
        collection.delete_one(query)
        client.close()
        return [items]

def get_all_storage_locations():
    # Queries Mongo for distinct locations in use
    # Returns these as a list
    client = MongoClient(host = MONGO_DB_HOST, port = MONGO_DB_PORT, username = MONGO_DB_USER, password = MONGO_DB_PASS, authSource = MONGO_DB_DBASE)
    db = client[MONGO_DB_DBASE]
    collection = db['storage']
    locations = collection.find().distinct('location')
    client.close()
    return locations

def get_items_stored_in_location(location):
    # Queries Mongo for all items with a particular location value
    # Returns a list of items, or an empty list if no matches
    client = MongoClient(host = MONGO_DB_HOST, port = MONGO_DB_PORT, username = MONGO_DB_USER, password = MONGO_DB_PASS, authSource = MONGO_DB_DBASE)
    db = client[MONGO_DB_DBASE]
    collection = db['storage']
    query = {
        'location': location
    }
    items = collection.find(query)
    if items:
        items = [i for i in collection.find(query)]
        client.close()
        return items
    else:
        client.close()
        return []