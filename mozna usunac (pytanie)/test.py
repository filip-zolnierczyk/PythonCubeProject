import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Szersze zakresy HSV dla lepszego rozpoznawania kolorów
COLOR_RANGES = {
    "czerwony": ((0, 140, 50), (10, 255, 255)),
    "pomarańczowy": ((10, 80, 100), (22, 255, 255)),
    "żółty": ((22, 100, 100), (40, 255, 255)),
    "zielony": ((40, 100, 50), (90, 255, 255)),
    "niebieski": ((90, 100, 50), (130, 255, 255)),
    "biały": ((0, 0, 180), (180, 50, 255))
}

COLOR_BGR = {
    "czerwony": (0, 0, 255),
    "pomarańczowy": (0, 140, 255),
    "żółty": (0, 255, 255),
    "zielony": (0, 255, 0),
    "niebieski": (255, 0, 0),
    "biały": (255, 255, 255),
    "nieznany": (100, 100, 100)
}

def get_color(hsv_pixel):
    """Porównuje piksel HSV z predefiniowanymi zakresami kolorów."""
    h, s, v = hsv_pixel
    for color, (lower, upper) in COLOR_RANGES.items():
        if lower[0] <= h <= upper[0] and lower[1] <= s <= upper[1] and lower[2] <= v <= upper[2]:
            return color
    return "nieznany"

while True:
    _, frame = cap.read()

    frame = cv2.flip(frame, 1)

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    hsv_frame = np.array(hsv_frame, dtype=np.float32)  # Konwersja do float
    hsv_frame[:, :, 1] = np.clip(hsv_frame[:, :, 1], 0, 255)  # Ograniczamy do 255
    hsv_frame = np.array(hsv_frame, dtype=np.uint8)  # Powrót do uint8

    frame = cv2.cvtColor(hsv_frame, cv2.COLOR_HSV2BGR)

    height, width, _ = frame.shape

    offsets = [-200, 0, 200]
    positions = [(width//2 + x, height//2 + y) for x in offsets for y in offsets]

    for (x, y) in positions:
        pixel = hsv_frame[y, x]
        color = get_color(pixel)
        bgr_color = COLOR_BGR[color]

        # Rysowanie kółek w wykrytym kolorze
        cv2.circle(frame, (x, y), 30, bgr_color, -1) 
        cv2.circle(frame, (x, y), 32, (255, 255, 255), 2)

    cv2.imshow('frame', frame)

    key = cv2.waitKey(1)
    if key == 27:  # ESC – zamknięcie programu
        break

cap.release()
cv2.destroyAllWindows()
