import math
import os

from utils import stringUtil
from utils import toolUtil
import cv2
import numpy as np

import fitz


def convert_pdf_to_image(path, dpi):
    f = stringUtil.get_name_po(path)
    pdf_document = fitz.open(path)
    directory_path = f"./log/{f}"
    if not os.path.exists(directory_path):
        os.mkdir(directory_path)
    for page_number in range(pdf_document.page_count):
        page = pdf_document[page_number]
        zoom_x = dpi / 72.0
        zoom_y = dpi / 72.0
        mat = fitz.Matrix(zoom_x, zoom_y)
        pix = page.get_pixmap(matrix=mat)
        image_file = f"./log/{f}/page_{page_number + 1}.png"
        pix.save(image_file, "png")
    pdf_document.close()
    print("convert pdf to image success")
    return ""


def trim_header(path):
    f = stringUtil.get_path_by_page(path, 1)
    frame = cv2.imread(f)
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.GaussianBlur(img, (5, 5), 0)
    canny_image = cv2.Canny(blurred_image, 50, 150)
    lines = cv2.HoughLines(canny_image, rho=1, theta=np.pi / 180, threshold=600)
    if lines is None:
        lines = cv2.HoughLines(canny_image, rho=1, theta=np.pi / 180, threshold=100)
    line = lines[0]
    rho, theta = line[0]
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    x1 = int(x0 + 1000 * (-b))
    y1 = int(y0 + 1000 * (a))
    x2 = int(x0 - 1000 * (-b))
    y2 = int(y0 - 1000 * (a))
    x_max, y_max = find_head_region_position(x1, x2, y1, y2, frame)
    header_crop = frame[0:y_max, 0:x_max]
    cv2.imwrite(f"{stringUtil.get_path_header(path)}/header.png", header_crop)
    print("crop header of image success")


def find_head_region_position(x1, x2, y1, y2, frame):
    _x = 0
    _y = 0
    w = frame.shape[1]

    if x1 > _x:
        _x1 = x1
    if x2 > _x:
        _x = x2

    if y1 > _y:
        _y = y1
    if y2 > _y:
        _y = y2
    if w > _x:
        _x = w

    return _x, _y


def find_contours_squares(path, area):
    image = cv2.imread(path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, 235, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    squares = []
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
        x = approx.ravel()[0]
        y = approx.ravel()[0]
        x1, y1, w, h = cv2.boundingRect(approx)
        if len(approx) > 3 and cv2.contourArea(approx) > area and x != 0:
            squares.append({'area': cv2.contourArea(approx), 'x': x1, 'y': y1, 'w': w, 'h': h, 'approx': [approx]})
    return sorted(squares, key=lambda x: x['area'], reverse=True)


def find_contours_line(path, min_width, hmp):
    image = cv2.imread(path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    lines_list = []
    lines = cv2.HoughLinesP(
        edges,  # Input edge image
        1,  # Distance resolution in pixels
        np.pi / 180,  # Angle resolution in radians
        threshold=100,  # Min number of votes for valid line
        minLineLength=5,  # Min allowed length of line
        maxLineGap=10  # Max allowed gap between line for joining them
    )
    for points in lines:

        x1, y1, x2, y2 = points[0]
        line_length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        if line_length > min_width:
            cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            if check_range_line(lines_list, y1, y2, hmp):
                lines_list.append([x1, y1, x2, y2])
    cv2.imwrite("tes.png", image)
    return sorted(lines_list, key=lambda x: x[1], reverse=False)


def check_range_line(arr, y1, y2, hmp):
    if len(arr) == 0:
        return True

    for i in range(0, len(arr)):
        if math.fabs(arr[i][1] - y1) <= hmp or math.fabs(arr[i][3] - y2) <= hmp:
            return False

    return True
