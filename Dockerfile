FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y apt-utils vim curl
RUN apt-get -y install python3
RUN ln /usr/bin/python3 /usr/bin/python
RUN apt-get -y install python3-pip
RUN ln /usr/bin/pip3 /usr/bin/pip
RUN apt-get -y install libmysqlclient-dev mysql-client
RUN pip install --upgrade pip
ADD ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD . /var/www/html/aib/
EXPOSE 80
ADD ./run.sh /run.sh
CMD ["./run.sh"]
