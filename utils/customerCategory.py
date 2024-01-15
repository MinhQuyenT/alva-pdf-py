from utils import stringUtil
from utils import pytesseractUtil as tes
import cv2

def detect_contract(path):
    f = f"{stringUtil.get_path_header(path)}/header.png"
    image = cv2.imread(f)
    text = tes.image_to_string(image)[0]

    if "Sandia National Laboratories" in text:
        print("SNL")
        return "SNL"
    elif "LOCKHEED MARTIN" in text:
        print("LM")
        return "LM"
    elif "Interstate Electronics" in text:
        print("L3")
        return "L3"
    elif "general atomics" in text.lower():
        print("GA")
        return "GA"
    elif "The Boeing Company" in text:
        print("BOEING2")
        return "BOEING2"
    elif "Order Number" in text and "Order Date" in text or "Change Order Sequence" in text and "Change Order Date" in text:
        print("BOEING1")
        return "BOEING1"
    elif "L3Harris" in text and "MPES" in text:
        print("L3PP1")
        return "L3PP1"
    elif "L3Harris Technologies" in text:
        print("L3PP2")
        return "L3PP2"
    elif "Power Paragon" in text and "harris" in text.lower() or "Power Paragon" in text:
        print("L3PP3")
        return "L3PP3"
    elif "NORTHROP" in text and "GRUMMAN" in text and "Change" in text:
        print("NGS2")
        return "NGS2"
    elif "NORTHROP" in text and "GRUMMAN" in text and "Purchase Order" in text:
        print("NGS1")
        return "NGS1"
    elif "Blue Origin" in text:
        print("BLUE")
        return "BLUE"
    else:
        print("not found")

