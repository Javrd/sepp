
# Table of contents
 * [Develop environment](#Develop-environment)
   * [Installing development enviroment](#Installing-development-enviroment)
     * [Ubuntu](#Ubuntu)
     * [Windows](#Windows)
   * [Installing python dependencies](#Installing-python-dependencies)
   * [Creating the database](#Creating-the-database)
   * [Populating database](#Populating-database)
   * [Runing the server](#Runing-the-server)
   * [Running automated tests](#Running-automated-tests)
 * [Pre-production environment](#Pre-production-environment)
 * [Production environment](#Production-environment)



# <a name="Develop-environment"></a>Develop environment
We use here ```python``` and ```pip```, but if you have python 2 installed in your system you may change them for ```python3``` and ```pip3```.
## <a name="Installing-development-enviroment"></a>Installing development enviroment
### <a name="Ubuntu"></a>Ubuntu
Instal dependencies:
```
sudo apt install -y python3 python3-pip mysql-server libmysqlclient-dev
```
You could also want to install mysql-workbench, so you can inspect database with an UI.
```
sudo apt install -y  mysql-workbench
```

### <a name="Windows"></a>Windows
Install [python](https://www.python.org/ftp/python/3.6.4/python-3.6.4.exe). Ensure you select "Add Python 3.6 to PATH" before selecting "Install Now" or "Customize installation". If you choose customize installation, you should select at least pip.

Install [mysql-server](https://dev.mysql.com/get/Downloads/MySQLInstaller/mysql-installer-web-community-5.7.21.0.msi). You could not want to install all the package. You need at least MySQL 5.7 and you could also want to install MySQL Workbench, so you can inspect database with an UI.

## <a name="Installing-python-dependencies"></a>Installing python dependencies
Open a terminal at repository folder:
```
pip install -r requirements.txt
```
## <a name="Creating-the-database"></a>Creating the database
```
mysql -u root -p < create_db.sql
```
You should input your mysql root password.

You could also open and run this scipt from mysql-workbench.

## <a name="Populating-database"></a>Populating database
Once database is created, you can generate tables for our model with this command:
```
python manage.py migrate
```
You also can populate it with some testing information with:
```
python populate.py
```

## <a name="Runing-the-server"></a>Runing the server
Use this command to mount localhost server. You can access at port 8000.
```
python manage.py runserver
```

## <a name="Running-automated-tests"></a>Running automated tests
Some test cases can be automated. In order to run all our test use this command:
```
python manage.py test mvp.test
```

# <a name="Pre-production-environment"></a>Pre-production-environment
We are using docker so deployed system should work in the same way as it does in local. The system has two services, the django web service and the database. We use a docker compose file with the mariadb image for the database and a dokerfile that we build for django. This dockerfile use an ubuntu image and install apache on it with mod_wsgi in order to deploy django system.

It's important change some settings of django in a production environment, so we use environment variables in docker compose to define those settings.


# <a name="Production-environment"></a>Production-environment
The deployed system is at http://artinbar.com