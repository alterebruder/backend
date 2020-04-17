sudo docker build -t altere_bruder_backend ./
sudo docker images
sudo docker stop altere-bruder.backend || echo 'no container found to stop!'
sudo docker rm altere-bruder.backend || echo 'no container found to rm!'
sudo docker run -p 8080:8080 -d --name altere-bruder.backend altere_bruder_backend

