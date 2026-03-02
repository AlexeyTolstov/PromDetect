lst_ru_operation = [
    "Грузовик на складе",
    "Погрузчик на складе",
    "Перемещение груза вилочным погрузчиком",
    "Перемещение груза с помощью крана",
    "Перемещение груза с помощью крана в грузовик"
]


""" ===== VIDEO ===== """
FRAME_WIDTH: int = 1024
FRAME_HEIGHT: int = 576
VIDEO_PATH: str = "Video/Cam 2.mp4"
MODEL_PATH: str = "saved_models/main_model.tflite"


""" ===== DRAW ===== """
isDrawAll: bool = True
isDrawTitle: bool = False
isDrawScore: bool = False
isDrawLines: bool = True


eps: float = 20
