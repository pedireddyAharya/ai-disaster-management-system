import cv2
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

def detect_people(frame):
    results = model(frame)
    count = 0

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            if cls == 0:  # person class
                count += 1

    return count, results[0].plot()