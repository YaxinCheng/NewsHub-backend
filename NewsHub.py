import os
from flask import Flask, request, make_response
from flask_pymongo import PyMongo
from flask_restful import Resource, Api
from bson.json_util import dumps
from contentCrawler import contentCrawler
from NewsSeeker import NewsSeeker


def output_json(obj, code, headers = None):
	resp = make_response(dumps(obj), code)
	resp.headers.extend(headers or {})
	return resp

DEFAULT_REPRESENTATIONS = {'application/json': output_json}

app = Flask(__name__)
MONGO_URI = os.environ.get('MONGO_URL')
if not MONGO_URI:
	MONGO_URI = "mongodb://heroku_gfp8zr4k:mu22sv8pm9q3b5o286vfjjq870@ds015335.mlab.com:15335/heroku_gfp8zr4k"

app.config['MONGO_URI'] = MONGO_URI
mongo = PyMongo(app)
api = Api(app)
api.representations = DEFAULT_REPRESENTATIONS



class index(Resource):
	def get(self):
		return {"Hello": "World"}

class parsePage(Resource):
	def get(self, source):
		if source == 'all':
			result = mongo.db.page.find()
		else:
			result = mongo.db.page.find({'_id': source})
		if result.count() > 0:
			return result
		URLs = {'metro': 'http://www.metronews.ca/halifax.html', 'chronicle': 'http://thechronicleherald.ca/'}
		if source != 'all':
			url = URLs[source]
			crawler = NewsSeeker(url = url, source = source)
			result = crawler.process()
			result['_id'] = source
			mongo.db.page.insert(result)
			return result
		else:
			result = []
			for each in URLs.keys():
				url = URLs[each]
				crawler = NewsSeeker(url = url, source = each)
				news = crawler.process()
				news['_id'] = each
				result.append(news)
			mongo.db.page.insert(result)
			return result

class parseNews(Resource):
	def post(self):
		url = request.form['url']
		result = mongo.db.news.find({'_id': url})
		if result.count() > 0:
			return result
		source = request.form['source']
		crawler = contentCrawler(url = url, source = source)
		details = crawler.process()
		mongo.db.news.insert(details.toDict())
		return details.toDict()

api.add_resource(index,'/')
api.add_resource(parseNews, '/api/details')
api.add_resource(parsePage,'/api/news/<string:source>')
if __name__ == '__main__':
	app.run()