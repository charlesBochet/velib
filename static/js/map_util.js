// Global vars
var autocompleteStart;
var autocompleteEnd;
var apiAddress = "api/stations";
var markers = []; //Map markers array
var map = loadMap(); //Construct map view

// Function drawing map view port with itinerary forms
function initItinerary() {
    /***********LOADING GOOGLE MAP *********/

    //Setting Bounds for Autocomplete (doesn't work properly)
    var SWCornerLocation = new google.maps.LatLng(48.959755, 2.529341);
    var NECornerLocation = new google.maps.LatLng(48.775562, 2.143934);
    var autocompleteBounds = new google.maps.LatLngBounds(SWCornerLocation, NECornerLocation);

    //Autocomplete Service Initialization : Start Point
    autocompleteStart = new google.maps.places.Autocomplete(
        document.getElementById('start'),
            { types: ['geocode'],
              bounds: autocompleteBounds,
              componentRestrictions: { country: 'fr' }}
    );

    //Autocomplete Service Initialization : End Point
    autocompleteEnd = new google.maps.places.Autocomplete(
        document.getElementById('end'),
            { types: ['geocode'] }
    );

    //Direction Service Initialization
    var directionsService = new google.maps.DirectionsService;

    //Direction Render Initialization
    var directionsDisplay = new google.maps.DirectionsRenderer({
        draggable: false,
        map: map,
        suppressBicyclingLayer: true,
        suppressMarkers:true,
    });

    /***********LINKING SEARCH FORM TO OUR API*********/
    var on_search = function() { // Add listener on search button
        $('#direction-panel').css('display', 'none');
        draw_directions(directionsService, directionsDisplay, apiAddress);
    };
    document.getElementById('submit-search').addEventListener('click', on_search);
}

//Function drawing map view port and display station status
function initStatusMap() {
    /**********LOADING ALL STATIONS *********/
    $.getJSON(apiAddress) //Request list of all station
    .done(function(data) {
        stations = [];
        $.each(data, function (i, item) {
          stations.push([item.address, item.lat, item.lng, 1, item.optimal_criterion, 'pick_and_drop', item.available_bikes, item.available_bike_stands, item.bike_stands]); //Extract meaningful information
        });
        setMarkers(stations);//Draw Stations on map
    });
}

//Load Google Map and Display it
function loadMap() {
    //Map Construction
    var map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 48.856614, lng: 2.3522219000000177},
        zoom: 13,
        disableDefaultUI: true
    });
    return map;
}

//Draw a specific station
function addMarker(station) {
    // Marker sizes are expressed as a Size of X,Y where the origin of the image
    // (0,0) is located in the top left of the image.
    if (station[5] == 'pick')
        var icon = images_marker[Math.round((10 - station[4]*10)/2)];
    else if(station[5] == 'drop')
        var icon = images_marker[Math.round((10 + station[4]*10)/2)];
    else if(station[5] == 'pick_and_drop')
        var icon = images_marker[Math.round(Math.abs(station[4]*10))]; //Icon  based on filling status
    var marker = new google.maps.Marker({
      position: {lat: station[1], lng: station[2]},
      map: map,
      icon:icon,
      title: station[0],
      zIndex: station[3]
    });
    var infowindow = new google.maps.InfoWindow({
    content: station[0]+ '<br />Capacité station : ' + station[8] + '<br />Bornes disponibles  : ' + station[7] +
        '<br />Velib disponibles  : ' + station[6] + '<br />Distance à l\'équilibre : '+Math.round(station[4]*100)+'%',
    });

    //Attach Info Tooltip
    marker.addListener('click', function() {
    infowindow.open(map, marker);
    });

    markers.push(marker);
}

//Draw markers on status map
function setMarkers(stations) {
  // Adds markers to the map.

  for (var i = 0; i < stations.length; i++) {
    var station = stations[i];
    addMarker(station)
  }
}

//Clear Markers
function clearMarkers() {
    for (var i = 0; i < markers.length; i++) {
            markers[i].setMap(null);
        }
        markers = [];
}


//Handle itinerary, called on search form submit
function draw_directions(directionsService, directionsDisplay, apiAddress) {
    //Clear map
    clearMarkers();

    //Request itinerary based on search form and get optimal station coordonates
    $.getJSON(apiAddress+'/itinerary/optimal/?a-address='+document.getElementById('start').value+"&b-address="+document.getElementById('end').value + "&r="+$('input#radius-slider').attr('data-value'))
    .done(function(data) {
        var startPoint = new google.maps.LatLng(data.origin.station.lat, data.origin.station.lng);
        var endPoint = new google.maps.LatLng(data.destination.station.lat, data.destination.station.lng);
        // request Google Maps itinerary
        directionsService.route({
            origin: startPoint,
            destination: endPoint,
            travelMode: google.maps.TravelMode.BICYCLING
        }, function(response, status) {
            if (status === google.maps.DirectionsStatus.OK) {
                //Display itinerary on map
                directionsDisplay.setDirections(response);

                //Display direction panel
                $('#direction-panel').css('display', 'block');
                $('#direction-panel').html("<b>Station de départ :</b> "+data.origin.station.address+"<br />" +
                                            "<b>Station d'arrivée : </b>"+data.destination.station.address+"<br />" +
                                            "<b>Durée : </b>"+response.routes[0].legs[0].duration.text+"<br/>"+
                                             "<b>Distance : </b>"+response.routes[0].legs[0].distance.text)

                //Display optimal stations in radius
                $.getJSON(apiAddress+"/optimal/pick/?address="+document.getElementById('start').value+"&r="+$('input#radius-slider').attr('data-value')+"&n=20")
                .done(function(data) {
                    stations = [];
                    $.each(data, function (i, item) {
                        stations.push([item.station.address, item.station.lat, item.station.lng, 1, item.station.optimal_criterion, 'pick', item.station.available_bikes, item.station.available_bike_stands, item.station.bike_stands]);
                    });
                    setMarkers(stations);
                });
                $.getJSON(apiAddress+"/optimal/drop/?address="+document.getElementById('end').value+"&r="+$('input#radius-slider').attr('data-value')+"&n=20")
                .done(function(data) {
                    stations = [];
                    $.each(data, function (i, item) {
                        stations.push([item.station.address, item.station.lat, item.station.lng, 1, item.station.optimal_criterion, 'drop', item.station.available_bikes, item.station.available_bike_stands, item.station.bike_stands]);
                    });
                    setMarkers(stations);
                });
            } else {
                //In case something went wrong
                $('#direction-panel').css('display', 'block');
                $('#direction-panel').html('Le calcul de l\'itinéraire a échoué')
            }
        });
    })
    .fail(function(data) {
        $('#direction-panel').css('display', 'block');
        $('#direction-panel').html('Aucune station velib n\'est utilisable dans le rayon demandé. Essayez un rayon plus grand')
    });
}
