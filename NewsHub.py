import os
from flask import Flask, request
from flask_pymongo import PyMongo
from flask_restful import Resource, Api
from bson.json_util import dumps
from contentCrawler import contentCrawler
from NewsSeeker import NewsSeeker
import datetime

app = Flask(__name__)
MONGO_URI = os.environ.get('MONGO_URL')
if not MONGO_URI:
	MONGO_URI = "mongodb://***REMOVED***.mlab.com:15335/heroku_gfp8zr4k"

app.config['MONGO_URI'] = MONGO_URI
mongo = PyMongo(app)
api = Api(app)

class index(Resource):
	def get(self):
		return {"Hello": "World"}

class parsePage(Resource):
	def post(self):
		URLs = {'metro': 'http://www.metronews.ca/halifax.html', 'chronicle': 'http://thechronicleherald.ca/'}
		source = request.form['source']
		result = mongo.db.pages.find({'_id': source})
		if result.count() > 0:
			return dumps(result)
		url = URLs[source]
		crawler = NewsSeeker(url = url, source = source)
		return crawler.process(original = True)

class parseNews(Resource):
	def post(self):
		url = request.form['url']
		result = mongo.db.news.find({'_id': url})
		if result.count() > 0:
			return dumps(result)
		source = request.form['source']
		crawler = contentCrawler(url = url, source = source)
		details = crawler.process()
		mongo.db.news.insert(details.toDict())
		return details.toDict()

api.add_resource(index,'/')
api.add_resource(parseNews, '/api/details')
api.add_resource(parsePage, '/api/news')
if __name__ == '__main__':
	app.run()