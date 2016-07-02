class News:
	def __init__(self, title, source, url, date, content = '', img = ''):
		self.title = title
		self.source = source
		self.url = url
		self.date = date
		self.content = content
		self.img = img

	def toDict(self):
		emptyDict = dict()
		emptyDict['title'] = self.title
		emptyDict['source'] = self.source
		emptyDict['url'] = self.url
		emptyDict['date'] = self.date
		emptyDict['content'] = self.content
		emptyDict['img'] = self.img
		return emptyDict