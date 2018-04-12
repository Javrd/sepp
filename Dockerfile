FROM ubuntu:17.10

RUN apt-get update
RUN apt-get install -y apt-utils vim curl apache2 apache2-utils
RUN apt-get -y install python3 libapache2-mod-wsgi-py3
RUN ln /usr/bin/python3 /usr/bin/python
RUN apt-get -y install python3-pip
RUN ln /usr/bin/pip3 /usr/bin/pip
RUN apt-get -y install libmysqlclient-dev mysql-client
RUN pip install --upgrade pip
ADD ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD ./aib.conf /etc/apache2/sites-available/000-default.conf
ADD . /var/www/html/aib/
EXPOSE 80
ADD ./run.sh /run.sh
CMD ["./run.sh"]
