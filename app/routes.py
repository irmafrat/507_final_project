from flask import render_template, request
from app import app
from app.tweet_loader import Tweet_DB, DB_NAME
ricky_db = Tweet_DB(DB_NAME)

@app.route('/')
def index():
    locations = ricky_db.get_user_locations()
    languages = ricky_db.get_languages()
    return render_template("form.html", locations=locations, languages=languages)


@app.route('/handle_form', methods=['POST'])
def handle_the_form():
    return render_template("response.html")
