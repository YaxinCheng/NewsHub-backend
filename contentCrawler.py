import urllib.request
import bs4
from bs4 import BeautifulSoup
import re
from News import News

class contentCrawler:
	contentPatterns = {'metro': '<div class="body parsys">(.*?|\s)*?<\/div>\s<\/div>',
						'chronicle': '<div class="article-related-content-wrapper"><\/div>(.|\s)*?<\/div>'}
	titlePatterns = {'metro':'<div class="body parsys">(.*?|\s)*?<\/p>\s<\/div>', 'chronicle': '<h1 property="dc:title">.*<\/h1>'}
	imgPatterns = {'metro': '<img src=".*?" alt=".*?" \/>\s*?<div class="caption">', 'chronicle': '<div class="main-image">\s*?<img src=".*?"'}
	datePatterns = {'metro': '<meta property="article:published" itemprop="datePublished" content=".*?" \/>', 'chronicle': '<\/font>.*?<br \/>'}

	def __init__(self, url, source):
		self.url = url
		self.source = source

	def process(self, content = True, img = True):
		self.data = self.__webInfo()
		title = self.__title()
		date = self.__date()
		news = News(title = title, source = self.source, url = self.url, date = date)
		if content == True:
			news.content = self.__content()
		if img == True:
			news.img = self.__image()

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

	def __content(self):
		if self.url is None or self.source is None:
			raise ValueError
		content = self.__searchInfo(patternGroup = contentCrawler.contentPatterns)
		soup = BeautifulSoup(content, 'html.parser')
		result = ''
		if self.source == 'metro':
			index = 2 # 0 is for title, and the content is only in the even indeces
			while index < len(soup.div.contents):
				result += soup.div.contents[index].p.text + '\n'
				index += 2
		elif self.source == 'chronicle':
			index = 1
			while index < len(soup.contents):
				try:
					result += soup.contents[index].string + '\n'
				except TypeError:
					for each in soup.contents[index].contents:
						if type(each) is bs4.element.NavigableString:
							result += each
						else:
							result += each.string
				index += 2
		return result

	def __title(self):
		if self.url is None or self.source is None:
			raise ValueError
		title = self.__searchInfo(patternGroup = contentCrawler.titlePatterns)
		soup = BeautifulSoup(title, 'html.parser')
		if self.source == 'metro':
			return soup.div.div.p.text
		elif self.source == 'chronicle':
			return soup.h1.text

	def __image(self):
		if self.url is None or self.source is None:
			raise ValueError
		img = self.__searchInfo(patternGroup = contentCrawler.imgPatterns)
		if self.source == 'metro':
			soup = BeautifulSoup(img, 'html.parser')
			return soup.img['src']
		elif self.source == 'chronicle':
			return img.split('src=')[1].strip('"')

	def __date(self):
		if self.url is None or self.source is None:
			raise ValueError
		date = self.__searchInfo(patternGroup = contentCrawler.datePatterns)
		if self.source == 'metro':
			soup = BeautifulSoup(date, 'html.parser')
			return soup.meta['content']
		elif self.source == 'chronicle':
			return date.split('</font>')[1].split('<br />')[0].strip()