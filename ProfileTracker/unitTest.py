import unittest
from profileTracker import readFileContent, createParser, sortedProfile, getWebStockValue

class PortfolioTrackerTest(unittest.TestCase):

    def setUp(self):
        parser = createParser()
        self.parser = parser

    def testInvalidFilepath(self):
		self.assertEqual(readFileContent('skjfnasldkfnsd'), [])

    def testInvalidArgument(self):
        with self.assertRaises(SystemExit):
            self.parser.parse_args([])

    def testValidArgument(self):
        args = self.parser.parse_args(['-f','./profiles.txt'])
        result = readFileContent(args.fileName)
        expected = ['MS - 10, GOOG - 10', 'GOOG - 50, MS - 100']
        self.assertEqual(result, expected)

    def testSortedResult(self):
        sortList = sortedProfile({'0_MS - 10, GOOG - 10':100,'1_GOOG - 50, MS - 100':200,'2_GOOG - 40, MS - 100':150})
        self.assertEqual(sortList, ['GOOG - 50, MS - 100','GOOG - 40, MS - 100','MS - 10, GOOG - 10'])

    def testWebValueStock(self):
        stockValue = getWebStockValue('MS')
        self.assertEqual(stockValue, 53.0200)

if __name__ == '__main__':
    unittest.main()