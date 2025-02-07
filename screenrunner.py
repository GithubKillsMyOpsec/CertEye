import os
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

# CONFIGURABLE PARAMETERS
FILTER_FOLDER = "filter"  # Folder containing images to compare against
SCAN_FOLDER = "screens"      # Folder containing images to be scanned
SIMILARITY_THRESHOLD = 0.97  # Adjust as needed (1.0 = identical)

def load_images_from_folder(folder):
    images = {}
    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)
        if os.path.isfile(filepath):
            image = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)  # Read in grayscale for better comparison
            if image is not None:
                images[filename] = image
    return images

def compare_images(imageA, imageB):
    """Resize images to the same dimensions and compute SSIM similarity."""
    imageB = cv2.resize(imageB, (imageA.shape[1], imageA.shape[0]))  # Resize to match dimensions
    score = ssim(imageA, imageB)
    return score

def scan_and_delete():
    filter_images = load_images_from_folder(FILTER_FOLDER)
    scan_images = load_images_from_folder(SCAN_FOLDER)

    if not filter_images:
        print("No filter images found. Exiting.")
        return

    for scan_name, scan_image in scan_images.items():
        for filter_name, filter_image in filter_images.items():
            similarity = compare_images(scan_image, filter_image)
            if similarity >= SIMILARITY_THRESHOLD:
                scan_path = os.path.join(SCAN_FOLDER, scan_name)
                os.remove(scan_path)  # Delete the matching image
                print(f"Deleted {scan_name} (matched with {filter_name}, similarity: {similarity:.2f})")
                break  # No need to check against other filter images once a match is found

if __name__ == "__main__":
    scan_and_delete()
