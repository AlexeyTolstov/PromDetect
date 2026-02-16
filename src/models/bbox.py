from dataclasses import dataclass


@dataclass
class BoundingBox:
    """BoundingBox для детекции объектов"""
    
    x1: int
    y1: int
    x2: int
    y2: int
    
    def width(self) -> int:
        """Ширина bbox"""
        return self.x2 - self.x1
    
    def height(self) -> int:
        """Высота bbox"""
        return self.y2 - self.y1

    def point1(self) -> tuple[int, int]:
        return (self.x1, self.y1)
    
    def point2(self) -> tuple[int, int]:
        return (self.x2, self.y2)