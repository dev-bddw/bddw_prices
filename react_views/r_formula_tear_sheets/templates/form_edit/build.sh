#!/bin/bash
cd /home/lance/dev/django-projects/bddw_prices/react_views/r_formula_tear_sheets/templates/form_edit/
npm run build
python3 replace.py
/home/lance/dev/django-projects/bddw_prices/react_views/staticfy.py
