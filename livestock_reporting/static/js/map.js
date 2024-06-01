var viewMapBtn = document.getElementById('view-map-btn');
var mapContainer = document.getElementById('map');
var distanceContainer = document.getElementById('distance-container');

viewMapBtn.addEventListener('click', function() {
  // Show the map container
  mapContainer.style.display = 'block';

  // Get user location using Geolocation API
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      var userLat = position.coords.latitude;
      var userLong = position.coords.longitude;

      // Create the map and set its center using the user's location
      var map1 = false;
      var map = L.map('map');

      // Add the OpenStreetMap tile layer
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
        maxZoom: 18,
      }).addTo(map);
      var map1 = true;


      // Replace the placeholder values with the actual latitude and longitude
      var caseLat = CASE_LATITUDE;
      var caseLong = CASE_LONGITUDE;

      // Create a LatLngBounds object to encompass the user's location and case location
      var bounds = L.latLngBounds([
        [userLat, userLong], // User's location
        [caseLat, caseLong] // Case location
      ]);

      // Fit the map to the bounds
      map.fitBounds(bounds);

      // Add a marker for the user's location
      L.marker([userLat, userLong]).addTo(map)
        .bindPopup('Your Location')
        .openPopup();

// Add a circle marker for the case location
L.circleMarker([caseLat, caseLong], {
  radius: 5, // Adjust the radius as needed
  color: 'red',
  fillColor: 'red',
  fillOpacity: 1
}).addTo(map);

// Draw a line between the user's location and the case location
var lineCoordinates = [
  [userLat, userLong], // User's location
  [caseLat, caseLong] // Case location
];

L.polyline(lineCoordinates, {
  color: 'red',
  weight: 2
}).addTo(map);

      // Calculate the distance between the user's location and the case location
      var distance = calculateDistance(userLat, userLong, caseLat, caseLong);

      // Render the distance in the distance container
      distanceContainer.textContent = 'You are located : ' + distance.toFixed(2) + ' km  away from the reported case';
    });
  } else {
    alert('Geolocation is not supported by your browser.');
  }
});

function calculateDistance(lat1, lon1, lat2, lon2) {
  const radius = 6371; // Radius of the Earth in kilometers
  const dLat = toRadians(lat2 - lat1);
  const dLon = toRadians(lon2 - lon1);
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(toRadians(lat1)) * Math.cos(toRadians(lat2)) * Math.sin(dLon / 2) * Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  const distance = radius * c;
  return distance;
}

function toRadians(degrees) {
  return degrees * (Math.PI / 180);
}