import cv2, math
import numpy as np


def draw_line_custom(img, start, end, color, thickness=1, style='solid', 
                     dash_length=15, gap_length=10):
    """
    Рисует линию разного стиля
    
    Args:
        img: изображение
        start, end: начальная и конечная точки
        color: цвет
        thickness: толщина
        style: 'solid', 'dashed', 'dotted'
        dash_length: длина штриха (для dashed)
        gap_length: длина пробела (для dashed)
    """
    if style == 'solid':
        cv2.line(img, start, end, color, thickness)
        return
    
    x1, y1 = start
    x2, y2 = end
    
    # Вычисляем параметры линии
    dx = x2 - x1
    dy = y2 - y1
    line_length = math.sqrt(dx**2 + dy**2)
    
    if line_length == 0:
        return
    
    # Нормализованный вектор направления
    unit_dx = dx / line_length
    unit_dy = dy / line_length
    
    if style == 'dashed':
        # Штриховая линия
        current_pos = 0
        while current_pos < line_length:
            # Начало штриха
            start_dash = current_pos
            end_dash = min(current_pos + dash_length, line_length)
            
            # Координаты начала и конца штриха
            dash_start = (int(x1 + unit_dx * start_dash), 
                         int(y1 + unit_dy * start_dash))
            dash_end = (int(x1 + unit_dx * end_dash), 
                       int(y1 + unit_dy * end_dash))
            
            cv2.line(img, dash_start, dash_end, color, thickness)
            
            # Переходим к следующему штриху
            current_pos += dash_length + gap_length
            
    elif style == 'dotted':
        # Точечная линия
        num_dots = int(line_length / gap_length)
        for i in range(num_dots + 1):
            dot_x = int(x1 + unit_dx * (i * gap_length))
            dot_y = int(y1 + unit_dy * (i * gap_length))
            cv2.circle(img, (dot_x, dot_y), max(1, thickness//2), color, -1)

if __name__ == "__main__":
    # Пример использования
    img = np.zeros((400, 400, 3), dtype=np.uint8)

    # Разные стили линий
    draw_line_custom(img, (50, 50), (350, 50), (0, 255, 0), 2, 'solid')
    draw_line_custom(img, (50, 100), (350, 100), (255, 0, 0), 2, 'dashed')
    draw_line_custom(img, (50, 150), (350, 150), (0, 0, 255), 2, 'dotted')

    # Линии под углом
    draw_line_custom(img, (50, 200), (300, 300), (255, 255, 0), 3, 'dashed', 20, 15)

    cv2.imshow('Line Styles', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()