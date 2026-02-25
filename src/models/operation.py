from .detection import Detection
from typing import Optional
from enum import Enum


class TypesOperations(Enum):
    """Типы детектируемых операций"""
    TRUCK_IN_WAREHOUS = 0               # Грузовик на складе
    FORKLIFT_TRUCK_IN_WAREHOUS = 1      # Погрузчик на складе
    MOVING_OBJECT_FORLIFT_TRUCK = 2     # Перемещение груза вилочным погрузчиком
    MOVING_OBJECT_CRANE = 3             # Перемещение груза с помощью крана
    MOVING_OBJECT_CRANE_IN_TRUCK = 4    # Перемещение груза с помощью крана в грузовик


class Operation:
    pass