import urllib.request
from bs4 import BeautifulSoup
from News import News
import re

class NewsSeeker:

	headlinePatterns = {'metro': '<div class="top-story"(.*?|\s)*?<\/div>',
						'chronicle': '<div class="text">(\s|.)*?<h2>.*?<\/h2>'}

	def __init__(self, url, source):
		self.url = url
		self.source = source

	def process(self):
		self.data = self.__webInfo()
		result = self.__headlines()
		print("Count " + str(len(result)))
		print(result[0])

	def __webInfo(self):
		return urllib.request.urlopen(self.url).read().decode('UTF-8')

	def __searchInfo(self, patternGroup):
		pattern = patternGroup[self.source]
		pattern = re.compile(pattern)
		info = re.search(pattern, self.data)
		if info is None:
			raise ValueError
		else:
			return info.group()

	def __headlines(self):
		if self.url is None or self.source is None:
			raise ValueError
		if self.source == 'metro':
			headline = self.__searchInfo(patternGroup = self.headlinePatterns)
			soup = BeautifulSoup(headline, 'html.parser')
			url = soup.a['href']
			img = soup.img['data-original']
			title = soup.h1.a.text
			subtitle = soup.h2.text.strip()
			return [News(title = title, url = url, source = self.source, content = subtitle, img = img)]
		elif self.source == 'chronicle':
			headlinePattern = re.compile(self.headlinePatterns[self.source])
			result = re.finditer(headlinePattern, self.data)
			titles = []
			for each in result:# Find all titles
				soup = BeautifulSoup(each.group(), 'html.parser')
				titles.append(soup.h2.text)
			imgs = []
			urls = []
			contents = []
			for index in range(len(titles)):
				headlineIntro = self.__processChronicleHeadline(index = index)
				soup = BeautifulSoup(headlineIntro, 'html.parser')
				imgs.append(soup.a.img['src'])
				urls.append('http://thechronicleherald.ca' + soup.a['href'])
				contents.append(soup.a.img['title'])
			headlines = []
			for index in range(len(titles)):
				headlines.append(News(title = titles[index], url = urls[index], source = self.source, content = contents[index], img = imgs[index] if len(imgs) > index else ''))
			return headlines

	def __processChronicleHeadline(self, index):
		introPattern = re.compile('<div id="tab-' + str(index) + '" class="ui-tabs-panel (ui-tabs-hide)?">(.|\s)*?<\/div>')
		return re.search(introPattern, self.data).group()

seeker = NewsSeeker('http://thechronicleherald.ca/', 'chronicle')
seeker.process()