# import urllib library
from urllib.request import urlopen
  
# import json
import json
# store the URL in url as 
# parameter for urlopen
with open ("all_the_loads.json") as file:
    data_json = json.load(file)
  
# print the json response
def get_load(desired_id):
    for i in range(len(data_json)):
        if data_json[i]['load_id'] == desired_id:
            output = {
                "load_id": data_json[i]["load_id"],
                "origin_city": data_json[i]["origin_city"],
                "origin_state": data_json[i]["origin_state"],
                "destination_city": data_json[i]["destination_city"],
                "destination_state": data_json[i]["destination_state"],
                "amount": data_json[i]["amount"]
            }
            return(output)
def get_load_cities(origin, destination):
    for i in range(len(data_json)):
        if data_json[i]['origin_city'] == "origin" & data_json[i]['destination_city'] == "destination":
            return data_json[i]["load_id"]

def find_loads(trips):
    for key,value in trips.items():
        if len(value[1]) > 1:
            for i in range(1, len(value[1])):
                get_load_cities()