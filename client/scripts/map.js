const OPEN_STREET_MAP_URL = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';

const tileLayerOptions = {
    maxZoom: 19,
    attribution: '© OpenStreetMap',
};

const map = L.map('map').setView([50.05, 20], 11);
L.tileLayer(OPEN_STREET_MAP_URL, tileLayerOptions).addTo(map);

let probabilitiesByCountry = {}

function getColorByProbability(probability = 0) {
    return probability > 0.9 ? '#800026' :
            probability > 0.8  ? '#BD0026' :
            probability > 0.7  ? '#E31A1C' :
            probability > 0.6  ? '#FC4E2A' :
            probability > 0.5   ? '#FD8D3C' :
            probability > 0.3   ? '#FEB24C' :
            probability > 0.2   ? '#FED976' :
            probability > 0.1   ? '#FFEDA0' :
                            '#fff4c4';
}

function getColorByCountry(country) {
    const probability = mapState.probabilitiesByCountry[country] || 0;
    return getColorByProbability(probability);
}

function style(feature) {
    return {
        fillColor: getColorByCountry(feature.properties.ADMIN),
        weight: 2,
        opacity: 1,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.7
    };
}

const legend = L.control({position: 'bottomright'});

legend.onAdd = function () {
    const div = L.DomUtil.create('div', 'info legend'),
    grades = [0.0, 0.1, 0.2, 0.3, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0];

    for (let i = grades.length - 1; i > 0; i--) {
        div.innerHTML +=
            '<i style="background:' + getColorByProbability(grades[i]) + '"></i> ' +
            100*grades[i] + (grades[i - 1] ? ' &ndash; ' + 100*grades[i - 1] + ' %<br>' : ' &ndash; 0 %');
    }

    return div;
};

legend.addTo(map);


var mapState = {
    contours: null,
    probabilitiesByCountry: {},
    markers: [],
};


  function handleResponse(response) {
    mapState.probabilitiesByCountry = getProbabilitiesByCountryNames(response.countries);
    const countryContours = getCountriesContours(response.countries);
    const markers = getMarkersForPlaces(response.markers);

    const countours = L.geoJson(countryContours, {style}).addTo(map);
    markers.forEach((marker) => {
        marker.addTo(map);
    })

    mapState.contours = countours;
    mapState.markers = markers;
  }

  function getProbabilitiesByCountryNames(responseCountries) {
    const probabilitiesByCountry = {};

    Object.entries(responseCountries).forEach(([countryCode, probability]) => {
        const countryName = countryNamesByCodes[countryCode.toUpperCase()];

        if (countryName) {
            probabilitiesByCountry[countryName] = probability;
        }
    });

    return probabilitiesByCountry;
  }

  function getMarkersForPlaces(places) {
    const markers = [];
    places.forEach((place) => {
        if (!place) return;

        const {point, name} = place;
        const marker = L.marker([point.lat, point.lng]);
        marker.bindPopup(name);

        markers.push(marker);
    });

    return markers;
  }

  function getCountriesContours(countryCodes) {
    const countours = [];

    Object.keys(countryCodes).forEach((countryCode) => {
        const countryName = countryNamesByCodes[countryCode.toUpperCase()];
        if (countryName) {
            const contour = countries[countryName];
            if (contour) {
                countours.push(countries[countryName]);
            }
        }
    });

    return countours;
  }
