import cv2, time, datetime
from src.detector import ObjectDetector
from src.models.detection import Detection
from src.utils import add_ru_text


FRAME_WIDTH: int = 1024
FRAME_HEIGHT: int = 576
VIDEO_PATH: str = "Video/Cam 2.mp4"
MODEL_PATH: str = "saved_models/main_model.tflite"


object_detector = ObjectDetector(
    model_path=MODEL_PATH,
    max_results=40,
    score_threshold=0.3
)

cap = cv2.VideoCapture(VIDEO_PATH)

current_frame: int = 0
total_frames: int = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
isPaused: bool = False

skip_seconds: int = 10 
video_fps: int = int(cap.get(cv2.CAP_PROP_FPS))
skip_frames: int = skip_seconds * video_fps


while cap.isOpened():
    # region Pause Events
    if isPaused:
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            print("Выход")
            break

        elif key == ord('p'):
            cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
            isPaused = False
        
        elif key == ord('f'):
            current_frame = min(current_frame + skip_frames, total_frames)
        
        elif key == ord('b'):
            current_frame = max(current_frame - skip_frames, 0)
        
        continue
    # endregion
    
    ret, frame = cap.read()
    current_frame += 1

    if not ret: break
    
    start = time.time()
    frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))

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


    # region Keyboard Events
    
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        print("Выход")
        break

    elif key == ord('s'):
        date = datetime.datetime.now()
        filename = "screenshots/" + date.strftime("%d_%m_%Y_%I_%M_%S") + ".jpg"
        cv2.imwrite(filename, frame)
        print("Скриншет сохранен")
    
    elif key == ord('f'):
        current_frame = min(current_frame + skip_frames, total_frames)
        cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
    
    elif key == ord('b'):
        current_frame = max(current_frame - skip_frames, 0)
        cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
    
    elif key == ord('p'):
        isPaused = True
    
    #endregion


cap.release()
cv2.destroyAllWindows()
