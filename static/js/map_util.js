var autocompleteStart;
var autocompleteEnd;
var apiAddress = "api/stations";

function initItinerary() {
    /***********LOADING GOOGLE MAP *********/
    var map = loadMap();

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
    });

    /***********LINKING SEARCH FORM TO OUR API*********/
    var on_search = function() {
        $('#direction-panel').css('display', 'none');
        draw_directions(map, directionsService, directionsDisplay, apiAddress);
    };
    document.getElementById('submit-search').addEventListener('click', on_search);
}

function initStatusMap() {
    var map = loadMap();

    /**********LOADING ALL STATIONS *********/
    $.getJSON(apiAddress
      //    , {
      //param: "mount rainier",}
      )
    .done(function(data) {
        stations = [];
        $.each(data, function (i, item) {
          stations.push([item.address, item.lat, item.lng, 1, item.optimal_criterion]);
        });
        setMarkers(map, stations);
    });
}

function loadMap() {
    //Map Construction
    var map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 48.856614, lng: 2.3522219000000177},
        zoom: 13,
        disableDefaultUI: true
    });
    return map;
}

function addMarker(map, station) {
    // Marker sizes are expressed as a Size of X,Y where the origin of the image
    // (0,0) is located in the top left of the image.
    var marker = new google.maps.Marker({
      position: {lat: station[1], lng: station[2]},
      map: map,
      icon:images_marker[Math.round(Math.abs(station[4]*10))],
      title: station[0],
      zIndex: station[3]
    });
    var infowindow = new google.maps.InfoWindow({
    content: station[0]+'<br />Etat : '+Math.round(station[4]*100)+'%',
    });

    marker.addListener('click', function() {
    infowindow.open(map, marker);
      });
}

function setMarkers(map, stations) {
  // Adds markers to the map.

  for (var i = 0; i < stations.length; i++) {
    var station = stations[i];
    addMarker(map, station)
  }
}

function draw_directions(map, directionsService, directionsDisplay, apiAddress) {
    $.getJSON(apiAddress+'/itinerary/optimal/?a-address='+document.getElementById('start').value+"&b-address="+document.getElementById('end').value + "&r="+$('input#radius-slider').attr('data-value'))
    .done(function(data) {
        var startPoint = new google.maps.LatLng(data.origin.station.lat, data.origin.station.lng);
        var endPoint = new google.maps.LatLng(data.destination.station.lat, data.destination.station.lng);
        directionsService.route({
            origin: startPoint,
            destination: endPoint,
            travelMode: google.maps.TravelMode.BICYCLING
        }, function(response, status) {
            if (status === google.maps.DirectionsStatus.OK) {
              directionsDisplay.setDirections(response);
                $('#direction-panel').css('display', 'block');
                $('#direction-panel').html("<b>Station de départ :</b> "+data.origin.station.address+"<br />" +
                                            "<b>Station d'arrivée : </b>"+data.destination.station.address+"<br />" +
                                            "<b>Durée : </b>"+response.routes[ 0 ].legs[ 0].duration.text+"<br/>"+
                                             "<b>Distance : </b>"+response.routes[ 0 ].legs[ 0].distance.text)
                $.getJSON(apiAddress+"/optimal/pick/?address="+document.getElementById('start').value+"&r="+$('input#radius-slider').attr('data-value')+"&n=20")
                .done(function(data) {
                stations = [];
                $.each(data, function (i, item) {
                    stations.push([item.station.address, item.station.lat, item.station.lng, 1, item.station.optimal_criterion]);
                });
                setMarkers(map, stations);
                });
                $.getJSON(apiAddress+"/optimal/drop/?address="+document.getElementById('end').value+"&r="+$('input#radius-slider').attr('data-value')+"&n=20")
                .done(function(data) {
                stations = [];
                $.each(data, function (i, item) {
                    stations.push([item.station.address, item.station.lat, item.station.lng, 1, item.station.optimal_criterion]);
                });
                setMarkers(map, stations);
                });
            } else {
                $('#direction-panel').css('display', 'block');
                $('#direction-panel').html('Le calcul de l\'itinéraire a échoué')
            }
        });
    });
}



