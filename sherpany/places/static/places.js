'use strict';

$(document).ready(function(){
	Places.initializeGMap();
	Places.initializeApp();	
});

var Places = {
	map: null,
	markers: null,
	geocoder: null
};

//
// method to initialize the google maps feature.
//
Places.initializeGMap = function()
{
	var portoCenter = {lat: 44.4833333, lng: 11.3333333}; // Porto
	
	Places.map = new google.maps.Map(document.getElementById('portoMap'), {
		center: portoCenter,
		zoom: 3
	});

	Places.geocoder = new google.maps.Geocoder();
	Places.markers = [];
	
	Places.loadMarkers();

	Places.map.addListener('click', function(e)
	{
	    var coord = e.latLng;

	    var obj = {
	      lat:coord.lat(),
	      lng:coord.lng()
	    }

	    Places.createAddress(coord.lat(), coord.lng());
	  });
};

//
// method to initialize all the components that are not in the map.
//
Places.initializeApp = function()
{
	$("#clearAll").click(function(){
		if (confirm("Are you sure you want to clear all the places?"))
		{
			Places.clearAll();
		}
	});
};

//
// method to load all the markers to the map
//
Places.loadMarkers = function()
{
	// load points from the fusion table
	$.get( "/places",
		function(data)
		{
			// if new point is valid then add the marker to the map
			if (data.status === 'ok')
			{
				$("#portoTable tbody").html("");
				for (var i = 0; i < data.items.length; i++)
				{
					var line = "<tr>"
						+ "<td scope='row'>" + data.items[i].id + "</td>"
						+ "<td>" + data.items[i].latitude + "</td>"
						+ "<td>" + data.items[i].longitude + "</td>"
						+ "<td>" + data.items[i].address + "</td></tr>";

					$("#portoTable tbody").append(line);

					Places.addMarker(data.items[i].latitude, data.items[i].longitude, data.items[i].address);
					console.log(line);
				};
			}
			else // otherwise show the message.
			{
				alert(data.message);
			}
			console.log(data);
		}
	);
};

// 
// method that creates a marker in the map
// 
Places.addMarker = function (latitude, longitude, address)
{
	var marker = new google.maps.Marker({
	    position: {lat: latitude, lng: longitude},
	    map: Places.map,
	    title: address
    });
		
	Places.markers.push(marker);
};

//
// method that checks the new point and creates the marker if everything is ok
//
Places.createAddress = function(latitude, longitude, address)
{
	// first step validate on the geocoder the point.
	Places.geocoder.geocode({
    	'location': {lat: latitude, lng: longitude}
		}, 
		function(results, status)
		{
			// in case we have an invalid address then report
			if (status !== google.maps.GeocoderStatus.OK && results.length == 0) {
				alert("Invalid geolocated point!");
				return null;
			}

			// otherwise we try to create the point in the server
			$.post( "/places/add", 
				{ latitude: latitude, longitude: longitude, address: address }, 
				function(data)
				{
					// if new point is valid then add the marker to the map
					if (data.status === 'ok')
					{
						Places.addMarker(latitude, longitude, address);
					}
					else // otherwise show the message.
					{
						alert(data.message);
					}
					console.log(data);
				}
			);
		}
	);
};

//
// method to load all the markers to the map
//
Places.clearAll = function()
{
	// load points from the fusion table
	$.get( "/places/clear",
		function(data)
		{
			// if new point is valid then add the marker to the map
			if (data.status === 'ok')
			{
				$("#portoTable tbody").html("");
				Places.clearMarkers();
				alert(data.message);
			}
			else // otherwise show the message.
			{
				alert(data.message);
			}
			console.log(data);
		}
	);

};

//
// method to delete all places on the  map
//
Places.clearMarkers = function()
{
	for (var i = 0; i < Places.markers.length; i++) {
    	Places.markers[i].setMap(null);
  	}
  	Places.markers = [];
}
