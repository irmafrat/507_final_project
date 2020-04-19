import json
import requests
import secrets
from requests_oauthlib import OAuth1
from bs4 import BeautifulSoup


class Tweet:
    def __init__(self:object, text: str, date: str, hashtags:str, source: str, id: int, geo=None, coordinates= None, place = None, user_location= None):
        """

        :type self: object
        """
        self.text = text
        self.date = date
        self.hashtags = hashtags
        self.source = source
        self.id = id
        self.geo= geo
        self.coordinates= coordinates
        self.place= place
        self.user_location = user_location

    def __str__(self):
        return (
                f"The user wrote:\n'{self.text}' \n\n" +
                f"\tHashtags: {self.hashtags}. \n" +
                f"\tDate: {self.date}\n\tDevice: '{self.source}'\n" +
                f"\tID: {self.id} \n" +
                f"\tUser Location: {self.user_location}\n" +
                f"\tGeo: {self.geo}\n" +
                f"\tCoordinates: {self.coordinates}\n" +
                f"\tPlace: {self.place}\n" +
                "\n"
        )

    def extract_tweet_data(tweet_str):
        #Obtains the data of interest from the tweet.
        converted_tweet = json.loads(tweet_str)
        data = {}
        data.update({'text' : converted_tweet["full_text"],
                     'date' : converted_tweet["created_at"],
                     'source' : converted_tweet["source"],
                     'id' : converted_tweet["id"],
                     'geo': converted_tweet["geo"],
                     'place': converted_tweet["place"],
                     'coordinates': converted_tweet["coordinates"],
                     'user_location':converted_tweet["user"]["location"]})
        if len(converted_tweet["entities"]["hashtags"]) > 0:
            data.update({'hashtags' : converted_tweet["entities"]["hashtags"][0]["text"]})
        else:
            data.update({'hashtags' : None})
        return data

    def tweet_from_str(api_json_str):
        # print(api_json_str)
        data = Tweet.extract_tweet_data(api_json_str)
        tweet = Tweet(data['text'], data['date'], data['hashtags'], data['source'], data['id'], data['geo'],data['coordinates'], data['place'], data['user_location'])
        return tweet


#Converting strings to Dictionaru
def convert_json(tweet_str):
    # Receive a string and returns a json file. Returns a dictionary.
    tweet = json.loads(tweet_str)
    return tweet


#Testing if the dictionary contains geographical data
def keep_tweet(tweet_str):
    #Returns a boolean. If the tweet contains geolocalization information will return T/F.
    converted_tweet = convert_json(tweet_str)
    if converted_tweet["geo"] != None or \
            converted_tweet["coordinates"] != None or \
            converted_tweet["place"]!= None  or \
            (converted_tweet["user"]["location"] != None and converted_tweet["user"]["location"] !=  ""):
        return True
    else:
        return False

#Selecting the tweets that contains geographical data
def display_tweets_geo(tweet_str):
    #Returns a tweet dictiorary that contains a geolocation.
    convert_json(tweet_str)
    while True:
        if keep_tweet(tweet_str) == True:
            return f"yay!!! here I am {tweet_str}"
        else:
            return f"ESTA CACA!"


#Extracting text from the tweet
def extract_tweet_data(tweet_str):
    #Obtains the data of interest from the tweet.
    converted_tweet = convert_json(tweet_str)
    text= converted_tweet["full_text"]
    date= converted_tweet["created_at"]
    # hashtags= converted_tweet["entities"]["hashtags"][0]["text"]
    source= converted_tweet["source"]
    tweet_id= converted_tweet["id"]
    tweet = Tweet(text, date, None, source, tweet_id)
    return tweet

# def cache_geo_tweet(tweet_str):
#     #Receives a tweet strings, confirms that contains geolocation using the funcion keep_tweet,
#     # extract the interested data using the function extract tweet data and send it to the cache file.
#     if keep_tweet(tweet_str)==True:
#        CACHE_FUNCTION(extract_tweet_data(tweet_str)
#         return f"Tweet is being saved in the cache file"


#Filter tweet id in the tweet str
def tweet_id(tweet_str):
    #Select the tweet id in the tweet_str and returns an integer(id).
    converted_tweet = convert_json(tweet_str)
    tweet_id= converted_tweet["id"]
    return tweet_id
#
# Using tweet id to get link of the tweet
def retrive_tweet(tweet_id):
    #Connects to the Twitter API and returns the twiter link:
    base_url= "https://api.twitter.com/1.1/statuses/lookup.jsonid="
    params= (f"?id={tweet_id}")
    response = requests.get(base_url, params, auth=oauth).json()
    result= response
    return result



#EXAMPLE OF GET https://api.twitter.com/1.1/statuses/lookup.json?id=20,1050118621198921728

if __name__ == "__main__":
    max_idx = 20000000000000
    client_key = secrets.TWITTER_API_KEY
    client_secret = secrets.TWITTER_API_SECRET
    access_token = secrets.TWITTER_ACCESS_TOKEN
    access_token_secret = secrets.TWITTER_ACCESS_TOKEN_SECRET

    oauth = OAuth1(client_key,
            client_secret=client_secret,
            resource_owner_key=access_token,
            resource_owner_secret=access_token_secret)

    # file = open("/home/irma/PycharmProjects/RickyUPRFinalProject/RickyRenunciaLlevateJunta.csv", "r")
    file= open("/home/irma/PycharmProjects/RickyUPRFinalProject/example.jsonl")
    # file= open("/home/irma/PycharmProjects/RickyUPRFinalProject/luchaSiEntregano.csv","r")
    # reader =file.readline()
    running_idx = 0
    kept_tweets = []
    count_kept = 0
    count_discard = 0
    while True:
        try:
            line = file.readline()
            line_dict = json.loads(line)
            jobjt = json.loads(line)
            # print("place:" + str(jobjt['place']))
            # print("Type place: " + str(type(jobjt['place'])))
            if keep_tweet(line):
                print(f"Kept tweet at index {running_idx}")
                # print(line)
                tweet = Tweet.tweet_from_str(line)
                print(tweet)
                kept_tweets.append(tweet)
                count_kept += 1
            else:
                count_discard += 1
            #     print("Tweet not kept")
            #     print(extract_tweet_data(line))
            #     print(display_tweets_geo(line))
            #     print(tweet_id(line))
            #     print(retrive_tweet(line))
            # print(convert_json(line))
            # print(keep_tweet(line))
        except:
            break
        running_idx +=1
        if running_idx > max_idx:
            break

    file.close()
    print(f"Total kept: {count_kept}\nTotal discard: {count_discard}")
    # line= reader
    # print(convert_json(line))
    # print(keep_tweet(line))
    # print(extract_tweet_data(line))
    # print(display_tweets_geo(line))
    # print(tweet_id(line))
    # print(retrive_tweet(line))
