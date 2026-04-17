import math

from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
# https://github.com/Shushimax/Sprite-Previewer
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

        self.next_button = QPushButton("Start")

        self.animation_slider.valueChanged.connect(self.frame_rate_change)
        self.next_button.clicked.connect(self.stopstart)
        self.isplaying = False

        self.timer = QTimer()
        self.framerate = self.animation_slider.value()
        self.timer.start(1000 // self.framerate)
        self.timer.timeout.connect(self.next_image)

        self.fpsdisplay = QLabel("Frames Per Second:")
        self.fpsdisplay_variable = QLabel(str(self.framerate))


        self.setupUI()

    def setupUI(self):
        # Central Widget
        frame = QFrame()

        #menu bar
        menubar = self.menuBar()
        file_menu = QMenu("&File",self)
        menubar.addMenu(file_menu)
        pause = QAction('Pause',self)
        pause.triggered.connect(self.stop)
        Exit = QAction('Exit',self)
        Exit.triggered.connect(self.close)

        file_menu.addAction(pause)
        file_menu.addAction(Exit)

        # Layouts
        main_layout = QVBoxLayout()
        central_layout = QHBoxLayout()
        central_layout.addWidget(self.image_label, alignment=Qt.AlignmentFlag.AlignCenter)
        central_layout.addWidget(self.animation_slider)

        Fps_layout = QHBoxLayout()
        Fps_layout.addWidget(self.fpsdisplay)
        Fps_layout.addWidget(self.fpsdisplay_variable)


        buttons_layout = QVBoxLayout()
        buttons_layout.addWidget(self.next_button)


        main_layout.addLayout(central_layout)
        main_layout.addLayout(Fps_layout)
        main_layout.addLayout(buttons_layout)


        frame.setLayout(main_layout)
        self.setCentralWidget(frame)



    def next_image(self):
        if self.isplaying:
            self.current_pic = (self.current_pic + 1) % self.num_frames
            self.image_label.setPixmap(self.sprites[self.current_pic])

    def frame_rate_change(self):
        if self.isplaying:
            self.framerate = self.animation_slider.value()
            self.timer.start(1000 // self.framerate)
        self.fpsdisplay_variable.setText(str(self.animation_slider.value()))
        print(self.animation_slider.value())

    def stopstart(self):
        if self.isplaying:
            self.next_button.setText("Start")
            self.isplaying = False
        else:
            self.next_button.setText("Stop")
            self.isplaying = True
            self.frame_rate_change()
            self.timer.start(1000 // self.framerate)

    def stop(self):
        self.next_button.setText("Start")
        self.isplaying = False
        self.timer.stop()



def main():
    app = QApplication([])
    window = Interface()
    window.show()

    app.exec()

if __name__ == "__main__":
    main()
