### Local test
docker build -t shuttleofx

### Run ShuttleOFX services
docker run --name shuttleofx_cnt -d -p 80:5000 -p 5004:5004 -p 5002:5002 -p 5005:5005 -p 27017:27017 -v <local logs folder>:/opt/logs shuttleofx

[http://localhost](http://localhost)
