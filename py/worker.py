from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QStyle, QSlider, QFileDialog
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
import sys
from PyQt5.QtCore import *
import os
workingClass = "C:\\"


class Worker(QObject):

    finished = pyqtSignal()  # give worker class a finished signal

    def __init__(self,start_video_function,stop_video_function,parent=None):
        QObject.__init__(self, parent=parent)
        self.continue_run = True  # provide a bool run condition for the class

        self.start_video_function=start_video_function
        self.stop_video_function=stop_video_function

    def do_work(self):

        while (1):
            if ("workingClass.lock" in os.listdir("C:\\Users\\isaac\\Desktop")):
                self.start_video_function()
            else:
                self.stop_video_function()

    def stop(self):
        self.continue_run = False  # set the run condition to false on stop