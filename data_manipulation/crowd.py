import time

import numpy as np
import pandas as pd


def absolute_count(data):
    max_ts = max([t['ts_aggregated'] for t in data])

    limit_last_hour = max_ts - 3600
    limit_last_day = max_ts - 3600 * 24
    limit_last_week = max_ts - 3600 * 24 * 7

    week = set([_['mac_address'] for _ in data if _['ts_aggregated'] >= limit_last_week])
    day = set([_['mac_address'] for _ in data if _['ts_aggregated'] >= limit_last_day])
    hour = set([_['mac_address'] for _ in data if _['ts_aggregated'] >= limit_last_hour])

    return {'operation': 'absolute_counting', 'payload': {'day': len(day), 'hour': len(hour), 'week': len(week)}}


def counting_last_hour(data):
    max_ts = max([t['ts_aggregated'] for t in data])
    intervals = [max_ts - 600 * i for i in range(6)][::-1]

    data_for_df = [{'device_id': d['station_id'],
                    'timestamp': d['ts_aggregated'],
                    'mac': d['mac_address']} for d in data]

    df = pd.DataFrame(data=list(data_for_df))

    # start = df['timestamp'].min()
    # stop = df['timestamp'].max()
    start = intervals[0]
    epoch_stop = intervals[-1]
    step_sec = 10 * 60

    stop = epoch_stop + step_sec*2

    print(int(start), int(stop), int(step_sec))

    intervals = np.arange(int(start), int(stop), int(step_sec))

    labels = []
    values = []
    if not df.empty:
        for t, t_frame in df.groupby(pd.cut(df["timestamp"], intervals)):
            values.append(len(set(t_frame["mac"])))
            labels.append(time.strftime('%Y-%m-%d %H:%M',
                                        time.localtime(t.right)))
            # labels.append(datetime.strftime(datetime.utcfromtimestamp(t.right), '%Y-%m-%d %H:%M'))

    print("ChartDataAccess CustomDateData STOP {}".format(time.time()))
    return {'operation': 'counting_hour', 'payload': {"labels": labels, "values": values}}


def counting_day(data):
    max_ts = max([t['ts_aggregated'] for t in data])
    intervals = [max_ts - 3600 * i for i in range(24)][::-1]

    data_for_df = [{'device_id': d['station_id'],
                    'timestamp': d['ts_aggregated'],
                    'mac': d['mac_address']} for d in data]

    df = pd.DataFrame(data=list(data_for_df))

    # start = df['timestamp'].min()
    # stop = df['timestamp'].max()
    start = intervals[0]
    epoch_stop = intervals[-1]
    step_sec = 60 * 60

    stop = epoch_stop + step_sec*2

    print(int(start), int(stop), int(step_sec))

    intervals = np.arange(int(start), int(stop), int(step_sec))

    labels = []
    values = []
    if not df.empty:
        for t, t_frame in df.groupby(pd.cut(df["timestamp"], intervals)):
            values.append(len(set(t_frame["mac"])))
            labels.append(time.strftime('%Y-%m-%d %H:%M',
                                        time.localtime(t.right)))
            # labels.append(datetime.strftime(datetime.utcfromtimestamp(t.right), '%Y-%m-%d %H:%M'))

    print("ChartDataAccess CustomDateData STOP {}".format(time.time()))
    return {'operation': 'counting_day', 'payload': {"labels": labels, "values": values}}
