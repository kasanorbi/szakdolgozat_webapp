import pytesseract
import cv2
import numpy as np
import re

def image_to_dict(image_path) -> dict:
    try:
        image = cv2.imread(image_path)
        
        lines_extracted = preprocess_image(image)

        lines = [line.replace('-', '').replace('"','').replace('  ', ' ') for line in lines_extracted.split('\n')]
        extraction = False
        products = []

        for line in lines:
            if any(keyword in line for keyword in ['Áfa', 'Kerekítés']):
                extraction = False
            if extraction:
                products.append(line)
            if "Cikkszám" in line:
                extraction = True
        
        products = list(filter(lambda x: x and len(x) >= 10, products))
        products_price = [product.split(' ')[-1].replace('.', '').replace(',','') for product in products]
        
        try:
            products_amount = [re.search(r'(\d+)\s*db', product).group(1) for product in products]
        except AttributeError as e:
            products_amount = [1] * len(products)
        
        products_item_number = [re.search(r'([A-ZÁÉÍÓÖŐÚÜŰ]+\s*[A-ZÁÉÍÓÖŐÚÜŰ\d]+)', product).group(1) for product in products]
        products_name = [' '.join(re.findall(r'\b[A-ZÁÉÍÓÖŐÚÜŰa-záéíóöőúüű]+\b', product)).rstrip(' db') for product in products]
       
        products_dict = {
            'itemNumber': products_item_number,
            'name': products_name,
            'amount': products_amount,
            'price': products_price
        }
        print(products_dict)
        return products_dict
    
    except Exception as e:
        print('Error:', e)

def preprocess_image(image) -> list:
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    _, im_bw = cv2.threshold(grayscale, 110, 255, cv2.THRESH_BINARY)

    kernel = np.ones((1,1), np.uint8)
    no_noise = cv2.dilate(im_bw, kernel, iterations=1)
    no_noise = cv2.erode(no_noise, kernel, iterations=1)
    no_noise = cv2.morphologyEx(no_noise, cv2.MORPH_CLOSE, kernel)
    no_noise = cv2.medianBlur(no_noise, 3)
    
    extract_text = pytesseract.image_to_string(no_noise, lang="hun")

    return extract_text

    