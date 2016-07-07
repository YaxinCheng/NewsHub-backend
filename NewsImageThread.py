from threading import Thread

class NewsImageThread(Thread):
	def __init__(self, queue):
		Thread.__init__(self)
		self.queue = queue

	def run(self):
		while True:
			news = self.queue.get()
			imageURL = news.img
			
