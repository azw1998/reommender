# Launch with
#
# gunicorn -D --threads 4 -b 0.0.0.0:5000 --access-logfile server.log --timeout 60 server:app glove.6B.300d.txt bbc

from flask import Flask, render_template
from doc2vec import *
import sys

app = Flask(__name__)

@app.route("/")
def articles():
    """Show a list of article titles"""
    article_links = [article[0] for article in articles]
    article_titles = [article[1] for article in articles]
    return render_template('articles.html', article_links=article_links, article_titles=article_titles)


@app.route("/article/<topic>/<filename>")
def article(topic,filename):
    """
    Show an article with relative path filename. Assumes the BBC structure of
    topic/filename.txt so our URLs follow that.
    """
    for article in articles:
        if article[0] == filename:
            article_paragraphs = article[2].split('\n')
            break
    # TODO make the links correct
    recommended_links = [article[0] for article in recommended(filename, articles, 5)]
    recommended_titles = [article[1] for article in recommended(filename, articles, 5)]

    return render_template('article.html', article_paragraphs=article_paragraphs,
                                               recommended_links=recommended_links,
                                               recommended_titles=recommended_titles)

# initialization
i = sys.argv.index('server:app')
glove_filename = sys.argv[i+1]
articles_dirname = sys.argv[i+2]

gloves = load_glove(glove_filename)
articles = load_articles(articles_dirname, gloves)
