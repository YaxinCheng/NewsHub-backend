from pymongo import MongoClient
import hashlib

def bsonToUser(bson):
		return User(email = bson['_id'], name = bson['name'], is_authenticated = bson['status'], is_active = bson['activated'])

class User:
	def __init__(self, email, name, is_authenticated, is_active = True):
		self.email = email
		self.name = name
		self.is_authenticated = is_authenticated
		self.is_active = is_active
		self.is_anonymous = False

	def get_id(self):
		return self.email

	def toDict(self):
		emptyDict = dict()
		emptyDict['_id'] = self.email
		emptyDict['name'] = self.name
		emptyDict['status'] = self.is_authenticated
		emptyDict['activated'] = self.is_active
		return emptyDict
		
	@staticmethod
	def register(email, name, password, registerTime):
		client = MongoClient('mongodb://heroku_gfp8zr4k:mu22sv8pm9q3b5o286vfjjq870@ds015335.mlab.com:15335/heroku_gfp8zr4k')
		mongodb = client.heroku_gfp8zr4k
		result = mongodb.Users.find({'_id': email})
		if result.count() > 0:
			client.close()
			return False
		else:
			user = User(email = email, name = name, is_authenticated = False, is_active = False)
			userDict = user.toDict()
			passwordHash = hashlib.sha256()
			passwordHash.update((email + registerTime + password).encode('UTF-8'))
			password = passwordHash.hexdigest()
			userDict['password'] = password
			userDict['registerTime'] = registerTime
			mongodb.Users.insert_one(userDict)
			client.close()
			return True

	@staticmethod
	def get(user_id):
		client = MongoClient('mongodb://heroku_gfp8zr4k:mu22sv8pm9q3b5o286vfjjq870@ds015335.mlab.com:15335/heroku_gfp8zr4k')
		mongodb = client.heroku_gfp8zr4k
		result = mongodb.Users.find({'_id': user_id})
		client.close()
		if result.count() > 0:
			return bsonToUser(bson = result[0])

	@staticmethod
	def validate(user_id, password):
		client = MongoClient('mongodb://heroku_gfp8zr4k:mu22sv8pm9q3b5o286vfjjq870@ds015335.mlab.com:15335/heroku_gfp8zr4k')
		mongodb = client.heroku_gfp8zr4k
		result = mongodb.Users.find({'_id': user_id})
		client.close()
		if result.count() > 0:
			bson = result[0]
			ID = bson['_id']
			Pw = bson['password']
			registerTime = bson['registerTime']
			passwordHash = hashlib.sha256()
			passwordHash.update((ID + registerTime + password).encode('UTF-8'))
			return ID == user_id and Pw == passwordHash.hexdigest()
		else:
			return None
