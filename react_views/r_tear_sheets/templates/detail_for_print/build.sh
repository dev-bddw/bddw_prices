#!/bin/bash
cd /home/lance/dev/django-projects/bddw_prices/react_views/r_tear_sheets/templates/detail_for_print/
npm run build
python3 replace.py
