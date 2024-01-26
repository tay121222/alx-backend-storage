#!/usr/bin/env python3
"""function that inserts a new document in a collection based on kwargs"""


def insert_school(mongo_collection, **kwargs):
    """Returns the new _id"""
    doc_to_insert = mongo_collection.insert_one(kwargs)
    return doc_to_insert.inserted_id
