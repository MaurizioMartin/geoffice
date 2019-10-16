import os
import requests
from dotenv import load_dotenv
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import pandas as pd
import urllib.request
from uber_rides.session import Session
from uber_rides.client import UberRidesClient
import random
load_dotenv()

GOOGLE_CRED = os.getenv("GOOGLE_CRED")
ZOMATO_CRED = os.getenv("ZOMATO_CRED")


def getGeoloc(params):
    params = "address="+params
    url = "https://maps.googleapis.com/maps/api/geocode/json?{}&key={}".format(params,GOOGLE_CRED)
    response = requests.get(url)
    data = response.json()
    for dat in data["results"]:
        return dat["geometry"]["location"]


def getZomatoGeocode(center):
    lat = center[0]
    lon = center[1]
    headers = {    
       "user-key": "{}".format(ZOMATO_CRED)
    }
    url = "https://developers.zomato.com/api/v2.1/geocode?lat={}&lon={}".format(lat,lon)
    response = requests.get(url,headers=headers)
    data=response.json()
    zomato_dict = {
        'location_title': data['location']['title'],
        'popularity': data['popularity']['popularity'],
        'nightlife': data['popularity']['nightlife_index'],
        'restaurants': []
    }
    for rest in data['nearby_restaurants']:
        name = rest['restaurant']['name']
        location = rest['restaurant']['location']['address']
        cuisines = rest['restaurant']['cuisines']
        rate = rest['restaurant']['user_rating']['aggregate_rating']
        photo = rest['restaurant']['featured_image']
        zomato_dict['restaurants'].append([name,location,cuisines,rate,photo])
    return zomato_dict


def getZomatoCityID(params):
    headers = {    
       "user-key": "{}".format(ZOMATO_CRED)
    }
    params = "q="+params
    url = "https://developers.zomato.com/api/v2.1/cities?{}".format(params)
    response = requests.get(url,headers=headers)
    data=response.json()
    dat = data["location_suggestions"]
    zomato_dict={
    "id":dat[0]["id"],
    "name":dat[0]["name"],
    "country_id": dat[0]["country_id"],
    "country_name": dat[0]["country_name"],
    "state_id": dat[0]["state_id"],
    "state_name": dat[0]["state_name"]
    }
    return zomato_dict

def getVeganRestaurants(id):
    headers = {    
       "user-key": "{}".format(ZOMATO_CRED)
    }
    url="https://developers.zomato.com/api/v2.1/search?entity_id="+str(id)+"&entity_type=city&count=10&radius=3000&cuisines=308&sort=rating&order=desc"
    response = requests.get(url,headers=headers)
    data=response.json()
    #print(data)
    zomato_list=[]
    for restaurant in data["restaurants"]:
        zomato_dict = {
            "rest_id": restaurant["restaurant"]["id"],
            "rest_name": restaurant["restaurant"]["name"],
            "address": restaurant["restaurant"]["location"]["address"],
            "lat": restaurant["restaurant"]["location"]["latitude"],
            "lon": restaurant["restaurant"]["location"]["longitude"]
        }
        zomato_list.append(zomato_dict)

    rests_df = pd.DataFrame(zomato_list)


    return rests_df

def getStarbucks(id):    
    headers = {    
       "user-key": "{}".format(ZOMATO_CRED)
    }
    url="https://developers.zomato.com/api/v2.1/search?entity_id="+str(id)+"&entity_type=city&q=starbucks&count=10&radius=1000"
    response = requests.get(url,headers=headers)
    data=response.json()
    zomato_list=[]
    for restaurant in data["restaurants"]:
        zomato_dict = {
            "rest_id": restaurant["restaurant"]["id"],
            "rest_name": restaurant["restaurant"]["name"],
            "address": restaurant["restaurant"]["location"]["address"],
            "lat": restaurant["restaurant"]["location"]["latitude"],
            "lon": restaurant["restaurant"]["location"]["longitude"]
        }
        zomato_list.append(zomato_dict)
    starbucks_df = pd.DataFrame(zomato_list)
    return starbucks_df

def getCenter(df1):
    suma = 0
    medlat = 0
    medlon = 0
    for col in df1[["lat","lon"]].values:
        suma+=1
        medlat+=float(col[0])
        medlon+=float(col[1])
    return [medlat/suma,medlon/suma]

