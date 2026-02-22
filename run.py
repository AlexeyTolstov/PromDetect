import cv2, time, datetime
from src.detector import ObjectDetector
from src.models.detection import Detection
from src.utils import add_ru_text


FRAME_WIDTH: int = 1024
FRAME_HEIGHT: int = 576
VIDEO_PATH: str = "Video/Cam 2.mp4"


object_detector = ObjectDetector(
    model_path="saved_models/main_model.tflite",
    max_results=40,
    score_threshold=0.5
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


    lst_oper = object_detector.detect_operation(lst_detection)
    for i, text in enumerate(lst_oper):
        frame = add_ru_text(frame, text, (600, 10 + (i * 30)))


    cv2.imshow(f"PromDetect Window", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        print("Выход")
        break

    if key == ord('s'):
        date = datetime.datetime.now()
        filename = "screenshots/" + date.strftime("%d_%m_%Y_%I_%M_%S") + ".jpg"
        cv2.imwrite(filename, frame)
        print("Скриншет сохранен")



cap.release()
cv2.destroyAllWindows()
