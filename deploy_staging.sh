cd /home/ubuntu/django-projects/bddw_prices
git pull origin staging
docker-compose -f staging.yml down
docker-compose -f staging.yml up --build -d
