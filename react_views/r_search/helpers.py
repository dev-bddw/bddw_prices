import json

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

    def get_tearsheets():
        """
        return list of tearsheet objects
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

    return json.dumps(
        {"auth_token": get_or_create_token(), "tearsheets": get_tearsheets()}
    )


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

        pass

    return matching_tearsheets
