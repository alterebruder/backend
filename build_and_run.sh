sudo docker build -t altere_bruder_backend ./
sudo docker images
sudo docker stop altere_bruder_backend || echo 'no container found to stop!'
sudo docker rm altere_bruder_backend || echo 'no container found to rm!'
sudo docker run --expose 8080 -p 8080:8080 -d --name altere_bruder_backend altere_bruder_backend

