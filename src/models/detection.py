from dataclasses import dataclass
from .bbox import BoundingBox
from .types_objects import TypesObjects


@dataclass
class Detection:
    """Detection информация о объектах"""
    
    typeObj: TypesObjects
    bbox: BoundingBox
    score: float

    def __eq__(self, value) -> bool:
        if (isinstance(value, Detection)):
            return value.typeObj == self.typeObj
        return False