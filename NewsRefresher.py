from pymongo import MongoClient
from NewsSeeker import NewsSeeker
from apscheduler.schedulers.blocking import BlockingScheduler

URLs = {'metro': 'http://www.metronews.ca/halifax.html', 'chronicle': 'http://thechronicleherald.ca/'}
sched = BlockingScheduler()

@sched.scheduled_job('interval', hours = 3)
def refresh_news():
	client = MongoClient('mongodb://heroku_gfp8zr4k:mu22sv8pm9q3b5o286vfjjq870@ds015335.mlab.com:15335/heroku_gfp8zr4k')
	db = client.heroku_gfp8zr4k
	for eachKey in URLs.keys():
		url = URLs[eachKey]
		seeker = NewsSeeker(url = url, source = eachKey)
		result = seeker.process()
		result['_id'] = eachKey
		db.page.insert_one(result)
	client.close()

@sched.scheduled_job('cron', day_of_week = 'fri', hour = 17)
def remove_news_caches():
	client = MongoClient('mongodb://heroku_gfp8zr4k:mu22sv8pm9q3b5o286vfjjq870@ds015335.mlab.com:15335/heroku_gfp8zr4k')
	db = client.heroku_gfp8zr4k
	db.news.drop()
	db.close()

sched.start()