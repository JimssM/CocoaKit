import os
from paddleocr import PaddleOCR
from .image_tools import *
from ..public import static_path

# Initialize PaddleOCR models
en_model = PaddleOCR(use_angle_cls=False, lang="en")  # English OCR model
ch_model = PaddleOCR(use_angle_cls=False, lang="ch")  # Chinese OCR model


def ppocr(rect, det=False, num_only=False, model="en"):
    """
    Perform OCR (Optical Character Recognition) on a specific screen region.

    Parameters:
        rect (tuple): The region to capture (x1, y1, x2, y2).
        det (bool): Whether to enable text detection (bounding box detection). Default is False.
        num_only (bool): Whether to extract only numeric characters. Default is False.
        model (str): The OCR model to use ("en" for English, "ch" for Chinese). Default is "en".

    Returns:
        str: Extracted text or numeric characters from the image.
    """
    if model not in ["en", "ch"]:
        raise ValueError("model must be 'en' or 'ch'")

    # Define the path to save the captured region as an image
    img_path = os.path.join(static_path, "ocr", "ocr.png")

    # Capture the specified screen region and save it as an image
    cv2.imwrite(img_path, grab_rect_to_cv2(rect))

    # Perform OCR using the specified model
    if model == "en":
        result = en_model.ocr(img_path, cls=False, det=det)
    elif model == "ch":
        result = ch_model.ocr(img_path, cls=False, det=det)

    # Process the OCR result
    for idx in range(len(result)):
        res = result[idx]
        if det:  # If detection is enabled, include bounding box information
            if res != []:
                if num_only:  # Extract only numeric characters
                    r = ''.join([char for char in res[0][1][0] if char.isdigit()])
                else:  # Extract all text
                    r = res[0][1][0]
                return r
        else:  # Detection is disabled, process text without bounding boxes
            if num_only:  # Extract only numeric characters
                r = ''.join([char for char in res[0][0] if char.isdigit()])
            else:  # Extract all text
                r = res[0][0]
            return r
