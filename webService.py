import requests
from BeautifulSoup import BeautifulSoup
import xml.etree.ElementTree as ET
import json
from bottle import route, run, request

"""
Using both BeautifulSoup and ElementTree just to show how both work
"""

@route('/', method='GET')
def index():
	return "Hello there, Its nice to meet you"

@route('/bankingService/<value>/<acc1>/<acc2>', method='GET')
def sendMoney(value, acc1, acc2):
    return 'Transaction of ' + value + ' from ' + acc1 + ' to ' + acc2 + ' is sucessuful'

@route('/myService/<query>', method='GET')
def searchGoodReadsAndEbay(query):
	GoodReadsKey = "uv1J3LcJ7zGuhzCXwaCcUQ"
	searchQuery = query

	searchParameters = {'q' : searchQuery, 'key' : GoodReadsKey}

	r = requests.get("https://www.goodreads.com/search/index.xml", params = searchParameters)

	supica = BeautifulSoup(r.text)

	results = supica.findAll(["title", "average_rating"])

	bookTitles = []
	bookRatings = []
	finalResults = []
	i = 0
	iter = 0
	for res in results:
		if (i == 0):
			i = 1
			bookRatings.append(float(res.string))
		else:
			i = 0
			bookTitles.append(res.string)
			iter = iter + 1
		#finalResults.append({"Title" : bookTitles[iter], "Ratings" : bookRatings[iter]})
	n = len(bookTitles)
	i = 0
	
	#SOME PROBLEM WITH EBAY, NOT GIVING MANY RESULTS, PROBABLY BECAUSE OF SANDBOX ENVIRONMENT
	while (i <= n - 1):
		AppID = "AaltoUni-ws-SBX-3e6eb0ea5-11d466dd"
		searchQuery = bookTitles[i]
		#Books category id = 267
		searchParameters = {"OPERATION-NAME" : "findItemsAdvanced",
							"SERVICE-VERSION" : "1.0.0",
							"SECURITY-APPNAME" : AppID,
							"RESPONSE-DATA-FORMAT" : "XML",
							"keywords": searchQuery,
							"paginationInput.entriesPerPage" : "2",
							"categoryId" : "267"}
		r = requests.get("http://svcs.sandbox.ebay.com/services/search/FindingService/v1", params = searchParameters)
		root = ET.fromstring(r.text)
			
		#root[3] are items, root[i][11][0] are current Price
		for item in root[3]:
			finalResults.append({"Title" : item[1].text, "Price" : item[11][0].text, "Currency" : item[11][0].attrib["currencyId"], "Ratings" : bookRatings[i]})
		i = i + 1
	
	return json.dumps(finalResults)

if __name__ == '__main__':
	run(host='localhost', port=8080, reloader=True)