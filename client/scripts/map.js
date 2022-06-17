const OPEN_STREET_MAP_URL = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';

const tileLayerOptions = {
    maxZoom: 19,
    attribution: '© OpenStreetMap',
};


const map = L.map('map').setView([50.05, 20], 11);

L.tileLayer(OPEN_STREET_MAP_URL, tileLayerOptions).addTo(map);
