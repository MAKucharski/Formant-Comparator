import pygame
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QCheckBox, QFileDialog
from PyQt5 import QtGui
from PyQt5.QtCore import QRect
from PyQt5 import QtCore
from pylab import*
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile
import scipy.signal as sig

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
        self.showMaximized()

        self.show()

    def load_file(self):
        filename = self.open_filename_dialog()
        fig, (ax, ax2, ax3) = plt.subplots(3, figsize=(10, 5))

        rate, data = wavfile.read(filename)
        print(rate)
        pygame.mixer.pre_init(rate, -16, 2, 2048)
        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.3)
        pygame.init()
        pygame.mixer.music.load(filename)

        time = np.arange(0, len(data)) / rate
        freq, tim, amplitude1 = sig.spectrogram(data, fs=rate, window=np.hamming(2048), nperseg=2048, noverlap=1536,
                            scaling='spectrum', mode='magnitude')

        Ts = 1.0 / rate;
        t = np.arange(0, 1, Ts)
        T = t[1] - t[0]
        N = data.size
        print(N)
        fft = np.fft.fft(data)[0:int(np.floor(N / 2))] / N

        f = np.linspace(0, 1 / T, N)
        fft[1:] = 2 * fft[1:]

        #second file
        filename2 = self.open_filename_dialog2()
        fig2, (ax4, ax5, ax6) = plt.subplots(3, figsize=(10, 5))

        rate2, data2 = wavfile.read(filename2)

        time2 = np.arange(0, len(data2)) / rate2

        freq2, tim2, amplitude2 = sig.spectrogram(data2, fs=rate2, window=np.hamming(2048), nperseg=2048, noverlap=1536,
                            scaling='spectrum', mode='magnitude')

        Ts2 = 1.0 / rate2;
        t2 = np.arange(0, 1, Ts2)
        T2 = t2[1] - t2[0]
        N2 = data2.size
        fft2 = np.fft.fft(data2)[0:int(np.floor(N2 / 2))] / N2

        f2 = np.linspace(0, 1 / T2, N2)
        fft2[1:] = 2 * fft2[1:]

        ax.plot(time, data)
        ax2.set_xscale('log')
        ax2.set_yscale('log')
        ax2.plot(f[:N // 2], np.abs(fft)[:N // 2] * 1 / N)
        ax3.specgram(data, Fs=rate)

        ax.set(xlabel='Time[s]', ylabel='Amplitude')
        ax.title.set_text('Time Course')
        ax2.set(xlabel='Frequency[Hz]', ylabel='Amplitude')
        ax2.title.set_text('Spectrum')
        ax3.set(xlabel='Time [s]', ylabel='Frequency [Hz]')
        ax3.title.set_text('Spectrogram')

        ax4.plot(time2, data2)
        ax5.set_xscale('log')
        ax5.set_yscale('log')
        ax5.plot(f[:N2 // 2], np.abs(fft2)[:N2 // 2] * 1 / N2)
        ax6.specgram(data2, Fs=rate2)

        ax4.set(xlabel='Time[s]', ylabel='Amplitude')
        ax4.title.set_text('Time Course')
        ax5.set(xlabel='Frequency[Hz]', ylabel='Amplitude')
        ax5.title.set_text('Spectrum')
        ax6.set(xlabel='Time [s]', ylabel='Frequency [Hz]')
        ax6.title.set_text('Spectrogram')

        nr_rows, nr_columns = amplitude1.shape
        table = amplitude2.copy()
        for i in range(nr_columns - amplitude2.shape[1]):
            table = np.insert(table, table.shape[1], 0, axis=1)
        table.resize(nr_rows, nr_columns)
        differ = np.subtract(amplitude1, table)
        print(differ)

        plt.figure(figsize=(16, 8
                            ))
        plt.pcolormesh(tim, freq, differ)
        plt.xlabel('Time [s]')
        plt.ylabel('Frequency [Hz]')
        plt.title('Difference between files')
        plt.ylim(0, 8000)
        plt.colorbar()
        plt.show()

    def open_filename_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Choose First Audio File!", "", "All Files (*)", options=options)
        if fileName:
            return fileName

    def open_filename_dialog2(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Choose Second Audio File!", "", "All Files (*)", options=options)
        if fileName:
            return fileName

    def ui_components(self):
        playbutton = QPushButton("Play", self)
        stopbutton = QPushButton("Stop", self)
        rewindbutton = QPushButton("Rewind", self)
        pausebutton = QPushButton("Pause", self)
        unpausebutton = QPushButton("Unpause", self)

        playbutton.setGeometry(QRect(100,50, 75, 50))
        playbutton.setToolTip("Plays the file")
        playbutton.clicked.connect(self.click_play)

        stopbutton.setGeometry(QRect(100, 150, 75, 50))
        stopbutton.clicked.connect(self.click_stop)

        rewindbutton.setGeometry(QRect(100, 250, 75, 50))
        rewindbutton.clicked.connect(self.click_rewind)

        pausebutton.setGeometry(QRect(100, 350, 75, 50))
        pausebutton.clicked.connect(self.click_pause)

        unpausebutton.setGeometry(QRect(100, 450, 75, 50))
        unpausebutton.clicked.connect(self.click_unpause)

        openfolderbutton = QPushButton("Load Files", self)
        openfolderbutton.setGeometry(QRect(350, 50, 100, 50))
        openfolderbutton.setToolTip("Opens two window dialogs one by one and lets you to choose two files you want to compare")
        openfolderbutton.clicked.connect(self.load_file)
        openfolderbutton.clicked.connect(self.mixer_quit)

        self.b = QCheckBox("Loop", self)
        self.b.stateChanged.connect(self.checkbox_loop)

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

    def mixer_quit(self):
        pygame.mixer.quit()


App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())




