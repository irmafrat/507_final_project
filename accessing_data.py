from irmacache import Cache, Embed_Cache
import json
import requests
import secrets
from requests_oauthlib import OAuth1
import sqlite3
from os import rename
from bs4 import BeautifulSoup
TWEET_EMBED_CACHE = Embed_Cache("embed_cache.json")
TWEET_CACHE = Cache("tweet_cache.json")

BASE_URL= "https://twitter.com/anyuser/status/"
EMBED_URL = "https://publish.twitter.com/oembed/"
DB_NAME = "/home/irma/PycharmProjects/RickyFinalProject/protest_database.sql"
PROJECT_FILES = ["/home/irma/PycharmProjects/RickyFinalProject/rickyrenuncia2K.jsonl", "/home/irma/PycharmProjects/RickyFinalProject/luchaSiEntregano2K.jsonl"]
PROJECT_IDS = ["1", "2"]
PROJECT_NAME = ["RickyRenuncia2019", "HuelgaUPR2017"]
PROJECT_TABLE = "project_info"
T_TABLE = "tweet_txt"
TH_TABLE = "tweet_hashtags"
GEO_TABLE = "geo_mapping"
UI_TABLE = "user_info"

class Tweet:
    def __init__(self:object, text: str, date: str, hashtags:list, source: str,
                 id: int, user_id: str, language: str, project_id: int, geo=None, coordinates= None, place = None, user_location= None):
        """

        :type self: object
        """
        self.text = text
        self.date = date
        self.hashtags = hashtags
        self.source = source
        self.id = id
        self.language = language
        self.geo= geo
        self.coordinates= coordinates
        self.place= place
        self.user_location = user_location
        self.user_id = user_id
        self.project_id = project_id


    def sql_insert(self, table_name):
        return f"INSERT INTO {table_name}" \
               f"(tweet_id, full_text, date, user_id, geo, coordinates, place, user_loc, valid_tweet_id, valid_embed, language, project_id) " \
               f"VALUES {self.sql_values()}"

    def sql_hashtags(self, table_name = "tweet_hashtags"):
        """

        :param table_name:
            table_name is the table that holds the tweet hashtag relationship
        :return:
            A list of queries relating a tweet with a hashtag
        """
        queries = []
        for hashtag in self.hashtags:
            queries.append(f"INSERT INTO {table_name}(tweet_id, hashtag) VALUES ({self.id}, \"{hashtag}\")")
        return queries


    def get_tweet_from_web(self):
        tweet_url = BASE_URL + str(self.id)
        response = TWEET_CACHE.get(tweet_url)
        return response

    def get_embed(self):
        tweet_url = BASE_URL + str(self.id)
        # tweet_url = tweet_url.replace("/","%2F")
        # tweet_url = tweet_url.replace(":","%3A")
        params= {'url': tweet_url}
        response = TWEET_EMBED_CACHE.get(EMBED_URL,params)
        # print(response)
        try:
            html=json.loads(response)['html']
            print("json.loads worked")
        except:
            html=None
            # print("json.loads failed!")
        return html

    def sql_values(self):
        uid = self.user_id
        if uid is None:
            uid = "Null"
        text = self.text
        if '"' in text:
            text = text.replace("'", "''")
            text = "'" + text + "'"
        else:
            text = '"' + text + '"'
        return f"({self.id}, {text}, \"{self.date}\", {uid}, \"{self.place}\" ," \
               f"\"{self.geo}\", \"{self.coordinates}\",\"{self.user_location}\", " \
               f"{self.valid_id()}, {self.valid_embed()}, \"{self.language}\", {self.project_id})"


    def  valid_id(self):
        return 0

    def valid_embed(self):
        if self.get_embed() is None:
            valid = 0
        else:
            valid = 1
        return valid

    def __str__(self):
        return (
                f"The user wrote:\n'{self.text}' \n\n" +
                f"\tHashtags: {str(self.hashtags)}. \n" +
                f"\tDate: {self.date}\n"
                f"\tDevice: '{self.source}'\n" +
                f"\tID: {self.id} \n" +
                f"\tUser Location: {self.user_location}\n" +
                f"\tGeo: {self.geo}\n" +
                f"\tCoordinates: {self.coordinates}\n" +
                f"\tPlace: {self.place}\n" +
                f"\tUserID: {self.user_id}\n" +
                f"\tLanguage: {self.language}\n"
        )

    def extract_tweet_data(tweet_str):
        #Obtains the data of interest from the tweet.
        converted_tweet = json.loads(tweet_str)
        data = {}
        data.update({'text' : converted_tweet["full_text"],
                     'date' : converted_tweet["created_at"],
                     'source' : converted_tweet["source"],
                     'id' : int(converted_tweet["id"]),
                     'language': converted_tweet["lang"],
                     'geo': converted_tweet["geo"],
                     'place': converted_tweet["place"],
                     'coordinates': converted_tweet["coordinates"],
                     'user_location': converted_tweet["user"]["location"].strip(), # striping spaces
                     'user_id': converted_tweet["user"]["id_str"]})
        hashtags = []
        if len(converted_tweet["entities"]["hashtags"]) > 0:
            for hash in converted_tweet["entities"]["hashtags"]:
                hashtags.append(hash["text"])
        data.update({'hashtags' : hashtags})
        return data

    def tweet_from_str(api_json_str, project_id):
        # print(api_json_str)
        data = Tweet.extract_tweet_data(api_json_str)
        tweet = Tweet.tweet_from_dict(data, project_id)
        return tweet

    def tweet_from_dict(data: dict, project_id: str):
        tweet = Tweet(data['text'], data['date'], data['hashtags'], data['source'], data['id'], data['user_id'], data['language'], project_id, data['geo'],data['coordinates'], data['place'], data['user_location'])
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
    client_key = secrets.TWITTER_API_KEY
    client_secret = secrets.TWITTER_API_SECRET
    access_token = secrets.TWITTER_ACCESS_TOKEN
    access_token_secret = secrets.TWITTER_ACCESS_TOKEN_SECRET

    oauth = OAuth1(client_key,
            client_secret=client_secret,
            resource_owner_secret=access_token_secret)
    base_url= "https://api.twitter.com/1.1/statuses/lookup.json"
    params= ({"id":tweet_id})
    response = requests.get(base_url, params, auth=oauth).json()
    result= response
    return result


