#!/bin/bash
cd /home/lance/dev/django-projects/bddw_prices/react_views/r_price_lists/templates/r_price_lists/pricelist/
npm run build
python3 replace.py

cd /home/lance/dev/django-projects/bddw_prices/react_views/r_price_lists/templates/r_price_lists/pricelist_print/
npm run build
python3 replace.py

cd /home/lance/dev/django-projects/bddw_prices/react_views/r_price_lists/templates/r_price_lists/pricelist_print_gbp/
npm run build
python3 replace.py

bash /home/lance/dev/django-projects/bddw_prices/react_views/run_static.sh
