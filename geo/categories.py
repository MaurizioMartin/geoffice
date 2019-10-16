from bs4 import BeautifulSoup
import requests
import re

def roleCategories():

    categories = {
        'programming':['web','software','games_video','network_hosting','search','hardware','analytics'],
        'publicity':['advertising','public relations','news','design'],
        'technology':['biotech','nanotech','cleantech','semiconductor'],
        'social':['social','messaging','photo_video','fashion','travel','sports','music'],
        'sales':['finance','enterprise','ecommerce','mobile','manufacturing','real estate','automotive'],
        'other':['other','local','hospitality','transportation','nonprofit'],
        'mix':['medical','legal','health','security','education','consulting','government']
    }

    return categories

def scrap():
    url = "https://www.britannica.com/topic/list-of-cities-and-towns-in-the-United-States-2023068"
    enlace = requests.get(url)
    soup = BeautifulSoup(enlace.content, 'html.parser')
    cities = []
    etiquetasA = soup.find_all('a', class_='md-crosslink')
    for et in etiquetasA:
        cities.append(et.get_text())
    return cities

'''
def cityLocations():
    locations = {
        'Alabama': ['Alexander City','Andalusia','Anniston','Athens','Atmore','Auburn','Bessemer','Birmingham','Chickasaw','Clanton','Cullman','Decatur','Demopolis'
Dothan
Enterprise
Eufaula
Florence
Fort Payne
Gadsden
Greenville
Guntersville
Huntsville
Jasper
Marion
Mobile
Montgomery
Opelika
Ozark
Phenix City
Prichard
Scottsboro
Selma
Sheffield
Sylacauga
Talladega
Troy
Tuscaloosa
Tuscumbia
Tuskegee],
        'Alaska': [],
        'Arizona': [],
        'Arkansas': [],
        'California': [],
        'Colorado': [],
        'Connecticut': [],
        'Delaware': [],
        'Florida': [],
        'Georgia': [],
        'Hawaii': [],
        'Idaho': [],
        'Illinois': [],
        'Indiana': [],
        'Iowa': [],
        'Kansas': [],
        'Kentucky': [],
        'Louisiana': [],
        'Maine': [],
        'Maryland': [],
        'Massachusetts': [],
        'Michigan': [],
        'Minnesota': [],
        'Mississippi': [],
        'Missouri': [],
        'Montana': [],
        'Nebraska': [],
        'Nevada': [],
        'New Hampshire': [],
        'New Jersey': [],
        'New Mexico': [],
        'New York': [],
        'North Carolina': [],
        'North Dakota': [],
        'Ohio': [],
        'Oklahoma': [],
        'Oregon': [],
        'Pennsylvania': [],
        'Rhode Island': [],
        'South Carolina': [],
        'South Dakota': [],
        'Tennessee': [],
        'Texas': [],
        'Utah': [],
        'Vermont': [],
        'Virginia': [],
        'Washington': [],
        'West Virginia': [],
        'Wisconsin': [],
        'Wyoming': []
    }

    return locations
'''