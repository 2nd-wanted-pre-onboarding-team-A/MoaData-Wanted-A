from mongoengine import *

def initialize_db(app):
    connect('moa')  # MongoDB Connector