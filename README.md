# bddw prices

An app that manages information about bddw prices.


# tests

To run pytest via docker container

    sudo docker compose -f local.yml run --rm django coverage run -m pytest

To create a report form testing information

    sudo docker compose -f local.yml run --rm django coverage html
