import pytesseract

def image_to_string(img):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    extracted_text = []
    text = pytesseract.image_to_string(img)
    extracted_text.append(text)
    return extracted_text
