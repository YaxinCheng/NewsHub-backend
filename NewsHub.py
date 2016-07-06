import os
from flask import Flask, request, make_response, abort
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
	MONGO_URI = "mongodb://***REMOVED***.mlab.com:15335/heroku_gfp8zr4k"

app.config['MONGO_URI'] = MONGO_URI
mongo = PyMongo(app)
api = Api(app)
api.representations = DEFAULT_REPRESENTATIONS



class index(Resource):
	def get(self):
		return {"Hello": "World"}

class parseAllPage(Resource):
	def get(self):
		URLs = {'metro': 'http://www.metronews.ca/halifax.html', 'chronicle': 'http://thechronicleherald.ca/'}
		headlines = mongo.db.headlines.find()
		normal = mongo.db.normal.find()
		head = []
		norm = []
		if headlines.count() > 0 and normal.count() > 0:
			for each in headlines:
				head += each['content']
			for each in normal:
				norm += each['content']
			return {'headlines': head, 'normal': norm}
		else:
			headlines = []
			normal = []
			for source in URLs.keys():
				url = URLs[source]
				crawler = NewsSeeker(url = url, source = source)
				news = crawler.process()
				headlines.append(news['headlines'])
				normal.append(news['normal'])
				mongo.db.headlines.save({'_id': source, 'content': news['headlines']})
				mongo.db.normal.save({'_id': source, 'content': news['normal']})
			result = {'headlines': headlines, 'normal': normal}
			return result

class parsePage(Resource):
	def get(self, source):
		URLs = {'metro': 'http://www.metronews.ca/halifax.html', 'chronicle': 'http://thechronicleherald.ca/'}
		if not source in URLs:
			abort(404)
		headlines = mongo.db.headlines.find({'_id': source})
		normal = mongo.db.normal.find({'_id': source})
		if headlines.count() > 0 and normal.count() > 0:
			return {'headlines': headlines[0]['content'], 'normal': normal[0]['content']}
		else:
			url = URLs[source]
			crawler = NewsSeeker(url = url, source = source)
			result = crawler.process()
			mongo.db.headlines.save({'_id': source, 'content': result['headlines']})
			mongo.db.normal.save({'_id': source, 'content': result['normal']})
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
		mongo.db.details.insert(details.toDict())
		return details.toDict()

api.add_resource(index,'/')
api.add_resource(parseNews, '/api/details')
api.add_resource(parseAllPage, '/api/news/')
api.add_resource(parsePage,'/api/news/<string:source>')
if __name__ == '__main__':
	app.run()