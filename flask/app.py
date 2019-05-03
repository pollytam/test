from flask import Flask, render_template, json, request, jsonify
from flask_cors import CORS
import pandas as pd 

app = Flask(__name__)
cors = CORS(app)
# CORS(app,resources={r"/*": {"origins": "*"}})
app.config["CACHE_TYPE"] = "null"


@app.route('/')
def hello_world():
    return render_template("index.html")
def fix_json(text):
    return text.replace("\'", "\"")

@app.route('/getbydate/<year>/<quar>/<origin>', methods=["POST", "GET"])
def getbydate(year,quar,origin):
    data = pd.read_csv("revised_flight_latlng.csv")
    dataAll = data[["Year", "Quarter","Origin","Fare","Origin Lat","Origin Lng","Destination Lat","Destination Lng"]]
    # print(dataAll)
    qury = str('Year=='+ year+ ' and Quarter=="'+ quar + '" and Origin=="'+ origin+'"')
    # qury = 'Year == '+ year
    dataAll.query(qury, inplace=True)
    return data[["Origin Lat","Origin Lng","Destination Lat","Destination Lng"]].to_json()
    # return dataAll.to_json()
    # return "Year"


@app.route('/get_origins', methods=["POST", "GET"])
def get_origins():
    data = pd.read_csv("revised_flight_latlng.csv")
    data = data["Origin"].unique()
    print(list(data))
    for i in list(data):
        print('<option value="'+i+'">'+i+'</option>')
    return jsonify(list(data))
    # return jsonify(data)

def getFilteredDF(jsonFromAjax):
    data = pd.read_csv("revised_flight_latlng.csv")
    dataAll = data[["Year", "Quarter","Origin","Destination","Fare","Origin Lat","Origin Lng","Destination Lat","Destination Lng"]]

    newData = data[ ["Year","Quarter","Origin","Destination","Fare","Origin Lat","Origin Lng","Destination Lat", "Destination Lng"] ]
    sortByYear = newData.loc[newData['Year'] == int(jsonFromAjax["year"]) ]
    sortByQuarter = sortByYear.loc[sortByYear['Quarter'] == int(jsonFromAjax["quarter"]) ]
    sortByOrigin = sortByQuarter.loc[sortByQuarter['Origin'] == (jsonFromAjax["city"]) ]

    return sortByOrigin

@app.route("/test", methods=["POST", "GET"])
def test():
    jsonFromAjax = request.get_json()
   
    sortByOrigin = getFilteredDF(jsonFromAjax)

    coords_All=[]
 
    for i, row in sortByOrigin.iterrows():
        coords=[]
        originCoords = {"lat": row['Origin Lat'], 
                        "lng": row['Origin Lng']
                        }
        destCoords = {"lat": row['Destination Lat'], 
                        "lng": row['Destination Lng']
                        }

        
        coords.append(originCoords)
        coords.append(destCoords)

        coords_All.append(coords)

    return jsonify(coords_All)

@app.route("/get_prices", methods=["POST", "GET"])
def price():

    jsonFromAjax = request.get_json()
   
    sortByOrigin = getFilteredDF(jsonFromAjax)

    dest=[]

    for p, row in sortByOrigin.iterrows():

        priceDest=[]
        price = row['Fare']
        destCoords = {"lat": row['Destination Lat'], 
                        "lng": row['Destination Lng']
                        }
        destination = row['Destination']
        # print(price)
        priceDest.append(price)
        priceDest.append(destCoords)
        priceDest.append(destination)
    
        dest.append(priceDest)

        # print(price)
    return jsonify(dest)


if __name__ == "__main__":
    app.run(debug=True)