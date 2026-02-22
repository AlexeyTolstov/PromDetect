from typing import Iterable
import cv2, time

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from src.models.bbox import BoundingBox
from src.models.detection import Detection
from src.models.types_objects import TypesObjects


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

        for detection in detection_result.detections:
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
                    score=score
                )
            )
        
        return lst_detection


    def draw_detection(
            self,
            image: cv2.typing.MatLike,
            lst_detection: list[Detection]
        ) -> cv2.typing.MatLike:

        cv2.line(image, (0, 200), (1024, 200), (0, 255, 0), 1, 4)
        
        for detect in lst_detection:
            cv2.rectangle(
                image,
                detect.bbox.point1(),
                detect.bbox.point2(),
                self.colorObjects[detect.typeObj.value],
                2
            )
        
        return image
    
    def detect_operation(
        self,
        lst_detection: list[Detection]
    ):
        lst = []
        forklift_truck_lst: Iterable[Detection] = filter(
            lambda d: d.typeObj == TypesObjects.FORKLIFT_TRUCK,
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

        for truck_obj in truck_lst:
            if truck_obj.bbox.y2 > 200:
                lst.append("Грузовик на складе")
            else:
                continue

        for forklift_obj in forklift_truck_lst:
            if forklift_obj.bbox.y2 > 200:
                lst.append("Погрузчик на складе")
            else:
                continue

            for proflist_obj in proflist_lst:
                if abs(forklift_obj.bbox.y2 - proflist_obj.bbox.y1) <= 100 and abs(forklift_obj.bbox.x1 - proflist_obj.bbox.x1) <= 100:
                    lst.append("Захватил объект")
            #         print('Захватил', end=" ")
            # print()
        
        return lst