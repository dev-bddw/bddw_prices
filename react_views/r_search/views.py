from django.contrib.auth.decorators import login_required
from django.shortcuts import render

import logging

from .helpers import return_context


@login_required
def search_view_entry(request):
    '''search view'''

    if request.method == "GET":
        context = return_context(request)

        return render(request, "r_search/search/dist/index.html", {"context": context})
