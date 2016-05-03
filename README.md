# report_script

- extract test cases from score board by given url

    get all status of test cases running

- read a cvs file for previous test case running status

    get all status including agent and local running result with comments

- update the current test cases status from previous csv file

    insert the old result to current case table

- export the current test cases to a csv file

    enable manually updating and comment



## how to use

- set path as old csv record

    if no such files, leave it as empty string

- set url as the url of score board which lists all suite

- generate the new csv file in your path with a "_new.csv" postfix

- check it out and use it for next day's old files