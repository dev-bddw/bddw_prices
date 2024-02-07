cd /home/ubuntu/django-projects/bddw_prices
git pull origin staging
sudo docker-compose -f staging.yml down
sudo docker-compose -f staging.yml up --build -d
