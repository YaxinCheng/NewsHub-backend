class Comment:
	def __init__(self, ID, name, content, time):
		self.ID = ID
		self.name = name
		self.content = content
		self.time = time

	def toDict(self):
		emptyDict = dict()
		emptyDict['ID'] = self.ID
		emptyDict['name'] = self.name
		emptyDict['content'] = self.content
		emptyDict['time'] = self.time
		return emptyDict