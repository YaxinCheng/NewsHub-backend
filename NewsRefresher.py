from pymongo import MongoClient
from NewsSeeker import NewsSeeker
from NewsThread import NewsThread
from queue import Queue
from apscheduler.schedulers.blocking import BlockingScheduler

URLs = ['http://www.metronews.ca/halifax.html',
	'http://www.metronews.ca/calgary.html', 
	'http://www.metronews.ca/edmonton.html', 
	'http://www.metronews.ca/winnipeg.html',
	'http://www.metronews.ca/ottawa.html',
	'http://www.metronews.ca/toronto.html',
	'http://www.metronews.ca/vancouver.html', 
	'http://thechronicleherald.ca/']
sched = BlockingScheduler()

@sched.scheduled_job('interval', hours = 2)
def refresh_news():
	client = MongoClient('mongodb://***REMOVED***.mlab.com:15335/heroku_gfp8zr4k')
	db = client.heroku_gfp8zr4k
	db.images.drop()
	headlines = []
	normal = []
	queues = []
	for index in range(2 * len(URLs)):
		queue = Queue()
		if index % 2 == 0:
			newsThread = NewsThread(queue = queue, storage = headlines, field = 'headlines')
		else:
			newsThread = NewsThread(queue = queue, storage = normal, field = 'normal')
		newsThread.daemon = True
		newsThread.start()
		url = URLs[int(index / 2)]
		source = 'metro' if 'metro' in url else 'chronicle'
		seeker = NewsSeeker(url = url, source = source)
		queue.put(seeker)
		queues.append(queue)
	for queue in queues:
		queue.join()
	client.close()

@sched.scheduled_job('cron', day_of_week = 'fri', hour = 17)
def remove_news_caches():
	client = MongoClient('mongodb://***REMOVED***.mlab.com:15335/heroku_gfp8zr4k')
	db = client.heroku_gfp8zr4k
	db.details.drop()
	client.close()

sched.start()