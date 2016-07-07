from pymongo import MongoClient
from NewsSeeker import NewsSeeker
from NewsThread import NewsThread
from queue import Queue
from apscheduler.schedulers.blocking import BlockingScheduler

URLs = {'metro': 'http://www.metronews.ca/halifax.html', 'chronicle': 'http://thechronicleherald.ca/'}
sched = BlockingScheduler()

@sched.scheduled_job('interval', hours = 3)
def refresh_news():
	client = MongoClient('mongodb://heroku_gfp8zr4k:mu22sv8pm9q3b5o286vfjjq870@ds015335.mlab.com:15335/heroku_gfp8zr4k')
	db = client.heroku_gfp8zr4k
	headlines = []
	normal = []
	queue = Queue()
	for _ in range(len(URLs)):
		headlineThread = NewsThread(queue = queue, storage = headlines, filed = 'headlines')
		headlineThread.daemon = True
		headlineThread.start()

		normalThread = NewsThread(queue = queue, storage = normal, field = 'normal')
		normalThread.daemon = True
		normalThread.start()
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
	db.close()

sched.start()