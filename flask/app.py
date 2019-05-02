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

@app.route("/test", methods=["POST", "GET"])
def test():
    jsonFromAjax = request.get_json()

    # test = request.get_json()
    # print(test["test"])
    
    # return "hello ajax"
    # print(request.args)

    data = pd.read_csv("revised_flight_latlng.csv")
    dataAll = data[["Year", "Quarter","Origin","Fare","Origin Lat","Origin Lng","Destination Lat","Destination Lng"]]

    # print(data.loc[data['Year'] == jsonFromAjax["Year"]])
    newData = data[ ["Year","Quarter","Origin","Fare","Origin Lat","Origin Lng","Destination Lat", "Destination Lng"] ]
    sortByYear = newData.loc[newData['Year'] == int(jsonFromAjax["year"]) ]
    sortByQuarter = sortByYear.loc[sortByYear['Quarter'] == int(jsonFromAjax["quarter"]) ]
    sortByOrigin = sortByQuarter.loc[sortByQuarter['Origin'] == (jsonFromAjax["city"]) ]

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


        # print(destCoords)

        # print({lat: 7.8731, lng: 80.7718, slide: 'RIGHT_ROUND'})
        # print(row['Origin Lat',"Origin Lng","Destination Lat", "Destination Lng"])

    # print(newData)

    # print()
    # print(dataAll)

    # return jsonify(testcoords)

    return jsonify(coords_All)

@app.route("/price", methods=["POST", "GET"])
def price():
    jsonObj = {
            "quarter": 1,
            "year": 2016,
            "city": "Tulsa, OK"}

    data = pd.read_csv("revised_flight_latlng.csv")
    dataAll = data[["Year", "Quarter","Origin","Fare","Origin Lat","Origin Lng","Destination Lat","Destination Lng"]]

    # print(data.loc[data['Year'] == jsonFromAjax["Year"]])
    newData = data[ ["Year","Quarter","Origin","Fare","Origin Lat","Origin Lng","Destination Lat", "Destination Lng"] ]
    sortByYear = newData.loc[newData['Year'] == jsonObj["year"] ]
    sortByQuarter = sortByYear.loc[sortByYear['Quarter'] == jsonObj["quarter"] ]
    sortByOrigin = sortByQuarter.loc[sortByQuarter['Origin'] == jsonObj["city"] ]
    destPrice = sortByOrigin['Fare']

    print(destPrice)
    return ""
# @app.route('/get_coord', methods=["POST", "GET"])
# def get_coord():

#     select= request.data
#     print(select)

    # data = pd.read_csv("revised_flight_latlng.csv")
    # print(data[ ["Year", "Quarter"] ].to_json( orient ="index"))


    # print(data["Year"])
    # return jsonify(data.loc[:, ["Year","Quarter","Origin","Fare","Origin Lat","Origin Lng","Destination Lat","Destination Lng"]])
    # return json.dumps(data.loc[ :, ["Year", "Quarter"] ])
    # print("hello")
    # return data[ ["Year", "Quarter","Origin","Fare","Origin Lat","Origin Lng","Destination Lat","Destination Lng"] ].to_json( orient ="index")
    # return select

# @app.route('/quarter', methods=['GET', 'POST'])
# def quarter():
#     select = request.form['form']
    # select= request.data
    # print(request.form.namedItem() )
    # print(select)
    # print("QUERTER ROUTE")
    # sort using request.data 
    # 
    # 

    # return jsonify("123")

if __name__ == "__main__":
    app.run(debug=True)