FROM golang:latest
MAINTAINER Dashazyk dashazyk@gmail.com
 
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y build-essential
RUN apt-get install -y python-is-python3
RUN apt-get install -y python3-pip
RUN python3 -m pip install flask
RUN python3 -m pip install requests
RUN python3 -m pip install grpcio
RUN python3 -m pip install grpcio-tools

RUN mkdir -p /etc/myserver/lab124
COPY lab124/. /etc/myserver/lab124
EXPOSE 8080

CMD ["sh", "-c", "/etc/myserver/lab124/start_script.sh"]
#CMD ["sh", "-c", "/etc/myserver/lab124/myserver &"]
#CMD ["python3", "/etc/myserver/lab124/weather_server.py"]
#CMD ["go", "run", "/etc/myserver/lab124/auth_server.go"]
