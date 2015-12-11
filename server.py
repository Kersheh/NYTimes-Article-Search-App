import urllib2, json
from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__, static_url_path="/static")

# index page routing
@app.route("/")
@app.route("/index.html")
def index():
  return open("static/index.html").read()

# find best available image in given articles json
def get_article_image(multimedia):
  if not multimedia:
    return "static/img/placeholder.png"
  image = ""
  subtype = ""
  for i in range(0, len(multimedia)):
    if(multimedia[i]["subtype"] == "xlarge"):
      return "http://static01.nyt.com/" + multimedia[i]["url"];
    elif(multimedia[i]["subtype"] == "wide"):
      image = "http://static01.nyt.com/" + multimedia[i]["url"]
      subtype = multimedia[i]["subtype"]
    elif(subtype != "wide"):
      image = "http://static01.nyt.com/" + multimedia[i]["url"]
  return image

# filter total character count of headline or snippet
def filter_character_count(string, type):
  if(type == "headline"):
    if(len(string) <= 120):
      return string
    else:
      return string[:120] + "..."
  if(type == "snippet"):
    if(len(string) <= 500):
      return string
    else:
      return string[:500] + "..."

# filter json from NYTimes
def filter_json(search_results):
  nyt_json = json.load(search_results)
  dict_results = {}
  for i in range(0, len(nyt_json["response"]["docs"])):
    dict_results[i] = {"headline": "", "author": "", "url": "", "date": "", "snippet": "", "img": ""}
    if(nyt_json["response"]["docs"][i]["headline"]["main"] != None):
      dict_results[i]["headline"] = filter_character_count(nyt_json["response"]["docs"][i]["headline"]["main"], "headline")
    else:
      dict_results[i]["headline"] = filter_character_count(nyt_json["response"]["docs"][i]["headline"]["name"], "headline")
    if not nyt_json["response"]["docs"][i]["byline"]:
      dict_results[i]["author"] = "Author Unavailable"
    else:
      dict_results[i]["author"] = nyt_json["response"]["docs"][i]["byline"]["original"]
    dict_results[i]["url"] = nyt_json["response"]["docs"][i]["web_url"]
    dict_results[i]["date"] = nyt_json["response"]["docs"][i]["pub_date"]
    if(nyt_json["response"]["docs"][i]["snippet"] != None):
      dict_results[i]["snippet"] = filter_character_count(nyt_json["response"]["docs"][i]["snippet"], "snippet")
    else:
      dict_results[i]["snippet"] = "Abstract Unavailable"
    dict_results[i]["img"] = get_article_image(nyt_json["response"]["docs"][i]["multimedia"])
  return json.dumps(dict_results)

# query app functionality
article_key = "API_KEY_HERE"
article_link = "http://api.nytimes.com/svc/search/v2/articlesearch.json"
article_fields = "web_url,snippet,headline,pub_date,multimedia,byline"
@app.route("/search/api/v1.0/<string:api>/<string:query>", methods=["GET"])
# filtered query by NYTimes Article API
def get_query(api, query):
  api_link = article_link + "?q=" + query + "&fl=" + article_fields + "&api-key=" + article_key
  # general article search by relevance 
  if(api == "article"):
    response = urllib2.urlopen(api_link)
  else:
    api_link = api_link + "&sort=newest"
    if(api == "world"):
      filter_query = "news_desk:(\"World\")"
    if(api == "us"):
      filter_query = "news_desk:(\"U.S.\")"
    if(api == "politics"):
      filter_query = "news_desk:(\"Politics\")"
    if(api == "business"):
      filter_query = "news_desk:(\"Business\")"
    if(api == "science"):
      filter_query = "news_desk:(\"Science\")"
    if(api == "sports"):
      filter_query = "news_desk:(\"Sports\")"
    response = urllib2.urlopen(api_link + "&fq=" + filter_query)
  result = filter_json(response)
  return result

if __name__ == "__main__":
  #app.run(host="127.0.0.1", port=5000)
  app.run()