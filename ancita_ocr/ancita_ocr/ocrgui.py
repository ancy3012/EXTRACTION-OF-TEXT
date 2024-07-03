import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
from Api_ocr import fun, ocr_from_pdf_with_text_extraction
from bs4 import BeautifulSoup
import requests
import pyperclip
from preprocess import Preprocess
import html2text

def extract_text_from_webpage(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        markdown_text = html2text.html2text(str(soup))
        return markdown_text
    except requests.exceptions.RequestException as e:
        print("Error fetching webpage:", e)
        return None

def submit():
    inputtext = image_entry.get()
    if (inputtext.startswith("http://") or inputtext.startswith("https://")):
        result_label.config(text="You entered a webpage: " + inputtext)
        webpage_text = extract_text_from_webpage(inputtext)
        webpage_text = str(webpage_text)
        if webpage_text:
            result_text.config(state=tk.NORMAL)
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, webpage_text)
            result_text.config(state=tk.DISABLED)
            pyperclip.copy(webpage_text)
        else:
            result_label.config(text="Error fetching webpage content.")
    else:
        if inputtext.lower().endswith(".pdf"):
            result_label.config(text="You entered a PDF path: " + inputtext)
            text_pdf = ocr_from_pdf_with_text_extraction(inputtext)
            result_text.config(state=tk.NORMAL)
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, text_pdf)
            result_text.config(state=tk.DISABLED)
        else:
            result_label.config(text="You entered an image path: " + inputtext)
            text_img = Preprocess(inputtext)
            result_text.config(state=tk.NORMAL)
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, text_img)
            result_text.config(state=tk.DISABLED)

window = tk.Tk()
window.title("OCR and Text Extraction")
window.geometry("600x400")

style = ThemedStyle(window)
style.set_theme("plastik")

image_label = ttk.Label(window, text="Enter an image or pdf path or webpage URL:", font=("Helvetica", 16))
image_entry = ttk.Entry(window, font=("Helvetica", 14))
submit_button = ttk.Button(window, text="Submit", command=submit, style="TButton")
result_label = ttk.Label(window, text="Extracted Text:", font=("Helvetica", 16))

image_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
image_entry.grid(row=1, column=0, padx=10, pady=10, sticky="we")
submit_button.grid(row=2, column=0, padx=10, pady=10)
result_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")

result_text = tk.Text(window, wrap=tk.WORD, height=40, width=100)
result_text.grid(row=4, column=0, padx=10, pady=10)
result_text.config(state=tk.DISABLED)

window.mainloop()
