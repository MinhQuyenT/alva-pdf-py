import os
import cv2

from utils import stringUtil
from utils import imageUtil
from utils import pytesseractUtil as tes


def find_q_clause(path):
    str_items = ""
    start = False
    length = 0
    for file in os.listdir(stringUtil.get_path_po(path)):
        if file.endswith(".png"):
            length += 1

    for i in range(1, length):
        f = stringUtil.get_path_po(path) + f"page_{i}.png"
        image = cv2.imread(f)
        squares = imageUtil.find_contours_squares(f, 7000)

        if squares:
            square = squares[0]
            cv2.drawContours(image, square['approx'], -1, (0, 255, 0), 3)
            y, x, w, h = square['y'], square['x'], square['w'], square['h']
            cropped_image = image[y:y + h, x:x + w]
            text = tes.image_to_string(cropped_image)

            if "Part" in text[0] and "Rev" in text[0] or "Tax Status" in text[0] and "Priority" in text[0]:
                start = True

            if start:
                if "PO Total" in text[0]:
                    start = False
                    break
                str_items = str_items + text[0]

    return get_item_info(str_items)


def get_item_info(text):
    substring = "Part:"
    result = []
    end = False
    str = text
    while not end:
        pos = find_start_line(str, substring)
        end_str = find_start_line(str[pos + 7], substring)
        if end_str != -1:
            str = text[pos:end_str]

        else:
            str = text[pos:]

        result.append(find_item_info(stringUtil.remove_rows_with_no_value(str.split("\n")), text, substring))
        if end_str == -1:
            end = True
    return result


def find_item_info(lines, text, substring):
    line_first = lines[0].split(" ")
    print(line_first, lines)
    promised = line_first[2]
    part = line_first[1]
    quantity = line_first[3]
    Rev = find_rev(text)
    text_new = text[7:]
    end = find_start_line(text_new, substring)
    if end != -1:
        text_clause = text[0:end]
    else:
        text_clause = text[0:]
    clauselist = get_clause_list(text_clause)
    price = line_first[4]
    return {'promised': promised, 'part': part, 'clause': clauselist, 'quantity': quantity, 'price': price,
            'Rev': Rev}


def get_clause_list(text):
    result = []
    lines = text.split("\n")
    for line in lines:
        if line.startswith("QAP-IEC-"):
            result.append(line.split(" ")[0])
    return result


def find_rev(text):
    result = ''
    lines = text.split("\n")
    for line in lines:
        if line.startswith("Rev:"):
            result = line.split(" ")[1]
    return result


def find_start_line(text, sub):
    if len(text) == 0:
        return -1
    lines = text.split("\n")
    for i in range(0, len(lines)):
        if lines[i].startswith(sub):
            return text.find(lines[i])
    return -1
