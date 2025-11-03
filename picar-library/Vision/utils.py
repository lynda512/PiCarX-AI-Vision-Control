import cv2

def draw_detections(frame, detections):
    """Draw bounding boxes and labels on frame for visualization."""
    for det in detections:
        x, y = det.get("position", (0, 0))
        label = det.get("label", "?")
        cv2.putText(frame, label, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
    return frame
