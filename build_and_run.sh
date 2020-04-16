sudo docker build -t altere_bruder_backend ./
sudo docker images
sudo docker network create altere_bruder_network || echo 'Network already exists!'
sudo docker stop altere-bruder.backend || echo 'no container found to stop!'
sudo docker rm altere-bruder.backend || echo 'no container found to rm!'
sudo docker run --expose 8080 -p 8080:8080 --network altere_bruder_network -d --name altere-bruder.backend altere_bruder_backend

