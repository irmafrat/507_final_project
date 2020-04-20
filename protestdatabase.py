import sqlite3

# CONECTION AND CURSOR
connection = sqlite3.connect("protest_database.sql")
crsr = connection.cursor()


#SQL COMMANDS
sql_command_1= "CREATE TABLE tweet_txt(tweet_id int PRIMARY KEY, full_text char(200), user_id int, hashtag varchar(30),place varchar(30))"
sql_command_2= "CREATE TABLE tweet_loc(tweet_id int PRIMARY KEY, place varchar(30), geo varchar(30), coordinates varchar(30),user_loc varchar(30))"
sql_command_3= "CREATE TABLE embed_tweet(tweet_id int PRIMARY KEY , validation int)"
sql_command_4= "CREATE TABLE tweet_info (tweet_id int PRIMARY KEY, user_id int,valid_tweet_id int, valid_user_id int)"
sql_command_5="CREATE TABLE geo_mapping(tweet_id int PRIMARY KEY, place varchar(30),converted_place char(30),google_api_loc varchar(30))"

#EXECUTE COMMANDS
crsr.execute(sql_command_1)
crsr.execute(sql_command_2)
crsr.execute(sql_command_3)
crsr.execute(sql_command_4)
crsr.execute(sql_command_5)



