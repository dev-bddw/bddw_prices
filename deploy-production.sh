cd /home/ubuntu/django-projects/bddw_prices
git pull origin production
sudo docker-compose -f production.yml down
sudo docker-compose -f production.yml up --build -d
