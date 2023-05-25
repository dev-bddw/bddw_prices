import json

from django.urls import reverse
from rest_framework.authtoken.models import Token

from formula_tear_sheets.models import FormulaTearSheet
from tear_sheets.models import TearSheet


def return_context(request):
    """
    returns context for search views
    """

    def get_or_create_token():
        """
        if user return token (or create one)
        else return none

        """
        user = request.user if request.user.is_authenticated else None

        if user is not None:
            try:
                token = Token.objects.get(user=user)
            except Token.DoesNotExist:
                token = Token.objects.create(user=user)
            return token.key
        else:
            return None

    return json.dumps(
        {"auth_token": get_or_create_token(), "tearsheets": get_tearsheets()}
    )


def get_tearsheets():
    """
    return list of ALL tearsheet objects
    """
    all_tearsheets = []

    def add_tearsheets():
        for obj in TearSheet.objects.all():
            all_tearsheets.append(
                {
                    "title": obj.title,
                    "url": obj.get_absolute_url(),
                    "image": obj.image.url,
                    "updated_on": obj.updated_on,
                    "type": "tearsheet",
                    "view": obj.get_absolute_url(),
                    "edit": obj.get_edit_url(),
                    "pdf": reverse(
                        "react_views:r_tear_sheets:print", kwargs={"id": obj.id}
                    ),
                    "pdf_list": reverse(
                        "react_views:r_tear_sheets:print-list",
                        kwargs={"id": obj.id},
                    ),
                }
            )

    def add_gbp_tearsheets():
        for obj in TearSheet.objects.all():
            all_tearsheets.append(
                {
                    "title": obj.title,
                    "url": obj.get_absolute_gbp_url(),
                    "image": obj.image.url,
                    "updated_on": obj.updated_on,
                    "type": "gbp",
                    "view": obj.get_absolute_gbp_url(),
                    "edit": reverse(
                        "react_views:r_gbp:edit-tearsheet", kwargs={"id": obj.id}
                    ),
                    "pdf": reverse("react_views:r_gbp:print", kwargs={"id": obj.id}),
                    "pdf_list": reverse(
                        "react_views:r_gbp:print-list", kwargs={"id": obj.id}
                    ),
                }
            )

    def add_form_tearsheets():
        for obj in FormulaTearSheet.objects.all():
            all_tearsheets.append(
                {
                    "title": obj.title,
                    "url": obj.get_absolute_url(),
                    "image": obj.image.url,
                    "updated_on": obj.updated_on,
                    "type": "formula",
                    "view": obj.get_absolute_url(),
                    "edit": obj.get_edit_url(),
                    "pdf": reverse(
                        "react_views:r_formula_tear_sheets:print",
                        kwargs={"id": obj.id},
                    ),
                    "pdf_list": reverse(
                        "react_views:r_formula_tear_sheets:print-list",
                        kwargs={"id": obj.id},
                    ),
                }
            )

    def add_form_gbp_tearsheets():
        for obj in FormulaTearSheet.objects.all():
            all_tearsheets.append(
                {
                    "title": obj.title,
                    "url": obj.get_absolute_gbp_url(),
                    "image": obj.image.url,
                    "updated_on": obj.updated_on,
                    "type": "formula gbp",
                    "edit": reverse(
                        "react_views:r_form_gbp:edit-tearsheet",
                        kwargs={"id": obj.id},
                    ),
                    "pdf": reverse(
                        "react_views:r_form_gbp:print", kwargs={"id": obj.id}
                    ),
                    "pdf_list": reverse(
                        "react_views:r_form_gbp:print-list", kwargs={"id": obj.id}
                    ),
                }
            )

    def sort_all_tearsheets():
        """sort the list of tearsheet objects"""
        all_tearsheets.sort(reverse=True, key=lambda x: x["updated_on"])

    def stringify_datetime():
        """
        change datetime to string
        """
        for obj in all_tearsheets:
            date_time = obj["updated_on"]
            obj.update({"updated_on": date_time.__str__()})

    add_tearsheets()
    add_gbp_tearsheets()
    add_form_tearsheets()
    add_form_gbp_tearsheets()
    sort_all_tearsheets()
    stringify_datetime()

    return all_tearsheets


