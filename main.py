import numpy as np
import pyautogui as ptg
from PIL import ImageDraw, Image
import cv2
import mss

w, h = ptg.size()
MONITOR = {'top': 0, 'left': 0, 'width': w, 'height': h}


def draw_cur(image, cur_size):
    image = Image.frombytes('RGB', (image.width, image.height), image.rgb)
    cur_x, cur_y = ptg.position()
    draw = ImageDraw.Draw(image)
    draw.polygon(
        ((cur_x - cur_size, cur_y - cur_size), (cur_x - cur_size, cur_y + cur_size), (cur_x + cur_size, cur_y)),
        fill='white',
        outline='black',
        width=1
    )
    return image


def stream():
    with mss.mss() as sct:
        while True:
            img = sct.grab(MONITOR)
            img = draw_cur(img, 10)
            img = np.array(img)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            small = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
            yield small


if __name__ == '__main__':
    for frame in stream():
        cv2.imshow('Stream', frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break


