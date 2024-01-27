#!/usr/bin/env python3
"""Python script that provides some stats about Nginx logs stored in MongoDB"""
from pymongo import MongoClient


def log_stats():
    """script that provides some stats"""
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    nginx_collection = db.nginx
    total_logs = nginx_collection.count_documents({})
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {method: nginx_collection.count_documents(
        {"method": method}
        ) for method in methods}
    status_check_count = nginx_collection.count_documents(
            {"method": "GET", "path": "/status"}
            )
    print("{} logs".format(total_logs))
    print("Methods:")
    for method in methods:
        print("\tmethod {}: {}".format(method, method_counts[method]))
    print("{} status check".format(status_check_count))


if __name__ == "__main__":
    log_stats()
