#!/bin/bash
cd /home/lance/dev/django-projects/bddw_prices/react_views/r_formula_tear_sheets/r_form_gbp/templates/form_gbp_detail_for_print/
npm run build
python3 replace.py
/home/lance/dev/django-projects/bddw_prices/react_views/staticfy.py
