# 507_final_project
# Mapping recent protest movement in Puerto Rico

## This project plans to create a database that gather, displays and allows the user to search tweets related to the following events :
    *University of Puerto Rico Student Protest(2017)
    *Ricky Renuncia Protest(2019)

### Data Provenance

|    DATA     |    FORMAT     |     URL     |
------------ | ------------- | -------------
|Ricky Renuncia Protest | JSONL | https://archive.org/details/tweetsRickyRenuncia-final|
|HuelgaUPRTweets | JSONL | https://archive.org/details/tweet-ids_HuelgaUPR20170420-0518|
|Embeded Tweets  | JSON  | Twitter API Response |

### Data Access: Ricky Renuncia Protest and HuelgaUPRTweets(University of Puerto Rico Student Protest)
The datasets were available through the Internet Archive and the Documenting the Now tweet catalog.
Both datasets were txt files that contained tweets ids.
Using the TWARC package and the Hydrator, both created by Documenting the Now, the program is able to retrieve the full record of the tweets.
The project is using cache to store the embedded tweets with an id of the user in order to provide a display or a link to the tweet


|    DATA     |    QUANTITY   |  RECORDS RETRIEVED |     FORMAT   | MODIFICATION|
------------ | ------------- | -------------      | -------------| -------------
|Ricky Renuncia Protest | 977,207 | Example files of 200 for testing | JSONl | Using the command "split -l $SPLIT_SIZE $FILE $PREFIX", the 6GB was splitted into 20 files of 50,000 JSONL |
|HuelgaUPRTweets | 19,914 | Example files of 200 for testing | JSONL | No modification, file to small. |

### Description of records

For the tweets that contains geographical data it will be extracted the following tags:

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

### Cache Implementation (Working)

#### Program running with and without cache

Currently, if the program runs without cache, it will display only the information selected.
        [Photo of the program running without the cache commands](https://drive.google.com/uc?export=view&id=1irtGTyhjnMa7j5Lh31j8mK_t3kkqB2zu)


While if the program is running with cache it wll display if a tweet has been deleted or not from the internet.
If the tweet has not been deleted, it will display a string of the tweet.
        [Photo of the program running with cache](https://drive.google.com/uc?export=view&id=1rCmSYWNBSm_4kYVIjnFVFxG2dmcVhY4X)

#### Cache code  and called used in the program
I created a class called Cache and use it on the program
        [Photo of the cache Code](https://drive.google.com/uc?export=view&id=1jnkWzzjC2OZwmY6VMXI-7rniqiPpGI2L)


Cache class code implemented in the program
        [Photo of the program code](https://drive.google.com/uc?export=view&id=1E6SH0FOdQWmRTXUL3zkB_QnQ3gtOMZ8b)


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









