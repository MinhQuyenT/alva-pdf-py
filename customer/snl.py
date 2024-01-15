import os
import cv2

from utils import stringUtil
from utils import imageUtil
from utils import pytesseractUtil as tes


def find_q_clause(path):
    result = []
    for file in os.listdir(stringUtil.get_path_po(path)):
        if file.endswith(".png"):
            result.extend(find_text_in_image(stringUtil.get_path_po(path) + file,
                                             f"{stringUtil.get_path_item(path)}crop{file[4:]}"))
    return result


def find_text_in_image(path, path_crop):
    result = []
    image = cv2.imread(path)
    squares = imageUtil.find_contours_squares(path, 7000)

    if squares:
        square = squares[0]
        cv2.drawContours(image, square['approx'], -1, (0, 255, 0), 3)
        y, x, w, h = square['y'], square['x'], square['w'], square['h']
        cropped_image = image[y:y + h, x:x + w]
        text = tes.image_to_string(cropped_image)

        if text and (text[0].startswith('Line') or text[0].startswith('Part Number')):
            result.extend(get_item_info(text[0]))
            cv2.imwrite(path_crop, cropped_image)
    return result


def get_item_info(text):
    substring = "Promised:"
    result = []
    lines = text.split("\n")
    for i in range(0, len(lines)):
        if lines[i].startswith(substring):
            quantity = get_quantity(lines[i])
            promised = get_promised_time(lines[i])
            price = get_price(lines[i])
            next_line = lines[i + 1] if len(lines[i + 1]) > 0 else lines[i + 2]
            part = get_part_number(next_line)
            clause = get_q_clause(next_line)
            result.append({'promised': promised, 'part': part, 'clause': clause, 'quantity': quantity, 'price': price})

    return result


def get_promised_time(line):
    return line.split(" ")[0].split(":")[1].strip()


def get_part_number(line):
    if "QA NOTES" in line:
        r = line.split("QA NOTES")[0].strip()
        if r.endswith("/") or  r.endswith("."):
            return r[:-1].strip()
        return r
    return ""


def get_q_clause(line):
    if "QA NOTES" in line:
        r = line.split("QA NOTES", 1)[1].strip()
        if r.startswith(':'):
            return check_clause_with_apply_per(r[1:].strip())
        return check_clause_with_apply_per(r)
    return ""


def check_clause_with_apply_per(str):
    if "apply per" in str:
        return str.split("apply per")[0].strip()
    return str


def get_quantity(line):
    if len(line) > 1:
        return line.split(" ")[1]
    return ''


def get_price(line):
    if len(line) > 3:
        return line.split(" ")[3]
    return ''
