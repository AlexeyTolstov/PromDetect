import cv2, time
from src.detector import ObjectDetector
from src.models.detection import Detection


FRAME_WIDTH: int = 1024
FRAME_HEIGHT: int = 576
VIDEO_PATH: str = "Video/Cam 0.mp4"

object_detector = ObjectDetector(
    model_path="saved_models/main_model.tflite",
    max_results=40,
    score_threshold=0.3
)

cap = cv2.VideoCapture(VIDEO_PATH)


while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break
    
    start = time.time()
    frame = cv2.resize(
        frame,
        (FRAME_WIDTH, FRAME_HEIGHT)
    )

    lst_detection: list[Detection] = object_detector.detect(frame)
    
    frame = object_detector.draw_detection(
        frame,
        lst_detection
    )

    delta = time.time() - start
    cv2.putText(
        frame,
        f"FPS: {1 / delta:.1f}",
        (30, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 0, 255),
        thickness=2
    )

    cv2.imshow(f"PromDetect Window", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
