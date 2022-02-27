from tracemalloc import start
from flask import Flask, jsonify, redirect, render_template, request, url_for, json
import json
from output import get_load
from testgraph import main
app = Flask(__name__)
app.config["DEBUG"] = True

tripID = None
latitude = None
longitude = None
startTime = None
endTime = None

values = {
    "input_trip_id": "",
    "start_latitude": "",
    "start_longitude": "",
    "start_time": "",
    "max_destination_time": ""
}


@app.route("/")
def index():
    return render_template("form.html")

@app.route("/", methods=["GET", "POST"])
def get_values():
    if request.method == "POST":
        try:
            tripID = int(request.form["tripID"])
            latitude = float(request.form["latitude"])
            longitude = float(request.form["longitude"])
        except:
            return redirect(url_for('index'))

        startTime = (request.form["startTime"])
        endTime = (request.form["endTime"])

        if tripID is not None and latitude is not None and longitude is not None and startTime is not None and endTime is not None:
            values["input_trip_id"] = tripID
            values["start_latitude"] = latitude
            values["start_longitude"] = longitude
            values["start_time"] = str(startTime).replace("T", " ")
            values["max_destination_time"] = str(endTime).replace("T", " ")

            file = json.dumps([values])
            with open("sample.json", 'w') as outfile:
                outfile.write(file)
            
            #Input is given here to Arty's code
            #...

            arty_output = main() #load id produced by arty code
            outputs = []

            for i in range(len(arty_output)):
                outputs.append(get_load(arty_output[i]))
            
            empty = {
                "load_id": " ",
                "origin_city": " ",
                "origin_state": " ",
                "destination_city": " ",
                "destination_state": " ",
                "amount": " "
            }

            for i in range(5):
                outputs.append(empty)

            return render_template("output.html", loadid_1=outputs[0]["load_id"],
                                                  origincity_1=outputs[0]["origin_city"],
                                                  originstate_1=outputs[0]["origin_state"],
                                                  destinationcity_1=outputs[0]["destination_city"],
                                                  destinationstate_1=outputs[0]["destination_state"],
                                                  amount_1=outputs[0]["amount"],
                                                  loadid_2=outputs[1]["load_id"],
                                                  origincity_2=outputs[1]["origin_city"],
                                                  originstate_2=outputs[1]["origin_state"],
                                                  destinationcity_2=outputs[1]["destination_city"],
                                                  destinationstate_2=outputs[1]["destination_state"],
                                                  amount_2=outputs[1]["amount"],
                                                  loadid_3=outputs[2]["load_id"],
                                                  origincity_3=outputs[2]["origin_city"],
                                                  originstate_3=outputs[2]["origin_state"],
                                                  destinationcity_3=outputs[2]["destination_city"],
                                                  destinationstate_3=outputs[2]["destination_state"],
                                                  amount_3=outputs[2]["amount"],
                                                  loadid_4=outputs[3]["load_id"],
                                                  origincity_4=outputs[3]["origin_city"],
                                                  originstate_4=outputs[3]["origin_state"],
                                                  destinationcity_4=outputs[3]["destination_city"],
                                                  destinationstate_4=outputs[3]["destination_state"],
                                                  amount_4=outputs[3]["amount"],
                                                  loadid_5=outputs[4]["load_id"],
                                                  origincity_5=outputs[4]["origin_city"],
                                                  originstate_5=outputs[4]["origin_state"],
                                                  destinationcity_5=outputs[4]["destination_city"],
                                                  destinationstate_5=outputs[4]["destination_state"],
                                                  amount_5=outputs[4]["amount"],

                            
                                                 )
        
        

        
