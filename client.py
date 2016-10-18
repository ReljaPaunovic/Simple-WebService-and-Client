import requests
import json

var = raw_input("Please enter keywords: ")

r = requests.get("http://localhost:8080/myService/" + var)

i=0
prices = []
for book in r.json():
	# I am ignoring the fact that currencies maybe different but I do now know the conversion rates
	prices.append(float(book["Price"]))
	print(str(i) + " : " + book["Title"] + ", Book Rating :  " + str(book["Ratings"]) + ", Book Price : " + book["Price"] + book["Currency"])
	i = i + 1
if (i == 0):
	print("No results")
	exit(1)
var = raw_input("Which books do you want to buy? ")

if (var != ""):
	var = var.split()
	value = 0
	for num in var:
		value = value + prices[int(num)]
	bank = raw_input("Bank 0 or 1?")
	if(bank == "0"):
		account_number = raw_input("Please input your bank account number (NO SPACES): ")
		r = requests.get("http://localhost:8080/bankingService/" + str(value) + "/" + account_number + "/" + "IB34537456")
		print(r.text)
	if(bank == "1"):
		account_number = raw_input("Please input your bank account number (IBAN): ")
		info = {
		"amountInCents": int(value * 100),
		"card": {
			"owner": "Filip Markovic",
			"number": "4111111111111111",
			"validYear": 2020,
			"validMonth": 9,
			"csv": "(CV)Well behaved with small children"
		  },
		  "targetIBAN": account_number,
		  "transactionMessage": "Hello my darling"}
		print("Is this you? : \n" + json.dumps(info, sort_keys=True, indent=4, separators=(',', ': ')))
		
		r = requests.post("http://demo.seco.tkk.fi/ws/6/t755300bank/api/v1/transactions", data = info)
		print(r.text)
		

