#!/bin/bash
cd /home/lance/dev/django-projects/bddw_prices/react_views/r_formula_tear_sheets/templates/form_detail_for_print_list/
npm run build
python3 replace.py
