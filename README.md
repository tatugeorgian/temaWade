# temaWade

Setup: </br>
pip install -U pytest </br>
pip install requests </br>
download and install mysql shell from here : https://dev.mysql.com/downloads/shell/ </br>
in the mysql command client run: </br>
CREATE DATABASE books; </br>
USE books; </br>
CREATE TABLE books(title varchar(255), author varchar(255), isbn varchar(255), price float (20, 10)); </br>

run the api.py script and then run the tests using pytest api_test.py </br>
