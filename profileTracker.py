import sys
import operator
import requests
import json
import unittest

API_KEY = 'MAD5VYK9IW353NH2'
Shares = {}

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
	#print stockName
	response = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol='+stockName+'&interval=15min&outputsize=compact&apikey='+API_KEY)
	#print 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol='+stockName+'&interval=15min&outputsize=compact&apikey='+API_KEY
	try:
		res = json.loads(response.text)
		timeSeries = res["Time Series (15min)"]
		stockValue = timeSeries[operator.itemgetter(0)(timeSeries.keys())]["1. open"]
		print "stock value for "+stockName+": "+str(stockValue)
	except:
		stockValue = 0.00
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
	print "\n======Profile Tracker======\n"
	if len(sys.argv) <= 1:
		print "#err: Please spicify file path"
		return
	filePath = sys.argv[1]
	profileList = readFileContent(filePath)
	print "Found ", len(profileList), " profiles\n"

	stockValueHashMap = findStockValues(profileList)

	for items in sortedProfile(stockValueHashMap): print items

class PortfolioTrackerTest(unittest.TestCase):
    
	def invalidFilePath(self):
        self.assertEqual(readFileContent('skjfnasldkfnsd'), [])


if __name__ == '__main__':
	main()