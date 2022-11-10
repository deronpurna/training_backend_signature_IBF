from flask import Flask
from flask import Response
from flask import request
#from flask_ngrok import run_with_ngrok #hanya digunakan ketika menggunakan google colab dan tidak untuk di deploy ke heroku
import json
import copy
from flask_cors import CORS
from jinja2.environment import internalcode


f = open('./about.json')
f_cb = open('./dissolved_filter_clipped_CB_me_75.geojson')
f_rh = open('./dissoloved_filter_clipped_RH_700_me_70.geojson')
f_tp = open('./dissolved_filter_clipped_TP.geojson')

geodata = json.load(f) #ini udah jadi dictionary
geodata_cb = json.load(f_cb)
geodata_rh = json.load(f_rh)
geodata_tp = json.load(f_tp)
geo = []

pelatihan_ibf_app = Flask(__name__)
#run_with_ngrok(pelatihan_ibf_app) #hanya digunakan ketika menggunakan google colab dan tidak untuk di deploy ke heroku  
CORS(pelatihan_ibf_app)


@pelatihan_ibf_app.route('/')
def send_json_data():
    return Response(response=json.dumps(geodata), #ngubah dari dict ke json pakai respone dan .dumps
                    status=200, # untuk OK, 404 untuk NOT FOUND
                    mimetype="application/json")
    
@pelatihan_ibf_app.route('/cb')
def send_json_data_cb():
    geodataspec = geodata_cb
    return Response(response=json.dumps(geodataspec), 
                    status=200,
                    mimetype="application/json")
    
@pelatihan_ibf_app.route('/rh')
def send_json_data_rh():
    geodataspec = geodata_rh
    return Response(response=json.dumps(geodataspec),
                    status=200,
                    mimetype="application/json")

@pelatihan_ibf_app.route('/tp')
def send_json_data_tp():
    geodataspec = geodata_tp
    return Response(response=json.dumps(geodataspec),
                    status=200,
                    mimetype="application/json")


@pelatihan_ibf_app.route('/query')
def send_json_data_query():
    param = request.args.get("var")
    if param == "cb":
      geodata = geodata_cb
    elif param == "rh":
      geodata = geodata_rh
    elif param == "tp":
      geodata = geodata_tp
    value = request.args.get('value')
    operator = request.args.get("operator")
    if operator == "morethan":
      dataquery = [p for p in geodata["features"] if p["properties"]["value"] > int(value)]
    elif operator == "lessthan":
      dataquery = [p for p in geodata["features"] if p["properties"]["value"] < int(value)]
    elif operator == "equals":
      dataquery = [p for p in geodata["features"] if p["properties"]["value"] == int(value)]

    return Response(response=json.dumps({"type": "FeatureCollection","features": dataquery}),
                    status=200,
                    mimetype="application/json")

@pelatihan_ibf_app.route('/impact', methods=["GET"])
def send_status():
    req = json.loads(request.data)
    return Response(response=json.dumps(geo)),
                    status=200,
                    mimetype="application/json")

@pelatihan_ibf_app.route('/impact/add', methods=["POST"])
def add_status():
  try:
    req = json.loads(request.data)
    geo.append(copy.copy(req))
    return Response(response=json.dumps(geo),
                    status=200,
                    mimetype="application/json")
  except:
    res = {
          "error": True,
          "message": "Key tidak ditemukan"
          }
    return Response(response=json.dumps(res),
                      status=404,
                      mimetype="application/json")

@pelatihan_ibf_app.route('/queryimpact')
def send_json_data_queryimpact():
    variable = request.args.get('type')
    value = request.args.get('category')
    operator = request.args.get("operator")
    if operator == "morethan":
      dataquery2 = [p for p in geo if p["properties"]["category"] > int(value) and p["properties"]["type"] == variable]
    elif operator == "lessthan":
      dataquery2 = [p for p in geo if p["properties"]["category"] < int(value) and p["properties"]["type"] == variable]
    elif operator == "equals":
      dataquery2 = [p for p in geo if p["properties"]["category"] == int(value) and p["properties"]["type"] == variable]

    return Response(response=json.dumps({"type": "FeatureCollection","features": dataquery2}),
                    status=200,
                    mimetype="application/json")


if __name__ == '__main__':
    pelatihan_ibf_app.run()