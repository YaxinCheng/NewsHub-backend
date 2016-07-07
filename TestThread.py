from queue import Queue
from NewsSeeker import NewsSeeker
from NewsThread import NewsThread

crawler = NewsSeeker(url = 'http://www.metronews.ca/halifax.html', source = 'metro')
result = []
queue = Queue()
thread = NewsThread(queue, result, 'headlines')
thread.daemon = True
thread.start()
queue.put(crawler)
queue.join()