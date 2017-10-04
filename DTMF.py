# -*- coding: utf-8 -*-
from PyQt4 import QtGui,QtCore
import pyqtgraph as pg
import pyqtgraph.exporters
import numpy as np
import soundfile as sf
import sounddevice as sd
import sys
import os
import ui_DTMF
import SWHear

class DTMF(QtGui.QMainWindow, ui_DTMF. Ui_MainWindow):
    def __init__(self, parent=None):
        super(DTMF, self).__init__(parent)
        self.setupUi(self)
        self.periodo = 1
        self.duration = 5
        self.fs = 44100
        self.maxFFT=0
        self.maxPCM=0
        self.decoding = False
        self.ear = SWHear.SWHear(rate = self.fs, updatesPerSecond = 20)
        self.pen = pyqtgraph.mkPen(color='g')

        #Real Plot Configuration
        self.widget_real_time_plot.setLabel("left", "Amplitude")
        self.widget_real_time_plot.setLabel("bottom", "Time", "seconds")
        self.widget_real_time_plot.setTitle("Real Time Plot")
        self.widget_real_time_plot.setMouseEnabled(y = False)
        self.widget_real_time_plot.showGrid(True, True, 0.5)       

        #Fourier Plot Configuration
        self.widget_fourier_plot.setLabel("left", "Magnitude", "decibels")
        self.widget_fourier_plot.setLabel("bottom", "Frequency", "Hertz")
        self.widget_fourier_plot.setTitle("Real Time Plot - Fourier")
        self.widget_fourier_plot.setMouseEnabled (y = False)
        self.widget_fourier_plot.setRange(xRange=(0,2000),yRange=(0,100))
        self.widget_fourier_plot.showGrid(True, True, 0.5)

        #DTMF Buttons
        self.dtmf_button_0.clicked.connect(lambda: self.makeTone(0))
        self.dtmf_button_1.clicked.connect(lambda: self.makeTone(1)) 
        self.dtmf_button_2.clicked.connect(lambda: self.makeTone(2)) 
        self.dtmf_button_3.clicked.connect(lambda: self.makeTone(3)) 
        self.dtmf_button_4.clicked.connect(lambda: self.makeTone(4)) 
        self.dtmf_button_5.clicked.connect(lambda: self.makeTone(5)) 
        self.dtmf_button_6.clicked.connect(lambda: self.makeTone(6)) 
        self.dtmf_button_7.clicked.connect(lambda: self.makeTone(7)) 
        self.dtmf_button_8.clicked.connect(lambda: self.makeTone(8)) 
        self.dtmf_button_9.clicked.connect(lambda: self.makeTone(9)) 
        self.dtmf_button_ast.clicked.connect(lambda: self.makeTone("*")) 
        self.dtmf_button_hash.clicked.connect(lambda: self.makeTone("#"))

        #Mode Selection
        if self.radio_mode_encoder.isChecked():
            self.unlockButtons()
            self.button_load_file_name.setEnabled(False)
            self.checkBox_saveDTMF_detected.setEnabled(False)
            self.checkBox_saveDTMF_chart.setEnabled(True)
            self.checkBox_saveDTMF_audio.setEnabled(True)
            self.cleanConsole()
            self.console("Selected Mode:")
            self.console("    ______                     __")
            self.console("   / ____/___  _________  ____/ /__  _____")
            self.console("  / __/ / __ \/ ___/ __ \/ __  / _ \/ ___/")
            self.console(" / /___/ / / / /__/ /_/ / /_/ /  __/ /")
            self.console("/_____/_/ /_/\___/\____/\__,_/\___/_/")
            self.console("͏͏͏͏          ")
            self.console("͏͏͏͏          ")

        #Mode Changer
        self.radio_mode_decoder.toggled.connect(lambda: self.modeChange("Decoder"))

        #Load File Button
        self.button_load_file_name.clicked.connect(lambda: self.loadFile())

    def modeChange(self, mode):
        if self.radio_mode_encoder.isChecked():
            self.unlockButtons()
            self.button_load_file_name.setEnabled(False)
            self.checkBox_saveDTMF_detected.setEnabled(False)
            self.checkBox_saveDTMF_chart.setEnabled(True)
            self.checkBox_saveDTMF_audio.setEnabled(True)
            self.cleanConsole()
            self.decoding = False
            self.console("Selected Mode:")
            self.console("    ______                     __")
            self.console("   / ____/___  _________  ____/ /__  _____")
            self.console("  / __/ / __ \/ ___/ __ \/ __  / _ \/ ___/")
            self.console(" / /___/ / / / /__/ /_/ / /_/ /  __/ /")
            self.console("/_____/_/ /_/\___/\____/\__,_/\___/_/")
            self.console("͏͏͏͏          ")
            self.console("͏͏͏͏          ")

        if self.radio_mode_decoder.isChecked():
            self.lockButtons()
            self.button_load_file_name.setEnabled(True)
            self.checkBox_saveDTMF_detected.setEnabled(True)
            self.checkBox_saveDTMF_chart.setEnabled(False)
            self.checkBox_saveDTMF_audio.setEnabled(False)
            self.decoding = True
            self.ear.stream_start()
            self.update()
            self.cleanConsole()
            self.console("Selected Mode:")
            self.console("    ____                      __")
            self.console("   / __ \___  _________  ____/ /__  _____")
            self.console("  / / / / _ \/ ___/ __ \/ __  / _ \/ ___/")
            self.console(" / /_/ /  __/ /__/ /_/ / /_/ /  __/ /")
            self.console("/_____/\___/\___/\____/\__,_/\___/_/")
            self.console("͏͏͏͏          ")
            self.console("͏͏͏͏          ")


    def loadFile(self):
        directory = os.getcwd()
        fileLocation = QtGui.QFileDialog.getOpenFileName(self, 'Open file', directory, "WAVE Files (*.wav)")
        path, fileName = os.path.split(fileLocation)
        self.loaded_file_name.setText(fileName)
        self.console("Audio File Loaded from: {}".format(fileLocation))
        audio_data, fs = sf.read(fileLocation)
        self.decoding = False
        self.plotData(audio_data)

    def saveFile(self, fileName, audio):
        if self.radio_mode_encoder.isChecked():
            if fileName == "*":
                fileName = "asterisk"
            if fileName == "#":
                fileName = "hashtag"

            filePath = "./audio/original/" + "tone_" + str(fileName) + ".wav"
            sf.write(filePath, audio, self.fs)
            self.console("Tone {0} was saved as: {1}".format(fileName, filePath))

        if self.radio_mode_decoder.isChecked():
            filePath = "./audio/received/" + str(fileName)
            sf.write(filePath, audio, self.fs)
            self.console("Recorded audio file saved as: {}".format(filePath))

    def savePlotData(self, fileName, item_plot1, item_plot2):
        exporter1 = pg.exporters.ImageExporter(item_plot1.plotItem)
        exporter2 = pg.exporters.ImageExporter(item_plot2.plotItem)
        if self.radio_mode_encoder.isChecked():
            if fileName == "*":
                fileName = "asterisk"
            if fileName == "#":
                fileName = "hashtag"

            filePath = "./img/encoder/original/" + "tone_" + str(fileName) + ".png"
            exporter1.export(filePath)
            self.console("Tone {0} chart was saved as: {1}".format(fileName, filePath))

            filePath = "./img/encoder/fourier/" + "tone_" + str(fileName) + "_fourier" + ".png"
            exporter2.export(filePath)
            self.console("Tone {0} fourier chart was saved as: {1}".format(fileName, filePath))

        if self.radio_mode_decoder.isChecked():
            filePath = "./audio/received/" + str(fileName)
            self.console("The data chart was saved as: {}").format(filePath) 

    def getTone(self, tone):
        DTMF = {1: (697, 1209),
                2: (697, 1336),
                3: (697, 1477),
                4: (770, 1209),
                5: (770, 1336),
                6: (770, 1477),
                7: (852, 1209),
                8: (852, 1336),
                9: (852, 1477),
                "*": (941, 1209),
                0: (941, 1336),
                "#": (941, 1477),
                } 
        return DTMF.get(tone)

    def makeTone(self, tone):
        created_tone = self.createToneWave(self.getTone(tone))
        self.lockButtons()
        sd.play(created_tone, self.fs)
        sd.wait()
        
        self.console("Tone {0} was reproduced".format(tone))

        if self.checkBox_saveDTMF_audio.isChecked():
            self.saveFile(tone, created_tone)

        self.plotData(created_tone)

        if self.checkBox_saveDTMF_chart.isChecked():
            self.savePlotData(tone, self.widget_real_time_plot, self.widget_fourier_plot)

        self.unlockButtons()

    def createToneWave(self, tone):      
        x = np.linspace(0, self.periodo, self.fs * self.periodo)
        lower, higher = tone
        return (((np.sin(2 * np.pi * x * lower) + np.sin(2 * np.pi * x * higher))*1.0)/2)

    def console(self, text):
        item = QtGui.QListWidgetItem()
        item.setText(text)
        item.setFlags(QtCore.Qt.NoItemFlags)
        self.console_display.addItem(item)
        
    def cleanConsole(self):
        self.console_display.clear()

    def FFT(self, data):
        from scipy.fftpack import fft

        fourier_data = fft(data)
        return(fourier_data)

    def plotData(self, data):
        self.widget_real_time_plot.clear()
        self.widget_real_time_plot.setLabel("left", "Amplitude")
        self.widget_real_time_plot.setLabel("bottom", "Time", "seconds")
        self.widget_real_time_plot.setTitle("Real Time Plot")
        self.widget_real_time_plot.setMouseEnabled(y = False)
        self.widget_real_time_plot.setMouseEnabled(x = True)
        self.widget_real_time_plot.showGrid(True, True, 0.5)  
        self.widget_real_time_plot.setRange(xRange=(100,600),yRange=(-2,2))
        self.widget_real_time_plot.plot(data, pen=self.pen)

        self.plotDataFourier(data)

    def plotDataFourier(self, data):
        self.widget_fourier_plot.clear()
        self.widget_fourier_plot.setLabel("left", "Magnitude", "decibels")
        self.widget_fourier_plot.setLabel("bottom", "Frequency", "Hertz")
        self.widget_fourier_plot.setTitle("Real Time Plot - Fourier")
        self.widget_fourier_plot.setMouseEnabled (y = False)
        self.widget_fourier_plot.setMouseEnabled(x = False)
        self.widget_fourier_plot.showGrid(True, True, 0.5)
        self.widget_fourier_plot.setRange(xRange=(0,2000),yRange=(0,100))
        audio_fft = self.FFT(data)[0:len(data)//2]
        self.widget_fourier_plot.plot(abs(audio_fft), pen=self.pen, clear = True)
        self.getNotoriousPeaks(audio_fft)

    def getNotoriousPeaks(self, data):
        from scipy.signal import argrelextrema
        peaks = argrelextrema(data, np.greater) #array of indexes of the locals maxima
        print(peaks[0:2])
     
    def lockButtons(self):
        self.dtmf_button_0.setEnabled(False)
        self.dtmf_button_1.setEnabled(False)
        self.dtmf_button_2.setEnabled(False)
        self.dtmf_button_3.setEnabled(False)
        self.dtmf_button_4.setEnabled(False)
        self.dtmf_button_5.setEnabled(False)
        self.dtmf_button_6.setEnabled(False)
        self.dtmf_button_7.setEnabled(False)
        self.dtmf_button_8.setEnabled(False)
        self.dtmf_button_9.setEnabled(False)
        self.dtmf_button_ast.setEnabled(False)
        self.dtmf_button_hash.setEnabled(False)
    
    def unlockButtons(self):
        self.dtmf_button_0.setEnabled(True)
        self.dtmf_button_1.setEnabled(True)
        self.dtmf_button_2.setEnabled(True)
        self.dtmf_button_3.setEnabled(True)
        self.dtmf_button_4.setEnabled(True)
        self.dtmf_button_5.setEnabled(True)
        self.dtmf_button_6.setEnabled(True)
        self.dtmf_button_7.setEnabled(True)
        self.dtmf_button_8.setEnabled(True)
        self.dtmf_button_9.setEnabled(True)
        self.dtmf_button_ast.setEnabled(True)
        self.dtmf_button_hash.setEnabled(True)

    def update(self):
        if self.decoding == True:
            if not self.ear.data is None:
                pcmMax = np.max(np.abs(self.ear.data))
                if pcmMax>self.maxPCM:
                    self.maxPCM = pcmMax
                    self.widget_real_time_plot.setRange(yRange = [-pcmMax, pcmMax])

                if np.max(self.ear.fft)>self.maxFFT:
                    self.maxFFT=np.max(np.abs(self.ear.fft))
                    self.widget_fourier_plot.plotItem.setRange(yRange=[0,self.maxFFT])
                    self.widget_fourier_plot.plotItem.setRange(yRange=[0,1])

                self.pbLevel.setValue(1000*pcmMax/self.maxPCM)
                self.widget_real_time_plot.setMouseEnabled(x = False)
                self.widget_fourier_plot.plot(self.ear.fftx,self.ear.fft/self.maxFFT,pen=self.pen,clear=True)
                self.widget_real_time_plot.plot(self.ear.datax, self.ear.data, pen=self.pen, clear=True)
            
            QtCore.QTimer.singleShot(1, self.update)
        else:
            self.ear.close()

if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    window = DTMF()
    window.show()
    app.exec_() 
