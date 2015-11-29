import urllib2
import json
import csv
import sqlite3


conn = sqlite3.connect('db.sqlite')
# alchemy apikey
apikey = 'apikey'
requrltit = 'http://gateway-a.watsonplatform.net/calls/url/URLGetTitle?'
requrltex = 'http://gateway-a.watsonplatform.net/calls/url/URLGetText?'


def get_article(url):
    callapi_title = requrltit + apikey + url + '&outputMode=json'
    callapi_text = requrltex + apikey + url + '&outputMode=json'
    ans1 = json.load(urllib2.urlopen(callapi_title))
    ans2 = json.load(urllib2.urlopen(callapi_text))
    to_spin_title = ans1['title']
    to_spin_text = ans2['text']
    return connect(to_spin_title, to_spin_text)


def connect(new_title, new_article):
    with conn:
        c = conn.cursor()
        c.execute("INSERT INTO article_fresh VALUES (?, ?);", (new_title, new_article))
        return conn.commit()


with open("urls.csv", "rb") as f:
    reader = csv.reader(f)
    for text in reader:
        get_article(str(text[0]))
