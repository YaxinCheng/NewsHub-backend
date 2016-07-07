import threading
from NewsSeeker import NewsSeeker
from pymongo import MongoClient

class NewsThread(threading.Thread):
	def __init__(self, queue, storage, field):
		threading.Thread.__init__(self)
		self.queue = queue
		self.storage = storage
		self.field = field
		client = MongoClient('mongodb://***REMOVED***.mlab.com:15335/heroku_gfp8zr4k')
		self.mongo = client.heroku_gfp8zr4k

	def run(self):
		while True:
			seeker = self.queue.get()
			if self.field == 'headlines':
				result = seeker.process(normal = False)
				self.storage += list(result)
				self.mongo.headlines.delete_many({'source': seeker.source})
				for news in result:
					self.mongo.headlines.insert_one(news)
			elif self.field == 'normal':
				result = seeker.process(headlines = False)
				self.storage += list(result)
				self.mongo.normal.delete_many({'source': seeker.source})
				for news in result:
					self.mongo.normal.insert_one(news)
			self.queue.task_done()			