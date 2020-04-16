FROM ubuntu:latest as builder_base
RUN apt update
RUN apt -y upgrade
RUN apt -y install apt-utils
RUN apt -y install make && apt -y install gcc && apt -y install g++ && apt -y install cmake
RUN apt -y install python3-dev && apt -y install python3-pip
RUN apt -y install libsm6 && apt -y install libxext6 && apt -y install libxrender-dev

FROM builder_base as builder
COPY requirements.txt/ /opt/altere_bruder/backend/requirements.txt
RUN pip3 install --upgrade pip setuptools
WORKDIR /opt/altere_bruder/backend/
RUN pip3 install -r requirements.txt

FROM builder
EXPOSE 8080
COPY server.py/ /opt/altere_bruder/backend/server.py
WORKDIR /opt/altere_bruder/backend/
CMD python3 ./server.py
