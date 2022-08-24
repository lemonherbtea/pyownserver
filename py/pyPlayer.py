from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QStyle, QSlider, QFileDialog
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import *
import sys
import worker



#Requiere un codec, instalar aca https://codecguide.com/
class WWindow(QWidget):




    def __init__(self):

        super().__init__()
        self.setWindowIcon(QIcon())
        self.setWindowTitle("YouHub")
        self.setGeometry(250,100, 700,500)

        p = self.palette()
        p.setColor(QPalette.Window,Qt.lightGray)
        self.setPalette(p)
        self.create_player()
        self.thread = QThread()
        self.worker = worker.Worker(self.mediaPlayer.play, self.mediaPlayer.pause)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.do_work)
        self.thread.start()


    def create_player(self):

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videowidget = QVideoWidget()

        self.openBtn = QPushButton('Abrir video')


        self.playBtn = QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.openBtn.clicked.connect(self.open_file)
        self.playBtn.clicked.connect(self.toggle_video)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0,0)
        self.slider.sliderMoved.connect(self.set_position)



        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)

        hbox.addWidget(self.openBtn)
        hbox.addWidget(self.playBtn)
        hbox.addWidget(self.slider)

        vbox = QVBoxLayout()
        vbox.addWidget(videowidget)
        vbox.addLayout(hbox)

        self.mediaPlayer.setVideoOutput(videowidget)

        self.setLayout(vbox)

        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Abrir video')

        if filename != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.playBtn.setEnabled(True)

    def toggle_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
            print("abc")
        elif self.mediaPlayer.state() != QMediaPlayer.PlayingState:
            self.mediaPlayer.play()
            print("def")



    def mediastate_changed(self, state):
        if self.mediaPlayer.state()== QMediaPlayer.PlayingState:
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))


        else:
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))


    def position_changed(self,position):
        self.slider.setValue(position)


    def duration_changed(self,duration):
        self.slider.setRange(0,duration)

    def set_position(self,position):
        self.mediaPlayer.setPosition(position)

app = QApplication(sys.argv)
window = WWindow()
window.show()
sys.exit(app.exec_())
