import sqlite3
from accessing_data import DB_NAME, T_TABLE, TH_TABLE, GEO_TABLE, UI_TABLE, EMBED_URL

class Tweet_DB:
    def __init__(self, db_name=DB_NAME):
        self.db_name = db_name

    def search(self):

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
    print(str(t_db.get_languages()))
    print(str(t_db.get_user_locations()))
    # for loc in t_db.get_user_locations():
    #     print(loc[0])
