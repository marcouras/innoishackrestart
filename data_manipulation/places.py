import operator
from collections import Counter

from geopy.distance import great_circle
from geopy import Nominatim


def top5(data):
    records = Counter(
        (x[0], x[1]) for x in [(float(d['station_coordinates'][0]), float(d['station_coordinates'][1])) for d in data if
                               (39.22862031 != d['station_coordinates'][0] and 9.15052704 !=
                                d['station_coordinates'][0])])
    final = dict(sorted(records.items(), key=operator.itemgetter(1), reverse=True))

    i = 0
    result = {}
    for f in final:
        if i < 5:
            geolocator = Nominatim(user_agent="application_testing")
            location = geolocator.reverse(str(f[0]) + "," + str(f[1]))
            hints = [final[f]]
            for idx, _f in enumerate(final):
                if idx >= 5:
                    if great_circle(f, _f).meters <= 100:
                        hints.append(final[_f])
            result[location.address] = sum(hints)
            i = i + 1

        else:
            break

    sorted_places = dict(sorted(result.items(), key=operator.itemgetter(1), reverse=True))
    places = [{'position': idx + 1, 'address': el, 'hints': sorted_places[el]} for idx, el in enumerate(sorted_places)]

    return {'operation': 'places', 'payload': places}


def top5_spiagge(data):
    records = Counter(
        (x[0], x[1]) for x in [(float(d['station_coordinates'][0]), float(d['station_coordinates'][1])) for d in data if
                               (39.22862031 != d['station_coordinates'][0] and 9.15052704 !=
                                d['station_coordinates'][0])])
    final = dict(sorted(records.items(), key=operator.itemgetter(1), reverse=True))
    locations = {(39.207850, 9.167187): "Chiosco Sesta Aerea, Viale Lungo Mare Poetto, 09126 Cagliari CA",
                 (39.208557, 9.168057): "Chiosco Il Miragio, Viale Lungo Mare Poetto, 09126 Cagliari CA",
                 (39.209102, 9.168722): "Chiosco Il Nilo, Viale Lungo Mare Poetto, 09126 Cagliari CA",
                 (39.209472, 9.169350): "Chiosco La Dolce Vita, Viale Lungo Mare Poetto, 09126 Cagliari CA",
                 (39.210087, 9.169951): "Chiosco Corto Maltese, Viale Lungo Mare Poetto, 09126 Cagliari CA"}
    i = 0
    result = {}
    for f in final:
        if i < 5:
            location = locations[f]
            hints = [final[f]-900]

            result[location] = sum(hints)
            i = i + 1

        else:
            break

    sorted_places = dict(sorted(result.items(), key=operator.itemgetter(1)))
    places = [{'position': idx + 1, 'address': el, 'hints': sorted_places[el]} for idx, el in enumerate(sorted_places)]

    return {'operation': 'places', 'payload': places}
