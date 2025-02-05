from flask import Flask, Response
import numpy as np
import pyautogui as ptg
from PIL import ImageDraw, Image
import cv2
import mss

app = Flask(__name__)

w, h = ptg.size()
MONITOR = {'top': 0, 'left': 0, 'width': w, 'height': h}


def draw_cur(image, cur_size):
    """Draws the cursor at the current cursor position"""
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


def generate_frames():
    """Generate current monitor frame"""
    with mss.mss() as sct:
        while True:
            img = sct.grab(MONITOR)
            img = draw_cur(img, 10)
            img = np.array(img)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            _, buffer = cv2.imencode('.jpg', img)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
