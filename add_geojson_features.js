/*
orange: #FFA500
aqua: #00FFFF GOOD
orangered: #FF4500
fushia: #FF00FF GOOD
*/

var myStyle = {
    "color": "#00FFFF",
    "weight": 5,
    "opacity": 0.65
};


function popup(feature, layer) {
    // does this feature have a property named popupContent?
    if (feature.properties) {
    	var msg = ""
    	if (feature.properties.user_id) {
    	    msg = msg.concat("user_id: ")
    	    msg = msg.concat(feature.properties.user_id)
    	    msg = msg.concat("<br>")
    	}
        if (feature.properties.distance) {
            msg = msg.concat("length: ")
    	    msg = msg.concat(feature.properties.distance)
    	    msg = msg.concat("<br>")
        }
        if (feature.properties.duration) {
            msg = msg.concat("duration: ")
    	    msg = msg.concat(feature.properties.duration)
    	    msg = msg.concat("<br>")
        }
        if (feature.properties.number_points) {
            msg = msg.concat("#points: ")
    	    msg = msg.concat(feature.properties.number_points)
    	    msg = msg.concat("<br>")
        }
        layer.bindPopup(msg);
    }
}


L.geoJson(geojson_features, {
    onEachFeature: popup,
    style: myStyle
}).addTo(map);