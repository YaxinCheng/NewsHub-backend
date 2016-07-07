import os
from flask import Flask, request, make_response, abort
from flask_pymongo import PyMongo
from flask_restful import Resource, Api
from bson.json_util import dumps
from contentCrawler import contentCrawler
from NewsSeeker import NewsSeeker
from queue import Queue
from NewsThread import NewsThread


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

class parseAllPage(Resource):
	def get(self):
		URLs = {'metro': 'http://www.metronews.ca/halifax.html', 'chronicle': 'http://thechronicleherald.ca/'}
		headlines = mongo.db.headlines.find()
		normal = mongo.db.normal.find()
		if headlines.count() > 0 and normal.count() > 0:
			return {'headlines': headlines, 'normal': normal}
		else:
			queue = Queue()
			headlines = []
			normal = []
			for source in URLs.keys():
				url = URLs[source]
				crawler = NewsSeeker(url = url, source = source)
				headlinesThread = NewsThread(queue = queue, storage = headlines, field = 'headlines')
				headlinesThread.daemon = True
				headlinesThread.start()
				
				normalThread = NewsThread(queue = queue, storage = normal, field = 'normal')
				normalThread.daemon = True
				normalThread.start()

				queue.put(crawler)
				queue.put(crawler)
			queue.join()
			return {'headlines': headlines, 'normal': normal}

class parsePage(Resource):
	def get(self, source):
		URLs = {'metro': 'http://www.metronews.ca/halifax.html', 'chronicle': 'http://thechronicleherald.ca/'}
		if not source in URLs:
			abort(404)
		headlines = mongo.db.headlines.find({'source': source})
		normal = mongo.db.normal.find({'source': source})
		if headlines.count() > 0 and normal.count() > 0:
			return {'headlines': headlines, 'normal': normal}
		else:
			queue = Queue()
			headlines = []
			normal = []
			url = URLs[source]
			crawler = NewsSeeker(url = url, source = source)
			headlinesThread = NewsThread(queue = queue, storage = headlines, field = 'headlines')
			headlinesThread.daemon = True
			headlinesThread.start()
			normalThread = NewsThread(queue = queue, storage = normal, field = 'normal')
			normalThread.daemon = True
			headlinesThread.start()
			queue.put(crawler)
			queue.put(crawler)
			queue.join()
			return {'headlines': headlines, 'normal': normal}
			
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