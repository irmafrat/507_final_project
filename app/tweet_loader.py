import sqlite3
from accessing_data import DB_NAME, T_TABLE, TH_TABLE, GEO_TABLE, UI_TABLE, EMBED_URL
from math import ceil as mceil

class Tweet_DB:
    def __init__(self, db_name=DB_NAME):
        self.db_name = db_name

    def search(self, search_query='', select_project='any',select_language='any',select_location='any',order_by= "", page =1, limit = 20, columns=["create_at", "user_loc", "full_text","tweet_id"]):
        if columns == []:
            col_str= "*"
        else:
            col_str= ", ".join(columns)
        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()

        and_conditional = Tweet_DB.search_conditions(search_query, select_project, select_language,select_location)

        query = f"SELECT {col_str} FROM {T_TABLE}"
        if and_conditional != "":
            query = query + f" WHERE {and_conditional}"
        if order_by in ["create_at","tweet_id", "project_id"]:
            query= query + f" ORDER BY {order_by}"
        off_set= limit * (page-1)
        query = query + f" LIMIT {off_set}, {limit}"
        print(query)
        cur.execute(query)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

    def search_conditions(search_query='', select_project='any',select_language='any',select_location='any'):
        conditional= []
        if select_project == 1:
            conditional.append("project_id= 1")
        elif select_project == 2:
            conditional.append("project_id= 2")
        if select_language != "any":
            conditional.append(f"lang = \"{select_language}\"")
        if select_location != "any":
            conditional.append(f"user_loc = \"{select_location}\"")
        if search_query.strip() != "":
            conditional.append(Tweet_DB.full_text_condition(search_query))
        and_conditional = " AND ".join(conditional)
        return and_conditional

    def search_count(self, search_query='', select_project='any',select_language='any',select_location='any'):
        query= f"SELECT COUNT(tweet_id) FROM {T_TABLE} WHERE " + Tweet_DB.search_conditions(search_query, select_project, select_language,select_location)
        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows[0][0]

    def search_pages(self, search_query='', select_project='any',select_language='any',select_location='any', limit= 20):
        total = self.search_count(search_query, select_project, select_language,select_location)
        return mceil(total/limit)

    def full_text_condition(user_input):
        words = user_input.strip().split(" ")
        conditions= []
        for word in words:
            conditions.append(f"full_text LIKE \"%{word}%\"")
        condition = " AND ".join(conditions)
        return condition


    # def project_id_condition(self):


    def get_languages(self):
        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()
        query = f"SELECT DISTINCT lang from {T_TABLE}"
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
    total= t_db.search_count("dios")
    print(total)
    print(type(total))
    # print(str(t_db.get_languages()))
    # print(str(t_db.get_user_locations()))
    # import time.sleep as sleep
    # sleep(2)
    # print (f"Prueba #1:{(t_db.search())}")
    # print (f"Prueba #2: {(t_db.search('',1))}")
    # print (f"Prueba #3: {(t_db.search('',2))}")
    print (f"Prueba #1: {(t_db.search('Lucha','all,', 'es', 'PR'))}")
    print (f"Prueba #2: {(t_db.search('Renuncia', 1, 'es', 'PR'))}")
    print (f"Prueba #3: {(t_db.search('UPRRP', 2, 'es', 'PR'))}")
    # # for loc in t_db.get_user_locations():
    #     print(loc[0])
