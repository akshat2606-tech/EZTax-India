# bill_and_expense.py

import sys
import cv2
import numpy as np
import easyocr
import google.generativeai as genai
import json
import time
from PIL import Image
import base64
from dotenv import load_dotenv
import os

# Load environment
load_dotenv()

# Allow OpenMP duplicate lib
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Initialize EasyOCR reader (CPU only to avoid GPU issues)
reader = easyocr.Reader(['en'], gpu=False)

def image_with_bb(image_to_edit, results):
    """Draw bounding boxes around detected text."""
    for detection in results:
        top_left = tuple(map(int, detection[0][0]))
        bottom_right = tuple(map(int, detection[0][2]))
        cv2.rectangle(image_to_edit, top_left, bottom_right, (0, 255, 0), 2)
    return image_to_edit

def process_image(image_data):
    """Apply OCR and annotate image."""
    try:
        np_arr = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh_image = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                             cv2.THRESH_BINARY, 199, 5)
        result = reader.readtext(thresh_image)
        extracted_text = " ".join([detection[1] for detection in result])
        annotated_image = image_with_bb(image.copy(), result)
        return extracted_text, annotated_image
    except Exception as e:
        return "", None

def load_image(image):
    """Convert BGR OpenCV image to PIL."""
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return Image.fromarray(image_rgb)

def generate_expense_prompt(ocr_text):
    return f"""
    You are a financial document parser. You are given:
    OCR Extracted Text -> {ocr_text}
    Use it to extract the following fields:
    - Total Amount
    - Date (ISO format)
    - Concerned Organization
    - Document_number
    - Payment Method (cash, card, bank transfer, UPI, etc.)
    - Category (Rent, Education, Medical, Insurance, etc.)
    - GSTIN or Tax ID (if present)
    - Is Tax Deductible (true/false)
    Return as JSON.
    """

def generate_response_with_retry(model, prompt, image, max_retries=3, delay=5):
    for attempt in range(max_retries):
        try:
            response = model.generate_content([prompt, image])
            return response.text
        except Exception as e:
            print(f"⚠️ Gemini API error: {e} (Retry {attempt + 1}/{max_retries})")
            time.sleep(delay)
    return json.dumps({"error": "Gemini API failed after retries"})

def main():
    try:
        # Read image as base64 from stdin
        base64_data = sys.stdin.read()
        image_bytes = base64.b64decode(base64_data)

        extracted_text, annotated_image = process_image(image_bytes)

        if not extracted_text:
            print(json.dumps({"error": "No text extracted from image."}))
            return

        prompt = generate_expense_prompt(extracted_text)
        image_pil = load_image(annotated_image)

        API_KEY = os.getenv("GEMINI_API_KEY")
        if not API_KEY:
            print(json.dumps({"error": "Gemini API key missing"}))
            return

        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")

        response = generate_response_with_retry(model, prompt, image_pil)

        try:
            parsed = json.loads(response)
            print(json.dumps(parsed))  # Ensure valid JSON
        except:
            print(json.dumps({"error": "Invalid JSON from Gemini", "raw": response}))

    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    main()
