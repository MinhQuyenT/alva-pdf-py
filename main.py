from utils import imageUtil
from utils import customerCategory as cus
from utils import detect

if __name__ == "__main__":
    pdf_file = "./data/L3 Interstate Electronic PO SM-00481.pdf"

    # convert pdf to image
    imageUtil.convert_pdf_to_image(pdf_file, 300)

    # Trim the header of each contract
    imageUtil.trim_header(pdf_file)

    # Determine the type of contract
    ct = cus.detect_contract(pdf_file)

    # file item in contract base on contract type
    detect.detect_item_base_contract(ct, pdf_file)
