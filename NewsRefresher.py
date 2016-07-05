from pymongo import MongoClient
from NewsSeeker import NewsSeeker
from apscheduler.schedulers.blocking import BlockingScheduler

URLs = {'metro': 'http://www.metronews.ca/halifax.html', 'chronicle': 'http://thechronicleherald.ca/'}
sched = BlockingScheduler()

@sched.scheduled_job('interval', hours = 3)
def refresh_news():
	client = MongoClient('mongodb://heroku_gfp8zr4k:mu22sv8pm9q3b5o286vfjjq870@ds015335.mlab.com:15335/heroku_gfp8zr4k')
	db = client.heroku_gfp8zr4k
	headlines = []
	normal = []
	for eachKey in URLs.keys():
		url = URLs[eachKey]
		seeker = NewsSeeker(url = url, source = eachKey)
		result = seeker.process()
		headlines += result['headlines']
		normal += result['normal']
		db.headlines.delete_many({'_id': eachKey})
		db.headlines.insert_one({'_id': eachKey, 'content': headlines})
		db.normal.delete_many({'_id': eachKey})
		db.normal.insert_one({'_id': eachKey, 'content': normal})
	client.close()

@sched.scheduled_job('cron', day_of_week = 'fri', hour = 17)
def remove_news_caches():
	client = MongoClient('mongodb://heroku_gfp8zr4k:mu22sv8pm9q3b5o286vfjjq870@ds015335.mlab.com:15335/heroku_gfp8zr4k')
	db = client.heroku_gfp8zr4k
	db.details.drop()
	db.close()

sched.start()