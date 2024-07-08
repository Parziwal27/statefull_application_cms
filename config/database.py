# config/database.py
import pymongo
from urllib.parse import quote_plus
from pymongo.mongo_client import MongoClient

encoded_username = quote_plus('kumar231')
encoded_password = quote_plus('rBy6HBjdfYZoGxOV')

connection_string = f'mongodb+srv://kumar231:{encoded_password}@cluster0.t64ui.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0&tlsAllowInvalidCertificates=true'

client = MongoClient(connection_string)
db = client['insurance_claim_2']  # Access database
