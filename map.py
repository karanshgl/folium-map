from folium import Map, FeatureGroup, Marker, Icon, LayerControl
import requests
import configparser
import os

####################################
############# CONSTANTS ############
####################################

CONFIG = configparser.ConfigParser()
CONFIG.read('config.ini')
zomato = CONFIG['keys']['zomato']

EP = 'https://developers.zomato.com/api/v2.1/{}' # endpoint for Zomato
EP_MAPS = 'https://maps.googleapis.com/maps/api/geocode/json' # endpoint for Google Maps
HEADER = {'user-key': zomato} # Headers constant

fg = [] # Feature Group for Folium
QUERY = input("Enter the Location > ") # Query by user


####################################
########### HTTP Requests ##########
####################################


r = requests.get(EP.format('categories'), headers=HEADER)
categories = r.json()
r = requests.get(EP.format('locations'), headers=HEADER, params={'query': QUERY})
location = r.json()

r = requests.get(EP_MAPS, params={'address': QUERY})
geo = r.json()
geo = geo['results'][0]['geometry']['location']



####################################
########### Folium Logic ###########
####################################

map = Map(location=[geo['lat'], geo['lng']], zoom_start=16)
index = 0

for i in categories['categories']:
    fg.append(FeatureGroup(name=i['categories']['name']))

    for l in location['location_suggestions']:

        param = {
        'entity_id': l['entity_id'],
        'entity_type': l['entity_type'],
        'category': i['categories']['id']
        }

        r = requests.get(EP.format('search'), headers=HEADER, params=param)
        rest = r.json()

        for loc in rest['restaurants']:
            loc = loc['restaurant']
            marker = Marker(
            location=[loc['location']['latitude'],loc['location']['longitude']],
            popup=loc['name'],
            icon=Icon(color='red'))

            fg[index].add_child(marker)

    map.add_child(fg[index])
    index += 1


if not os.path.exists('rendered_html'):
    os.mkdir('rendered_html')

map.add_child(LayerControl())
map.save("./rendered_html/{}.html".format(QUERY))
