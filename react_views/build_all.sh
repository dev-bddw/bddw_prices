#!/bin/bash
# helpful script to rebuild every react template
# templates still need to be manually changed so tha tthe
# react js and react css are in the correct template position
# then run run_static.sh to apply static template tags to the
# react templates (index.html)
cd /home/lance/dev/django-projects/bddw_prices/react_views/
./r_tear_sheets/templates/edit/build.sh
./r_tear_sheets/templates/detail/build.sh
./r_tear_sheets/templates/detail_for_print/build.sh
./r_tear_sheets/templates/detail_for_print_list/build.sh
./r_formula_tear_sheets/templates/form_edit/build.sh
./r_formula_tear_sheets/templates/form_detail/build.sh
./r_formula_tear_sheets/templates/form_detail_for_print/build.sh
./r_formula_tear_sheets/templates/form_detail_for_print_list/build.sh
./r_formula_tear_sheets/r_form_gbp/templates/form_gbp_edit/build.sh
./r_formula_tear_sheets/r_form_gbp/templates/form_gbp_detail/build.sh
./r_formula_tear_sheets/r_form_gbp/templates/form_gbp_detail_for_print/build.sh
./r_formula_tear_sheets/r_form_gbp/templates/form_gbp_detail_for_print_list/build.sh
./r_tear_sheets/r_gbp/templates/gbp_detail/build.sh
./r_tear_sheets/r_gbp/templates/gbp_edit/build.sh
./r_tear_sheets/r_gbp/templates/gbp_detail_for_print/build.sh
./r_tear_sheets/r_gbp/templates/gbp_detail_for_print_list/build.sh
./r_search/templates/r_search/search/build.sh
./r_price_lists/templates/r_price_lists/pricelist/build.sh
