import sqlite3
from accessing_data import DB_NAME, T_TABLE, TH_TABLE, GEO_TABLE, UI_TABLE, EMBED_URL

class Tweet_DB:
    def __init__(self, db_name=DB_NAME):
        self.db_name = db_name

    def search(self, select_project,select_language,select_location,search_query, order_by= "", page =1, limit = 20):
        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()
        conditional= []
        if select_project == "all":
            query = f"SELECT * from {T_TABLE}"
        elif select_project == 1:
            conditional.append("project_id= 1")
        elif select_project == 2:
            conditional.append("project_id= 2")
        if select_language != "Any":
            conditional.append(f"lang = \"{select_language}\"")
        if select_location != "Any":
            conditional.append(f"user_loc = \"{select_location}\"")
        if search_query.strip() != " ":
            conditional.append(Tweet_DB.full_text_condition(search_query))
        and_conditional = " AND ".join("conditional")

        query = f"SELECT * FROM {T_TABLE}"
        if and_conditional != "":
            query = query + f" WHERE {and_conditional}"
        if order_by in ["create_at","tweet_id", "project_id"]:
            query= query + f" ORDER BY {order_by}"
        off_set= limit * (page-1)
        query = query + f" LIMIT {off_set}, {limit}"
        cur.execute(query)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

    def full_text_condition(user_input):
        words = user_input.strip().split(" ")
        conditions= []
        for word in words:
            conditions.append(f"full_text=\"%{word}%\"")
        condition = " AND ".join("conditions")
        return condition


    # def project_id_condition(self):


    def get_languages(self):
        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()
        query = f"SELECT DISTINCT language from {T_TABLE}"
        cur.execute(query)
        tmp_rows = cur.fetchall()
        cur.close()
        conn.close()
        rows=[]
        for loc in tmp_rows:
            rows.append(loc[0])
        rows.sort()
        return tuple(rows)

    def get_user_locations(self):
        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()
        query = f"SELECT DISTINCT user_loc from {T_TABLE}"
        cur.execute(query)
        tmp_rows = cur.fetchall()
        cur.close()
        conn.close()
        rows=[]
        for loc in tmp_rows:
            rows.append(loc[0])
        rows.sort()
        return tuple(rows)



if __name__=="__main__":
    print("Testing tweet_loader.py")
    t_db = Tweet_DB(DB_NAME)
    # print(str(t_db.get_languages()))
    # print(str(t_db.get_user_locations()))
    # import time.sleep as sleep
    # sleep(2)
    # print (f"Prueba #1:{(t_db.search('all'))}")
    # print (f"Prueba #2: {(t_db.search(1))}")
    # print (f"Prueba #3: {(t_db.search(2))}")
    print (f"Prueba #1: {(t_db.search('all', 'es', 'PR','lucha'))}")
    print (f"Prueba #2: {(t_db.search(1, 'en', 'PR', 'lucha'))}")
    print (f"Prueba #3: {(t_db.search(2, 'es', 'PR', 'lucha'))}")
    # for loc in t_db.get_user_locations():
    #     print(loc[0])
