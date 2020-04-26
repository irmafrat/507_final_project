from flask import Flask
from flask import MySQL

app = Flask(__name__)


app.config['MYSQL_USER']
app.config['MYSQL_PASSWORD']
app.config['MYSQL_HOST']
app.config['MYSQL_DB']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route("/")
def index():
    cur= mysql.connection.cursor()
    cur.execute("CREATE TABLE example(id INTEGER, name VARCHAR(20))")
    return "Table created!"