# CONECTION AND CURSOR
def create_db(db_name=DB_NAME):
    rename(DB_NAME, DB_NAME + ".old")
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()


    #SQL TABLES
    create_tweet_txt= f"CREATE TABLE {T_TABLE}(tweet_id UNSIGNED BIG INT, " \
                      f"full_text char(200), " \
                      f"date datetime,"\
                      f"user_id int, " \
                      f"place varchar(30), " \
                      f"geo varchar(30), " \
                      f"coordinates varchar(30)," \
                      f"user_loc varchar(30), " \
                      f"valid_tweet_id int, " \
                      f"valid_embed int,"\
                      f"language str , " \
                      f"project_id int, " \
                      f"PRIMARY KEY(project_id, tweet_id), " \
                      f"CONSTRAINT fk_column " \
                      f"FOREIGN KEY (project_id) " \
                      f"REFERENCES {PROJECT_TABLE}(project_id))"

    create_project = f"CREATE TABLE {PROJECT_TABLE}(project_id int PRIMARY KEY, name str)"

    create_tweet_hashtag= f"CREATE TABLE {TH_TABLE}(tweet_hash_rel INTEGER PRIMARY KEY AUTOINCREMENT, " \
                          f"tweet_id int, hashtag varchar(30)," \
                          f"CONSTRAINT fk_column " \
                          f"FOREIGN KEY (tweet_id) " \
                          f"REFERENCES {T_TABLE}(tweet_id))"


    # create_user_info= f"CREATE TABLE {UI_TABLE} (user_id int PRIMARY KEY," \
    #                    f"valid_user_id int)"


    # create_geo_mapping = f"CREATE TABLE {GEO_TABLE}(tweet_id int PRIMARY KEY, " \
    #                      f"place varchar(30)," \
    #                      f"converted_place char(30)," \
    #                      f"google_api_loc varchar(100))"

    #EXECUTE COMMANDS
    cur.execute(create_project)
    cur.execute(create_tweet_txt)
    cur.execute(create_tweet_hashtag)
    # cur.execute(create_user_info)
    # cur.execute(create_geo_mapping)
    conn.commit()
    cur.close()
    conn.close()


def add_project(project_id, project_name, db_name):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    query = f"INSERT INTO {PROJECT_TABLE}(project_id, name) VALUES ({project_id}, \"{project_name}\")"
    cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()


def tweets_to_db(tweets: dict, db_name):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    for id, queries in tweets.items():
        # [tweet_query, [h1, h2, ...] ]
        query = queries[0]
        hashtag_queries = queries[1]
        embed_html = queries[2]
        # print(query)
        cur.execute(query)
        for hash_query in hashtag_queries:
            cur.execute(hash_query)
    # for tweet in tweets:
    #     test = tweet_in_db(tweet.id, conn, "tweet_txt")
    #     print(test)
    #     print(tweet.sql_insert("tweet_txt"))
    #     if not test:
    #         cur.execute(tweet.sql_insert("tweet_txt"))
    #         conn.commit()
    conn.commit()
    conn.close()


