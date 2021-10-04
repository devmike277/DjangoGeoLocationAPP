from django.shortcuts import render
import requests
import json
import folium

# Create your views here.
def index(request):
    
    ip = requests.get('https://api.ipify.org?format=json')
    ip_data = json.loads(ip.text)
    res = requests.get('http://ip-api.com/json/'+ip_data['ip'])
    location_data = json.loads(res.text)

    point = (location_data['lat'],location_data['lon'])
    folium_map= folium.Map(width=800,height=500,location=point)
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

    return render(request,'index.html',context)