def return_search_results(query):
    """
    return list of tearsheet objects matching query
    """
    matching_tearsheets = []

    def add_tearsheets():
        for obj in TearSheet.objects.filter(title__contains=query):
            matching_tearsheets.append(
                {
                    "title": obj.title,
                    "url": obj.get_absolute_url(),
                    "image": obj.image.url,
                    "updated_on": obj.updated_on,
                    "type": "tearsheet",
                    "view": obj.get_absolute_url(),
                    "edit": obj.get_edit_url(),
                    "pdf": reverse(
                        "react_views:r_tear_sheets:print", kwargs={"id": obj.id}
                    ),
                    "pdf_list": reverse(
                        "react_views:r_tear_sheets:print-list", kwargs={"id": obj.id}
                    ),
                }
            )

    def add_gbp_tearsheets():
        for obj in TearSheet.objects.filter(title__contains=query):
            matching_tearsheets.append(
                {
                    "title": obj.title,
                    "url": obj.get_absolute_gbp_url(),
                    "image": obj.image.url,
                    "updated_on": obj.updated_on,
                    "type": "gbp",
                    "view": obj.get_absolute_gbp_url(),
                    "edit": reverse(
                        "react_views:r_gbp:edit-tearsheet", kwargs={"id": obj.id}
                    ),
                    "pdf": reverse("react_views:r_gbp:print", kwargs={"id": obj.id}),
                    "pdf_list": reverse(
                        "react_views:r_gbp:print-list", kwargs={"id": obj.id}
                    ),
                }
            )

    def add_form_tearsheets():
        for obj in FormulaTearSheet.objects.filter(title__contains=query):
            matching_tearsheets.append(
                {
                    "title": obj.title,
                    "url": obj.get_absolute_url(),
                    "image": obj.image.url,
                    "updated_on": obj.updated_on,
                    "type": "formula",
                    "view": obj.get_absolute_url(),
                    "edit": obj.get_edit_url(),
                    "pdf": reverse(
                        "react_views:r_formula_tear_sheets:print", kwargs={"id": obj.id}
                    ),
                    "pdf_list": reverse(
                        "react_views:r_formula_tear_sheets:print-list",
                        kwargs={"id": obj.id},
                    ),
                }
            )

    def add_form_gbp_tearsheets():
        for obj in FormulaTearSheet.objects.filter(title__contains=query):
            matching_tearsheets.append(
                {
                    "title": obj.title,
                    "url": obj.get_absolute_gbp_url(),
                    "image": obj.image.url,
                    "updated_on": obj.updated_on,
                    "type": "formula gbp",
                    "edit": reverse(
                        "react_views:r_form_gbp:edit-tearsheet", kwargs={"id": obj.id}
                    ),
                    "pdf": reverse(
                        "react_views:r_form_gbp:print", kwargs={"id": obj.id}
                    ),
                    "pdf_list": reverse(
                        "react_views:r_form_gbp:print-list", kwargs={"id": obj.id}
                    ),
                }
            )

    def sort_all_tearsheets():
        """sort the list of tearsheet dicts"""
        matching_tearsheets.sort(reverse=True, key=lambda x: x["updated_on"])

    def stringify_datetime():
        """
        change datetime to string
        """
        for obj in matching_tearsheets:
            date_time = obj["updated_on"]
            obj.update({"updated_on": date_time.__str__()})

    if query != " " and query != "":

        add_tearsheets()
        add_gbp_tearsheets()
        add_form_tearsheets()
        add_form_gbp_tearsheets()
        sort_all_tearsheets()
        stringify_datetime()

    else:

        matching_tearsheets = get_tearsheets()

    return matching_tearsheets
