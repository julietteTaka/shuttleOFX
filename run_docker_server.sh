sudo docker run -td --name shuttleofx_cnt -p 80:5000 -p 5004:5004 -p 5002:5002 -p 5005:5005 -p 27017:27017 \
-v /var/log/shuttleofx:/var/log/shuttleofx \
-v /opt/mongo-data:/opt/mongo-data \
-v /opt/shuttleofx/render/resources:/opt/shuttleofx/render/resources \
-v /opt/shuttleofx/catalog/resources:/opt/shuttleofx/catalog/resources \
-v /etc/shuttleofx:/etc/shuttleofx \
shuttleofx/shuttleofx
