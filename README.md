
# Table of contents
 * [Develop environment](#Develop-environment)
   * [Installing development enviroment](#Installing-development-enviroment)
     * [Ubuntu](#Ubuntu)
     * [Windows](#Windows)
   * [Installing redis](#Installing-redis)
     * [Option 1: Docker](#Option-1)
     * [Option 2: Bare metal](#Option-2)
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

```bash
sudo apt install -y python3 python3-pip mysql-server libmysqlclient-dev
```

You could also want to install mysql-workbench, so you can inspect database with an UI.

```bash
sudo apt install -y  mysql-workbench
```

### <a name="Windows"></a>Windows

Install [python](https://www.python.org/ftp/python/3.6.4/python-3.6.4.exe). Ensure you select "Add Python 3.6 to PATH" before selecting "Install Now" or "Customize installation". If you choose customize installation, you should select at least pip.

Install [mysql-server](https://dev.mysql.com/get/Downloads/MySQLInstaller/mysql-installer-web-community-5.7.21.0.msi). You could not want to install all the package. You need at least MySQL 5.7 and you could also want to install MySQL Workbench, so you can inspect database with an UI.

## <a name="Installing-redis"></a>Installing redis

As we use redis for the channel layer of websockets, we need this service working on the correct port. To use it we have two options. We only use websocket for the chat feature, so if you don't run this service the only feature affected is the chat.

### <a name="Option-1"></a>Option 1: Docker

The easier way. With docker installed, just run this command to get redis working:

```bash
docker run -p 6379:6379 -d redis:2.8
```

### <a name="Option-2"></a>Option 2: Bare metal

#### Ubuntu

If you want install it in a linux enviroment,  use those commands:

```bash
wget http://download.redis.io/releases/redis-2.8.24.tar.gz
tar xzf redis-2.8.24.tar.gz
cd redis-2.8.24
make
```

You can use redis now using this command in the same folder:

```bash
src/redis-server
```

#### Windows

If you want to use redis on windows you should install the non official port. You can download the installer [here](https://github.com/MicrosoftArchive/redis/releases/download/win-2.8.2402/Redis-x64-2.8.2402.msi). Make sure you select add to the path when installing it.

To run the service, open a terminal and execute:

```bash
redis-server --maxheap 150M
```

Then go to your repository folder and execute:

```bash
pip install pypiwin32
```


## <a name="Installing-python-dependencies"></a>Installing python dependencies
Open a terminal at repository folder:

```bash
pip install -r requirements.txt
```

## <a name="Creating-the-database"></a>Creating the database

```bash
mysql -u root -p < create_db.sql
```

You should input your mysql root password.

You could also open and run this scipt from mysql-workbench.

## <a name="Populating-database"></a>Populating database
Once database is created, you can generate tables for our model with this command:

```bash
python manage.py migrate
```

You also can populate it with some testing information with:

```bash
python populate.py
```

## <a name="Runing-the-server"></a>Runing the server
Use this command to mount localhost server. You can access at port 8000.

```bash
python manage.py runserver
```

## <a name="Running-automated-tests"></a>Running automated tests
Some test cases can be automated. In order to run all our test use this command:

```bash
python manage.py test mvp.test
```

# <a name="Pre-production-environment"></a>Pre-production-environment
We are using docker so deployed system should work in the same way as it does in local. The system has two services, the django web service and the database. We use a docker compose file with the mariadb image for the database and a dokerfile that we build for django. This dockerfile use an ubuntu image and install apache on it with mod_wsgi in order to deploy django system.

It's important change some settings of django in a production environment, so we use environment variables in docker compose to define those settings.

# <a name="Production-environment"></a>Production-environment
The deployed system is at http://artinbar.es
