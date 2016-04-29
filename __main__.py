import gen


def main():
    # old_suites_table = readCSV('all_test.csv')
    # print(getCSVString(old_suites_table))

    url = "http://rscoreboard.mcp.com/scoreboard/scoreboard.php?filter=Parity"
    new_suite_table = gen.get_new_result(url)
    # print get_csv_string(new_suite_table)


# print(getCSVString(new_suite_table))

if __name__ == "__main__":
    main()