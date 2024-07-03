import requests
import os
import tempfile
import pyperclip
import fitz
API_KEY ="dabd63118bmsh4d3d354cb873c03p12f1f6jsn08a4483b777c"


def fun(save_path):
    url = "//ocr-text-extraction.p.rapidapi.com/v1/ocr/"
    querystring = {"etype": "image"}


    image_path = save_path
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    payload = {"image": ("image.jpg", image_data)}

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "ocr-text-extraction.p.rapidapi.com"
    }

    response = requests.post(url, files=payload, headers=headers, params=querystring)

    if response.status_code == 200:
        result = response.json()
        # print(result)
        text = result['results'][0]['entities'][0]['objects'][0]['entities'][0]['text']
        print("Extracted Text:", text)

    else:
        print("Error:", response.status_code)
    pyperclip.copy(text)
    return text


def ocr_from_pdf_with_text_extraction(pdf_file_path):
    url = "//ocr-text-extraction.p.rapidapi.com/v1/ocr/"
    querystring = {"etype": "image"}  # Change "etype" to "image" for image input

    pdf_document = fitz.open(pdf_file_path)
    extracted_text = []

    for page_number in range(pdf_document.page_count):
        page = pdf_document.load_page(page_number)

        # Convert the page to an image
        pix = page.get_pixmap()

        # Save the image to a temporary file
        temp_image_path = f"./Temp_dir/page_{page_number}.jpg"
        pix.save(temp_image_path, "jpeg")

        with open(temp_image_path, "rb") as image_file:
            image_data = image_file.read()

        payload = {"image": ("image.jpg", image_data)}

        headers = {
            "X-RapidAPI-Key":API_KEY ,
            "X-RapidAPI-Host": "ocr-text-extraction.p.rapidapi.com"
        }

        response = requests.post(url, files=payload, headers=headers, params=querystring)

        if response.status_code == 200:
            result = response.json()
            extracted_text_page = result['results'][0]['entities'][0]['objects'][0]['entities'][0]['text']
            extracted_text.append(extracted_text_page)
            print(f"Page {page_number + 1} - Extracted Text:", extracted_text_page)
        else:
            print(f"Error processing page {page_number + 1}:", response.status_code)

    pdf_document.close()

    
    combined_text = "\n".join(extracted_text)

    
    pyperclip.copy(combined_text)
    return combined_text


