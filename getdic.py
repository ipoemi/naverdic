# encoding: utf-8
import sys
import urllib
from sgmllib import SGMLParser

class LinkGrabber(SGMLParser):
	def __init__(self, verbose = 0):
		SGMLParser.__init__(self, verbose)
		self.data = []

	def start_a(self, attrs):
		for attr in attrs:
			if attr[0]  ==  "href":
				self.data.append(attr[1])

	def handle_data(self, data):
		pass

	def getResult(self):
		return self.data

class TextGrabber(SGMLParser):
	def __init__(self, verbose = 0):
		SGMLParser.__init__(self, verbose)
		self.data = ""

	def start_br(self, attrs):
		self.data += "\n"

	def handle_data(self, data):
		self.data += data

	def getResult(self):
		return self.data

def getDic(word):
	resultText = ""
	word = word.strip()
	word = unicode(word, 'utf-8').encode('cp949')
	address\
		= "http://endic.naver.com/small_search.nhn?kind=keyword&query="\
		+ word + "&page="
	for i in xrange(1, 4):
		html = urllib.urlopen(address+str(i))
		contents = unicode(html.read(), "cp949", "ignore").encode("utf-8")
		start = contents.find("<!-- 검색결과 -->")
		end = contents.find("<!--//검색결과-->")
		if start != -1 and end != -1:
			linkGrabber = LinkGrabber()
			linkGrabber.feed(contents[start:end])
			linkGrabber.close()
			links = linkGrabber.getResult()
			for link in links:
				if not link.startswith("http"):
					link = "http://endic.naver.com" + link
				text = unicode(\
				urllib.urlopen(link).read(), "cp949", "ignore").encode("utf-8")
				textStart = text.find("<!-- 뜻풀이-->")
				textEnd = text.find("<!-- //뜻풀이-->")
				if textStart != -1 and textEnd != -1:
					textGrabber = TextGrabber()
					textGrabber.feed(text[textStart:textEnd])
					textGrabber.close()
					resultText += textGrabber.getResult() + "\n"
	if resultText:
		return resultText
	else:
		return "not found"

if __name__ == '__main__':
	print getDic('a')
