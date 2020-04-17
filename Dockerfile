FROM centos:latest as builder_base
RUN yum -y update
RUN yum -y install make && yum -y install gcc && yum -y install gcc-c++ && yum -y install cmake && yum -y install python3-devel
RUN yum -y install libSM && yum -y install libXext && yum -y install libXrender-devel

FROM builder_base as builder
COPY requirements.txt/ /opt/altere_bruder/backend/requirements.txt
RUN pip3 install --upgrade pip setuptools
WORKDIR /opt/altere_bruder/backend/
RUN pip3 install -r requirements.txt

FROM builder
EXPOSE 8080
COPY server.py/ /opt/altere_bruder/backend/server.py
WORKDIR /opt/altere_bruder/backend/
COPY files/ files/
CMD python3 ./server.py
