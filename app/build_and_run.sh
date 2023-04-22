sudo docker build --no-cache -t myimage .
sudo docker run -d --name mycontainer -p 80:80 myimage