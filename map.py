import folium
import requests
import json
import key

search = raw_input("Enter the Location");

url = 'https://developers.zomato.com/api/v2.1/categories'
headers = {'user-key': key.key}
r = requests.get(url, headers=headers)

j=r.json();
print(j)

map=folium.Map(location=[28.7041,77.1025], zoom_start=6, tiles="Mapbox Bright");
fg = folium.FeatureGroup(name="Map")


#fg.add_child(folium.Marker(location=coordinates['co'], popup=coordinates['pop'], icon=folium.Icon(color='red')));

map.add_child(fg);

map.save("./rendered_html/Map1.html");
