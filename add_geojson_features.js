/*
orange: #FFA500
aqua: #00FFFF GOOD
orangered: #FF4500
fushia: #FF00FF GOOD
*/

var myStyle = {
    "color": "#FF00FF",
    "weight": 5,
    "opacity": 0.65
};


function popup(feature, layer) {
    // does this feature have a property named popupContent?
    if (feature.properties && feature.properties.user_id) {
        layer.bindPopup("user_id: ".concat(feature.properties.user_id));
    }
}


L.geoJson(geojson_features, {
    onEachFeature: popup,
    style: myStyle
}).addTo(map);