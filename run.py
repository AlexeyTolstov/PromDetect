import cv2, time, datetime
from src.utils import add_ru_text
from src.detector import ObjectDetector

from src.models.detection import Detection
from src.models.types_objects import TypesObjects
from src.models.operation import TypesOperations

from src.config import *
from src.utils import *

from random import randint
import pandas as pd


df = pd.DataFrame(columns=['Date', 'Time', 'Operation'])

object_detector = ObjectDetector(
    model_path=MODEL_PATH,
    max_results=40,
    score_threshold=0.3
)

cap = cv2.VideoCapture(VIDEO_PATH)

current_frame: int = 6900 # FIXME
total_frames: int = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
isPaused: bool = False

skip_seconds: int = 20 
video_fps: int = int(cap.get(cv2.CAP_PROP_FPS))
skip_frames: int = skip_seconds * video_fps

# FIXME
cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)

# FIXME!!!!
last_time_truck_in_warehous = 0
last_send_message = None
start_time_truck_in_warehous = None

lst: list[Detection] = []


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

    # FIXME
    lst_detection_on_frame: list[Detection] = object_detector.detect(frame)
    lst_detection: list[Detection] = []
    used: list[bool] = [False] * len(lst_detection_on_frame) 

    del_obj = []

    for d in lst:
        isAdd: bool = False

        for [i2, d2] in enumerate(lst_detection_on_frame):
            if d == d2 and not used[i2]:
                used[i2] = True
                
                if not isAdd:
                    lst_detection.append(
                        Detection(
                            typeObj=d2.typeObj,
                            bbox=d2.bbox,
                            score=d2.score,
                            id=d.id,
                            last_time=time.time()
                        )
                    )
                
                isAdd = True
        
        if not isAdd:
            if time.time() - d.last_time < 0.5:
                lst_detection.append(d)
                
    for del_o in del_obj:
        lst.remove(del_o)

    for i in range(len(lst_detection_on_frame)):
        if not used[i]:
            d2 = lst_detection_on_frame[i]
            lst_detection.append(
                Detection(
                    typeObj=d2.typeObj,
                    bbox=d2.bbox,
                    score=d2.score,
                    id=randint(100, 1000),
                    last_time=time.time()
                )
            )
    lst = lst_detection
    


    # lst_detection: list[Detection] = lst_detection_temp
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
    
    frame = add_ru_text(frame, "Текущие операции:", (600, 0), text_size=25)



    for i, operation in enumerate(oper_lst):
        if operation.type_operation == TypesOperations.TRUCK_IN_WAREHOUS:
            operation.upd_time(time.time())
            cv2.imwrite("screenshots/truck_on_sclad.jpg", frame)

            if start_time_truck_in_warehous is None:
                df.loc[len(df)] = ['28.02.2026', time.time(), 'Грузовик приехал']
                start_time_truck_in_warehous = time.time()
            
            last_time_truck_in_warehous = time.time()


            delta_time = time.time() - start_time_truck_in_warehous
            
            frame = add_ru_text(
                frame, 
                f"Грузовик на складе: {delta_time:.1f} секунд", 
                (600, 25 + (i * 30)), text_size=20
            )

            if delta_time >= 5 and (last_send_message is None or time.time() - last_send_message > 5):
                send_telegram("ПРОСТОЙ у грузовика")
                df.loc[len(df)] = ['28.02.2026', time.time(), 'Простой грузовика']
                last_send_message = time.time()
        else: 
            frame = add_ru_text(frame, str(operation), (600, 15 + (i * 30)), text_size=20)

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
    
    df.to_csv('test.csv')
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
