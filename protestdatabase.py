import sqlite3
import json

# CONECTION AND CURSOR
DB_NAME = "protest_database.sql"
def create_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()


    #SQL TABLES
    create_tweet_txt= "CREATE TABLE tweet_txt(tweet_id int PRIMARY KEY, " \
                      "full_text char(200), " \
                      "user_id int, " \
                      "place varchar(30), " \
                      "geo varchar(30), " \
                      "coordinates varchar(30)," \
                      "user_loc varchar(30), " \
                      "valid_tweet_id int, " \
                      "valid_embed int)"


    create_tweet_hashtag= "CREATE TABLE tweet_hashtags(tweet_hash_rel int PRIMARY KEY AUTOINCREMENT, " \
                          "tweet_id int, hashtag varchar(30))"

    # create_tweet_loc = "CREATE TABLE tweet_loc(tweet_id int PRIMARY KEY, " \
    #                    "place varchar(30), " \
    #


    # create_embeded_tweet= "CREATE TABLE embed_tweet(tweet_id int PRIMARY KEY , " \
    #                       "validation int)"


    create_user_info= "CREATE TABLE user_info (user_id int PRIMARY KEY," \
                       "valid_user_id int)"


    create_geo_mapping = "CREATE TABLE geo_mapping(tweet_id int PRIMARY KEY, " \
                         "place varchar(30)," \
                         "converted_place char(30)," \
                         "google_api_loc varchar(100))"

    #EXECUTE COMMANDS
    cur.execute(create_tweet_txt)
    cur.execute(create_tweet_hashtag)
    cur.execute(create_user_info)
    cur.execute(create_geo_mapping)
    conn.commit()
    conn.close()

def load_bars():
    file_contents= open('example.jsonl','r')
    # jsonl_reader = file_contents.readline()
    # next(jsonl_reader)
    # while
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    counter = 0
    for jsonl in file_contents:
        object = json.loads(jsonl)


        counter += 1
        if counter % 5 == 0:
            conn.commit()
            counter = 0

    file_contents.close()
    conn.commit()
    conn.close()



if __name__ == '__main__':
    load_bars()




