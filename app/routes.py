from flask import render_template, request
import json
from app import app
from app.tweet_loader import Tweet_DB, DB_NAME
from accessing_data import BASE_URL,EMBED_URL, TWEET_EMBED_CACHE
tweet_db = Tweet_DB(DB_NAME)

def get_embed(tweet_id):
    tweet_url = BASE_URL + str(tweet_id)
    params= {'url': tweet_url}
    response = TWEET_EMBED_CACHE.get(EMBED_URL,params)
    # print(response)
    # print(type(response))
    try:
        html=json.loads(response)['html']
        # print("json.loads worked")
    except:
        html=""
        # print("json.loads failed!")
    return html



@app.route('/')
def index():
    locations = tweet_db.get_user_locations()
    languages = tweet_db.get_languages()
    return render_template("form.html", locations=locations, languages=languages)


@app.route('/search/<page>/', methods=['GET'])
def search_results(page):
    page = int(page)
    # sq= request.args.get("search_query")
    # if sq == "":
    #     sq =
    print(type(request.args.get("search_query")))
    print(f"#{request.args.get('search_query')}#")
    args_str = request.url.split("?")[1]
    if request.method == 'GET':

        total_pages= tweet_db.search_pages(search_query=request.args.get("search_query"), select_project=request.args.get("project"),
                                           select_language=request.args.get("tweet_language"),select_location=request.args.get("tweet_location"))
        if page > total_pages or page < 1:
            return f"Page {page} does not exist for the given search."
        else:
            rows = tweet_db.search(search_query=request.args.get("search_query"), select_project=request.args.get("project"),
                                           select_language=request.args.get("tweet_language"),select_location=request.args.get("tweet_location"),page= page)
            return render_template("grid.html", page=page, total_pages=total_pages, rows=rows, args_str=args_str)



@app.route('/tweet/<tweet_id>')
def display_tweet(tweet_id):
    tweet_data= tweet_db.get_tweet(int(tweet_id))
    if len(tweet_data) < 1:
        return f"Tweet {tweet_id} not in database."
    else:
        tweet = tweet_data[0]
        embed_html= get_embed(tweet_id)
        print(embed_html)
        return render_template("tweet.html",tweet=tweet, embed_html=embed_html)
