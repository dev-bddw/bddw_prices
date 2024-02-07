## BDDW PRICES

Create and manage beautiful tearsheets.

## GETTING STARTED

This is a django application that uses docker. To begin, clone the repository. Then:

>> cd bddw_prices
>> sudo docker-compose -f local.yml up --build

This builds the application and begins a development server on localhost.

>> sudo docker-compose -f local.yml run --rm django python manage.py createsuperuser

Follow the prompts to create an admin user. Now you have access to the backend at localhost:8000/admin.

# Questions

For any questions, please reach out to lance@bddw.com !
