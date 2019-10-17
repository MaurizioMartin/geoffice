import pandas as pd
import numpy as np
from joblib import dump, load
import pickle
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import jellyfish
import geo.categories as ctg
import geo.typeform as tform
from geotext import GeoText
import nltk

def getCategories(role):

    categories = ctg.roleCategories()

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

def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)

def extract_topn_from_vector(feature_names, sorted_items, topn=10):
    """get the feature names and tf-idf score of top n items"""
    
    #use only topn items from vector
    sorted_items = sorted_items[:topn]

    score_vals = []
    feature_vals = []

    for idx, score in sorted_items:
        
        #keep track of feature name and its corresponding score
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])

    #create a tuples of feature,score
    #results = zip(feature_vals,score_vals)
    results= {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]]=score_vals[idx]
    
    return results

def getLoad(path):
    return pickle.load(open(path, 'rb'))

def get_stop_words(stop_file_path):
    """load stop words """
    
    with open(stop_file_path, 'r', encoding="utf-8") as f:
        stopwords = f.readlines()
        stop_set = set(m.strip() for m in stopwords)
        return frozenset(stop_set)

def getKeywords(texto):

    feature_names = getLoad('geo/models/feature_names.joblib')
    tfidf_transformer = getLoad('geo/models/tfidf_transformer.joblib')
    cv = getLoad('geo/models/cvfit.joblib')
    
    #generate tf-idf for the given document
    tf_idf_vector=tfidf_transformer.transform(cv.transform(texto))

    #sort the tf-idf vectors by descending order of scores
    sorted_items=sort_coo(tf_idf_vector.tocoo())
    #extract only the top n; n here is 10
    keywords=extract_topn_from_vector(feature_names,sorted_items,10)
    
    return keywords

def checkJaro(kw,cat):
    lista = []
    for category in cat.values():
        for cat in category:
            lista.append((cat,jellyfish.jaro_distance(kw,cat)))
    return lista

def checkKeyWords(keywords,data):
    if data == 'role':
        kdict = {}
        lista = []
        categories = ctg.roleCategories()
        for kw in keywords:
            kdict[kw] = checkJaro(kw,categories)      
        for key,value in kdict.items():
            lista.append(max(value,key=lambda item:item[1]))
        return sorted(lista, key=lambda item:item[1], reverse=True)[0][0]
    elif data == 'numWork':
        pass

def getNouns(text):
    is_noun = lambda pos: pos[:2] == 'NN'
    tokenized = nltk.word_tokenize(text)
    print(nltk.pos_tag(tokenized))
    nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)] 
    return nouns

def getSize(text):
    size_pos = nltk.pos_tag(text.split())
    grammar = 'NumericalPhrase: {<NN|NNS>?<RB>?<JJR><IN><CD><NN|NNS>?}'
    parser = nltk.RegexpParser(grammar)
    #print([tree.leaves() for tree in parser.parse(size_pos).subtrees() if tree.label() == 'NumericalPhrase'])
    return parser.parse(size_pos)


def cleandictionary(dictio):
    print(dictio)
    cleandictio = {}
    # role
    rolekw = getKeywords([dictio['role']])
    role = checkKeyWords(list(rolekw), 'role')
    cleandictio['role'] = role
    # near
    nouns = getNouns(dictio['near'])
    cleandictio['near'] = nouns
    # located
    places = GeoText(dictio['located'])
    cleandictio['located'] = places.cities[0]
    # size
    size = getSize(dictio['numWork'])
    cleandictio['size'] = size

    print(cleandictio)
    return cleandictio

        #print(sorted(kdict.items(), key=lambda x: x[1], reverse=True))
        #print(kdict)    
            #k = sorted(k, key=lambda x: x[1])
        #print(kdict)


#cleandictionary(tform.getDataDict())