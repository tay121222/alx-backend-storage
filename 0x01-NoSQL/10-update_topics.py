#!/usr/bin/env python3
"""function that changes all topics of a school document based on the name"""


def update_topics(mongo_collection, name, topics):
    """Update function"""
    mongo_collection.update(
        { "name": name },
        { "$set": { "topics" : topics } },
        multi = True
    )
