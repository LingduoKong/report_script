import urllib
from bs4 import BeautifulSoup

class testCaseSuite(object):
	"""docstring for testCaseSuite"""
	def __init__(self, name, url):
		self.name = name
		self.url = url

	def getAllTestCases():
		page = urllib.urlopen(self.url).read()
		soup = BeautifulSoup(page, 'html.parser')
		suites = soup.find_all("td", class_="even suite_name")

		suburl = suites[0].a['href']
		subpage = urllib.urlopen(suburl).read()
		subsoup = BeautifulSoup(subpage, 'html.parser')
		tables = subsoup.find_all("table", class_="info")

		test_cases = {}
		for tr in tables[1].find_all("tr"):
			case_name = tr.find_all("td")[0].a.text
			status = tr.find_all("td")[1].span.text
			test_cases[case_name] = status
	 	
	 	return test_cases


def getAllTestCases(url):
	page = urllib.urlopen(url).read()
	soup = BeautifulSoup(page, 'html.parser')
	suites = soup.find_all("td", class_="even suite_name")

	suburl = suites[0].a['href']
	subpage = urllib.urlopen(suburl).read()
	subsoup = BeautifulSoup(subpage, 'html.parser')
	tables = subsoup.find_all("table", class_="info")

	test_cases = {}
	for tr in tables[1].find_all("tr"):
		case_name = tr.find_all("td")[0].a.text
		status = tr.find_all("td")[1].span.text
		test_cases[case_name] = status
 	
 	return test_cases

def readCSV(path):

	pass

def writeCSV(path, final_table):
	csv = open(path, 'w')
	for suite_name_key in final_table:
	csv.write(suite_name_key)
	test_cases_dict = final_table[suite_name_key]
	for test_case_key in test_cases_dict:
		csv.write(',' + test_case_key)
		csv.write(',' + test_cases_dict[test_case_key] + '\n')
	csv.close()
	pass

def mergeTables(prev_table, final_table):

	pass



# generate table
url = "http://rscoreboard.mcp.com/scoreboard/scoreboard.php?filter=Parity"
path = 'all_cases.csv'

response = urllib.urlopen(url)

page = response.read()

soup = BeautifulSoup(page, 'html.parser')

suites = soup.find_all("td", class_="even suiteName")

final_table = {}

for suite in suites:
	suite_name = suite.a.string
	suite_test_cases = getAllTestCases(suite.a['href'])
	final_table[suite_name] = suite_test_cases

prev_table = readCSV(path)

final_table = mergeTables(prev_table, final_table)

writeCSV(path, final_table)

# csv = open('all_cases.csv', 'w')
# for suite_name_key in final_table:
# 	csv.write(suite_name_key)
# 	test_cases_dict = final_table[suite_name_key]
# 	for test_case_key in test_cases_dict:
# 		csv.write("," + test_case_key)
# 		csv.write(',' + test_cases_dict[test_case_key] + '\n')
# csv.close()


# print(final_table)

