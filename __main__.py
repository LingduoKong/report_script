import gen


def main():

    path = 'all_new_test.csv'
    url = "http://rscoreboard.mcp.com/scoreboard/scoreboard.php?filter=Parity"

    old_suite_table = gen.read_csv_file(path)
    new_suite_table = gen.get_new_result(url)

    gen.update_new_result(new_suite_table, old_suite_table)

    csv_content = gen.get_csv_string(new_suite_table)

    f = open(path + "_new.csv", 'w')
    f.write(csv_content)
    f.close()


if __name__ == "__main__":
    main()