def updateCenter(coord1,coord2):
    lat = (coord1[0]*0.5)+(coord2[0]*0.5)
    lon = (coord1[1]*0.5)+(coord2[1]*0.5)
    return [lat,lon]

def getCenterPonderate(com,res,star):
    lat = (com[0]*0.3)+(res[0]*0.2)+(star[0]*0.5)
    lon = (com[1]*0.3)+(res[1]*0.2)+(star[1]*0.5)
    return [lat,lon]

def getAddress(center):
    url = "https://maps.googleapis.com/maps/api/geocode/json?latlng="+str(center[0])+","+str(center[1])+"&key="+GOOGLE_CRED
    response = requests.get(url)
    data=response.json()
    data=data["results"][0]["formatted_address"]
    return data


def getMap(search,df,center):
    marcadores=[]
    label = 0

    for col in df[["lat","lon"]].values:
        marcadores.append("&markers=color:blue%7Clabel:"+str(label)+"%7C"+str(col[0])+","+str(col[1]))
        label+=1
    marcadores.append("&markers=color:red%7Clabel:C%7C"+str(center[0])+","+str(center[1]))
    marcadores= "".join(marcadores)
    #print(marcadores)
    #img = "https://maps.googleapis.com/maps/api/staticmap?center="+search+"&zoom=13&size=600x300&maptype=roadmap&markers=color:blue%7Clabel:S%7C"+str(lat)+","+str(lon)+"&key="+GOOGLE_CRED
    img = "https://maps.googleapis.com/maps/api/staticmap?center="+search+"&zoom=14&size=600x450&maptype=roadmap"+marcadores+"&key="+GOOGLE_CRED
    return img

def getNearMap(search,near,lista,center):
    marcadores=[]
    colors = ['blue','yellow','green','orange','brown']
    selectedcol = random.sample(colors, len(lista))
    for index,e in enumerate(lista):
        marcadores.append("&markers=color:"+selectedcol[index]+"%7Clabel:"+str(index)+"%7C"+str(near[e][0])+","+str(near[e][1]))
    marcadores.append("&markers=color:red%7Clabel:C%7C"+str(center[0])+","+str(center[1]))
    marcadores= "".join(marcadores)
    img = "https://maps.googleapis.com/maps/api/staticmap?center="+search+"&zoom=13&size=600x550&maptype=roadmap"+marcadores+"&key="+GOOGLE_CRED
    return img

def getSchools(search,lat,lon):
    src="https://www.google.com/maps/embed/v1/search?key="+GOOGLE_CRED+"&q=schools+in+"+search+"&zoom=12&center="+str(lat)+","+str(lon)
    return src

def getCenterMap(center):
    src="https://www.google.com/maps/embed/v1/view?key="+GOOGLE_CRED+"&center="+str(center[0])+","+str(center[1])+"&zoom=18&maptype=satellite"
    return src

def getDirWalk(center,coord):
    orig=getAddress(center)
    orig=orig.replace(" ","+")
    dest=getAddress(coord)
    dest=dest.replace(" ","+")
    src="https://www.google.com/maps/embed/v1/directions?key="+GOOGLE_CRED+"&origin="+orig+"&destination="+dest+"&mode=walking"
    return src

def getDirCar(center,coord):
    orig=getAddress(center)
    orig=orig.replace(" ","+")
    dest=getAddress(coord)
    dest=dest.replace(" ","+")
    src="https://www.google.com/maps/embed/v1/directions?key="+GOOGLE_CRED+"&origin="+orig+"&destination="+dest+"&mode=driving"
    return src

def autocomplete():
    url = "https://maps.googleapis.com/maps/api/place/autocomplete/json?input=Vict&types=geocode&key={}".format(GOOGLE_CRED)
    response = requests.get(url)
    data=response.json()
    return data

def nearby(text,coord):
    url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input="+text+"&inputtype=textquery&fields=photos,formatted_address,name,opening_hours,geometry&locationbias=circle:2000@"+str(coord[0])+","+str(coord[1])+"&key={}".format(GOOGLE_CRED)
    response = requests.get(url)
    data=response.json()
    name = data['candidates'][0]['name']
    location = data['candidates'][0]['geometry']['location']
    return [location['lat'], location['lng'],name]
