from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
import sqlite3
import re


wp = Client('xmlrpc WP url', 'user', 'password')
conn = sqlite3.connect('db.sqlite')


def prepare_wp():
    with conn:
        c = conn.cursor()
        d = conn.cursor()
        c.execute("SELECT title FROM article_unique")
        d.execute("SELECT text FROM article_unique")
        titles = c.fetchall()
        texts = d.fetchall()
        for t, i in zip(titles, texts):
            title = clean_title(t)
            body = clean_text(i)
            post_wp(title, body)


def post_wp(title, body):
            post = WordPressPost()
            post.title = title
            post.content = body
            post.post_status = 'publish'
            return wp.call(NewPost(post))


def clean_title(toclean):
    m = re.findall("'(.*?)\'", str(toclean))
    return ''.join([item.rstrip('\n') for item in m])


def clean_text(toclean):
    m = re.findall("'(.*?)\'", str(toclean))
    topass = ''.join([item.rstrip('\n') for item in m])
    return formater(topass)


def formater(place):
    image = "<center><a href='http://google.com/logo.png'>link</a></center>"
    places = re.sub("(\.)", nth_matcher(7, ". \n\n" + image + "\n\n"), place)
    return places


def nth_matcher(n, replacement):

        def alternate(n):
            i = 0
            while True:
                i += 1
                yield i % n == 0
        gen = alternate(n)

        def match(m):
            replace = gen.next()
            if replace:
                return replacement
            else:
                return m.group(0)
        return match

prepare_wp()
