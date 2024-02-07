cd /home/ubuntu/django-projects/bddw_prices
git pull origin staging
sudo docker-compose -f production.yml down
sudo docker-compose -f production.yml up --build -d
