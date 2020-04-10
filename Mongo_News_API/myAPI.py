import json

import pymongo
from bson import json_util
from bson.objectid import ObjectId
from flask import Flask, jsonify, make_response, abort, request
from datetime import datetime

app = Flask(__name__)
app.config.from_pyfile('../isentia_scrapy/settings.py')
collection = 'g_news'

client = pymongo.MongoClient(app.config['MONGODB_URI'], ssl_ca_certs="../isentia_scrapy/servercert.crt")
db = client[app.config['MONGODB_DATABASE']]


@app.route('/guardian_news/api/v1.0/articles/<string:maxCount>', methods=['GET'])
def get_articles(maxCount):
    """Retrieves all articles in the collection
    """
    # query all the articles
    if maxCount is None:
        maxCount = 10  # by default fetch any 10 articles
    cur = db[collection].find().limit(maxCount)
    if not cur:
        abort(400)
    # iterate the cursor and add docs to a dict
    articles = [article for article in cur]
    return jsonify({'articles': json.dumps(articles, default=json_util.default)})

@app.route('/guardian_news/api/v1.0/get_recent_articles/<string:maxCount>', methods=['GET'])
def get_recent_articles(maxCount):
    """Retrieves articles in the collection
    """
    # query all the articles sort by date
    if maxCount is None:
        maxCount = 10  # by default fetch any 10 articles
    cur = db[collection].find().sort('scrape_date').limit(maxCount)
    if not cur:
        abort(400)
    # iterate the cursor and add docs to a dict
    articles = [article for article in cur]
    return jsonify({'articles': json.dumps(articles, default=json_util.default)})


@app.route('/guardian_news/api/v1.0/article_by_id/<string:article_id>', methods=['GET'])
def get_article(article_id):
    """
    Retrieves a specific article by article_id
    http://127.0.0.1:5000/guardian_news/api/v1.0/get_article_with/58f37230e9bc0d0ddc533a4e
    """
    # query for specified article by _id
    article = db[collection].find_one(
        {'_id': ObjectId(str(article_id))
         })
    if not article:
        abort(404)
    return jsonify({'article': json.dumps(article, default=json_util.default)})


@app.route('/guardian_news/api/v1.0/get_article_with/<string:keyword>', methods=['GET'])
def get_article_with(keyword):
    """
    Retrieves article(s) url by searching for a keyword in headline
    Example: http://127.0.0.1:5000/guardian_news/api/v1.0/get_article_with/trump
    """
    article = db[collection].find_one(
        {'headline': {'$regex': keyword, '$options': 'i'}  # employ case insensitivity
         })
    if not article:
        abort(404)
    return jsonify({'url': json.dumps(article['url'], default=json_util.default)})

@app.route('/guardian_news/api/v1.0/get_article_about/<string:keyword>', methods=['GET'])
def get_article_about(keyword):
    """
    Retrieves article(s) url by searching 'article_about' field
    Example: http://127.0.0.1:5000/guardian_news/api/v1.0/get_article_about/india
    """
    article = db[collection].find_one(
        {'article_about': {'$regex': keyword, '$options': 'i'}  # employ case insensitivity
         })
    if not article:
        abort(404)
    return jsonify({'url': json.dumps(article['url'], default=json_util.default)})


@app.route('/guardian_news/api/v1.0/articles', methods=['POST'])
# @auth.login_required
def create_article():
    """ Add new article
    """
    article_json = request.get_json()
    if not article_json:
        abort(400)
    article = {
        'text': article_json['text'],
        'scrape_date': datetime.now(),
        'article_about': article_json['article_about'],
        'author': article_json['author'],
        'comment_count': article_json['comment_count'],
        'url': article_json['url']
    }
    # insert the article dict into the g_news collection
    res = db[collection].insert(article)
    if not res:
        abort(400)
    return jsonify({'article': json.dumps(article, default=json_util.default)}), 201


@app.errorhandler(404)
def not_found(error):
    """A 404 response will be returned
    when a resource cannot be found
    """
    return make_response(jsonify({'error': 'Document not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)
