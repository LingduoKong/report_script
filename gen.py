import urllib
from bs4 import BeautifulSoup


class TestCaseSuite(object):
    """docstring for TestCaseSuite"""
    test_cases = {}
    url = None

    def __init__(self, name):
        self.name = name

    def fetch_test_cases(self):
        if len(self.test_cases) > 0 or self.url is None:
            return self.test_cases

        page = urllib.urlopen(self.url).read()
        soup = BeautifulSoup(page, 'html.parser')
        suites = soup.find_all("td", class_="even suite_name")

        sub_url = suites[0].a['href']
        sub_page = urllib.urlopen(sub_url).read()
        sub_soup = BeautifulSoup(sub_page, 'html.parser')
        tables = sub_soup.find_all("table", class_="info")

        for tr in tables[1].find_all("tr"):
            name = tr.find_all("td")[0].a.text
            print(name)
            prev_status = ''
            cur_status = tr.find_all("td")[1].span.text
            test_case = TestCase(name, prev_status, cur_status)
            self.test_cases[name] = test_case

        return self.test_cases


class TestCase(object):
    """docstring for TestCase"""
    comment = ''

    def __init__(self, name, prev_status, cur_status):
        self.name = name
        self.prev_status = prev_status
        self.cur_status = cur_status


def read_csv_file(path):
    old_csv = open(path, 'r+')
    suites_table = {}

    suite = None
    for line in old_csv:
        elements = line.split(',')
        if len(elements[0].strip()) > 0:
            name = elements[0].strip()
            suite = TestCaseSuite(name)
            suites_table[name] = suite

        case_name = elements[1]
        prev_status = elements[2]
        cur_staus = elements[3]
        case = TestCase(case_name, prev_status, cur_staus)
        if len(elements) > 4:
            case.comment = elements[4]
        suite.test_cases[case_name] = case

    old_csv.close()
    return suites_table


def get_csv_string(suites_table):
    content = ""
    for suite_name, suite in suites_table.iteritems():
        content += suite_name
        for case_name, case in suite.test_cases.iteritems():
            content += "," + case_name
            content += "," + case.prev_status
            content += "," + case.cur_status
            content += "," + case.comment
        content += "\n"
    return content


def get_new_result(url):
    response = urllib.urlopen(url)
    page = response.read()
    soup = BeautifulSoup(page, 'html.parser')
    suites = soup.find_all("td", class_="even suiteName")

    print 'there are %d suites in total', len(suites)

    new_suite_table = {}
    for suite in suites:
        suite_name = suite.a.string
        suite_obj = TestCaseSuite(suite_name)
        suite_obj.url = suite.a['href']
        suite_obj.fetch_test_cases()
        new_suite_table[suite_name] = suite_obj

    return new_suite_table

