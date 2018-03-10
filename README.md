# Art in bar develop information
We use here ```python``` and ```pip```, but if you have python 2 installed in your system you may change them for ```python3``` and ```pip3```.
## Installing development enviroment
### Ubuntu
Instal dependencies:
```
sudo apt install -y python3 python3-pip mysql-server libmysqlclient-dev
```
You could also want to install mysql-workbench, so you can inspect database with an UI.
```
sudo apt install -y  mysql-workbench
```

### Windows
Install [python](https://www.python.org/ftp/python/3.6.4/python-3.6.4.exe). Ensure you select "Add Python 3.6 to PATH" before selecting "Install Now" or "Customize installation". If you choose customize installation, you should select at least pip.

Install [mysql-server](https://dev.mysql.com/get/Downloads/MySQLInstaller/mysql-installer-web-community-5.7.21.0.msi). You could not want to install all the package. You need at least MySQL 5.7 and you could also want to install MySQL Workbench, so you can inspect database with an UI.

## Install python dependencies:
Open a terminal at repository folder:
```
pip install -r requirements.txt
```
## Creating the database
```
mysql -u root -p < create_db.sql
```
You should input your mysql root password.

You could also open and run this scipt from mysql-workbench.

## Runing the server
```
python manage.py runserver
```