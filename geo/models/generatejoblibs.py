from pymongo import MongoClient
import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.externals import joblib
import pickle
import os
from dotenv import load_dotenv
load_dotenv()

MONGO_PWD = os.getenv("MONGO_PWD")

def conections(user,host="mmartin-c1diq.gcp.mongodb.net/test?retryWrites=true&w=majority",pwd=MONGO_PWD,port="27017"):
    client = MongoClient("mongodb+srv://"+user+":"+pwd+"@"+host)
    db = client.geoffice
    return db

def pre_process(text):
    
    # lowercase
    print(text)
    text=text.lower()
    
    #remove tags
    text=re.sub("</?.*?>"," <> ",text)
    
    # remove special characters and digits
    text=re.sub("(\\d|\\W)+"," ",text)
    
    return text

db = conections("mmartin")
data = db.companiesOffices.find({
        "overview": {"$ne":"null"}}
)
df = pd.DataFrame(data)
overlist = df["overview"].tolist()
overclean = [pre_process(text) for text in overlist if text is not None]

def get_stop_words(stop_file_path):
    """load stop words """
    
    with open(stop_file_path, 'r', encoding="utf-8") as f:
        stopwords = f.readlines()
        stop_set = set(m.strip() for m in stopwords)
        return frozenset(stop_set)

#load a set of stop words
stopwords=get_stop_words("stopwords.txt")

#get the text
#overclean
#create a vocabulary of words, 
#ignore words that appear in 85% of documents, 
#eliminate stop words
#limit our vocabulary size to 10,000
cv=CountVectorizer(max_df=0.85,ngram_range=(1, 2),stop_words=stopwords,max_features=10000)
cv._validate_vocabulary()
cvfit = cv.fit(overclean)
word_count_vector=cvfit.transform(overclean)
pickle.dump(cvfit,open('cvfit.joblib', 'wb')) 
tfidf_transformer=TfidfTransformer(smooth_idf=True,use_idf=True)
tfidf_transformer.fit(word_count_vector)
pickle.dump(tfidf_transformer,open('tfidf_transformer.joblib', 'wb')) 
# you only needs to do this once
feature_names=cv.get_feature_names()
pickle.dump(feature_names, open('feature_names.joblib', 'wb'))