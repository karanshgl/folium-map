import folium

map=folium.Map(location=[28.7041,77.1025], zoom_start=6, tiles="Mapbox Bright");
fg = folium.FeatureGroup(name="Map")

points = [{'co': [28,77], 'pop' : "This is Marker 1"},{'co': [27,78], 'pop' : "This is Marker 2"}];

for coordinates in points:
    fg.add_child(folium.Marker(location=coordinates['co'], popup=coordinates['pop'], icon=folium.Icon(color='red')));

map.add_child(fg);

map.save("Map1.html");
