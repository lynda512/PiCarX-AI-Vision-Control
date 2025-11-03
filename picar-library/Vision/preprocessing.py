import cv2

def preprocess_image(frame):
    """Convert to grayscale, reduce noise, and normalize."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    return blur

def enhance_contrast(frame):
    """Optional CLAHE-based contrast enhancement."""
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    return clahe.apply(frame)
