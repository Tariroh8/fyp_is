var districts = DISTRICTS
  
var wards = WARDS
  
  var hoverPopup = L.popup({
    closeButton: false,
    autoClose: false
  });
  
  var map = L.map('map').setView([-17, 30.8], 6);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map);
  
  L.geoJSON(districts, {
    style: {
      fillColor: 'blue',
      color: 'blue',
      fillOpacity: 0.01,
      weight: 1
    },
    onEachFeature: function (feature, layer) {
      layer.on('mouseover', function (e) {
        var districtName = feature.properties.name_2;
        hoverPopup.setLatLng(e.latlng).setContent(districtName).openOn(map);
      });
  
      layer.on('mouseout', function (e) {
        hoverPopup.remove();
      });
    }
  }).addTo(map);
  
  L.geoJSON(wards, {
    style: {
      fillColor: '',
      color: 'purple',
      fillOpacity: 0.1,
      weight: 0.5
    },
    onEachFeature: function (feature, layer) {
      var animalType = feature.properties.spicies;
      layer.bindPopup(animalType);
    }
  }).addTo(map);