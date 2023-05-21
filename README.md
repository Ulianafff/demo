#demo

1) data_backup.sh:
Checks new files, archives them and moves from targetDirectory to destinationDirectory.

2) process_web_log.py:
Simple DAG, processing text file, executes every minute. 

3) automation.py:
Updates DB2 table with new records from MySQL table.

4) DataChange.py:
Changes data column from "09/03/19" format to "2019-03-09" format.

5) test_dag1.py:
Downloading, extracting needed columns from different files, aggregating and transforming data records.

6) web_scrp1.py:
Webscrapping with BeautifulSoup, extracting table to DataFrame + writing to json file