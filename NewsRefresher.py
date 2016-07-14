from pymongo import MongoClient
from NewsSeeker import NewsSeeker
from NewsThread import NewsThread
from queue import Queue
from apscheduler.schedulers.blocking import BlockingScheduler

URLs = {'metro': 'http://www.metronews.ca/halifax.html', 'chronicle': 'http://thechronicleherald.ca/'}
sched = BlockingScheduler()

@sched.scheduled_job('interval', hours = 0.5)
def refresh_news():
	client = MongoClient('mongodb://heroku_gfp8zr4k:mu22sv8pm9q3b5o286vfjjq870@ds015335.mlab.com:15335/heroku_gfp8zr4k')
	db = client.heroku_gfp8zr4k
	db.images.drop()
	headlines = []
	normal = []
	queue = Queue()
	for index in range(2 * len(URLs)):
		if index % 2 == 0:
			newsThread = NewsThread(queue = queue, storage = headlines, field = 'headlines')
		else:
			newsThread = NewsThread(queue = queue, storage = normal, field = 'normal')			
		newsThread.daemon = True
		newsThread.start()
	for eachKey in URLs.keys():
		url = URLs[eachKey]
		seeker = NewsSeeker(url = url, source = eachKey)
		queue.put(seeker)
		queue.put(seeker)
	queue.join()
	client.close()

@sched.scheduled_job('cron', day_of_week = 'fri', hour = 17)
def remove_news_caches():
	client = MongoClient('mongodb://heroku_gfp8zr4k:mu22sv8pm9q3b5o286vfjjq870@ds015335.mlab.com:15335/heroku_gfp8zr4k')
	db = client.heroku_gfp8zr4k
	db.details.drop()
	client.close()

@sched.scheduled_job('cron', day_of_week = 'sun-fri', hour = 22)
def remove_everything():
	client = MongoClient('mongodb://heroku_gfp8zr4k:mu22sv8pm9q3b5o286vfjjq870@ds015335.mlab.com:15335/heroku_gfp8zr4k')
	db = client.heroku_gfp8zr4k
	db.headlines.delete_many({})
	db.images.delete_many({})
	db.normal.delete_many({})

sched.start()