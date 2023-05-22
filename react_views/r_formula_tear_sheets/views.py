from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .helpers import return_context


@login_required
def detail_view_entry(request, id):
    """
    detail view for fomula tear sheets

    """
    if request.method == "GET":

        context = return_context(request, id)

        return render(
            request, "form_detail/dist/index.html", {"id": id, "context": context}
        )


@login_required
def edit_view_entry(request, id):
    """
    edit view for formula tear sheets

    """

    if request.method == "GET":

        context = return_context(request, id)

        return render(
            request, "form_edit/dist/index.html", {"id": id, "context": context}
        )
