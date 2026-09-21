import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Camera 0 could not be opened")
else:
    print("✅ Camera 0 opened successfully")

    while True:
        ret, frame = cap.read()

        if not ret:
            print("❌ Could not read frame")
            break

        cv2.imshow("Webcam Test", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()
