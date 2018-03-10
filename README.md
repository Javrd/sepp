# Art in bar develop information
## Installing development enviroment
### Ubuntu
Instal dependencies:
```
sudo apt install -y python3 python3-pip mysql-server libmysqlclient-dev
pip3 install -r requirements.txt
```
You could also want to install mysql-workbench, so you can inspect database with an UI.
```
sudo apt install -y  mysql-workbench
```

### Windows

## Creating the database
```
mysql -u root -p < create_db.sql
```
You should input your mysql root password.

## Runing the server
```
python3 manage.py runserver
```