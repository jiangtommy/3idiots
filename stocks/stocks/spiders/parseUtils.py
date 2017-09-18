import re
import time

# before covert: http://guba.eastmoney.com/news,[stockId],[postId].html
# after covert:  http://guba.eastmoney.com/news,[stockId],[postId]_1.html
def addPageForUrl(url):
	return url[:-5] + '_1' + url[-5:]

# format for url: http://guba.eastmoney.com/news,[stockId],[postId]_[pageId].html
# return an array: [stockId, postId]
def getIDSfromUrl(url):
	return re.findall(r'[,](\d+)', url)

def getTimefromText(timeText):
	print timeText
	formatTime = re.findall(r'\s(\d+-\d+-\d+\s+\d+:\d+:\d+)', timeText)[0]
	return time.mktime(time.strptime(formatTime, "%Y-%m-%d %H:%M:%S"))

