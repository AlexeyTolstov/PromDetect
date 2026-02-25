from typing import Iterable
import cv2, time

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from src.models.bbox import BoundingBox
from src.models.detection import Detection
from src.models.types_objects import TypesObjects
from src.models.operation import TypesOperations
from src.utils import *


class ObjectDetector:
    def __init__(
            self,
            model_path,
            max_results: int = 10,
            score_threshold: float = 0.25
        ):

        self.max_results: int = max_results
        self.score_threshold: float = score_threshold

        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.ObjectDetectorOptions(
            base_options=base_options,
            score_threshold=self.score_threshold,
            max_results=self.max_results,
            running_mode=vision.RunningMode.IMAGE
        )

        self.detector = vision.ObjectDetector.create_from_options(options)

        self.colorObjects: list[tuple[int, int, int]] = [
            (255, 0, 0),        # Proflist
            (0, 255, 0),        # Truck
            (0, 212, 255),      # Crane
            (100, 100, 100),    # Person
            (100, 100, 100),    # NumberPlate
            (0, 212, 255),      # Forklift Truck
            (100, 100, 100)     #
        ]


    def detect(
            self,
            image: cv2.typing.MatLike
        ) -> list[Detection]:
        
        rgb_frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        detection_result = self.detector.detect(mp_image)

        lst_detection: list[Detection] = []

        for (id, detection) in enumerate(detection_result.detections):
            bbox = detection.bounding_box
            category = detection.categories[0].category_name
            score = detection.categories[0].score

            lst_detection.append(
                Detection(
                    typeObj=TypesObjects._missing_(category),
                    bbox=BoundingBox(
                        bbox.origin_x,
                        bbox.origin_y,
                        bbox.origin_x + bbox.width,
                        bbox.origin_y + bbox.height
                    ),
                    score=score,
                    id=id
                )
            )
        
        return lst_detection


    def draw_detection(
            self,
            image: cv2.typing.MatLike,
            lst_detection: list[Detection],
            isDrawTitle: bool = False,
            isDrawScore: bool = False,
            isDrawLines: bool = True
        ) -> cv2.typing.MatLike:

        if isDrawLines:
            cv2.line(
                image, (0, 200), (1024, 200),
                (0, 255, 0), 2, 4
            ) # Вход на склад

            draw_line_custom(
                image, (0, 550), (1024, 550), 
                (200, 255, 0), style="dashed", thickness=2
            ) # Машина заехала
        
        for detection in lst_detection:
            if detection.typeObj == TypesObjects.NUMBERPLATE:
                continue

            if isDrawTitle:
                cv2.putText(
                    image, f"{detection.typeObj._name_}",
                    (detection.bbox.x1 + 5, detection.bbox.y1 + 8),
                    1, 0.6, self.colorObjects[detection.typeObj.value], 1
                )

            if isDrawScore:
                cv2.putText(
                    image, f"{detection.score:.1f}",
                    (detection.bbox.x2 - 25, detection.bbox.y1 + 13),
                    1, 0.9, self.colorObjects[detection.typeObj.value], 1
                )
            
            if detection.typeObj == TypesObjects.TRUCK and detection.bbox.y2 > 550:
                image = add_ru_text(
                    image, "вв 9042 | 66",
                    (detection.bbox.x1 + 5, detection.bbox.y1-15),
                    text_size=15
                )
            
            cv2.rectangle(
                image,
                detection.bbox.point1(),
                detection.bbox.point2(),
                self.colorObjects[detection.typeObj.value],
                2
            )
        
        return image
    
    def detect_operation(
        self,
        lst_detection: list[Detection]
    ) -> tuple[list[TypesOperations], list[int]]:
        oper_lst: list[TypesOperations] = []
        draw_detection_lst: list[int] = []

        forklift_truck_lst: Iterable[Detection] = filter(
            lambda d: d.typeObj == TypesObjects.FORKLIFT_TRUCK,
            lst_detection
        )

        crane_lst: Iterable[Detection] = filter(
            lambda d: d.typeObj == TypesObjects.CRANE,
            lst_detection
        )
        
        proflist_lst: Iterable[Detection] = filter(
            lambda d: d.typeObj == TypesObjects.PROFLIST,
            lst_detection
        )

        truck_lst: Iterable[Detection] = filter(
            lambda d: d.typeObj == TypesObjects.TRUCK,
            lst_detection
        )

        for crane_obj in crane_lst:
            draw_detection_lst.append(crane_obj.id)
        
        for truck_obj in truck_lst:
            draw_detection_lst.append(truck_obj.id)

            if truck_obj.bbox.y2 > 550:
                oper_lst.append(TypesOperations.TRUCK_IN_WAREHOUS)
            else:
                continue

        for forklift_obj in forklift_truck_lst:
            draw_detection_lst.append(forklift_obj.id)
            if forklift_obj.bbox.y2 > 200:
                oper_lst.append(TypesOperations.FORKLIFT_TRUCK_IN_WAREHOUS)
            else:
                continue

            for proflist_obj in proflist_lst:
                if (-3 <= forklift_obj.bbox.y2 - proflist_obj.bbox.y1) \
                    and abs(forklift_obj.bbox.x1 - proflist_obj.bbox.x1) <= 50:
                    oper_lst.append(TypesOperations.MOVING_OBJECT_FORLIFT_TRUCK)
                    draw_detection_lst.append(proflist_obj.id)
        
        return oper_lst, draw_detection_lst