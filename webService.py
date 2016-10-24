import requests
from BeautifulSoup import BeautifulSoup
import xml.etree.ElementTree as ET
import json
from bottle import route, run, request

@route('/', method='GET')
def index():
	return "Hello there, Its nice to meet you"

@route('/bankingService/<value>/<acc1>/<acc2>', method='GET')
def sendMoney(value, acc1, acc2):
    return 'Transaction of ' + value + ' from ' + acc1 + ' to ' + acc2 + ' is sucessuful'

@route('/myService/<query>', method='GET')
def searchGoodReadsAndEbay(query):
	print("Hello There")
	GoodReadsKey = "uv1J3LcJ7zGuhzCXwaCcUQ"
	searchQuery = query

	searchParameters = {'q' : searchQuery, 'key' : GoodReadsKey}

	r = requests.get("https://www.goodreads.com/search/index.xml", params = searchParameters)

	root = ET.fromstring(r.text.encode("utf8"))
	
	bookRatings = []
	bookId = []
	bookISBN = []
	#item[8][0] = book_id, item[7] = average_rating, always in that order
	for item in root[1][6]:
		bookId.append(float(item[8][0].text))
		bookRatings.append(item[7].text)

	#root[1][2] = ISBN of book
	for id in bookId:
		searchParameters = {'key': GoodReadsKey, 'id' : id}
		r = requests.get("https://www.goodreads.com/book/show", params = searchParameters)
		
		root = ET.fromstring(r.text.encode('utf8'))
		isbn = root[1][2].text
		if (isbn != None):
			bookISBN.append(isbn)
		
	
	finalResults = []
	i = 0
	iter = 0
	
	n = len(bookISBN)
	i = 0
	#url="http://svcs.sandbox.ebay.com/services/search/FindingService/v1" -- Sanbox doesnt give me much
	url = "http://svcs.ebay.com/services/search/FindingService/v1"
	AppID = "AaltoUni-ws-PRD-6e6e6803e-27f37b0f"
	headers = {
					'X-EBAY-SOA-SERVICE-NAME': 'FindingService',
					'X-EBAY-SOA-OPERATION-NAME': 'findItemsByProduct',
					'X-EBAY-SOA-SERVICE-VERSION': '1.0.0',
					'X-EBAY-SOA-GLOBAL-ID': 'EBAY-US',
					'X-EBAY-SOA-SECURITY-APPNAME': AppID,
					'X-EBAY-SOA-REQUEST-DATA-FORMAT': 'XML',
					'X-EBAY-SOA-MESSAGE-PROTOCOL': 'SOAP12',
					'CONTENT-TYPE' : 'application/soap+xml'
		}
	
	while (i <= n - 1):
		isbn = bookISBN[i]
		print(isbn)
		body = """
				<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns="http://www.ebay.com/marketplace/search/v1/services">
				   <soap:Header/>
				   <soap:Body>
					  <findItemsByProductRequest>
						 <productId type="ISBN">{0}</productId>
					  </findItemsByProductRequest>
				   </soap:Body>
				</soap:Envelope>
				""".format(isbn)
				
		response = requests.post(url,data=body,headers=headers)
		root = ET.fromstring(response.text.encode('utf8'))
		#root[3] are items, root[i][11][0] are current Price
		for item in root[1][0][3].getchildren():
			for subItem in item.getchildren():
				if(subItem.tag == '{http://www.ebay.com/marketplace/search/v1/services}sellingStatus'):
					currency = subItem[0].attrib["currencyId"]
					price = subItem[0].text
			finalResults.append({"Title" : item[1].text, "Price" : price, "Currency" : currency, "Ratings" : bookRatings[i]})

		i = i + 1
	return json.dumps(finalResults)

if __name__ == '__main__':
	run(host='localhost', port=8080, reloader=True)