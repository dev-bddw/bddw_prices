import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .helpers import return_context


@login_required
def search_view_entry(request):
    '''search view'''
    logger = logging.getLogger("watchtower")
    logger.info(f"This is the log for your life")


    if request.method == "GET":
        context = return_context(request)

        return render(request, "r_search/search/dist/index.html", {"context": context})
