docker build --tag python-docker .
docker container ps
docker stop vetebooks
docker container prune -f
docker run -d --name vetebooks -p 5000:5000 python-docker
