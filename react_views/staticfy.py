import fileinput
import os

"""
this is a small app to help you change your
react files to django static files
place in the application root
"""

cwd = dir_path = os.path.dirname(os.path.realpath(__file__))

template_dirs = [
    "/r_tear_sheets/templates/edit/",
    "/r_tear_sheets/templates/detail/",
    "/r_tear_sheets/templates/detail_for_print/",
    "/r_tear_sheets/templates/detail_for_print_list/",
    "/r_formula_tear_sheets/templates/form_edit/",
    "/r_formula_tear_sheets/templates/form_detail/",
    "/r_formula_tear_sheets/templates/form_detail_for_print/",
    "/r_formula_tear_sheets/templates/form_detail_for_print_list/",
    "/r_tear_sheets/r_gbp/templates/gbp_detail/",
    "/r_tear_sheets/r_gbp/templates/gbp_edit/",
    "/r_tear_sheets/r_gbp/templates/gbp_detail_for_print/",
    "/r_tear_sheets/r_gbp/templates/gbp_detail_for_print_list/",
]


paths = [(cwd + x + "dist/index.html", cwd + x + "dist/assets/") for x in template_dirs]


def static_my_react_dependences(path_tuple):
    """
    take the dir / asset dir
    find the files in asset dir
    then use them to replace the src dependencis lines in
    index.html
    """
    index, assets = path_tuple
    assets_list = os.listdir(assets)

    js = assets_list[0] if assets_list[0].endswith(".js") else assets_list[1]
    css = assets_list[1] if assets_list[1].endswith(".css") else assets_list[0]

    line_1 = f'<script type="module" crossorigin src="/static/{js}"></script>'
    line_2 = f'<link rel="stylesheet" href="/static/{css}">'
    new_line_1 = (
        '<script type="module" crossorigin src="BB% static "{0}" %BE"></script>'.format(
            js
        )
        .replace("BB", "{")
        .replace("BE", "}")
    )  # noqa
    new_line_2 = (
        '<link rel="stylesheet" href="BB% static "{0}" %BE">'.format(css)
        .replace("BB", "{")
        .replace("BE", "}")
    )

    with fileinput.FileInput(index, inplace=True, backup=".bak") as file:
        for line in file:
            print(line.replace(line_1, new_line_1), end="")

    with fileinput.FileInput(index, inplace=True, backup=".bak") as file:
        for line in file:
            print(line.replace(line_2, new_line_2), end="")

    print(f"Successfully altered {index}")


if __name__ == "__main__":
    print("Starting replace...")
    for path in paths:
        static_my_react_dependences(path)
    print("Replace complete.")
# print(paths)
