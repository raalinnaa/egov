function initMap(lona, lata, lonb, latb) {
    console.log("initMap");
    const urlParams = new URLSearchParams(window.location.search);

    console.log(lona, lata, lonb, latb);
    const center = {
        lat: (lata + latb) / 2,
        lng: (lona + lonb) / 2,
    }

    var R = 6371; // km
    var dLat = (latb - lata) * Math.PI / 180;
    var dLon = (lonb - lona) * Math.PI / 180;
    var a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(lata * Math.PI / 180) * Math.cos(latb * Math.PI / 180) *
        Math.sin(dLon / 2) * Math.sin(dLon / 2);
    var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    var d = R * c;
    var zoom = Math.round(Math.log(40000 / d) / Math.log(2));

    const map = new google.maps.Map(document.getElementById("map"), {
        center: center,
        zoom: zoom,
    });



    // show also traffic jams
    fetch("/map")
        .then((response) => response.json())
        .then((data) => {
            const startMarker = new google.maps.Marker({
                position: data.start,
                map: map,
                title: "Starting Location",
            });

            const endMarker = new google.maps.Marker({
                position: data.end,
                map: map,
                title: "Destination",
            });

            const directionsService = new google.maps.DirectionsService();
            const directionsRenderer = new google.maps.DirectionsRenderer();
            directionsRenderer.setMap(map);

            const request = {
                origin: startMarker.getPosition(),
                destination: endMarker.getPosition(),
                travelMode: google.maps.TravelMode.DRIVING,

            };

            directionsService.route(request, (result, status) => {
                if (status === google.maps.DirectionsStatus.OK) {
                    directionsRenderer.setDirections(result);
                }
            });
        })
        .catch((error) => console.error(error));

}