import threading
from NewsSeeker import NewsSeeker
from pymongo import MongoClient
import requests
from PIL import Image
from io import BytesIO
import base64

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
					if not len(news['img']) == 0 and '.jpg' in news['img']:
						self.__generateThumbnail(url = news['img'], resolution = (500, 500))
			elif self.field == 'normal':
				result = seeker.process(headlines = False)
				self.storage += list(result)
				self.mongo.normal.delete_many({'source': seeker.source})
				for news in result:
					self.mongo.normal.insert_one(news)
					if not len(news['img']) == 0:
						self.__generateThumbnail(url = news['img'], resolution = (150, 150))
			self.queue.task_done()		

	def __generateThumbnail(self, url, resolution):
		imageURL = url
		response = requests.get(imageURL)
		imageFile = Image.open(BytesIO(response.content))
		imageFile.thumbnail(resolution)
		imageBuffer = BytesIO()
		imageFile.save(imageBuffer, format = "JPEG")
		imageString = base64.b64encode(imageBuffer.getvalue()).decode('UTF-8')
		try:
			self.mongo.images.insert_one({'_id': url, 'img': imageString})
		except DuplicateKeyError:
			pass