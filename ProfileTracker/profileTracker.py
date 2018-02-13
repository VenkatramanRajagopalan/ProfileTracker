import sys
import operator
import requests
import json
import argparse

# pylint: disable=print-statement

API_KEY = 'MAD5VYK9IW353NH2'
Shares = {}

#Parses the command line arguments 
def createParser():
    parser = argparse.ArgumentParser(description="Portfolio Tracker")

    parser.add_argument(
        '-f','--fileName', type=str, required=True,help="Filename to read portfolios from"
    )

    return parser

#Method to read file content and return a list
def readFileContent(filePath):
	fileContent = []
	print "Processing file -> ", filePath
	try:
		f = open(filePath, 'rU')
		for line in f:
			fileContent.append(line.rstrip())
		f.close()
	except:
		print "file open error"

	print "Found ", len(fileContent), " profiles\n"
	return fileContent

#Get value for stock from local or from web
def getValuForStock(stockName):
	if stockName in Shares:
		return Shares[stockName]
	else:
		stockValue = getWebStockValue(stockName)
		Shares[stockName] = stockValue
		return stockValue

#Get stock value from alphavantage.com
def getWebStockValue(stockName):
	response = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol='+stockName+'&interval=15min&outputsize=compact&apikey='+API_KEY)
	try:
		res = json.loads(response.text)
		timeSeries = res["Time Series (15min)"]
		stockValue = timeSeries[operator.itemgetter(0)(timeSeries.keys())]["1. open"]
		print "stock value for "+stockName+": "+str(stockValue)
	except:
		stockValue = 10.00
		print "something went wrong in fetching stock value for "+stockName
	return float(stockValue)

#Split the profiles and find total stock value for a profile
def findStockValues(profiles):
	profielHash = {}
	i=0
	for profile in profiles:

		if ',' in profile:
			stocks = profile.split(',')
		else:
			stocks = [profile]
		
		#print "Stocks -> ",stocks
		stockValue = 0
		for stock in stocks:
			stockValuePair = stock.split('-')
			stockName, stockCount = operator.itemgetter(0,1)(stockValuePair)
			stockValue += (getValuForStock(str(stockName).strip()) * int(stockCount))
			#print "Stock Value -> ",stockValue
		
		profielHash[str(i)+"_"+profile] = stockValue
		i = i + 1
	
	return profielHash

#sort the profile base on calculated total stock value 
def sortedProfile(profileMap):
	profileSorted = []
	sortedProfileList = sorted(profileMap.items(), key=operator.itemgetter(1), reverse=True)
	for item in sortedProfileList:
		name, value = item
		profileSorted.append(str(name)[str(name).index('_')+1:])
	return profileSorted

#Main function
#Gets file path from command line argument
#Reads and prints the profiles based on total stock value
def main():
	print "\n======Portfolio Tracker======\n"
	parser = createParser()
	args = parser.parse_args()
	profileList = readFileContent(args.fileName)
	stockValueHashMap = findStockValues(profileList)

	for items in sortedProfile(stockValueHashMap): print items




if __name__ == '__main__':
	main()