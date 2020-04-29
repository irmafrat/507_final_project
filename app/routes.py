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

#EXAMPLE CODE TO MANAGE REQUEST/POST FROM THE USER
# @app.route('/success/<name>')
# def success(name):
#    return 'welcome %s' % name
#
# @app.route('/login',methods = ['POST', 'GET'])
# def login():
#    if request.method == 'POST':
#       user = request.form['nm']
#       return redirect(url_for('success',name = user))
#    else:
#       user = request.args.get('nm')
#       return redirect(url_for('success',name = user))
