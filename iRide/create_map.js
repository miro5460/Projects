var myLat = 0;
var myLng = 0;
var me = new google.maps.LatLng(myLat, myLng);
var myOptions = {
	zoom: 14, 
	center: me,
	mapTypeId: google.maps.MapTypeId.ROADMAP 
}; 
var map;
var infowindow = new google.maps.InfoWindow();


function init() {
	map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
	getMyLocation();
}

function getMyLocation() {
	navigator.geolocation.getCurrentPosition(function(position) {
		myLat = position.coords.latitude;
		myLng = position.coords.longitude;
		renderMap();
	});
}

function renderMap() {
	me = new google.maps.LatLng(myLat, myLng);
	map.panTo(me);
	var marker = new google.maps.Marker({
		position: me,
		icon: "pickup.png",
		title: "Username: JlIH50AZeg"
	});
	marker.setMap(map);
		
	google.maps.event.addListener(marker, 'click', function() {
		infowindow.setContent(marker.title);
		infowindow.open(map, marker);
	});

	sendMyInfo();
}

function sendMyInfo() {
	var xhr = new XMLHttpRequest();
	var url = "https://obscure-brushlands-80466.herokuapp.com/rides";

	xhr.open("POST", url, true);
	xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

	xhr.onreadystatechange = function() {
	    	if(xhr.readyState == 4 && xhr.status == 200) {
		        var locations = JSON.parse(xhr.responseText); 
		        var cars = locations.passengers ? locations.passengers : locations.vehicles;
		        var icon = locations.passengers ? "pickup.png" : "car.png";
		        var distances = [];

		        if (cars) {
		        	for (var key in cars) {
			        	var passLat = cars[key].lat;
			        	var passLng = cars[key].lng;
			        	var passposit = new google.maps.LatLng(passLat, passLng);
			        	var marker = new google.maps.Marker({
							position: passposit,
							icon: icon,
							map: map,
							title: "Username: " + cars[key].username
						});

						var distance = (google.maps.geometry.spherical.computeDistanceBetween(me, passposit) * 0.000621371192).toFixed(3);
						distances.push(parseFloat(distance));

						(function (marker, infowindow, distance) {
		               		google.maps.event.addListener(marker, "click", function (e) {
			                    infowindow.setContent(marker.title + "<br/>" + distance + " miles away");
			                    infowindow.open(map, marker);
			                });
		            	})(marker, infowindow, distance);
		            }

					distances.sort(function(a, b) { return a - b });
		        	setMyMarker(distances[0]);
		        }
	    	}
	};
	xhr.send("username=JlIH5OAZeg&lat=" + myLat + "&lng=" + myLng + "")
}

function setMyMarker(distance) {
	me = new google.maps.LatLng(myLat, myLng);
	map.panTo(me);
	var marker = new google.maps.Marker({
		position: me,
		icon: "pickup.png",
		title: "Username: JlIH50AZeg" + "<br/>" + distance + " miles to closest"
	});
	marker.setMap(map);
		
	google.maps.event.addListener(marker, 'click', function() {
		infowindow.setContent(marker.title);
		infowindow.open(map, marker);
	});
}
























