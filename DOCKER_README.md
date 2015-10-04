Development
===========

### Download the latest ShuttleOFX image

```
docker pull shuttleofx/shuttleofx
```

### Local image build

Useful if you need to modify the Dockerfile.

```
docker build -t shuttleofx <source folder>
```

### Run ShuttleOFX services

```
docker run -t --name shuttleofx_cnt -p 80:5000 -p 5004:5004 -p 5002:5002 -p 5005:5005 -p 27017:27017 -v <local logs folder>:/opt/logs -v <local source code folder>:/opt/shuttleofx_git -v <local mongo data folder>:/opt/mongo-data -v <local resources folder>:/opt/shuttleofx/render/resources shuttleofx
```

 - **Interactive**: You can enter into the image with the option: ```-i --entrypoint /bin/bash```
 - **Clean image**: You can autoclean the image between runs: ```--rm=True```

[http://localhost](http://localhost)

Server
======

```
docker run -t --name shuttleofx_cnt -p 80:5000 -p 5004:5004 -p 5002:5002 -p 5005:5005 -p 27017:27017 -v /var/log/shuttleofx:/opt/logs -v /opt/shuttleofx_git:/opt/shuttleofx_git -v /opt/mongo-data:/opt/mongo-data -v /opt/shuttleofx/render/resources:/opt/shuttleofx/render/resources --rm=True shuttleofx
```
