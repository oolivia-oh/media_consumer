import sys
import random
from pynput import keyboard
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import QApplication, QLabel, QWidget


def create_overlay(x, y, width, hieght):
    overlay = QWidget()
    overlay.setWindowFlags(
        Qt.FramelessWindowHint
        | Qt.WindowStaysOnTopHint
        | Qt.Tool
    )
    overlay.setAttribute(Qt.WA_TransparentForMouseEvents)
    overlay.setAttribute(Qt.WA_ShowWithoutActivating)
    overlay.setGeometry(x, y, width, hieght)
    return overlay

class Overlay:
    def __init__(self, enable_tunnel=False, enable_random=False):
        self.app = QApplication(sys.argv)
        self.enable_tunnel = enable_tunnel
        self.enable_random = enable_random
        self.moving_pressed = []
        self.n_randoms = 100
        self.i_random = 0
        self.create_tunnel_overlays(90,0,1830,1080,800,800)
        self.create_random_overlays(90+self.hole_left,self.hole_top,800,800,30,3,3)
        self.start()
        self.app.exec()

    def on_press(self, key):
        try:
            if key.char == 'e' or key.char == 'd' or key.char == 's' or key.char == 'f':
                if key.char not in self.moving_pressed:
                    self.moving_pressed.append(key.char)
                    self.update_movement()
            if key.char == '#':
                self.stop()
                self.app.quit()
                sys.exit()
        except AttributeError:
            pass

    def on_release(self, key):
        try:
            if key.char == 'e' or key.char == 'd' or key.char == 's' or key.char == 'f':
                self.moving_pressed.remove(key.char)
                self.update_movement()
        except AttributeError:
            pass

    def update_movement(self):
        if len(self.moving_pressed) == 0:
            self.hide_overlays()
        else:
            self.show_overlays()

    def create_tunnel_overlays(self, start_x, start_y, width, height, hole_width, hole_height):
        self.tunnel_overlays = {}
        self.midway_x = width//2
        self.midway_y = height//2
        self.hole_midway_x = hole_width//2
        self.hole_midway_y = hole_height//2
        self.hole_top = self.midway_y - self.hole_midway_y
        self.hole_bottom = self.midway_y + self.hole_midway_y
        self.hole_left = self.midway_x - self.hole_midway_x
        self.hole_right = self.midway_x + self.hole_midway_x
        self.tunnel_overlays['top'] = create_overlay(start_x, start_y, width, self.hole_top)
        self.tunnel_overlays['bottom'] = create_overlay(start_x, start_y + self.hole_bottom, width, self.hole_top)
        self.tunnel_overlays['left'] = create_overlay(start_x, start_y + self.hole_top, self.hole_left, hole_height)
        self.tunnel_overlays['right'] = create_overlay(start_x + self.hole_right, start_y + self.hole_top, self.hole_left, hole_height)

    def create_random_overlays(self, start_x, start_y, width, height, size, n_columns, n_rows):
        self.random_overlays = []
        self.random_cycle = []
        column_width = width//n_columns
        row_height = height//n_rows
        for y_i in range(n_rows):
            for x_i in range(n_columns):
                x = start_x + int((x_i+0.5)*column_width-size/2)
                y = start_y + int((y_i+0.5)*row_height-size/2)
                self.random_overlays.append(create_overlay(x, y, size, size))
        for i_r in range(self.n_randoms):
            self.random_cycle.append([])
            for y_i in range(n_rows):
                for x_i in range(n_columns):
                    i = x_i + y_i*n_columns
                    x = start_x + random.randint(x_i*column_width, (x_i+1)*column_width-size)
                    y = start_y + random.randint(y_i*row_height, (y_i+1)*row_height-size)
                    self.random_cycle[i_r].append((x, y))

    def hide_overlays(self):
        if self.enable_tunnel:
            for overlay in self.tunnel_overlays.values():
                overlay.hide()
        if self.enable_random:
            for overlay in self.random_overlays:
                overlay.hide()
    def show_overlays(self):
        if self.enable_tunnel:
            for overlay in self.tunnel_overlays.values():
                overlay.show()
        if self.enable_random:
            for i, overlay in enumerate(self.random_overlays):
                overlay.show()
                x, y = self.random_cycle[self.i_random][i]
                overlay.move(x, y)
            self.i_random += 1
            self.i_random = self.i_random % self.n_randoms

    def start(self):
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()
    def stop(self):
        self.listener.stop()



# Transparent window background
#overlay.setAttribute(Qt.WA_TranslucentBackground)

# Let mouse clicks pass through the overlay


#label = QLabel("Overlay active", overlay)
#label.setGeometry(0, 0, 1600, 100)
#label.setAlignment(Qt.AlignCenter)
#label.setFont(QFont(" sans", 20))
#label.setStyleSheet("""
#    QLabel {
#        color: white;
#        background-color: rgba(0, 0, 0, 180);
#        border-radius: 8px;
#    }
#""")

overlay = Overlay(enable_tunnel=True, enable_random=True)

