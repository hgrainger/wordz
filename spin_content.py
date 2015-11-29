from wordai.turing import TuringWordAi as WordAi
import sqlite3
import re


wai = WordAi('email', 'password')
conn = sqlite3.connect('db.sqlite')


def spin():
    with conn:
        c = conn.cursor()
        d = conn.cursor()
        c.execute("SELECT title FROM article_fresh")
        d.execute("SELECT text FROM article_fresh")
        titles = c.fetchall()
        texts = d.fetchall()
        for i, j in zip(titles, texts):
            plaintext = clean(i)
            plainbody = clean(j)
            titleuni = wai.unique_variation(str(plaintext))
            bodyuni = wai.unique_variation(str(plainbody))
            post(titleuni, bodyuni)


def clean(toclean):
    m = re.findall("'(.*?)\'", str(toclean))
    rdy = ''.join([item.rstrip('\n') for item in m])
    return pretty(rdy)


def pretty(pret):
    m = re.findall("\D", str(pret))
    rdy = ''.join([item.rstrip('\n') for item in m])
    return rdy


def post(title, text):
    with conn:
            c = conn.cursor()
            c.execute("INSERT INTO article_unique VALUES (?, ?);", (title, text))
            return conn.commit()


spin()
