"""
File: README
Version: 1.0
Author: Surender Kumar
Copyright @ *****
Contact: kumarsu44@gmail.com

Prerequisite to run this Flickr Crawler
---------------------------------------
- Python configured
- Active MySQL Server configured
- Functioning internet connection
- The 'cryptography' package

Steps to Configure DB and Run
-----------------------------
- To change the default SQL credentials (i.e. the SQL hostname, username and
  the DB), refer 'SQLDB.py' file, and to change the DB password, refer
  'EncDec.py' file. Just search for 'DB_PASSWD'.

- To run, just use the Python interpreter
	python FlickrCrawler.py

- To rerun, you need to manually cleanup the created DB. However, this could
  have been done automatically.

- To see the log, tail the following file.
	tail -f log.txt

- Results can be seen into the the MySQL database (default DB: 'SKFlickrDB').
"""
