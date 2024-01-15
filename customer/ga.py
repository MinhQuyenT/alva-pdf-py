import os
import cv2

from utils import stringUtil
from utils import imageUtil
from utils import pytesseractUtil as tes


# @Date 22-09-2023
# @author Minh Phúc

def find_q_clause(path):
    start = False
    result = []
    str_items = ""
    length = 0
    for file in os.listdir(stringUtil.get_path_po(path)):
        if file.endswith(".png"):
            length += 1

    for j in range(1, length):
        f = stringUtil.get_path_po(path) + f"page_{j}.png"
        image = cv2.imread(f)
        lines = imageUtil.find_contours_line(f, 2000, 10)
        height, width, _ = image.shape
        if lines is not None:
            if len(lines) > 1:
                crop_img = image[lines[0][1]:lines[1][1], 0:width]
                cv2.imwrite("crop.png", crop_img)
                text = tes.image_to_string(crop_img)
                if text[0].startswith("LINE") and "PART NUMBER" in text[0] and "REV" in text[0]:
                    start = True

            if start:
                for i in range(1, len(lines)):
                    y1 = lines[i][1]
                    y2 = lines[i + 1][1] if len(lines) - 1 > i else height
                    x1 = 0
                    x2 = width
                    crop_img = image[y1:y2, x1:x2]
                    text = tes.image_to_string(crop_img)
                    if "Total Amount without Tax" in text[0]:
                        start = False
                        break
                    str_items += text[0]

    end = False
    substring = str_items
    while not end:
        pos = get_pos_start_item(substring)
        substring = substring[pos:]
        result.append(find_item_info(stringUtil.remove_rows_with_no_value(substring.split("\n"))))
        substring = substring[get_pos_end_item(substring) + 20:]
        if get_pos_start_item(substring) == -1:
            end = True
    return result


def get_pos_start_item(text):
    lines = stringUtil.remove_rows_with_no_value(text.split("\n"))
    for i in range(0, len(lines)):
        if i < len(lines) - 1 and lines[i].startswith("Tax Status"):
            return text.find(lines[i - 1])

    return -1


def get_pos_end_item(text):
    lines = stringUtil.remove_rows_with_no_value(text.split("\n"))
    for i in range(0, len(lines)):
        if i < len(lines) - 1 and lines[i].startswith("Tax Status"):
            return text.find(lines[i])

    return -1


def find_item_info(lines):
    line_first = lines[0].split(" ")
    part = line_first[1]
    rev = line_first[2]
    promised = line_first[3]
    quantity = line_first[4]
    price = line_first[8]
    clause = lines[2]
    if not lines[3].startswith("DESCRIPTION"):
        clause += lines[3]
    return {'part': part, 'rev': rev, 'promised': promised, 'quantity': quantity, 'price': price, 'clause': clause}
