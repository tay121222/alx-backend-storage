#!/usr/bin/env python3
"""Contains function that lists all documents"""


def list_all(mongo_collection):
    """function that lists all documents in a collection
    Return an empty list if no document in the collection"""
    document = list(mongo_collection.find())
    return document
