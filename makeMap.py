from __future__ import print_function

class Map(object):
    def __init__(self):
        self._points = []
    def add_point(self, coordinates):
        self._points.append(coordinates)
    def __str__(self):
        centerLat = sum(( x[0] for x in self._points )) / len(self._points)
        centerLon = sum(( x[1] for x in self._points )) / len(self._points)
        markersCode = "\n".join(
            [ """new google.maps.Marker({{
                position: new google.maps.LatLng({lat}, {lon}),
                map: map
                }});""".format(lat=x[0], lon=x[1]) for x in self._points
            ])
        return """
            <script src="https://maps.googleapis.com/maps/api/js?v=3.exp&sensor=false"></script>
            <div id="map-canvas" style="height: 100%; width: 100%"></div>
            <script type="text/javascript">
                var map;
                function show_map() {{
                    map = new google.maps.Map(document.getElementById("map-canvas"), {{
                        zoom: 8,
                        center: new google.maps.LatLng({centerLat}, {centerLon})
                    }});
                    {markersCode}
                }}
                google.maps.event.addDomListener(window, 'load', show_map);
            </script>
        """.format(centerLat=centerLat, centerLon=centerLon,
                   markersCode=markersCode)


if __name__ == "__main__":
        map = Map()
        # Add Beijing, you'll want to use your geocoded points here:
        map.add_point((39.908715, 116.397389))
        with open("output.html", "w") as out:
            print(map, file=out)
            