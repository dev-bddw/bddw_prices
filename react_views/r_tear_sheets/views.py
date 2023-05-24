from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .helpers import return_context


@login_required
def detail_view_entry(request, id):
    """
    react detail view for tearsheet matching id
    """

    if request.method == "GET":
        context = return_context(request, id)

        return render(request, "detail/dist/index.html", {"id": id, "context": context})


@login_required
def edit_view_entry(request, id):
    """
    react edit view for tearsheet matching id
    """

    if request.method == "GET":
        context = return_context(request, id)

        return render(request, "edit/dist/index.html", {"id": id, "context": context})
