# Set the base image to Ubuntu
FROM tuttleofx/tuttleofx:latest

# File Author / Maintainer
MAINTAINER ShuttleOFX <shuttleofx-dev@googlegroups.com>

# Update the repository
RUN apt-get update

# Download and Install
RUN apt-get install -y vim wget python-setuptools python-pip nodejs-legacy npm xdg-utils libpython2.7 python-flask
RUN pip install pymongo python-oauth2 flask-oauthlib

#Install last mongodb version to have text search feature
RUN cd /opt/ && \
    wget https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-3.0.6.tgz && \
    tar -zxvf mongodb-linux-x86_64-3.0.6.tgz && \
    mv mongodb-linux-x86_64-3.0.6 mongodb && \
    mkdir /opt/mongo-data

# Expose ports
EXPOSE 5000
EXPOSE 5004
EXPOSE 5002
EXPOSE 5005
EXPOSE 27017

ENV SHUTTLEOFX_DEV=/opt/shuttleofx_git
ENV PATH=${PATH}:/opt/mongodb/bin

COPY . ${SHUTTLEOFX_DEV}
RUN cd ${SHUTTLEOFX_DEV}/shuttleofx_client/ && npm install && npm install -g grunt-cli && grunt build
RUN cp -R ${SHUTTLEOFX_DEV}/etc/shuttleofx /etc && mkdir /opt/logs

RUN chmod 777 ${SHUTTLEOFX_DEV}/start.sh

#ENTRYPOINT ["/opt/shuttleofx_git/start.sh"]

