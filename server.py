# Launch with
#
# gunicorn -D --threads 4 -b 0.0.0.0:5000 --access-logfile server.log --timeout 60 server:app glove.6B.300d.txt bbc

from flask import Flask, render_template
from doc2vec import *
import sys
import pathlib

app = Flask(__name__)

def getIP():
    path = pathlib.Path(__file__).parent.resolve()
    with open(os.path.join(path, "IP.txt")) as f:
        host = f.read().strip()
        if ':' not in host:
            host += ':5000'
    return host

IP = getIP()

@app.route("/")
def articles():
    """Show a list of article titles"""
    #from: /users/anthonywang/pycharmprojects/recommender/data/bbc/topic/filename
    #tp: ip/articles/topic/filename
    global article_list, IP
    prefix = 'http://' + IP + '/article/'
    article_links = [prefix + '/'.join(article[0].split('/')[-2:]) for article in article_list]
    #print('article_list:{length1} article_links:{length2}'.format(length1 = len(article_list), length2 = len(article_links)))
    return render_template('articles.html', article_list=article_list, article_links=article_links)


@app.route("/article/<topic>/<filename>")
def article(topic,filename):
    """
    Show an article with relative path filename. Assumes the BBC structure of
    topic/filename.txt so our URLs follow that.
    """
    global article_list, IP, articles_dirname
    article = find_article(article_list, topic, filename)
    if not article:
        raise Exception('Article not found.')
    title = article[1]
    text = article[2]
    recommended_links = []
    recommended_titles = []
    prefix = 'http://' + IP + '/article/'
    #(distance, [filename, title, text, centroid])
    recommended_articles = recommended(article, article_list, 5)
    for a in recommended_articles:
        recommended_links.append(prefix + '/'.join(a[1][0].split('/')[-2:]))
        recommended_titles.append(a[1][1])

    return render_template('article.html', title=title, text=text,
                           recommended_links=recommended_links, recommended_titles=recommended_titles)

def find_article(article_list, topic, filename):
    for article in article_list:
        if article[0].endswith('/' + topic + '/' + filename):
            return article
    return None


# initialization
#if __name__ == '__main__':
i = sys.argv.index('server:app')
glove_filename = sys.argv[i+1]
articles_dirname = sys.argv[i+2]

#print(glove_filename)
#print(articles_dirname)

gloves = load_glove(glove_filename)
article_list = load_articles(articles_dirname, gloves)
#print(len(gloves))
#print(len(article_list))

#app.run('0.0.0.0')
