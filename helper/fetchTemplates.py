import pymongo
# from config import conn_str

conn_str = "mongodb+srv://botuser:KiotMDeS0Zc8qS4a@awscluster.zy5pw80.mongodb.net/?retryWrites=true&w=majority&appName=AWSCluster"


client = pymongo.MongoClient(conn_str)  
database = client["healthcare_bot"]  

# Assuming you have a collection named "mycollection"
collection = database["templates"]

def fetch_template(value):
    doc = collection.find_one({"name": value})
    template = doc['value']

    return template
