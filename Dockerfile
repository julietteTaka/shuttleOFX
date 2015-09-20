# Set the base image to Ubuntu
FROM ubuntu:latest

# File Author / Maintainer
MAINTAINER ShuttleOFX <shuttleofx-dev@googlegroups.com>

# Update the repository
RUN apt-get update

# Install utility tools
RUN apt-get install -y vim wget

# Download and Install
RUN apt-get install -y nginx debhelper python-setuptools git python-pip uwsgi nginx nodejs-legacy npm xdg-utils uwsgi-plugin-python libpython2.7 python-flask mongodb
RUN pip install pymongo python-oauth2 flask-oauthlib

# Expose ports
EXPOSE 80
EXPOSE 5004
EXPOSE 5002
EXPOSE 5005
EXPOSE 27017

ENV SHUTTLEOFX_DEV=/opt/shuttleofx_git

COPY . ${SHUTTLEOFX_DEV}
RUN cd ${SHUTTLEOFX_DEV}/shuttleofx_client/ && npm install && npm install -g grunt-cli && grunt build
RUN cd ${SHUTTLEOFX_DEV} && dpkg-buildpackage -uc -us && dpkg -i ../python-shuttleofx_1.1.0-1_all.deb

# enable nginx apps
RUN rm /etc/nginx/sites-enabled/default
# RUN ln -s /etc/nginx/sites-available/shuttleofx_analyser /etc/nginx/sites-enabled/
# RUN ln -s /etc/nginx/sites-available/shuttleofx_render /etc/nginx/sites-enabled/
RUN ln -s /etc/nginx/sites-available/shuttleofx_client /etc/nginx/sites-enabled/
RUN ln -s /etc/nginx/sites-available/shuttleofx_catalog /etc/nginx/sites-enabled/

# enable uwsgi apps
RUN ln -s /etc/uwsgi/apps-available/shuttleofx_catalog.ini /etc/uwsgi/apps-enabled/
RUN ln -s /etc/uwsgi/apps-available/shuttleofx_render.ini /etc/uwsgi/apps-enabled/
RUN ln -s /etc/uwsgi/apps-available/shuttleofx_client.ini /etc/uwsgi/apps-enabled/
RUN ln -s /etc/uwsgi/apps-available/shuttleofx_analyser.ini /etc/uwsgi/apps-enabled/

RUN mkdir /opt/shuttleofx
RUN chown www-data:www-data /opt/shuttleofx

# ENTRYPOINT ["/etc/init.d/uwsgi", "start"]

