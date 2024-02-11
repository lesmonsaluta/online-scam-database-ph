import re
import pytesseract
import cv2
import numpy as np
import hashlib

def process_image(image_file):
    # Read the image file using OpenCV
    contents = image_file.file.read()
    nparr = np.fromstring(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Process the image
    img = cv2.blur(img, (5, 5))

    # OCR
    text = pytesseract.image_to_string(img, config='--psm 6', output_type=pytesseract.Output.STRING)
    pattern = r'(\+63\s*\(?\d{3}\)?\s*\d{3}\s*\d{4})|(09\s*\(?\d{2}\)?\s*\d{3}\s*\d{4})'

    # Find all matches
    matches = re.findall(pattern, text)

    # Process matches
    extracted_numbers = []
    for match in matches:
        number = ''.join(match)
        number = re.sub(r'[\s\(\)]', '', number)
        extracted_numbers.append(number)

    # Split the text into lines
    text_lines = text.replace('\n', ' ')
    
    # Hashing image binary to generate image uuid
    bin_contents = contents
    hash_object = hashlib.sha256(bin_contents)
    hex_digest = hash_object.hexdigest()

    # Return if useful details were received
    if extracted_numbers and text_lines:
        return (extracted_numbers, text, bin_contents, hex_digest), None
    else:
        return None, "No detected number and text"