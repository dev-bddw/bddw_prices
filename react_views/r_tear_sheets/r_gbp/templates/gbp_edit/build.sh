#!/bin/bash
cd /home/lance/dev/django-projects/bddw_prices/react_views/r_tear_sheets/r_gbp/templates/gbp_edit/
npm run build
python3 replace.py
