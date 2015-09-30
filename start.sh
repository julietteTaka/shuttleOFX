#!/bin/bash

echo "Starting mongodb"
/opt/mongodb/bin/mongod --dbpath /opt/mongo-data > /opt/logs/mongo.log 2>&1 &

python ${SHUTTLEOFX_DEV}/shuttleofx_analyser/__init__.py > /opt/logs/analyser.log 2>&1 &
python ${SHUTTLEOFX_DEV}/shuttleofx_render/__init__.py > /opt/logs/render.log 2>&1 &
python ${SHUTTLEOFX_DEV}/shuttleofx_catalog/__init__.py > /opt/logs/catalog.log 2>&1 &
python ${SHUTTLEOFX_DEV}/shuttleofx_client/__init__.py > /opt/logs/client.log 2>&1
