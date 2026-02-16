from enum import Enum
from typing import Optional


class TypesObjects(Enum):
    """Типы объектов для детекции"""
    
    PROFLIST = 0
    TRUCK = 1
    CRANE = 2
    PERSON = 3
    NUMBERPLATE = 4

    @classmethod
    def _missing_(cls, value: str) -> TypesObjects:
        """
        Поиск enum по строковому значению

        Args:
            value: строка для поиска (имя enum)
        
        Returns:
            Найденный элемент enum или None
        """

        if not isinstance(value, str):
            raise KeyError(f"Category 'f{value}' not found")

        for member in cls:
            if member.name.lower() == value.lower():
                return member
        
        raise KeyError(f"Category 'f{value}' not found")