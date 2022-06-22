const videoInput = document.getElementById('video-input');
const videoPlayer = document.getElementById('video-player');
const clearVideoButton = document.getElementById('clear-video-button');
const uploadVideoButton = document.getElementById('upload-video-button');
const form = document.querySelector('form');

videoInput.addEventListener('change', handleVideoInputChange);
clearVideoButton.addEventListener('click', resetFormAndClearMap);
form.addEventListener('submit', handleFormSubmit);

const response = {
  "countries": {
    "pl": 0.74,
    "sk": 0.12,
    "de": 0.31,
    "cz": 0.1,
  },
  "markers": [
    {
      "point": {
        "lat": 53.127505049999996,
        "lng": 23.147050870161664
      },
      "name": "Białystok",
      "country": "Polska"
    },
    {
      "point": {
        "lat": 53.15,
        "lng": 23.14
      },
      "name": "Białystok rondo",
      "country": "Polska"
    },
    {
      "point": {
        "lat": 52.87,
        "lng": 22.88
      },
      "name": "Białystok wzgórze",
      "country": "Polska"
    },
  ]
}

function handleVideoInputChange() {
  const file = videoInput.files[0];
  if (file) {
    const video = URL.createObjectURL(file);
    videoPlayer.src= video;
    uploadVideoButton.disabled = false;
  };
}

function handleFormSubmit(e) {
  e.preventDefault();

  // fetch('www.google.com', {
  //   method: 'POST',
  //   body: document.forms[0].elements.video.files[0],
  // });

  const file = videoInput.files[0];
  if (file) {
    handleResponse(response);
  }
}

function resetFormAndClearMap() {
  videoInput.value = null;
  videoPlayer.src = null;
  uploadVideoButton.disabled = true;

  mapState.contours?.remove();
  mapState.markers?.forEach((marker) => {
    marker.remove();
  });

  mapState = {
    contours: null,
    probabilitiesByCountry: {},
    markers: [],
  };
}
