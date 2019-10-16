import os
import requests
from dotenv import load_dotenv
load_dotenv()

TYPEFORM_TOKEN = os.getenv("TYPEFORM_TOKEN")
TYPEFORM_ID = os.getenv("TYPEFORM_ID")


def getAnswerData():
    headers = {    
       "Authorization": "Bearer {}".format(TYPEFORM_TOKEN)
    }
    url = "https://api.typeform.com/forms/"+TYPEFORM_ID+"/responses?page_size=1&completed=true"
    response = requests.get(url,headers=headers)
    data=response.json()
    return data

def getDataDict():
    data = getAnswerData()
    dictio = {}
    for ans in data["items"][0]["answers"]:
        idd = ans["field"]['id']
        if idd == "acyK4BvwUV2F":
            dictio['role'] = ans["text"]
        elif idd == "fckMTY5YY9gQ":
            dictio['located'] = ans['text']
        elif idd == "BVZaZarHKb8M":
            dictio['numWork'] = ans["text"]
        elif idd == "uZmq4BR1Oj19":
            dictio['near'] = ans["text"]
        elif idd == "QE6lOXhM0PAk":
            dictio['place'] = ans["text"]

    return dictio
