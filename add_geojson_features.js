/*
orange: #FFA500
aqua: #00FFFF GOOD
orangered: #FF4500
fushia: #FF00FF GOOD
*/

var myStyle = {
    color: "#00FFFF",
    weight: 3,
    opacity: 0.5
};


var highlightStyle = {
    color: '#FF00FF', 
    weight: 5,
    opacity: 1,
};

// got from this website
// http://palewi.re/posts/2012/03/26/leaflet-recipe-hover-events-features-and-polygons/

function onEachFeature(feature, layer) {
    // Load the default style. 
    // Create a self-invoking function that passes in the layer
    // and the properties associated with this particular record.
    (function(layer, properties) {
      // Create a mouseover event
      layer.on("mouseover", function (e) {
        // Change the style to the highlighted version
        layer.setStyle(highlightStyle);});
      // Create a mouseout event that undoes the mouseover changes
      layer.on("mouseout", function (e) {
        // Start by reverting the style back
        layer.setStyle(myStyle); });
      // Close the "anonymous" wrapper function, and call it while passing
      // in the variables necessary to make the events work the way we want.
    })(layer, feature.properties);

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
    onEachFeature: onEachFeature,
    style: myStyle
}).addTo(map);