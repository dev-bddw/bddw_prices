import fileinput
import os

"""
this is a small app to help you change your
react files to django static files
place in the application root
"""


"""
TBI:
    look at the index.html (django template)
    move the css and js dependencies to the css/jss template block

"""


def static_my_react_dependences(path_tuple):
    """
    take the dir / asset dir
    find the files in asset dir
    then use them to replace the src dependencis lines in
    index.html
    """
    index, assets = path_tuple
    assets_list = os.listdir(assets)

    # get the file names from the assets directory
    js = assets_list[0] if assets_list[0].endswith(".js") else assets_list[1]
    css = assets_list[1] if assets_list[1].endswith(".css") else assets_list[0]

    js_boil = '<script type="module" crossorigin src="#"></script>'
    css_boil = '<link rel="stylesheet" href="#">'

    # build the lines you're expecting to see
    js_old = f'<script type="module" crossorigin src="/static/{js}"></script>'
    js_new = (
        '<script type="module" crossorigin src="BB% static "{0}" %BE"></script>'.format(
            js
        )
        .replace("BB", "{")
        .replace("BE", "}")
    )  # noqa

    css_old = f'<link rel="stylesheet" href="/static/{css}">'
    css_new = (
        '<link rel="stylesheet" href="BB% static "{0}" %BE">'.format(css)
        .replace("BB", "{")
        .replace("BE", "}")
    )

    # remove the non static urls from the top of the file (vite puts them there)
    with fileinput.FileInput(index, inplace=True, backup=".bak") as file:
        for line in file:
            # remove line matching the old js that we saved to memory already
            print(line.replace(js_old, ""), end="")

    with fileinput.FileInput(index, inplace=True, backup=".bak") as file:
        for line in file:
            # replace line matching the old css that we saved to memory already
            print(line.replace(css_old, ""), end="")

    # replace the boiler plate with that non-static urls first
    with fileinput.FileInput(index, inplace=True, backup=".bak") as file:
        for line in file:
            # replace the js path html tag with django url tag
            print(line.replace(js_boil, js_old), end="")

    with fileinput.FileInput(index, inplace=True, backup=".bak") as file:
        for line in file:
            # replace the css path html tag with django url tag
            print(line.replace(css_boil, css_old), end="")

    # replace the no-static urls with django tags
    with fileinput.FileInput(index, inplace=True, backup=".bak") as file:
        for line in file:
            # replace the js path html tag with django url tag
            print(line.replace(js_old, js_new), end="")

    with fileinput.FileInput(index, inplace=True, backup=".bak") as file:
        for line in file:
            # replace the css path html tag with django url tag
            print(line.replace(css_old, css_new), end="")

    print(f"Successfully altered {index}")


if __name__ == "__main__":
    print("Starting replace...")

    cwd = dir_path = os.path.dirname(os.path.realpath(__file__))

    template_dirs = [
        # tearsheets
        "/r_tear_sheets/templates/edit/",
        "/r_tear_sheets/templates/detail/",
        "/r_tear_sheets/templates/detail_for_print/",
        "/r_tear_sheets/templates/detail_for_print_list/",
        # formula
        "/r_formula_tear_sheets/templates/form_edit/",
        "/r_formula_tear_sheets/templates/form_detail/",
        "/r_formula_tear_sheets/templates/form_detail_for_print/",
        "/r_formula_tear_sheets/templates/form_detail_for_print_list/",
        # formula gbp
        "/r_formula_tear_sheets/r_form_gbp/templates/form_gbp_edit/",
        "/r_formula_tear_sheets/r_form_gbp/templates/form_gbp_detail/",
        "/r_formula_tear_sheets/r_form_gbp/templates/form_gbp_detail_for_print/",
        "/r_formula_tear_sheets/r_form_gbp/templates/form_gbp_detail_for_print_list/",
        # gbp
        "/r_tear_sheets/r_gbp/templates/gbp_detail/",
        "/r_tear_sheets/r_gbp/templates/gbp_edit/",
        "/r_tear_sheets/r_gbp/templates/gbp_detail_for_print/",
        "/r_tear_sheets/r_gbp/templates/gbp_detail_for_print_list/",
        # search
        "/r_search/templates/r_search/search/",
        # pricelists
        "/r_price_lists/templates/r_price_lists/pricelist/",
        "/r_price_lists/templates/r_price_lists/pricelist_print/",
        "/r_price_lists/templates/r_price_lists/pricelist_print_gbp/",
    ]

    paths = [
        (cwd + x + "dist/index.html", cwd + x + "dist/assets/") for x in template_dirs
    ]

    for path in paths:
        static_my_react_dependences(path)
    print("Replace complete.")
# print(paths)
