#!/bin/bash
cd /home/lance/dev/django-projects/bddw_prices/react_views/r_formula_tear_sheets/r_form_gbp/templates/form_gbp_edit/
npm run build
python3 replace.py
