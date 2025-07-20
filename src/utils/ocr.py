from pdf2image import convert_from_bytes
from typing import List, Optional
from PIL import Image
import os
import requests
import json
import pytesseract

def ocr(pdf):
    images = convert_from_bytes(pdf)
    ocr_texts = []
    
    for i, image in enumerate(images):
        image_path = f"page_{i + 1}.png"
        image.save(image_path, "PNG")
        print(f"Saved {image_path}")
    images_path = [f"page_{i + 1}.png" for i in range(len(images))]
    for image_path in images_path:
        image = Image.open(image_path)
        with Image.open(image_path) as image:
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                
                text = pytesseract.image_to_string(
                    image, 
                    lang='eng',
                    config='--psm 6'  
                )   
                text = text.replace('\n', ' ').strip()
                ocr_texts.append(text)
        os.remove(image_path)
        print(f"Removed {image_path}")
        
    return ocr_texts