#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    articles = Article.query.all()
    articles_list = [{
        "id": article.id,
        "title": article.title,
        "author": article.author,
        "preview": article.preview,
        "minutes_to_read": article.minutes_to_read,
        "date": article.date.isoformat()
    } for article in articles]
    return jsonify(articles_list), 200

@app.route('/articles/<int:id>')
def show_article(id):
    # Initialize session page views if not set
    session['page_views'] = session.get('page_views', 0)

    # Increment page views
    session['page_views'] += 1

    if session['page_views'] <= 3:
        article = Article.query.get(id)
        if article:
            # Ensure 'author' is included in the response if it's an attribute of Article
            return jsonify({
                "id": article.id,
                "title": article.title,
                "content": article.content,
                "author": article.author,
                "preview": article.preview,
                "minutes_to_read": article.minutes_to_read,
                "date": article.date.isoformat()
            }), 200
        else:
            return {'message': '404: Article not found.'}, 404
    else:
        return {'message': 'Maximum pageview limit reached'}, 401

if __name__ == '__main__':
    app.run(port=5555)
