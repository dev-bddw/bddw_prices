import fileinput

with fileinput.FileInput("./dist/index.html", inplace=True, backup=".bak") as file:
    for line in file:
        print(line.replace("/assets/", "/static/"), end="")
