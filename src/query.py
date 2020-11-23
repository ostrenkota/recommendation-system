from SPARQLWrapper import SPARQLWrapper, JSON
import requests
import pandas as pd


def getFilmsIds(marks):
    movieNames = pd.read_csv('./resources/movie_names.csv', delimiter=', ', names=['index', 'name'], engine='python')
    movies = list(map(lambda x: x, marks.keys()))
    names = []
    for movie in movies:
        names.append(movieNames[movieNames['index'] == movie].values[0][1])
    API_ENDPOINT = "https://www.wikidata.org/w/api.php"
    wikiIds = {}
    for name in names:
        params = {
            'action': 'wbsearchentities',
            'format': 'json',
            'language': 'en',
            'search': name
        }
        res = requests.get(API_ENDPOINT, params=params)
        wikiIds[name] = res.json()['search'][0]['id']
    return wikiIds


def sparqlQueryExecute(wikiId):
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql_query = """
    SELECT ?actor ?actorLabel ?birthPlaceLabel ?coords
    WHERE 
    {
      wd:""" + wikiId + """ wdt:P161 ?actor.
      ?actor wdt:P19 ?birthPlace.
      ?birthPlace wdt:P625 ?coords.
      SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
    }"""
    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results['results']['bindings']