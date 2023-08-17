#!/bin/bash
cd /home/lance/dev/django-projects/bddw_prices/react_views/r_tear_sheets/templates/detail/
npm run build
python3 replace.py
/home/lance/dev/django-projects/bddw_prices/react_views/staticfy.py
