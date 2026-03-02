from dataclasses import dataclass
from .bbox import BoundingBox
from .types_objects import TypesObjects
from src.config import eps


@dataclass
class Detection:
    """Detection информация о объектах"""    

    typeObj: TypesObjects
    bbox: BoundingBox
    score: float
    id: int
    last_time: float


    def __eq__(self, value: Detection) -> bool:
        if self.typeObj != value.typeObj: return False

        return abs(self.bbox.x1 - value.bbox.x1) <= eps and \
               abs(self.bbox.x2 - value.bbox.x2) <= eps and \
               abs(self.bbox.x1 - value.bbox.x1) <= eps and \
               abs(self.bbox.x2 - value.bbox.x2) <= eps 
