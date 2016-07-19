import os
from flask import Flask, request, make_response, abort, session
from flask_pymongo import PyMongo
from flask_restful import Resource, Api
from flask_login import LoginManager, login_required, login_user, logout_user
from bson.json_util import dumps
from NewsContentCrawler import NewsContentCrawler
from NewsSeeker import NewsSeeker
from queue import Queue
from NewsThread import NewsThread
import json
from User import User
import hashlib

def output_json(obj, code, headers = None):
	resp = make_response(dumps(obj), code)
	resp.headers.extend(headers or {})
	return resp

DEFAULT_REPRESENTATIONS = {'application/json': output_json}

app = Flask(__name__)

app.secret_key = '***REMOVED***'
login_manager = LoginManager()
login_manager.init_app(app)

MONGO_URI = os.environ.get('MONGO_URL')
if not MONGO_URI:
	MONGO_URI = "mongodb://***REMOVED***.mlab.com:15335/heroku_gfp8zr4k"

app.config['MONGO_URI'] = MONGO_URI
mongo = PyMongo(app)
api = Api(app)
api.representations = DEFAULT_REPRESENTATIONS

@login_manager.user_loader
def load_user(user_id):
	return User.get(user_id)

class index(Resource):
	@login_required
	def get(self):
		return {"Hello": "World"}

class parseAllPage(Resource):
	def get(self):
		URLs = {'metro': 'http://www.metronews.ca/halifax.html', 'chronicle': 'http://thechronicleherald.ca/'}
		page = 1 if not 'page' in request.headers else int(request.headers['page'])
		headlines = mongo.db.headlines.find() if page == 1 else None
		normal = mongo.db.normal.find().sort([('tag', 1)]).limit(15).skip((page - 1) * 15)
		if (headlines is None or headlines.count() > 0) and normal.count() > 0:
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
		page = 1 if not 'page' in request.headers else int(request.headers['page'])
		headlines = mongo.db.headlines.find({'source': source}) if page == 1 else None
		normal = mongo.db.normal.find({'source': source}).sort([('tag', 1)]).limit(15).skip((page - 1) * 15)
		if (headliens is None or headlines.count() > 0) and normal.count() > 0:
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
			normalThread.start()
			queue.put(crawler)
			queue.put(crawler)
			queue.join()
			return {'headlines': headlines, 'normal': normal}
			
class parseNews(Resource):
	def post(self):
		content = json.loads(json.dumps(request.get_json(force = True)))
		url = content['url']
		result = mongo.db.details.find({'_id': url})
		if result.count() > 0:
			return result[0]
		source = content['source']
		crawler = NewsContentCrawler(url = url, source = source)
		details = crawler.process()
		mongo.db.details.insert(details.toDict())
		return details.toDict()

class getThumbnail(Resource):
	def post(self):
		content = json.loads(json.dumps(request.get_json(force = True)))
		url = content['url']
		result = mongo.db.images.find({'_id': url})
		if result.count() > 0:
			return result[0]
		else:
			return {'Error': 'image not found'}

class register(Resource):
	def get(self):
		return {'Requirement': 'Hash your password before posting'}
	def post(self):
		content = json.loads(json.dumps(request.get_json(force = True)))
		email = content['email']
		password = content['password']
		registerTime = content['registerTime']
		name = content['name']
		result = User.register(email = email, name = name, password = password, registerTime = registerTime)
		if result == False:
			return {"ERROR": "The email is already registered"}
		else:
			return {'SUCCESS': 'Register Successfully'}

class login(Resource):
	def post(self):
		content = json.loads(json.dumps(request.get_json(force = True)))
		email = content['email']
		password = content['password']
		validateResult = User.validate(user_id = email, password = password)
		if validateResult is None:
			return {"ERROR": 'Email and password do not match'}
		elif validateResult == False:
			return {'ERROR': 'Email and password do not match'}
		else:
			user = User.get(email)
			login_user(user, remember = True)
			userinfo = mongo.db.Users.find({'_id': email})[0]
			userinfo['status'] = True
			userinfo['activated'] = True
			mongo.db.Users.update({'_id': email}, userinfo)
			return user.toDict()

class changePassword(Resource):
	@login_required
	def post(self):
		content = json.loads(json.dumps(request.get_json(force = True)))
		email = content['email']
		password = content['password']
		validateResult = User.validate(user_id = email, password = password)
		if validateResult is None:
			return {"ERROR": 'Email and password do not match'}
		elif validateResult == False:
			return {'ERROR': 'Email and password do not match'}
		else:
			logout_user()
			user = User.get(email)
			newPassword = content['newpassword']
			time = content['time']
			user.changePassword(newpassword = newpassword, time = time)
			return {'SUCCESS': 'Password changed'}

api.add_resource(index,'/')
api.add_resource(parseNews, '/api/details')
api.add_resource(parseAllPage, '/api/news/')
api.add_resource(parsePage,'/api/news/<string:source>')
api.add_resource(getThumbnail, '/api/thumbnails')
api.add_resource(register, '/register')
api.add_resource(login, '/login')
api.add_resource(changePassword, '/uManage/password')

if __name__ == '__main__':
	app.run()
