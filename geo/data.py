from pymongo import MongoClient
import pandas as pd
import json
from geopy.distance import geodesic
from dotenv import load_dotenv
import os
load_dotenv()

MONGO_PWD = os.getenv("MONGO_PWD")

def conections(user,host="mmartin-c1diq.gcp.mongodb.net/test?retryWrites=true&w=majority",pwd=MONGO_PWD,port="27017"):
    client = MongoClient("mongodb+srv://"+user+":"+pwd+"@"+host)
    db = client.geoffice
    return db

def loadData(db):
    data = db.companies.find()
    df = pd.DataFrame(data)
    return df

def geonear(db, geopoint, maxdistance=1000):
    data = db.companies.find({
        "geo":{
            "$near":{
                "$geometry":geopoint,
                "$maxDistance":maxdistance
            }}})
    df = pd.DataFrame(data)
    return df


def geopoint(lat,lon):
    return {'type': 'Point', 'coordinates': [lon, lat]}

def getlat(geopoint):
    lat = geopoint["coordinates"][1]
    return lat

def getlon(geopoint):
    lon = geopoint["coordinates"][0]
    return lon

def getDf(lat,lon,radio):
    db = conections("mmartin")
    geo = geopoint(lat,lon)
    df = geonear(db,geo,radio)
    df["lat"] = df["geo"].apply(getlat)
    df["lon"] = df["geo"].apply(getlon)
    df = df[["name","description","category_code","homepage_url","lat","lon"]]
    return df

def addDistance(latitude,longitude,center):
    return geodesic(tuple(center), (latitude,longitude)).miles

def orderdf(df,center):
    df["distance"] = df.apply(lambda x: addDistance(x["lat"], x["lon"],center), axis = 1)
    df = df.sort_values(by=['distance'])
    return df.head(10)

def geonearAir(db, geopoint, maxdistance=1000):
    data = db.airports.find({
        "geo":{
            "$near":{
                "$geometry":geopoint,
                "$maxDistance":maxdistance
            }}})
    df = pd.DataFrame(data)
    return df


def loadDataAirports(lat,lon,center):
    radio = 20000
    db = conections("mmartin")
    geo = geopoint(lat,lon)
    df = geonearAir(db,geo,radio)
    if df.empty:
        return df
    else:
        df = orderdf(df,center)
        return df


