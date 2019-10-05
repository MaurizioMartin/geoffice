import pandas as pd
import numpy as np
from joblib import dump, load

def getCategories(role):

    categories = {
        'programming':['web','software','games_video','network_hosting','search','hardware','analytics'],
        'publicity':['advertising','public_relations','news','design'],
        'technology':['biotech','nanotech','cleantech','semiconductor'],
        'social':['social','messaging','photo_video','fashion','travel','sports','music'],
        'sales':['finance','enterprise','ecommerce','mobile','manufacturing','real_estate','automotive'],
        'other':['other','local','hospitality','transportation','nonprofit'],
        'mix':['medical','legal','health','security','education','consulting','government']
    }

    data = {}

    for category in categories.keys():
        data[category] = 1 if role in categories[category] else 0
    data_df = pd.DataFrame(data,index=[0])
    model = load('geo/models/pca.joblib') 
    comp_pca = model.transform(data_df)
    comp_pca_df = pd.DataFrame(data = comp_pca)
    company_clusters = load('geo/models/kmeans.joblib') 
    data_df['labels'] = company_clusters.predict(comp_pca_df)
    colnames=['label', 'category', 'num'] 
    labels_df = pd.read_csv("geo/models/labels.csv", names = colnames)
    category_codes = list(labels_df['category'][labels_df.label == int(data_df.labels)])
    return category_codes

