import requests
import json
import secrets
from requests_oauthlib import OAuth1
from time import sleep

class Cache:
    def __init__(self, filename="irma_cache.json"):
        self.filename= filename
        self.cache = self.load_cache()


    def load_cache(self):
        try:
            with open(self.filename, 'r') as handler:
                cache = json.load(handler)

        except FileNotFoundError:
            cache = {}
        return cache


    def get(self, url:str, params:dict):
        key = url + '?' + str(params)
        if key not in self.cache.keys():
            get_response = self.update(url, params)
        else:
            get_response = self.cache[key]
        return get_response

    def delete(self, url:str, params:dict):
        self.cache.pop(url + "?" + str(params))
        with open(self.filename,"w") as cache_file:
            json.dump(self.cache, cache_file)

    def update(self, url:str, params:dict):
        get_response = requests.get(url,params).text
        self.cache.update({url + "?" + str(params):get_response})
        with open(self.filename,"w") as cache_file:
            json.dump(self.cache, cache_file)
        return get_response

class Tweet_Cache(Cache):
    def __init__(self, filename="irma_cache.json"):
        self.filename= filename
        self.cache = self.load_cache()

    def get(self, url:str, params:dict):
        key = url + '?' + str(params)
        if key not in self.cache.keys():
            get_response = self.update(url, params)
        else:
            get_response = self.cache[key]
            if "\"code\":88" in get_response:
                self.delete(url,params)
                get_response = self.update(url, params)
        return get_response

    def update(self, url:str, params:dict):
        client_key = secrets.TWITTER_API_KEY
        client_secret = secrets.TWITTER_API_SECRET
        oauth = OAuth1(client_key=client_key,
                client_secret=client_secret)
        get_response = requests.get(url,params, auth=oauth).text
        if "\"code\":88" in get_response:
            print("Rate Limit Exceeded: waiting 15 minutes\n")
            sleep(15*60+4)
            get_response = requests.get(url,params, auth=oauth).text
        self.cache.update({url + "?" + str(params):get_response})
        with open(self.filename,"w") as cache_file:
            json.dump(self.cache, cache_file)
        return get_response

class Embed_Cache(Cache):
    def __init__(self, filename="irma_cache.json"):
        self.filename= filename
        self.cache = self.load_cache()

    def update(self, url:str, params:dict):
        get_response = requests.get(url,params).text
        self.cache.update({url + "?" + str(params):get_response})
        try:
            resp_dict = json.loads(get_response)
            with open(self.filename,"w") as cache_file:
                json.dump(self.cache, cache_file)
        except:
            get_response = f'Embed not available. Tweet ({params["url"].split("/")[-1]}) may have been deleted.'

        return get_response
