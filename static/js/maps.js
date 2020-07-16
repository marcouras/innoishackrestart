function get_zoom() {
    if (window.location.pathname == "/dashboard") {
        return 13
    } else if (window.location.pathname == "/dashboard_spiagge") {
        return 17
    }

}

function get_latitude() {
    if (window.location.pathname == "/dashboard") {
        return 39.229185
    } else if (window.location.pathname == "/dashboard_spiagge") {
        return 39.209102
    }
}

function get_longitude() {
    if (window.location.pathname == "/dashboard") {
        return 9.109180
    } else if (window.location.pathname == "/dashboard_spiagge") {
        return 9.168722
    }
}

var mapOptions = {
    center: new google.maps.LatLng(get_latitude(), get_longitude()),
    zoom: get_zoom(),
    mapTypeId: 'roadmap',
    mapTypeControlOptions: {
        style: google.maps.MapTypeControlStyle.HORIZONTAL_BAR,
        position: google.maps.ControlPosition.TOP_CENTER
    },
    zoomControlOptions: {
        style: google.maps.ZoomControlStyle.SMALL,
        position: google.maps.ControlPosition.BOTTOM_CENTER
    },
    streetViewControlOptions: {
        position: google.maps.ControlPosition.TOP_CENTER
    },
    fullscreenControl: false,
    styles: [
        {
            "elementType": "geometry",
            "stylers": [
                {
                    "color": "#1d2c4d"
                }
            ]
        },
        {
            "elementType": "labels.text.fill",
            "stylers": [
                {
                    "color": "#8ec3b9"
                }
            ]
        },
        {
            "elementType": "labels.text.stroke",
            "stylers": [
                {
                    "color": "#1a3646"
                }
            ]
        },
        {
            "featureType": "administrative.country",
            "elementType": "geometry.stroke",
            "stylers": [
                {
                    "color": "#4b6878"
                }
            ]
        },
        {
            "featureType": "administrative.land_parcel",
            "elementType": "labels.text.fill",
            "stylers": [
                {
                    "color": "#64779e"
                }
            ]
        },
        {
            "featureType": "administrative.province",
            "elementType": "geometry.stroke",
            "stylers": [
                {
                    "color": "#4b6878"
                }
            ]
        },
        {
            "featureType": "landscape.man_made",
            "elementType": "geometry.stroke",
            "stylers": [
                {
                    "color": "#334e87"
                }
            ]
        },
        {
            "featureType": "landscape.natural",
            "elementType": "geometry",
            "stylers": [
                {
                    "color": "#023e58"
                }
            ]
        },
        {
            "featureType": "poi",
            "elementType": "geometry",
            "stylers": [
                {
                    "color": "#283d6a"
                }
            ]
        },
        {
            "featureType": "poi",
            "elementType": "labels.text.fill",
            "stylers": [
                {
                    "color": "#6f9ba5"
                }
            ]
        },
        {
            "featureType": "poi",
            "elementType": "labels.text.stroke",
            "stylers": [
                {
                    "color": "#1d2c4d"
                }
            ]
        },
        {
            "featureType": "poi.park",
            "elementType": "geometry.fill",
            "stylers": [
                {
                    "color": "#023e58"
                }
            ]
        },
        {
            "featureType": "poi.park",
            "elementType": "labels.text.fill",
            "stylers": [
                {
                    "color": "#3C7680"
                }
            ]
        },
        {
            "featureType": "road",
            "elementType": "geometry",
            "stylers": [
                {
                    "color": "#304a7d"
                }
            ]
        },
        {
            "featureType": "road",
            "elementType": "labels.text.fill",
            "stylers": [
                {
                    "color": "#98a5be"
                }
            ]
        },
        {
            "featureType": "road",
            "elementType": "labels.text.stroke",
            "stylers": [
                {
                    "color": "#1d2c4d"
                }
            ]
        },
        {
            "featureType": "road.highway",
            "elementType": "geometry",
            "stylers": [
                {
                    "color": "#2c6675"
                }
            ]
        },
        {
            "featureType": "road.highway",
            "elementType": "geometry.stroke",
            "stylers": [
                {
                    "color": "#255763"
                }
            ]
        },
        {
            "featureType": "road.highway",
            "elementType": "labels.text.fill",
            "stylers": [
                {
                    "color": "#b0d5ce"
                }
            ]
        },
        {
            "featureType": "road.highway",
            "elementType": "labels.text.stroke",
            "stylers": [
                {
                    "color": "#023e58"
                }
            ]
        },
        {
            "featureType": "transit",
            "elementType": "labels.text.fill",
            "stylers": [
                {
                    "color": "#98a5be"
                }
            ]
        },
        {
            "featureType": "transit",
            "elementType": "labels.text.stroke",
            "stylers": [
                {
                    "color": "#1d2c4d"
                }
            ]
        },
        {
            "featureType": "transit.line",
            "elementType": "geometry.fill",
            "stylers": [
                {
                    "color": "#283d6a"
                }
            ]
        },
        {
            "featureType": "transit.station",
            "elementType": "geometry",
            "stylers": [
                {
                    "color": "#3a4762"
                }
            ]
        },
        {
            "featureType": "water",
            "elementType": "geometry",
            "stylers": [
                {
                    "color": "#0e1626"
                }
            ]
        },
        {
            "featureType": "water",
            "elementType": "labels.text.fill",
            "stylers": [
                {
                    "color": "#4e6d70"
                }
            ]
        }
    ]
};

var map = new google.maps.Map(document.getElementById('map'),
    mapOptions);

function get_url() {
    if (window.location.pathname == "/dashboard") {
        return 'statistics'
    } else if (window.location.pathname == "/dashboard_spiagge") {
        return 'statistics_spiagge'
    }
}

function get_radius() {
    if (window.location.pathname == "/dashboard") {
        return 30
    } else if (window.location.pathname == "/dashboard_spiagge") {
        return 150
    }
}

function get_weight() {
    if (window.location.pathname == "/dashboard") {
        return 100
    } else if (window.location.pathname == "/dashboard_spiagge") {
        return 100
    }
}


function heatmap() {
    $.ajax({
        url: get_url(),

        success: function (data, status) {
            var pts = [];

            data = JSON.parse(data);


            data.forEach(function (e) {
                pts.push({
                    location: new google.maps.LatLng(e["latitude"], e["longitude"]),
                    weight: get_weight()
                })
            });


            var heatmap = new google.maps.visualization.HeatmapLayer({
                data: pts,
                map: map,
                radius: get_radius()
            });

            response_handler()
        }
    })

}

heatmap();


