# 507_final_project
# Recent protest movement in Puerto Rico

## This project plans to create a database that gather, displays and allows the user to search tweets related to the following events :
    *[University of Puerto Rico Student Protest(2017)](https://catalog.docnow.io/datasets/20170519-huelgaupr-tweets-april-20-may-18-2017/)
    *[Ricky Renuncia Protest(2019)](https://catalog.docnow.io/datasets/20190930-rickyrenuncia/)

## Instructions to run the program:
1. Clone or Download the project.
2. Make sure that you have the packages used in the project installed. (They are listed below this instructions).
3. Run the accessing_data.py file in your terminal to generate the SQL database and Cache files.
4. Run the app.py file in your terminal and access the url.
5. The URL will open a browser will the front-end of the database.
6. Interact and submit requests in the database front-end page! :)

### Packages used in the project:
1. Hydrator - To gather the JSONL tweets
2. Flask - To develop a front end for the database
3. Sqlite3 - To develop the database
4. OAuth1 - To manage the program authorization
5. Time - To manage [Twitter Rate Limits](https://developer.twitter.com/en/docs/basics/rate-limiting).
6. Math - To manage database display pages. (i.e the PREV. and NEXT buttons)
7. os - (os.rename) To change the database name every time the app runs and save the previous one.
7. JSON
8. Requests
9. Secrets


### Data Provenance

|    DATA     |    FORMAT     |     URL     |
------------ | ------------- | -------------
|Ricky Renuncia Protest | JSONL | https://archive.org/details/tweetsRickyRenuncia-final|
|HuelgaUPRTweets | JSONL | https://archive.org/details/tweet-ids_HuelgaUPR20170420-0518|
|Embeded Tweets  | JSON  | Twitter API Response |

### Data Access: Ricky Renuncia Protest and HuelgaUPRTweets(University of Puerto Rico Student Protest)

The datasets were available through the [Documenting the Now tweet catalog](https://catalog.docnow.io/).
Both datasets were txt files that contained tweets ids.
Using the TWARC package and the Hydrator, both created by Documenting the Now, the program is able to retrieve the full record of the tweets.

|    DATA    |    ORIGINAL FILE RETRIEVAL   |   QUANTITY USED IN THE DATABASE    |   FORMAT     | CODE TO SELECT TWEETS GENERATE A SMALLER SAMPLE |
|------------| --------------------------   | ---------------------------------- | ------------ | -------------|
|Ricky Renuncia Protest | 977,207 | 2,000 | JSONL | shuf -n 2000 RickyRenunciaLlevateJunta.jsonl > rickyrenuncia2k.jsonl |
|HuelgaUPRTweets | 19,914 | 2,000 | JSONL | shuf -n 2000 luchaSiEntregano.jsonl > luchaSiEntregano2k.jsonl |


###Cache Implementation

The project is using cache to store the embedded tweets with an id of the user in order to provide a display and a link to the tweet.
It is important to mention that Twitter do controls the tweets that are visible to the public. Twitter only displays the [3,200 most recent tweets] of the user.(https://help.twitter.com/en/using-twitter/missing-tweets)
This affects the behavior of the cache and the display of the tweet in the program.

### Description of records

From the tweets it will be extracted the following data using the following tags:

    *["full_text"]= Text that contains the tweet
    *["created_at"] =  Date and time
    *["source"] = Device used to publish the tweet
    *["id"] = Tweet identifier
    *["geo"] = Geographical metadata
    *["place"]= Geographical metadata
    *["coordinates"] = Geographical metadata
    *["user"]["location"] = User entry about geographical metadata
    *["user"]["id_str"] = User identifier
    *["entities"]["hashtags"] = Hashtags used in the tweet

This information will be transformed into a dictionary in order to facilitate the retrieval of the tweets on the SQL database.
It is important to mention that the localization data and the language data does not refer to the actual location or language of the tweet, it refeers to the location and language that the user decided to identify with.


### Database (Working)
This project will create one database with five tables.
The tables are the following with their SQL code:

    *tweet_txt = contains the full text of the tweet.
        **CODE** CREATE TABLE tweet_txt(tweet_id int PRIMARY KEY, full_text char(200), user_id int, hashtag varchar(30),place varchar(30))

    *tweet_loc = contains information about the location of the user at the moment to publish the tweet.
        **CODE** CREATE TABLE tweet_loc(tweet_id int PRIMARY KEY, place varchar(30), geo varchar(30), coordinates varchar(30),user_loc varchar(30))

    *embed_tweet= contains information about the tweets and their Twiter link.
        **CODE** CREATE TABLE embed_tweet(tweet_id int PRIMARY KEY , validation int, link char (200))

    *twit_info = contains users_id, tweets_id and if the tweet has been deleted or not.
        **CODE** CREATE TABLE tweet_info (tweet_id int PRIMARY KEY, user_id int,valid_tweet_id int, valid_user_id int)

    *geo_mapping = the table pairs the place string with the Google MAPS API data of the place location.
        **CODE** CREATE TABLE geo_mapping(tweet_id int PRIMARY KEY, place varchar(30),converted_place char(30),google_api_loc varchar(30))


 ### Interaction and Presentation Plans (Working)

With this program the user will be able to search a database of tweets related to historical events in Puerto Rico.
The user will be able to fill a form setting up the dates, keywords, hashtags, and locations.
With this metadata, the user will see a table displaying the data requested,
a link of the location that the tweet is related and an embedding of the tweet;
if the tweet has been deleted the user will see a link or a warning message.

I am planning to use Flask to display the form and table.









