// server.js

const express = require("express");
const app = express();
const port = 4000;

app.use(express.static("public"));

app.get("/map", (req, res) => {
    const lat1 = parseFloat(req.query.lat1);
    const lng1 = parseFloat(req.query.lng1);
    const lat2 = parseFloat(req.query.lat2);
    const lng2 = parseFloat(req.query.lng2);
    console.log(lat1, lng1, lat2, lng2);

    if (!lat1 || !lng1 || !lat2 || !lng2) {
        res.status(400).send("Missing query parameters.");
        return;
    }

    center = {
        lat: (lat1 + lat2) / 2,
        lng: (lng1 + lng2) / 2,
    }
    res.send(`
    <!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>Walking Route Map</title>
    <style>
      #map {
        height: 100vh;
        width: 100%;
      }
    </style>
  </head>
  <body>
    <div id="map"></div>
    <script>
      function initMap() {
        const map = new google.maps.Map(document.getElementById("map"), {
          center: { lat: ${center.lat}, lng: ${center.lng} },
          zoom: 13,
        });

        const startMarker = new google.maps.Marker({
          position: { lat: ${lat1}, lng: ${lng1} },
          map: map,
          title: "Starting Location",
        });

        const endMarker = new google.maps.Marker({
          position: { lat: ${lat2}, lng: ${lng2} },
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
      }
    </script>
    <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyD7s4PzstYghKQt9a6SkIbv8PkSzWIOhSQ&callback=initMap"
    async defer></script>
    </body>
    </html>
  `);
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}.`);
});
