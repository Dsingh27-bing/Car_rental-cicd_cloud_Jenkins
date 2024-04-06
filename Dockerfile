FROM ubuntu:18.04
RUN apt update; apt install -y gnupg2
RUN apt install -y software-properties-common
RUN apt-get install -y curl
RUN curl -fsSL https://pgp.mongodb.com/server-6.0.asc | \gpg -o /usr/share/keyrings/mongodb-server-6.0.gpg \--dearmor
RUN echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-6.0.gpg ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/6.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-6.0.list
RUN apt-get update
RUN apt-get install -y mongodb-org
WORKDIR /data
WORKDIR /data/db 
RUN apt install -y python3-pip
RUN pip3 install cython
# Upgrade setuptools
RUN pip3 install --upgrade setuptools
RUN pip3 install pandas
RUN pip3 install flask
RUN pip3 install numpy
COPY . ./.
RUN /bin/sh -c pip3 install -r requirements.txt
# Expose the port(s) the app runs on
EXPOSE 9090
CMD mongod --bind_ip=0.0.0.0 & python3 ImportData.py & python3 app.py 
