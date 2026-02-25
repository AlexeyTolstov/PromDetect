import cv2, time, datetime
from src.utils import add_ru_text
from src.detector import ObjectDetector

from src.models.detection import Detection
from src.models.types_objects import TypesObjects
from src.models.operation import TypesOperations

FRAME_WIDTH: int = 1024
FRAME_HEIGHT: int = 576
VIDEO_PATH: str = "Video/Cam 2.mp4"
MODEL_PATH: str = "saved_models/main_model.tflite"


"""DRAW"""
isDrawAll: bool = False
isDrawTitle: bool = False
isDrawScore: bool = False
isDrawLines: bool = True


object_detector = ObjectDetector(
    model_path=MODEL_PATH,
    max_results=40,
    score_threshold=0.2
)

cap = cv2.VideoCapture(VIDEO_PATH)

current_frame: int = 0
total_frames: int = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
isPaused: bool = False

skip_seconds: int = 20 
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

    oper_lst, draw_detection_id_lst = object_detector.detect_operation(lst_detection)
    
    add_ru_text(frame, "Текущие операции", (600, 5), text_size=20)
    lst_ru_operation = [
        "Грузовик на складе", "Погрузчик на складе", "Перемещение груза вилочным погрузчиком"
    ]

    for i, operation in enumerate(oper_lst):
        if operation == TypesOperations.TRUCK_IN_WAREHOUS:
            cv2.imwrite("screenshots/truck_on_sclad.jpg", frame)
        
        frame = add_ru_text(frame, lst_ru_operation[operation.value], (600, 15 + (i * 30)), text_size=20)
    

    draw_detection_lst = [
        next((d for d in lst_detection if d.id == id))
            for id in draw_detection_id_lst
    ]


    frame = object_detector.draw_detection(
        frame, (lst_detection if isDrawAll else draw_detection_lst),
        isDrawTitle=isDrawTitle, isDrawScore=isDrawScore, isDrawLines=isDrawLines
    )


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
