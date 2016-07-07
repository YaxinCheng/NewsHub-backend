class News:
	def __init__(self, title, source, url, date = '', content = '', img = ''):
		self.title = title
		self.source = source
		self.url = url
		self.date = date
		self.content = content
		self.img = img
		# if not len(self.img) == 0:
		# 	queue = Queue()
		# 	thread = NewsImageThread(queue = queue)
		# 	thread.daemon = True
		# 	thread.start()
		# 	queue.put(self)
		# 	queue.join()

	def toDict(self):
		emptyDict = dict()
		emptyDict['title'] = self.title
		emptyDict['source'] = self.source
		emptyDict['_id'] = self.url
		emptyDict['content'] = self.content
		emptyDict['img'] = self.img
		if len(self.date) > 0:
			emptyDict['date'] = self.date
		return emptyDict

	def __str__(self):
		return 'Title: ' + self.title + '\nSource: ' + self.source + '\nURL: ' + self.url + '\nDate: ' + self.date + '\nContent: ' + self.content + '\nImg: ' + self.img