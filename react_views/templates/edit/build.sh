#!/bin/bash
cd /home/lance/dev/django-projects/bddw_prices/react_views/templates/edit/
npm run build
python3 replace.py
