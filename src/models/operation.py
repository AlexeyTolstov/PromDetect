from .detection import Detection
from typing import Optional
from enum import Enum
from time import time
from src.config import lst_ru_operation


class TypesOperations(Enum):
    """Типы детектируемых операций"""
    TRUCK_IN_WAREHOUS = 0               # Грузовик на складе
    FORKLIFT_TRUCK_IN_WAREHOUS = 1      # Погрузчик на складе
    MOVING_OBJECT_FORLIFT_TRUCK = 2     # Перемещение груза вилочным погрузчиком
    MOVING_OBJECT_CRANE = 3             # Перемещение груза с помощью крана
    MOVING_OBJECT_CRANE_IN_TRUCK = 4    # Перемещение груза с помощью крана в грузовик

    @classmethod
    def from_string(cls, value: str):
        """Создание из строки"""
        for member in cls:
            if member.value == value:
                return member
        raise ValueError(f"Unknown operation type: {value}")


class Operation:
    def __init__(
            self,
            start_time: float,
            last_time: float,
            type_operation: TypesOperations
        ):
        self.start_time: float = start_time
        self.last_time: float = last_time
        self.type_operation: TypesOperations = type_operation
    
    def upd_time(self, last_time: float):
        self.last_time = last_time

    @property
    def duration(self) -> float:
        """Длительность операции в секундах"""
        if self.start_time:
            return self.last_time - self.start_time
        return 0

    def on_start(self):
        print(f"'{lst_ru_operation[self.type_operation.value]}' - Началась")

    def on_running(self):
        pass

    def __str__(self) -> str:
        return f"{self.type_operation.name}, длится: {self.duration}"