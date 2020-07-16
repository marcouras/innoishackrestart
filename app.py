import json
import operator
from collections import Counter
from random import randint
from datetime import datetime

import requests
from flask import Flask, render_template
from flask_socketio import SocketIO
from geopy import Nominatim

from data_manipulation.crowd import absolute_count, counting_last_hour, counting_day
from data_manipulation.places import top5, top5_spiagge
from data_manipulation.weather import WeatherAndPollutionData

app = Flask(__name__)
socket = SocketIO(app)

api_key = "ea61555e4b7ed67abbe5481a188f242ed00856be57f8c8f72f94a3f61b7a9519c3f38573812b5177b8d24daaf607ec8da7a5be57930536aaede765503bb34c13"
url = "https://www.pmanalytics.cloud/api_v1"
stations = [{'name': 'CTM_Test_1', 'sid': 'e211b421-89d5-4542-9d8b-6caa6abf8d11'},
            {'name': 'CTM_Test_2', 'sid': '846460a3-8689-4ec2-a91a-9a967bc55e30'}]
start_dt = "26/06/2020_00:00"
# start_dt = "02/07/2020_10:00"
stop_dt = "02/07/2020_23:59"


# stop_dt = "02/07/2020_13:00"


def reformat(data_all, name):
    return {'name': name, 'timeseries': [
        {'name': name, 'mac': data['mac_address'], 'time': data['date_time'], 'ts_aggregated': data['ts_aggregated'],
         'latitude': float(data['station_coordinates'][0]),
         'longitude': float(data['station_coordinates'][1]), 'station_id': data['station_id']} for data in data_all if
        39.22862031 != data['station_coordinates'][0] and 9.15052704 != data['station_coordinates'][0]]}


def reformat_spiagge(data_all, name):
    iterations_real = {(39.207850, 9.167187): 318,  # Sesta aerea
                       (39.208557, 9.168057): 192,  # Il miragio
                       (39.209102, 9.168722): 231,  # Il nilo
                       (39.209472, 9.169350): 284,  # La dolce vita
                       (39.210087, 9.169951): 253}  # Corto maltese

    iterations = {(39.207850, 9.167187): 1000,
                  (39.208557, 9.168057): 100,
                  (39.209102, 9.168722): 200,
                  (39.209472, 9.169350): 850,
                  (39.210087, 9.169951): 250}

    timeseries = []
    for k in iterations:
        for j in range(iterations[k]):
            t = {'latitude': float(k[0]),
                 'longitude': float(k[1])}
            timeseries.append(t)

    return {'name': name, 'timeseries': timeseries}

    # return {'name': name, 'timeseries': [
    #    {'name': name, 'mac': data['mac_address'], 'time': data['date_time'], 'ts_aggregated': data['ts_aggregated'],
    #     'latitude': float(data['station_coordinates'][0]),
    #     'longitude': float(data['station_coordinates'][1]), 'station_id': data['station_id']} for data in data_all if
    #    39.22862031 != data['station_coordinates'][0] and 9.15052704 != data['station_coordinates'][0]]}


def conditioning(data_all):
    coordinates = [(39.207850, 9.167187), (39.208557, 9.168057), (39.209102, 9.168722), (39.209472, 9.169350),
                   (39.210087, 9.169951)]
    dats = [datetime(2020, 7, 14, 14, 0, 0), datetime(2020, 7, 14, 14, 10, 0), datetime(2020, 7, 14, 14, 20, 0),
            datetime(2020, 7, 14, 14, 30, 0), datetime(2020, 7, 14, 14, 40, 0), datetime(2020, 7, 14, 14, 50, 0),
            datetime(2020, 7, 14, 15, 0, 0), datetime(2020, 7, 14, 15, 10, 0)]

    def replace_values(d):
        i = randint(0, len(coordinates) - 1)
        j = randint(0, len(dats) - 1)
        d['station_coordinates'][0] = coordinates[i][0]
        d['station_coordinates'][1] = coordinates[i][1]
        d['ts_aggregated'] = datetime.timestamp(dats[j])
        d['date_time'] = dats[j].strftime("%Y-%m-%d %H:%M:%S")
        return d

    return [replace_values(d) for d in data_all[0:int(len(data_all) / 25)]]


@app.route('/')
def index():
    return render_template('index.html')


# city
@app.route('/dashboard')
def dashboard():
    weather_data = WeatherAndPollutionData().actual_weather()
    pollution_data = WeatherAndPollutionData().actual_pollution()

    return render_template('main_dash.html', weather_data=weather_data, pollution_data=pollution_data, city=True)


@app.route('/statistics')
def statistics():
    try:
        f = "data.json"
        data_ctm_2_raw = json.load(open(f))
    except:
        payload_wifi = [
            {'apikey': api_key, 'start_dt': start_dt, 'stop_dt': stop_dt, 'data_type': "wifi",
             'station_id': s['sid']} for s in stations]
        # req_ctm_1_wifi = requests.post(url + '/timeSeries', json=payload_wifi[0])
        # data_ctm_1_raw = req_ctm_1_wifi.json()
        # data_ctm_1 = reformat(data_ctm_1_raw, 'CTM_Test_1')
        req_ctm_2_wifi = requests.post(url + '/timeSeries', json=payload_wifi[1])
        data_ctm_2_raw = req_ctm_2_wifi.json()

    @socket.on('request_data')
    def tnl_mng(msg):
        operation = json.loads(msg)['operations']
        actions_map = {
            "absolute_counting": absolute_count,
            "places": top5,
            "counting_hour": counting_last_hour,
            "counting_day": counting_day,
        }
        data = actions_map[operation](data_ctm_2_raw)
        socket.emit('events', data=json.dumps(data))

    data_ctm_2 = reformat(data_ctm_2_raw, 'CTM_Test_2')

    return json.dumps(data_ctm_2['timeseries'])


# spiagge
@app.route('/dashboard_spiagge')
def dashboard_spiagge():
    weather_data = WeatherAndPollutionData().actual_weather()
    pollution_data = WeatherAndPollutionData().actual_pollution()
    infos = {'area': "kmq 20", "soglia": "m 5"}

    return render_template('main_dash.html', weather_data=weather_data, pollution_data=pollution_data, infos=infos)


@app.route('/statistics_spiagge')
def statistics_spiagge():
    roba = {'_id': {'$oid': '5ef576f75b12872eeb35f87b'},
            'mac_address': 'f82fbb665f427f58aa0bfaeb254b6967b055dabf26882be139fd81467ebf7458', 'power': -54.47,
            'station_id': '846460a3-8689-4ec2-a91a-9a967bc55e30', 'ts_aggregated': 1593152279.279317,
            'date_time': '2020-06-26 06:17:59.279317', 'station_coordinates': [39.22862031, 9.15052704]}

    f = "spiagge.json"
    # data_ctm_2_raw = conditioning(json.load(open(f)))
    data_ctm_2_raw = json.load(open(f))

    @socket.on('request_data_spiagge')
    def tnl_mng(msg):
        operation = json.loads(msg)['operations']
        actions_map = {
            "absolute_counting": absolute_count,
            "places": top5_spiagge,
            "counting_hour": counting_last_hour,
            "counting_day": counting_day,
        }
        data = actions_map[operation](data_ctm_2_raw)
        socket.emit('events', data=json.dumps(data))

    data_ctm_2 = reformat_spiagge(data_ctm_2_raw, 'CTM_Test_2')

    return json.dumps(data_ctm_2['timeseries'])


if __name__ == '__main__':
    app.run()
