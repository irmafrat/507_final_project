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

### Data Access: Ricky Renuncia Protest and HuelgaUPRTweets(University of Puerto Rico Student Protest(2017))
The datasets were available thorough the Internet Archive and the Documenting the Now tweet catalog.
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

### Cache Implementation


