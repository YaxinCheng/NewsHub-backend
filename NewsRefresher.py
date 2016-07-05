from pymongo import MongoClient
from NewsSeeker import NewsSeeker
from apscheduler.schedulers.blocking import BlockingScheduler

URLs = {'metro': 'http://www.metronews.ca/halifax.html', 'chronicle': 'http://thechronicleherald.ca/'}
sched = BlockingScheduler()

@sched.scheduled_job('interval', hours = 3)
def refresh_news():
	client = MongoClient('mongodb://***REMOVED***.mlab.com:15335/heroku_gfp8zr4k')
	db = client.heroku_gfp8zr4k
	for eachKey in URLs.keys():
		url = URLs[eachKey]
		seeker = NewsSeeker(url = url, source = eachKey)
		result = seeker.process()
		headlines = result['headlines']
		normal = result['normal']
		headlines = [ eachNews for eachNews in headlines ]
		normal = [ eachNews for eachNews in normal ]
		if len(headlines) > 0:
			if db.headlines.find({'_id': eachKey}).count() > 0:
				db.headlines.delete_many({'_id': eachKey})
			db.headlines.insert_one({eachKey: headlines})
		if len(normal) > 0:
			if db.normal.find({'_id': eachKey}).count() > 0:
				db.normal.delete_many({'_id': eachKey})
			db.normal.insert_one({eachKey: headlines})
	client.close()

@sched.scheduled_job('cron', day_of_week = 'fri', hour = 17)
def remove_news_caches():
	client = MongoClient('mongodb://***REMOVED***.mlab.com:15335/heroku_gfp8zr4k')
	db = client.heroku_gfp8zr4k
	db.news.drop()
	db.close()

sched.start()