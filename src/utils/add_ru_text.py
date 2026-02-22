import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import cv2

def add_ru_text(
        img: np.ndarray,
        text: str,
        position: tuple[int, int],
        text_color: tuple[int, int, int] = (0, 255, 0),
        text_size: int = 30
    ):
    """
    Добавление текста (русского) на картинку
    """

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(img_rgb)
    
    draw = ImageDraw.Draw(pil_img)

    font_path: Path = Path(__file__).parent.parent / "assets" / "fonts" / "arialmt.ttf"

    font = ImageFont.truetype(str(font_path), text_size, encoding="utf-8")

    draw.text(position, text, font=font, fill=text_color[::-1])
    result_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    
    return result_img
