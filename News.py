from pymongo import MongoClient

class News:
	def __init__(self, title, source, url, location, date = '', content = '', img = ''):
		self.title = title
		self.source = source
		self.url = url
		self.date = date
		self.content = content
		self.img = img
		self.location = location
		self.tag = self.__tag()

	def toDict(self):
		emptyDict = dict()
		emptyDict['title'] = self.title
		emptyDict['source'] = self.source
		emptyDict['_id'] = self.url
		emptyDict['content'] = self.content
		emptyDict['img'] = self.img
		emptyDict['location'] = self.location
		emptyDict['tag'] = self.tag
		emptyDict['liked'] = 0
		if len(self.date) > 0:
			emptyDict['date'] = self.date
		return emptyDict

	def __str__(self):
		return 'Title: ' + self.title + '\nSource: ' + self.source + '\nURL: ' + self.url + '\nDate: ' + self.date + '\nContent: ' + self.content + '\nImg: ' + self.img

	def __tag(self):
		components = self.url.split('/')
		filterWords = ['news', 'views', 'content']
		for index in range(3, len(components)):
			if not components[index] in filterWords:
				return self.__formatTag(components[index])

	def __formatTag(self, tag):
		replaceWords = {'novascotia': 'halifax', 'halifax': 'halifax', 
						'bluejays': 'sports', 'sports': 'sports',
						'artslife': 'life', 'homesnews': 'life', 'life': 'life', 
						'wheelnews': 'wheels', 'metro': 'other', 'chronicle': 'other'}
		if tag.isdigit():
			return 'other'
		if tag in replaceWords:
			return replaceWords[tag]
		return tag

	@staticmethod
	def newsFromBSON(bson):
		news = News(bson['title'], bson['source'], bson['_id'], bson['location'])
		try:
			news.tag = bson['tag']
			news.img = bson['img']
			news.content = bson['content']
			news.date = bson['date']
		except:
			pass
		return news

	@staticmethod
	def newsFromURL(url):
		client = MongoClient('mongodb://***REMOVED***.mlab.com:15335/heroku_gfp8zr4k')
		mongodb = client.heroku_gfp8zr4k
		news = mongodb.headlines.find({'_id': url})
		if news.count() > 0:
			return newsFromBSON(news[0])
		else:
			news = mongodb.normal.find({'_id': url})
			if news.count > 0:
				return newsFromBSON(news[0])
			return None