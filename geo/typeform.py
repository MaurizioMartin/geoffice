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
        if idd == "pYdlUL4BDYXz":
            dictio['role'] = ans["choice"]['label']
        elif idd == "lCsYeYRuKTU7":
            dictio['numWork'] = ans["choice"]['label']
        elif idd == "PXoY6034ffcD":
            dictio['near'] = ans["choices"]['labels']
        elif idd == "QE6lOXhM0PAk":
            dictio['place'] = ans["text"]

    return dictio
