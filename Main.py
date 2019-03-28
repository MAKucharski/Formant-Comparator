import pygame
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QInputDialog, QCheckBox, QFileDialog, QLabel, QGridLayout
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtGui
from PyQt5.QtCore import QRect
from PyQt5 import QtCore
import os
from pylab import*
import scipy.io.wavfile as wavefile
import matplotlib.pyplot as plt
from scipy.fftpack import fft
import numpy as np
from scipy.io import wavfile


#filename = ""
#currentsong = ""
name = ""


class Window(QMainWindow,QWidget):
    name = ""
    def __init__(self):
        super().__init__()

        self.title = "Formant Comparator"
        self.top = 100
        self.left = 100
        self.width = 1000
        self.height = 1000
        self.init_window()

    def init_window(self):
        self.setWindowIcon(QtGui.QIcon("Untitled.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.ui_components()
        self.load_file()


        self.show()

    def load_file(self):
        filename = self.open_filename_dialog()  #ścieżka do pliku audio
        fig, (ax, ax2, ax3) = plt.subplots(3, figsize=(15, 8))
        rate, data = wavfile.read(filename) #załadowanie pliku WAVE --> zamienić na libsndfile
        print(rate)
        pygame.mixer.pre_init(rate, -16, 2, 2048) #nie działa za drugim razem
        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.3)
        pygame.init()
        pygame.mixer.music.load(filename)

        time = np.arange(0, len(data)) / rate

        Ts = 1.0 / rate;  # sampling interval
        t = np.arange(0, 1, Ts)  # time vector
        T = t[1] - t[0]
        y = np.sin(2 * np.pi * 500 * t)  #funkcja testowa sinus
        N = data.size
        print(N)
        fft = np.fft.fft(data)[0:int(np.floor(N / 2))] / N  # FFT function from numpy

        f = np.linspace(0, 1 / T, N)
        fft[1:] = 2 * fft[1:]  # need to take the single-sided spectrum only

        ax=self.figure.add_subplot(111)
        ax.plot(time, data)
        self.canvas.draw()
        ax2.set_xscale('log')
        ax2.set_yscale('log')
        ax2.plot(f[:N // 2], np.abs(fft)[:N // 2] * 1 / N)
        ax3.specgram(data, Fs=rate) #nie działa dla plików stereo

        ax.set(xlabel='Time[s]', ylabel='Amplitude')

        plt.show()
        global name
        if name !="":
            QLabel.clear(self)
        name = os.path.basename(filename)
        currentsong = QLabel("Now playing: " + name, self)

        currentsong.setGeometry(QRect(400, 5, 150, 50))
        print (name)

    def open_filename_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Choose Audio File!", "", "All Files (*)", options=options)
        if fileName:
            return fileName

    def ui_components(self):
        playbutton = QPushButton(self)
        stopbutton = QPushButton(self)
        rewindbutton = QPushButton("Rewind", self)
        pausebutton = QPushButton(self)
        unpausebutton = QPushButton(self)

        playbutton.setGeometry(QRect(100,50, 35,35))
        playbutton.setIcon(QtGui.QIcon("playbutton1.png"))
        playbutton.setIconSize(QtCore.QSize(25,25))
        playbutton.setToolTip("Plays the file")
        playbutton.clicked.connect(self.click_play)

        stopbutton.setGeometry(QRect(150, 50, 35, 35))
        stopbutton.setIcon(QtGui.QIcon("stopbutton.png"))
        stopbutton.setIconSize(QtCore.QSize(25, 25))
        stopbutton.clicked.connect(self.click_stop)

        rewindbutton.setGeometry(QRect(200, 50, 35, 35))
        rewindbutton.clicked.connect(self.click_rewind)

        pausebutton.setGeometry(QRect(250, 50, 35, 35))
        pausebutton.setIcon(QtGui.QIcon("pausebutton.png"))
        pausebutton.setIconSize(QtCore.QSize(25, 25))
        pausebutton.clicked.connect(self.click_pause)

        unpausebutton.setGeometry(QRect(300, 50, 35, 35))
        unpausebutton.setIcon(QtGui.QIcon("unpausebutton.png"))
        unpausebutton.setIconSize(QtCore.QSize(25, 25))
        unpausebutton.clicked.connect(self.click_unpause)

        openfolderbutton = QPushButton("Load another file", self)
        openfolderbutton.setGeometry(QRect(350, 50, 35, 35))
        openfolderbutton.clicked.connect(self.load_file)

        self.b = QCheckBox("Loop", self)
        self.b.stateChanged.connect(self.checkbox_loop)


        self.figure = plt.figure(figsize=(15,5))
        self.canvas = FigureCanvas(self.figure)


    def get_position(self):
        return pygame.mixer.music.get_pos()

    def click_play(self):
        pygame.mixer.music.play(loops=0)

    def click_stop(self):
        pygame.mixer.music.stop()

    def click_rewind(self):
        pygame.mixer.music.rewind()

    def click_pause(self):
        pygame.mixer.music.pause()

    def click_unpause(self):
        pygame.mixer.music.unpause()

    def checkbox_loop(self, state):
        if state == QtCore.Qt.Checked:
            pygame.mixer.music.play(loops=-1)
        else:
            pygame.mixer.music.play(loops=0)



App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())




