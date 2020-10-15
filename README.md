# temaWade

Setup:
pip install -U pytest
pip install requests
download and install mysql shell from here : https://dev.mysql.com/downloads/shell/
in the mysql command client run:
CREATE DATABASE books;
CREATE TABLE books(title varchar(255), author varchar(255), isbn varchar(255), price float (20, 10));

run the api.py script and then run the tests using pytest api_test.py
