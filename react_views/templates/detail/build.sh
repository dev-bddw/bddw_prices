#!/bin/bash
cd /home/lance/dev/django-projects/bddw_prices/react_views/templates/detail/
npm run build
python3 replace.py
