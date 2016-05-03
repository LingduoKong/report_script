import urllib
from bs4 import BeautifulSoup


class TestCaseSuite(object):
    """docstring for TestCaseSuite"""

    def __init__(self, name):
        self.name = name
        self.test_cases = {}
        self.url = None

    def fetch_test_cases(self):

        page = urllib.urlopen(self.url).read()
        soup = BeautifulSoup(page, 'html.parser')
        suites = soup.find_all("td", class_="even suite_name")

        sub_url = suites[0].a['href']
        sub_page = urllib.urlopen(sub_url).read()
        sub_soup = BeautifulSoup(sub_page, 'html.parser')
        tables = sub_soup.find_all("table", class_="info")

        if tables is None or len(tables) < 2:
            return self.test_cases

        for tr in tables[1].find_all("tr"):
            name = tr.find_all("td")[0].a.text
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

    if path is None or len(path) == 0:
        return {}

    old_csv = open(path, 'r+')
    suites_table = {}

    suite = None
    for line in old_csv:
        elements = line.split(',')

        if len(elements[0].strip()) > 0:
            name = elements[0].strip()
            suite = TestCaseSuite(name)
            suites_table[name] = suite
        else:
            if len(elements) > 1:
                case_name = elements[1]

            if len(elements) > 2:
                prev_status = elements[2]

            if len(elements) > 3:
                cur_status = elements[3]

            if len(elements) > 4:
                case.comment = elements[4]

            case = TestCase(case_name, prev_status, cur_status)
            suite.test_cases[case_name] = case

    old_csv.close()
    return suites_table


def get_csv_string(suites_table):
    content = ""
    for suite_name, suite in suites_table.iteritems():
        content += suite_name.strip() + '\n'
        for case_name, case in suite.test_cases.iteritems():
            content += "," + case_name.strip()
            content += "," + case.prev_status.strip()
            content += "," + case.cur_status.strip()
            content += "," + case.comment.strip()
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


def update_new_result(new_suite_table, old_suite_table):

    for name, old_suite in old_suite_table.iteritems():
        if name not in new_suite_table:
            new_suite_table[name] = old_suite
        else:
            new_suite = new_suite_table[name]
            for case_name, case in old_suite.test_cases.iteritems():
                if case_name not in new_suite.test_cases:
                    new_suite.test_cases[case_name] = case
                else:
                    if case.prev_status.strip().upper() == "PASS" or case.cur_status.strip().upper() == "PASS":
                        new_suite.test_cases[case_name].prev_status = "PASS"
                    else:
                        new_suite.test_cases[case_name].prev_status = case.cur_status

    return

