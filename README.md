# 507_final_project
# Recent protest movement in Puerto Rico

## This project plans to create a database that gather, displays and allows the user to search tweets related to the following events :
- [University of Puerto Rico Student Protest(2017)](https://catalog.docnow.io/datasets/20170519-huelgaupr-tweets-april-20-may-18-2017/)
- [Ricky Renuncia Protest(2019)](https://catalog.docnow.io/datasets/20190930-rickyrenuncia/)


## Data Provenance

|    DATA    |    FORMAT     |     URL     |
------------ | ------------- | -------------
|Ricky Renuncia Protest | JSONL | https://catalog.docnow.io/datasets/20190930-rickyrenuncia/|
|HuelgaUPRTweets | JSONL | https://catalog.docnow.io/datasets/20170519-huelgaupr-tweets-april-20-may-18-2017/|
|Embeded Tweets  | JSON  | Twitter API Response |

### Data Access & Manipulation: Ricky Renuncia Protest and HuelgaUPRTweets(University of Puerto Rico Student Protest)

The datasets were available through the [Documenting the Now tweet catalog](https://catalog.docnow.io/).
Both datasets were txt files that contained tweets ids.
Using the Hydrator, program created by Documenting the Now, this app is able to retrieve the full record of the tweets.

|    DATA    |    ORIGINAL FILE RETRIEVAL   |   QUANTITY USED IN THE DATABASE    |   FORMAT     | CODE TO SELECT TWEETS GENERATE A SMALLER SAMPLE |
|------------| --------------------------   | ---------------------------------- | ------------ | -------------|
|Ricky Renuncia Protest | 977,207 | 2,000 | JSONL | shuf -n 2000 RickyRenunciaLlevateJunta.jsonl > rickyrenuncia2k.jsonl |
|HuelgaUPRTweets | 19,914 | 2,000 | JSONL | shuf -n 2000 luchaSiEntregano.jsonl > luchaSiEntregano2k.jsonl |


### Cache Implementation

The project is using cache to store the embedded tweets with an id of the user in order to provide a display and a link to the tweet.
It is important to mention that Twitter do controls the tweets that are visible to the public. Twitter only displays the [3,200 most recent tweets](https://help.twitter.com/en/using-twitter/missing-tweets) of the user.
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

### Packages used in the project:
1. Hydrator - To gather the JSONL tweets
2. Flask - To develop a front end for form the database
3. Sqlite3 - To develop the database
4. OAuth1 - To manage the program authorization
5. Time - To manage [Twitter Rate Limits](https://developer.twitter.com/en/docs/basics/rate-limiting).
6. Math - To manage database display pages. (i.e the PREV. and NEXT buttons)
7. os - (os.rename) To change the database name every time the app runs and save the previous one.
7. JSON
8. Requests
9. Secrets

### Database
This project will create one database with 3 tables.
The tables and their relation are the following:

![Photo of project protest_database](https://github.com/irmafrat/507_final_project/blob/master/readme_images/Entity%20Relationship%20Diagram%20(UML%20Notation).jpeg)

Photo of ERD Diagram for protest_database


#### Code developed to create the database:

```

SQL TABLES
create_tweet_txt= f"CREATE TABLE {T_TABLE}(tweet_id UNSIGNED BIG INT, " \
          f"full_text char(200), " \
          f"create_at datetime,"\
          f"user_id int, " \
          f"place varchar(30), " \
          f"geo varchar(30), " \
          f"coordinates varchar(30)," \
          f"user_loc varchar(30), " \
          f"valid_tweet_id int, " \
          f"valid_embed int,"\
          f"lang str , " \
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

```


Photo of project protest database with data. I am using SQLite Browser to navigate my database.


![Photo of project protest database with data](https://github.com/irmafrat/507_final_project/blob/master/readme_images/database.png)



### Interaction and Presentation

####LINK TO PROGRAM DEMO-----> https://www.loom.com/share/feccf3bd70de41849e8aa773e867f0d0


With this program the user will be able to search a database of tweets related to historical events in Puerto Rico.
The user will be able to fill a form setting up the historical event, language, location and the search query.
With this metadata, the user will see a table displaying the data requested and a hyperlinked tweet id.
If the user wants to see the embedded tweet, it just needs to click on the tweet id number.
if the tweet has been deleted the user will see the tweet id and a warning message.

I am using to use Flask to display the form and table.

#### Instructions to run the program:

1. Clone or Download the project.
2. Make sure that you have the packages used in the project installed. (They are listed above).
3. Run the accessing_data.py file in your terminal to generate the SQL database and Cache files.
4. Run the app.py file in your terminal and access the url.
5. The URL will open a browser will the front-end of the database.
6. Interact and submit requests in the database front-end page! :)


![GIF displaying program implementation](https://github.com/irmafrat/507_final_project/blob/master/readme_images/app_implementation_2.gif)










