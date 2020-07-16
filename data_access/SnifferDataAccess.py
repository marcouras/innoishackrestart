import requests


class StationData(object):
    url = "https://www.pmanalytics.cloud/api_v1"

    def __init__(self, payload):
        self.data_raw = requests.post(self.url + '/timeSeries', json=payload)

    def reformat(self, name):
        return {'name': name, 'timeseries': [
            {'name': name, 'time': data['date_time'], 'latitude': float(data['station_coordinates'][0]),
             'longitude': float(data['station_coordinates'][1]), 'station_id': data['station_id']} for data in
            self.data_raw]}
