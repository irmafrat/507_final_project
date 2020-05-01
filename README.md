# 507_final_project
# Recent protest movement in Puerto Rico

## This project plans to create a database that gather, displays and allows the user to search tweets related to the following events :
- [University of Puerto Rico Student Protest(2017)](https://catalog.docnow.io/datasets/20170519-huelgaupr-tweets-april-20-may-18-2017/)
- [Ricky Renuncia Protest(2019)](https://catalog.docnow.io/datasets/20190930-rickyrenuncia/)

## Instructions to run the program:
1. Clone or Download the project.
2. Make sure that you have the packages used in the project installed. (They are listed below these instructions).
3. Run the accessing_data.py file in your terminal to generate the SQL database and Cache files.
4. Run the app.py file in your terminal and access the url.
5. The URL will open a browser will the front-end of the database.
6. Interact and submit requests in the database front-end page! :)

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


## Data Provenance

|    DATA    |    FORMAT     |     URL     |
------------ | ------------- | -------------
|[Ricky Renuncia Protest | JSONL | https://catalog.docnow.io/datasets/20190930-rickyrenuncia/|
|[HuelgaUPRTweets | JSONL | https://catalog.docnow.io/datasets/20170519-huelgaupr-tweets-april-20-may-18-2017/|
|Embeded Tweets  | JSON  | Twitter API Response |

### Data Access: Ricky Renuncia Protest and HuelgaUPRTweets(University of Puerto Rico Student Protest)

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


### Database
This project will create one database with 3 tables.
The tables and their relation are the following:

Photo of ERD Diagram for protest_database


![Photo of project protest_database](https://github.com/irmafrat/507_final_project/blob/master/readme_images/Entity%20Relationship%20Diagram%20(UML%20Notation).jpeg)



Photo of project protest database with data. I am using SQLite Browser to navigate my database.


![Photo of project protest database with data](https://github.com/irmafrat/507_final_project/blob/master/readme_images/database.png)



### Interaction and Presentation Plans

![GIF displaying program implementation](https://github.com/irmafrat/507_final_project/blob/master/readme_images/app_implementation.gif)

With this program the user will be able to search a database of tweets related to historical events in Puerto Rico.
The user will be able to fill a form setting up the dates, keywords, hashtags, and locations.
With this metadata, the user will see a table displaying the data requested,
a link of the location that the tweet is related and an embedding of the tweet;
if the tweet has been deleted the user will see a link or a warning message.

I am planning to use Flask to display the form and table.









