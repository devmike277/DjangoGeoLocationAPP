from django.shortcuts import render
import requests
import json
import folium
import re
from django.contrib import messages
import ipaddress

# Create your views here.
def index(request):

    context = {
        'data':'null'
    }

    return render(request,'index.html',context)

def geolocate(request):
    ip = request.POST['ip']
    context = {
        'data':'null'
    }

    regex_pattern = "^([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])$"
    if (bool( re.match( regex_pattern, ip ) )):

        res = requests.get('http://ip-api.com/json/'+ip)
        location_data = json.loads(res.text)

        point = (location_data['lat'],location_data['lon'])
        folium_map= folium.Map(width=750,height=450,location=point)
        folium.Marker(
                    [location_data['lat'],location_data['lon']],
                    tooltip='click here for more information',
                    popup=location_data['city'],
                    icon=folium.Icon(color='red')
                    ).add_to(folium_map)
        folium_map = folium_map._repr_html_()

        context = {
            'data':location_data,
            'map':folium_map
        }
        
    else:
        messages.info(request,'Invalid IP')

    return render(request,'index.html',context)
    

    

    