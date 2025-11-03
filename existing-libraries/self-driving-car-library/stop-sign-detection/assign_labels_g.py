import os
import cv2
import csv

STOP_DIR = "stop"
NOT_STOP_DIR = "not_stop"
OUTPUT_CSV = "annotations.csv"

drawing = False
ix, iy = -1, -1
box = []

"""
Interactive annotation tool for STOP / NOT-STOP images.

Usage:
- Place STOP images under the folder named "stop" and non-STOP images under "not_stop".
- Run this script; annotate bounding boxes on STOP images by clicking two points (drag or two clicks).
- Controls:
    - Enter: save current box for the displayed image (must have selected a box)
    - 's': skip the current image without annotation
    - ESC: exit the annotator early and save what has been collected so far
Output:
- annotations.csv with header: filename, x_min, y_min, x_max, y_max, label
  label: 1 for stop, 0 for not_stop; not_stop entries use -1 for bbox coordinates.
Notes:
- Images are resized to 640x480 for annotation; saved file paths refer to the original path.
"""


def get_all_images(folder):
    """Return list of image file paths in folder.

    Args:
        folder (str): Path to directory containing images.

    Returns:
        list[str]: Sorted list of full paths to files with extensions .jpg, .png, .jpeg (case-insensitive).
    """
    return [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]


def draw_rectangle(event, x, y, flags, param):
    """Mouse callback to let the user draw a single rectangle on the image.

    This callback updates the module-global variables used by the annotation loop:
        - ix, iy: initial click coordinates
        - drawing: whether the left button is held
        - box: final rectangle coordinates [x1, y1, x2, y2]
        - img_copy: preview image with the rectangle drawn

    Args (provided by OpenCV callback):
        event: mouse event type (e.g., cv2.EVENT_LBUTTONDOWN, cv2.EVENT_LBUTTONUP)
        x, y: mouse coordinates
        flags, param: unused OpenCV callback parameters

    Side effects:
        - On EVENT_LBUTTONDOWN starts drawing and records start coords.
        - On EVENT_LBUTTONUP records final box and updates img_copy with a green rectangle.
        - Shows the annotated preview in the "Annotate STOP Sign" window.
    """
    global ix, iy, drawing, box, img_copy

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
        box = []

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        box = [ix, iy, x, y]
        img_copy = img.copy()
        cv2.rectangle(img_copy, (ix, iy), (x, y), (0, 255, 0), 2)
        cv2.imshow("Annotate STOP Sign", img_copy)


def annotate_stop_images(image_paths):
    """Interactively annotate stop images with a single bounding box each.

    Args:
        image_paths (list[str]): List of file paths to images that should contain a STOP sign.

    Returns:
        list[list]: List of annotations where each annotation is:
            [img_path, x_min, y_min, x_max, y_max, 1]

    Behavior:
        - Each image is loaded and resized to 640x480 for annotation.
        - The user draws a box (two clicks/drag). Press Enter to save the box for that image.
        - Press 's' to skip an image (no annotation added).
        - Press ESC to exit annotation early and return collected annotations so far.
        - Coordinates are normalized to the resized image coordinate system (as produced).
    """
    global img, img_copy, box
    annotations = []

    for img_path in image_paths:
        img = cv2.imread(img_path)
        img = cv2.resize(img, (640, 480))
        img_copy = img.copy()
        box = []

        print(f"\n[INFO] Annotating: {img_path}")
        cv2.imshow("Annotate STOP Sign", img)
        cv2.setMouseCallback("Annotate STOP Sign", draw_rectangle)

        while True:
            key = cv2.waitKey(0) & 0xFF
            if key == 13:  # Enter key to save
                if box:
                    x_min = min(box[0], box[2])
                    y_min = min(box[1], box[3])
                    x_max = max(box[0], box[2])
                    y_max = max(box[1], box[3])
                    annotations.append([img_path, x_min, y_min, x_max, y_max, 1])
                    break
                else:
                    print("⚠️ No box selected. Please click two points.")
            elif key == ord('s'):  # skip image
                print("⏭ Skipping...")
                break
            elif key == 27:  # ESC to exit
                print("🚪 Exiting annotation.")
                cv2.destroyAllWindows()
                return annotations

    return annotations


def annotate_not_stop_images(image_paths):
    """Create annotations for non-STOP images (no bounding box).

    Args:
        image_paths (list[str]): List of file paths to images without STOP signs.

    Returns:
        list[list]: List of annotations where each annotation is:
            [img_path, -1, -1, -1, -1, 0]
        (-1 coordinates indicate no bounding box; label 0 marks NOT-STOP)
    """
    return [[img_path, -1, -1, -1, -1, 0] for img_path in image_paths]


def main():
    """Main entry: collect annotations for stop and not_stop images and write CSV.

    Behavior:
        - Gathers image paths from STOP_DIR and NOT_STOP_DIR.
        - Runs interactive annotation for STOP images; generates placeholder annotations for NOT_STOP images.
        - Writes annotations to OUTPUT_CSV with header.
    """
    stop_images = get_all_images(STOP_DIR)
    not_stop_images = get_all_images(NOT_STOP_DIR)

    print(f"🛑 {len(stop_images)} STOP images to annotate.")
    stop_annots = annotate_stop_images(stop_images)

    print(f"🚫 {len(not_stop_images)} NON-STOP images.")
    not_stop_annots = annotate_not_stop_images(not_stop_images)

    all_annots = stop_annots + not_stop_annots

    with open(OUTPUT_CSV, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['filename', 'x_min', 'y_min', 'x_max', 'y_max', 'label'])
        writer.writerows(all_annots)

    print(f"\n✅ Saved annotations to {OUTPUT_CSV}")
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
