import os


def get_name_po(pdf_file):
    names = pdf_file.split("/")
    return names[len(names) - 1].split(".")[0]


def get_path_header(path):
    f = get_name_po(path)
    directory_path = f"./log/{f}/header"
    if not os.path.exists(directory_path):
        os.mkdir(directory_path)
    return directory_path


def get_path_po(path):
    f = get_name_po(path)
    return f"./log/{f}/"


def get_path_by_page(path, page):
    f = get_name_po(path)
    return f"./log/{f}/page_{page}.png"


def get_path_item(path):
    f = get_name_po(path)
    directory_path = f"./log/{f}/item/"
    if not os.path.exists(directory_path):
        os.mkdir(directory_path)
    return directory_path


def remove_rows_with_no_value(lines):
    r = []
    for i in range(0, len(lines)):
        if len(lines[i]) > 0:
            r.append(lines[i])

    return r