def tweet_in_db(tweet_id, db_conn: sqlite3.connect, table_name=T_TABLE):
    # conn = sqlite3.connect(db_name)
    cur = db_conn.cursor()
    query = f"SELECT * from {table_name} WHERE tweet_id = {tweet_id}"
    cur.execute(query)
    rows = cur.fetchall()
    cur.close()
    if len(rows) > 0:
        return True
    else:
        return False
#EXAMPLE OF GET https://api.twitter.com/1.1/statuses/lookup.json?id=20,1050118621198921728


def load_tweets(project_file, project_id, db_name=DB_NAME):
    file = open(project_file)
    for jsonl in file:
        # print(jsonl[:-1])
        tweet = Tweet.tweet_from_str(jsonl, project_id)
        if str(tweet.id) not in tweets.keys():
            tweets.update({str(tweet.id):[tweet.sql_insert(T_TABLE), tweet.sql_hashtags(TH_TABLE),tweet.get_embed()]})
        else:
            print(f"Tweet {tweet.id} duplicated.")
        # print(tweet)
    tweets_to_db(tweets, db_name)
    print("Tweets from " + project_file + " Saved!")

if __name__ == "__main__":
    r = retrive_tweet(1151300011151564800)
    print(r)
    i = input("hey")
    max_idx = 20
    client_key = secrets.TWITTER_API_KEY
    client_secret = secrets.TWITTER_API_SECRET
    access_token = secrets.TWITTER_ACCESS_TOKEN
    access_token_secret = secrets.TWITTER_ACCESS_TOKEN_SECRET

    oauth = OAuth1(client_key,
            client_secret=client_secret,
            resource_owner_secret=access_token_secret)

    # file = open("/home/irma/PycharmProjects/RickyFinalProject/RickyRenunciaLlevateJunta.jsonl", "r")
    # file= open("/home/irma/PycharmProjects/RickyFinalProject/RickyRenunciaLlevateJunta.jsonl")
    # file= open("/home/irma/PycharmProjects/RickyFinalProject/luchaSiEntregano.jsonl","r")
    # reader =file.readline()
    # running_idx = 0
    # kept_tweets = []
    # unkept_tweets = []
    # all_tweets = []
    # count_kept = 0
    # count_discard = 0
    # while True:
    #     try:
    #         line = file.readline()
    #         # tweet = Tweet.tweet_from_str(line)
    #         # print(tweet)
    #         if keep_tweet(line):
    #             print(f"Kept tweet at index {running_idx}")
    #             # print(line)
    #             tweet = Tweet.tweet_from_str(line)
    #             print(tweet)
    #             kept_tweets.append(tweet.__dict__)
    #             count_kept += 1
    #         else:
    #             unkept_tweets.append(line)
    #             count_discard += 1
    #
    #     except:
    #         break
    #     running_idx +=1
    #     if running_idx > max_idx:
    #         break


    # create_db(DB_NAME)
    tweets = {}
    create_db(DB_NAME)
    for idx in range(len(PROJECT_NAME)):
        add_project(PROJECT_IDS[idx], PROJECT_NAME[idx], DB_NAME)

    # load_tweets("/home/irma/PycharmProjects/RickyFinalProject/rand_rickyrenuncia.jsonl", PROJECT_IDS[0], DB_NAME)
    load_tweets("/home/irma/PycharmProjects/RickyFinalProject/example_tail.jsonl", PROJECT_IDS[0], DB_NAME)
    # # file = open(PROJECT_FILES[0])
    # file = open("/home/irma/PycharmProjects/RickyFinalProject/rand_rickyrenuncia.jsonl")
    # for jsonl in file:
    #     # print(jsonl[:-1])
    #     tweet = Tweet.tweet_from_str(jsonl, PROJECT_IDS[0])
    #     if str(tweet.id) not in tweets.keys():
    #         tweets.update({str(tweet.id):[tweet.sql_insert(T_TABLE), tweet.sql_hashtags(TH_TABLE)]})
    #     else:
    #         print(f"Tweet {tweet.id} duplicated.")
    #     # print(tweet)
    # tweets_to_db(tweets, DB_NAME)
    # print("Tweets Saved!")
    # file.close()
    # print(f"Total kept: {count_kept}\nTotal discard: {count_discard}")
    # with open('kept_tweets.json', 'w') as out_file:
    #     json.dump(kept_tweets, out_file)
    # cache = Embed_Cache("embed_cache.json")
    # print("cache made")
    # for idx in range(10, len(kept_tweets)):
    #     params= {'url': BASE_URL + str(kept_tweets[idx]['id'])}
    #     response = cache.get(EMBED_URL,params)
    #     print(response)
    #     try:
    #         html=json.loads(response)['html']
    #         print(html)
    #     except:
    #         continue
    # file.close()
