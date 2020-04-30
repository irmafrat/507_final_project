from flask import render_template, request
from app import app
from app.tweet_loader import Tweet_DB, DB_NAME
tweet_db = Tweet_DB(DB_NAME)


@app.route('/')
def index():
    locations = tweet_db.get_user_locations()
    languages = tweet_db.get_languages()
    return render_template("form.html", locations=locations, languages=languages)


# @app.route('/handle_form', methods=['POST'])
# def handle_the_form():
#     return render_template("response.html")


@app.route('/search/<page>/', methods=['GET'])
def search_results(page):
    page = int(page)
    if request.method == 'GET':

        total_pages= tweet_db.search_pages(search_query=request.args.get("search_query"), select_project=request.args.get("project"),
                                           select_language=request.args.get("tweet_language"),select_location=request.args.get("tweet_location"))
        if page > total_pages or page < 1:
            return f"Page {page} does not exist for the given search."
        else:
            rows = tweet_db.search(search_query=request.args.get("search_query"), select_project=request.args.get("project"),
                                           select_language=request.args.get("tweet_language"),select_location=request.args.get("tweet_location"),page= page)
            return render_template("grid.html", page=page, total_pages=total_pages, rows=rows)





# EXAMPLE CODE TO MANAGE REQUEST/POST FROM THE USER
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
