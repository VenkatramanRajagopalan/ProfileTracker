import sys
import operator

#Method to read file content and return a list
def readFileContent(filePath):
	fileContent = []
	print "Processing file -> ", filePath
	f = open(filePath, 'rU')
	for line in f:
		fileContent.append(line.rstrip())

	f.close()

	return fileContent

def getValuForStock(stockName):
	return 10

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
			stockValue += (getValuForStock(stockName) * int(stockCount))
			#print "Stock Value -> ",stockValue
		
		profielHash[str(i)+"_"+profile] = stockValue
		i = i + 1
	
	return profielHash

def sortedProfile(profileMap):
	profileSorted = []
	sortedProfileList = sorted(profileMap.items(), key=operator.itemgetter(1), reverse=True)
	for item in sortedProfileList:
		name, value = item
		profileSorted.append(str(name)[str(name).index('_')+1:])
	return profileSorted

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


if __name__ == '__main__':
	main()