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
        self.pbLevel.setValue(0)

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
            self.button_record_mic.setEnabled(False)
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

        self.button_record_mic.clicked.connect(lambda: self.recordMic())

    def modeChange(self, mode):
        if self.radio_mode_encoder.isChecked():
            self.unlockButtons()
            self.button_load_file_name.setEnabled(False)
            self.checkBox_saveDTMF_detected.setEnabled(False)
            self.button_record_mic.setEnabled(False)
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
            self.button_record_mic.setEnabled(True)
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
        self.decoding = False
        directory = os.getcwd()
        fileLocation = QtGui.QFileDialog.getOpenFileName(self, 'Open file', directory, "WAVE Files (*.wav)")
        path, fileName = os.path.split(fileLocation)
        self.loaded_file_name.setText(fileName)
        self.console("Audio File Loaded from: {}".format(fileLocation))
        audio_data, fs = sf.read(fileLocation)
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
            filePath = "./img/decoder/original/" + "tone_" + str(fileName) + ".png"
            exporter1.export(filePath)
            self.console("Tone {0} chart was saved as: {1}".format(fileName, filePath))

            filePath = "./img/decoder/fourier/" + "tone_" + str(fileName) + "_fourier" + ".png"
            exporter2.export(filePath)
            self.console("Tone {0} fourier chart was saved as: {1}".format(fileName, filePath))

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
        N = len(data)
        fourier_data = fft(data)
        #y = fourier_data[0:N // 2]
        return fourier_data[0:N // 2]

    def plotData(self, data):
        self.widget_real_time_plot.clear()
        self.widget_real_time_plot.setLabel("left", "Amplitude")
        self.widget_real_time_plot.setLabel("bottom", "Time", "seconds")
        self.widget_real_time_plot.setTitle("Real Time Plot")
        self.widget_real_time_plot.setMouseEnabled(y = True)
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
        self.widget_fourier_plot.setMouseEnabled(x = True)
        self.widget_fourier_plot.showGrid(True, True, 0.5)
        self.widget_fourier_plot.setRange(xRange=(0,2000),yRange=(0,100))
        audio_fft = self.FFT(data)
        self.widget_fourier_plot.plot(abs(audio_fft), pen=self.pen, clear = True)
        #self.getNotoriousPeaks(audio_fft)
        self.getPeaks(audio_fft)          
            
    def getPeaks(self, data):
        from peakDetect import peakdet
        #print(abs(data))
        peaks, _ = peakdet(abs(data), 50)

        peaks_feq = [item[0] for item in peaks]

        #print(peaks)
        if self.radio_mode_encoder.isChecked():
            self.console("These frequencies were detected in the FFT: {}Hz, {}Hz".format(peaks[0][0],peaks[1][0]))
            if 697-5 <= peaks[0][0] <= 697+5 and 1209-5 <= peaks[1][0] <= 1209+5:
                    self.console("Which indicates that the tone reproduced was: {}".format("1"))
            elif 697-5 <= peaks[0][0] <= 697+5 and 1336-5 <= peaks[1][0] <= 1336+5:
                    self.console("Which indicates that the tone reproduced was: {}".format("2"))
            elif 697-5 <= peaks[0][0] <= 697+5 and 1477-5 <= peaks[1][0] <= 1477+5:
                    self.console("Which indicates that the tone reproduced was: {}".format("3"))
            elif 770-5 <= peaks[0][0] <= 770+5 and 1209-5 <= peaks[1][0] <= 1209+5:
                    self.console("Which indicates that the tone reproduced was: {}".format("4"))
            elif 770-5 <= peaks[0][0] <= 770+5 and 1336-5 <= peaks[1][0] <= 1336+5:
                    self.console("Which indicates that the tone reproduced was: {}".format("5"))
            elif 770-5 <= peaks[0][0] <= 770+5 and 1477-5 <= peaks[1][0] <= 1477+5:
                    self.console("Which indicates that the tone reproduced was: {}".format("6"))
            elif 852-5 <= peaks[0][0] <= 852+5 and 1209-5 <= peaks[1][0] <= 1209+5:
                    self.console("Which indicates that the tone reproduced was: {}".format("7"))
            elif 852-5 <= peaks[0][0] <= 852+5 and 1336-5 <= peaks[1][0] <= 1336+5:
                    self.console("Which indicates that the tone reproduced was: {}".format("8"))
            elif 852-5 <= peaks[0][0] <= 852+5 and 1477-5 <= peaks[1][0] <= 1477+5:
                    self.console("Which indicates that the tone reproduced was: {}".format("9"))
            elif 941-5 <= peaks[0][0] <= 941+5 and 1209-5 <= peaks[1][0] <= 1209+5:
                    self.console("Which indicates that the tone reproduced was: {}".format("*"))
            elif 941-5 <= peaks[0][0] <= 941+5 and 1336-5 <= peaks[1][0] <= 1336+5:
                    self.console("Which indicates that the tone reproduced was: {}".format("0"))
            elif 941-5 <= peaks[0][0] <= 941+5 and 1477-5 <= peaks[1][0] <= 1477+5:
                    self.console("Which indicates that the tone reproduced was: {}".format("#"))
            else:
                self.console("Tone not detected")
            self.console("͏͏͏͏          ")

        if self.radio_mode_decoder.isChecked():
            peaks_found = self.getOnlyNiceFeq(peaks)
            self.console("These frequencies were detected in the FFT: {}Hz, {}Hz".format(peaks_found[0],peaks_found[1]))
            if 697-5 <= peaks_found[0] <= 697+5 and 1209-5 <= peaks_found[1] <= 1209+5:
                    self.console("Which indicates that the tone reproduced was: {}".format("1"))
                    if self.checkBox_saveDTMF_detected.isChecked():
                        self.savePlotData("1", self.widget_real_time_plot, self.widget_fourier_plot)
                        self.renameFile("./audio/received/" + "{}".format(self.loaded_file_name.text()) , "./audio/received/recorded_tone_1.wav")
            elif 697-5 <= peaks_found[0] <= 697+5 and 1336-5 <= peaks_found[1] <= 1336+5:
                    self.console("Which indicates that the tone reproduced was: {}".format("2"))
                    if self.checkBox_saveDTMF_detected.isChecked():
                        self.savePlotData("2", self.widget_real_time_plot, self.widget_fourier_plot)
                        self.renameFile("./audio/received/" + "{}".format(self.loaded_file_name.text()) , "./audio/received/recorded_tone_2.wav")
            elif 697-5 <= peaks_found[0] <= 697+5 and 1477-5 <= peaks_found[1] <= 1477+5:
                    self.console("Which indicates that the tone reproduced was: {}".format("3"))
                    if self.checkBox_saveDTMF_detected.isChecked():
                        self.savePlotData("3", self.widget_real_time_plot, self.widget_fourier_plot)
                        self.renameFile("./audio/received/" + "{}".format(self.loaded_file_name.text()) , "./audio/received/recorded_tone_3.wav")
            elif 770-5 <= peaks_found[0] <= 770+5 and 1209-5 <= peaks_found[1] <= 1209+5:
                    self.console("Which indicates that the tone reproduced was: {}".format("4"))
                    if self.checkBox_saveDTMF_detected.isChecked():
                        self.savePlotData("4", self.widget_real_time_plot, self.widget_fourier_plot)
                        self.renameFile("./audio/received/" + "{}".format(self.loaded_file_name.text()) , "./audio/received/recorded_tone_4.wav")
            elif 770-5 <= peaks_found[0] <= 770+5 and 1336-5 <= peaks_found[1] <= 1336+5:
                    self.console("Which indicates that the tone reproduced was: {}".format("5"))
                    if self.checkBox_saveDTMF_detected.isChecked():
                        self.savePlotData("5", self.widget_real_time_plot, self.widget_fourier_plot)
                        self.renameFile("./audio/received/" + "{}".format(self.loaded_file_name.text()) , "./audio/received/recorded_tone_5.wav")
            elif 770-5 <= peaks_found[0] <= 770+5 and 1477-5 <= peaks_found[1] <= 1477+5:
                    self.console("Which indicates that the tone reproduced was: {}".format("6"))
                    if self.checkBox_saveDTMF_detected.isChecked():
                        self.savePlotData("6", self.widget_real_time_plot, self.widget_fourier_plot)
                        self.renameFile("./audio/received/" + "{}".format(self.loaded_file_name.text()) , "./audio/received/recorded_tone_6.wav")
            elif 852-5 <= peaks_found[0] <= 852+5 and 1209-5 <= peaks_found[1] <= 1209+5:
                    self.console("Which indicates that the tone reproduced was: {}".format("7"))
                    if self.checkBox_saveDTMF_detected.isChecked():
                        self.savePlotData("7", self.widget_real_time_plot, self.widget_fourier_plot)
                        self.renameFile("./audio/received/" + "{}".format(self.loaded_file_name.text()) , "./audio/received/recorded_tone_7.wav")
            elif 852-5 <= peaks_found[0] <= 852+5 and 1336-5 <= peaks_found[1] <= 1336+5:
                    self.console("Which indicates that the tone reproduced was: {}".format("8"))
                    if self.checkBox_saveDTMF_detected.isChecked():
                        self.savePlotData("8", self.widget_real_time_plot, self.widget_fourier_plot)
                        self.renameFile("./audio/received/" + "{}".format(self.loaded_file_name.text()) , "./audio/received/recorded_tone_8.wav")
            elif 852-5 <= peaks_found[0] <= 852+5 and 1477-5 <= peaks_found[1] <= 1477+5:
                    self.console("Which indicates that the tone reproduced was: {}".format("9"))
                    if self.checkBox_saveDTMF_detected.isChecked():
                        self.savePlotData("9", self.widget_real_time_plot, self.widget_fourier_plot)
                        self.renameFile("./audio/received/" + "{}".format(self.loaded_file_name.text()) , "./audio/received/recorded_tone_9.wav")
            elif 941-5 <= peaks_found[0] <= 941+5 and 1209-5 <= peaks_found[1] <= 1209+5:
                    self.console("Which indicates that the tone reproduced was: {}".format("*"))
                    if self.checkBox_saveDTMF_detected.isChecked():
                        self.savePlotData("asterisk", self.widget_real_time_plot, self.widget_fourier_plot)
                        self.renameFile("./audio/received/" + "{}".format(self.loaded_file_name.text()) , "./audio/received/recorded_tone_asterisk.wav")
            elif 941-5 <= peaks_found[0] <= 941+5 and 1336-5 <= peaks_found[1] <= 1336+5:
                    self.console("Which indicates that the tone reproduced was: {}".format("0"))
                    if self.checkBox_saveDTMF_detected.isChecked():
                        self.savePlotData("0", self.widget_real_time_plot, self.widget_fourier_plot)
                        self.renameFile("./audio/received/" + "{}".format(self.loaded_file_name.text()) , "./audio/received/recorded_tone_0.wav")
            elif 941-5 <= peaks_found[0] <= 941+5 and 1477-5 <= peaks_found[1] <= 1477+5:
                    self.console("Which indicates that the tone reproduced was: {}".format("#"))
                    if self.checkBox_saveDTMF_detected.isChecked():
                        self.savePlotData("hashtag", self.widget_real_time_plot, self.widget_fourier_plot)
                        self.renameFile("./audio/received/" + "{}".format(self.loaded_file_name.text()) , "./audio/received/recorded_tone_hashtag.wav")
            else:
                self.console("Tone not detected")
                self.console("These are some frenquecies that were notable in the audio:")
                self.console("{}".format(peaks_feq))
            self.console("͏͏͏͏          ")
            
    def getOnlyNiceFeq(self, data):
        data_low = data
        data_high = data

        dataset_low = [item[0] for item in data_low]
        l1 = list(filter(lambda x: x > 691, dataset_low))
        low_feq = list(filter(lambda x: x < 946, l1))
        rl = np.mean(low_feq)

        dataset_high = [item[0] for item in data_high]
        h1 = list(filter(lambda x: x > 1204, dataset_high))
        high_feq = list(filter(lambda x: x < 1481, h1))
        rh = np.mean(high_feq)

        return rl, rh

    def renameFile(self, fileOld, fileNew):
        os.rename(fileOld, fileNew)
        self.console("The file {} was renamed to: {}".format(fileOld,fileNew))

    def recordMic(self):
        audio = sd.rec(1*self.fs, channels = 1)
        print ("Mic recording... ")
        sd.wait()
        y = audio[:,0]

        import uuid
        filename = "recorded_" + str(uuid.uuid4()) + ".wav"

        self.saveFile(filename, y)

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
                self.widget_real_time_plot.setMouseEnabled(x = True)
                self.widget_fourier_plot.plot(self.ear.fftx, abs(self.ear.fft)/self.maxFFT,pen=self.pen,clear=True)
                self.widget_real_time_plot.plot(self.ear.datax, self.ear.data, pen=self.pen, clear=True)
                # audio_fft = self.FFT(self.ear.data)
                # self.getPeaks(audio_fft)
            QtCore.QTimer.singleShot(1, self.update)
        else:
            self.ear.close()

if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    window = DTMF()
    window.show()
    app.exec_() 
