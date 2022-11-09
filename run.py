from flask import Flask
from flask import Response
#from flask_ngrok import run_with_ngrok #hanya digunakan ketika menggunakan google colab dan tidak untuk di deploy ke heroku
import json

f = open('./about.json')
f_cb = open('./dissolved_filter_clipped_CB_me_75.geojson')
f_rh = open('./dissoloved_filter_clipped_RH_700_me_70.geojson')
f_tp = open('./dissolved_filter_clipped_TP.geojson')

geodata = json.load(f) #ini udah jadi dictionary
geodata_cb = json.load(f_cb)
geodata_rh = json.load(f_rh)
geodata_tp = json.load(f_tp)

pelatihan_ibf_app = Flask(__name__)
#run_with_ngrok(pelatihan_ibf_app) #hanya digunakan ketika menggunakan google colab dan tidak untuk di deploy ke heroku  

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

if __name__ == '__main__':
    pelatihan_ibf_app.run()