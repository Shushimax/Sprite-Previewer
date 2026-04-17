import math

from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

def load_sprite(sprite_folder_name, number_of_frames):
    frames = []
    padding = math.ceil(math.log(number_of_frames - 1, 10))
    for frame in range(number_of_frames):
        folder_and_file_name = sprite_folder_name + "/sprite_" + str(frame).rjust(padding, '0') + ".png"
        frames.append(QPixmap(folder_and_file_name))

    return frames

class Interface(QMainWindow):
    def __init__(self):
        super().__init__()

        self.num_frames = 21
        self.sprites = load_sprite('spriteImages',self.num_frames)
        self.current_pic = 0

        self.image_label = QLabel()
        self.image_label.setPixmap(self.sprites[self.current_pic])

        self.animation_slider = QSlider()
        self.animation_slider.setRange(1,100)
        self.animation_slider.setTickPosition(QSlider.TickPosition.TicksBothSides)

        self.exit_button = QPushButton("Exit")
        self.next_button = QPushButton("Next")

        self.animation_slider.valueChanged.connect(self.frame_rate_change)
        self.exit_button.clicked.connect(self.exit_program)
        self.next_button.clicked.connect(self.next_image)

        self.timer = QTimer()
        self.framerate = 1
        self.timer.start(1000 // self.framerate)
        self.timer.timeout.connect(self.next_image)


        self.setupUI()

    def setupUI(self):
        # Central Widget
        frame = QFrame()

        # Layouts
        main_layout = QVBoxLayout()
        central_layout = QHBoxLayout()
        central_layout.addWidget(self.image_label, alignment=Qt.AlignmentFlag.AlignCenter)
        central_layout.addWidget(self.animation_slider)


        buttons_layout = QVBoxLayout()
        buttons_layout.addWidget(self.next_button)
        buttons_layout.addWidget(self.exit_button)

        main_layout.addLayout(central_layout)
        main_layout.addLayout(buttons_layout)


        frame.setLayout(main_layout)
        self.setCentralWidget(frame)

    def exit_program(self):
        QApplication.quit()

    def next_image(self):
        self.current_pic = (self.current_pic + 1) % self.num_frames
        self.image_label.setPixmap(self.sprites[self.current_pic])

    def frame_rate_change(self):
        self.framerate = self.animation_slider.value()
        self.timer.start(1000 // self.framerate)
        self.timer.timeout.connect(self.next_image)
        print(self.animation_slider.value())


def main():
    app = QApplication([])
    window = Interface()
    window.show()

    app.exec()

if __name__ == "__main__":
    main()
