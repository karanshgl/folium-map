import folium
import requests
import json
import key

search = input("Enter the Location ");

url = 'https://developers.zomato.com/api/v2.1/categories'
headers = {'user-key': key.key}
r = requests.get(url, headers=headers)
categories=r.json();

url= 'https://developers.zomato.com/api/v2.1/locations?query=' + search.replace(" ", "%20");
r = requests.get(url, headers=headers)
location = r.json();
fg=[];
index=0;
map=folium.Map(location=[28.7041,77.1025],zoom_start=14);
for i in categories['categories']:
    fg.append(folium.FeatureGroup(name=i['categories']['name']))
    for l in location['location_suggestions']:
        url = 'https://developers.zomato.com/api/v2.1/search?entity_id=' +str(l['entity_id']) + '&entity_type=' +l['entity_type'] + '&category=' + str(i['categories']['id']);
        r = requests.get(url, headers=headers);
        rest = r.json();
        for loc in rest['restaurants']:
            fg[index].add_child(folium.Marker(location=[loc['restaurant']['location']['latitude'],loc['restaurant']['location']['longitude']], popup=loc['restaurant']['name'] + 'URL : ' + loc['restaurant']['url'], icon=folium.Icon(color='red')));
    map.add_child(fg[index]);
    index=index+1;


map.add_child(folium.LayerControl());
map.save("./rendered_html/Map1.html");
