# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.exporters
from pyqtgraph import PlotWidget
import sounddevice as sd
import soundfile as sf
import numpy as np
import os

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class MainWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.setObjectName(_fromUtf8("MainWindow"))
        self.resize(900, 675)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(900, 675))
        self.setMaximumSize(QtCore.QSize(900, 675))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Consolas"))
        self.setFont(font)
        self.centralwidget = QtGui.QWidget(self)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 901, 671))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setMargin(10)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.info_layout = QtGui.QVBoxLayout()
        self.info_layout.setContentsMargins(11, 10, 10, 10)
        self.info_layout.setSpacing(5)
        self.info_layout.setObjectName(_fromUtf8("info_layout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_settings = QtGui.QLabel(self.horizontalLayoutWidget)
        self.label_settings.setMaximumSize(QtCore.QSize(16777215, 15))
        self.label_settings.setFrameShape(QtGui.QFrame.Box)
        self.label_settings.setObjectName(_fromUtf8("label_settings"))
        self.verticalLayout.addWidget(self.label_settings)
        self.label_select_mode = QtGui.QLabel(self.horizontalLayoutWidget)
        self.label_select_mode.setObjectName(_fromUtf8("label_select_mode"))
        self.verticalLayout.addWidget(self.label_select_mode)
        self.radio_mode_encoder = QtGui.QRadioButton(self.horizontalLayoutWidget)
        self.radio_mode_encoder.setToolTip(_fromUtf8("Mode: DMTF encoder (play tones)"))
        self.radio_mode_encoder.setShortcut(_fromUtf8(""))
        self.radio_mode_encoder.setChecked(True)
        self.radio_mode_encoder.setObjectName(_fromUtf8("radio_mode_encoder"))
        self.verticalLayout.addWidget(self.radio_mode_encoder)
        self.radio_mode_decoder = QtGui.QRadioButton(self.horizontalLayoutWidget)
        self.radio_mode_decoder.setToolTip(_fromUtf8("Mode: DMTF decoder (record tones)"))
        self.radio_mode_decoder.setStatusTip(_fromUtf8(""))
        self.radio_mode_decoder.setObjectName(_fromUtf8("radio_mode_decoder"))
        self.verticalLayout.addWidget(self.radio_mode_decoder)
        spacerItem = QtGui.QSpacerItem(20, 15, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        self.verticalLayout.addItem(spacerItem)
        self.checkBox_saveDTMF = QtGui.QCheckBox(self.horizontalLayoutWidget)
        self.checkBox_saveDTMF.setObjectName(_fromUtf8("checkBox_saveDTMF"))
        self.verticalLayout.addWidget(self.checkBox_saveDTMF)
        self.checkBox_saveDTMF_chart = QtGui.QCheckBox(self.horizontalLayoutWidget)
        self.checkBox_saveDTMF_chart.setObjectName(_fromUtf8("checkBox_saveDTMF_chart"))
        self.verticalLayout.addWidget(self.checkBox_saveDTMF_chart)
        spacerItem4 = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem4)
        self.button_load_file_name = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.button_load_file_name.setObjectName(_fromUtf8("button_load_file_name"))
        self.verticalLayout.addWidget(self.button_load_file_name)
        self.loaded_file_name = QtGui.QLineEdit(self.horizontalLayoutWidget)
        self.loaded_file_name.setEnabled(False)
        self.loaded_file_name.setObjectName(_fromUtf8("loaded_file_name"))
        self.verticalLayout.addWidget(self.loaded_file_name)
        spacerItem1 = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.input_save_audio = QtGui.QLineEdit(self.horizontalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.input_save_audio.sizePolicy().hasHeightForWidth())
        self.input_save_audio.setSizePolicy(sizePolicy)
        self.input_save_audio.setInputMask(_fromUtf8(""))
        self.input_save_audio.setText(_fromUtf8(""))
        self.input_save_audio.setMaxLength(32763)
        self.input_save_audio.setObjectName(_fromUtf8("input_save_audio"))
        self.verticalLayout.addWidget(self.input_save_audio)
        self.button_save_audio_file = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.button_save_audio_file.setObjectName(_fromUtf8("button_save_audio_file"))
        self.verticalLayout.addWidget(self.button_save_audio_file)
        spacerItem2 = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.label_save_charts = QtGui.QLabel(self.horizontalLayoutWidget)
        self.label_save_charts.setObjectName(_fromUtf8("label_save_charts"))
        self.verticalLayout.addWidget(self.label_save_charts)
        self.input_save_graph1 = QtGui.QLineEdit(self.horizontalLayoutWidget)
        self.input_save_graph1.setText(_fromUtf8(""))
        self.input_save_graph1.setObjectName(_fromUtf8("input_save_graph1"))
        self.verticalLayout.addWidget(self.input_save_graph1)
        self.input_save_graph2 = QtGui.QLineEdit(self.horizontalLayoutWidget)
        self.input_save_graph2.setText(_fromUtf8(""))
        self.input_save_graph2.setObjectName(_fromUtf8("input_save_graph2"))
        self.verticalLayout.addWidget(self.input_save_graph2)
        self.button_save_graphs = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.button_save_graphs.setObjectName(_fromUtf8("button_save_graphs"))
        self.verticalLayout.addWidget(self.button_save_graphs)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setSpacing(5)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.dtmf_label = QtGui.QLabel(self.horizontalLayoutWidget)
        self.dtmf_label.setMaximumSize(QtCore.QSize(16777215, 15))
        self.dtmf_label.setFrameShape(QtGui.QFrame.Box)
        self.dtmf_label.setObjectName(_fromUtf8("dtmf_label"))
        self.verticalLayout_2.addWidget(self.dtmf_label)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setSpacing(5)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.dtmf_button_4 = QtGui.QPushButton(self.horizontalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dtmf_button_4.sizePolicy().hasHeightForWidth())
        self.dtmf_button_4.setSizePolicy(sizePolicy)
        self.dtmf_button_4.setStyleSheet(_fromUtf8("font: 75 14pt \"Consolas\";"))
        self.dtmf_button_4.setObjectName(_fromUtf8("dtmf_button_4"))
        self.gridLayout_2.addWidget(self.dtmf_button_4, 1, 1, 1, 1)
        self.dtmf_button_3 = QtGui.QPushButton(self.horizontalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dtmf_button_3.sizePolicy().hasHeightForWidth())
        self.dtmf_button_3.setSizePolicy(sizePolicy)
        self.dtmf_button_3.setStyleSheet(_fromUtf8("font: 75 14pt \"Consolas\";"))
        self.dtmf_button_3.setObjectName(_fromUtf8("dtmf_button_3"))
        self.gridLayout_2.addWidget(self.dtmf_button_3, 0, 3, 1, 1)
        self.dtmf_button_0 = QtGui.QPushButton(self.horizontalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dtmf_button_0.sizePolicy().hasHeightForWidth())
        self.dtmf_button_0.setSizePolicy(sizePolicy)
        self.dtmf_button_0.setStyleSheet(_fromUtf8("font: 75 14pt \"Consolas\";"))
        self.dtmf_button_0.setObjectName(_fromUtf8("dtmf_button_0"))
        self.gridLayout_2.addWidget(self.dtmf_button_0, 3, 2, 1, 1)
        self.dtmf_button_9 = QtGui.QPushButton(self.horizontalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dtmf_button_9.sizePolicy().hasHeightForWidth())
        self.dtmf_button_9.setSizePolicy(sizePolicy)
        self.dtmf_button_9.setStyleSheet(_fromUtf8("font: 75 14pt \"Consolas\";"))
        self.dtmf_button_9.setObjectName(_fromUtf8("dtmf_button_9"))
        self.gridLayout_2.addWidget(self.dtmf_button_9, 2, 3, 1, 1)
        self.dtmf_button_2 = QtGui.QPushButton(self.horizontalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dtmf_button_2.sizePolicy().hasHeightForWidth())
        self.dtmf_button_2.setSizePolicy(sizePolicy)
        self.dtmf_button_2.setStyleSheet(_fromUtf8("font: 75 14pt \"Consolas\";"))
        self.dtmf_button_2.setObjectName(_fromUtf8("dtmf_button_2"))
        self.gridLayout_2.addWidget(self.dtmf_button_2, 0, 2, 1, 1)
        self.dtmf_button_7 = QtGui.QPushButton(self.horizontalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dtmf_button_7.sizePolicy().hasHeightForWidth())
        self.dtmf_button_7.setSizePolicy(sizePolicy)
        self.dtmf_button_7.setStyleSheet(_fromUtf8("font: 75 14pt \"Consolas\";"))
        self.dtmf_button_7.setObjectName(_fromUtf8("dtmf_button_7"))
        self.gridLayout_2.addWidget(self.dtmf_button_7, 2, 1, 1, 1)
        self.dtmf_button_8 = QtGui.QPushButton(self.horizontalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dtmf_button_8.sizePolicy().hasHeightForWidth())
        self.dtmf_button_8.setSizePolicy(sizePolicy)
        self.dtmf_button_8.setStyleSheet(_fromUtf8("font: 75 14pt \"Consolas\";"))
        self.dtmf_button_8.setObjectName(_fromUtf8("dtmf_button_8"))
        self.gridLayout_2.addWidget(self.dtmf_button_8, 2, 2, 1, 1)
        self.dtmf_button_5 = QtGui.QPushButton(self.horizontalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dtmf_button_5.sizePolicy().hasHeightForWidth())
        self.dtmf_button_5.setSizePolicy(sizePolicy)
        self.dtmf_button_5.setStyleSheet(_fromUtf8("font: 75 14pt \"Consolas\";"))
        self.dtmf_button_5.setObjectName(_fromUtf8("dtmf_button_5"))
        self.gridLayout_2.addWidget(self.dtmf_button_5, 1, 2, 1, 1)
        self.dtmf_button_1 = QtGui.QPushButton(self.horizontalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dtmf_button_1.sizePolicy().hasHeightForWidth())
        self.dtmf_button_1.setSizePolicy(sizePolicy)
        self.dtmf_button_1.setStyleSheet(_fromUtf8("font: 75 14pt \"Consolas\";"))
        self.dtmf_button_1.setObjectName(_fromUtf8("dtmf_button_1"))
        self.gridLayout_2.addWidget(self.dtmf_button_1, 0, 1, 1, 1)
        self.dtmf_button_ast = QtGui.QPushButton(self.horizontalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dtmf_button_ast.sizePolicy().hasHeightForWidth())
        self.dtmf_button_ast.setSizePolicy(sizePolicy)
        self.dtmf_button_ast.setStyleSheet(_fromUtf8("font: 75 14pt \"Consolas\";"))
        self.dtmf_button_ast.setObjectName(_fromUtf8("dtmf_button_ast"))
        self.gridLayout_2.addWidget(self.dtmf_button_ast, 3, 1, 1, 1)
        self.dtmf_button_6 = QtGui.QPushButton(self.horizontalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dtmf_button_6.sizePolicy().hasHeightForWidth())
        self.dtmf_button_6.setSizePolicy(sizePolicy)
        self.dtmf_button_6.setStyleSheet(_fromUtf8("font: 75 14pt \"Consolas\";"))
        self.dtmf_button_6.setObjectName(_fromUtf8("dtmf_button_6"))
        self.gridLayout_2.addWidget(self.dtmf_button_6, 1, 3, 1, 1)
        self.dtmf_button_hash = QtGui.QPushButton(self.horizontalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dtmf_button_hash.sizePolicy().hasHeightForWidth())
        self.dtmf_button_hash.setSizePolicy(sizePolicy)
        self.dtmf_button_hash.setStyleSheet(_fromUtf8("font: 75 14pt \"Consolas\";"))
        self.dtmf_button_hash.setObjectName(_fromUtf8("dtmf_button_hash"))
        self.gridLayout_2.addWidget(self.dtmf_button_hash, 3, 3, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_2)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.info_layout.addLayout(self.horizontalLayout_2)
        spacerItem3 = QtGui.QSpacerItem(20, 5, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.info_layout.addItem(spacerItem3)
        self.console_label = QtGui.QLabel(self.horizontalLayoutWidget)
        self.console_label.setMaximumSize(QtCore.QSize(16777215, 15))
        self.console_label.setFrameShape(QtGui.QFrame.Box)
        self.console_label.setObjectName(_fromUtf8("console_label"))
        self.info_layout.addWidget(self.console_label)
        self.console_display = QtGui.QListWidget(self.horizontalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.console_display.sizePolicy().hasHeightForWidth())
        self.console_display.setSizePolicy(sizePolicy)
        self.console_display.setStyleSheet(_fromUtf8("background-color: rgb(0, 0, 0);\n"
                                                    "font: 8pt \"Consolas\";\n"
                                                    "color: rgb(0, 255, 0);"))
        self.console_display.setObjectName(_fromUtf8("console_display"))
        self.console_display.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.console_display.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.info_layout.addWidget(self.console_display)
        self.horizontalLayout.addLayout(self.info_layout)
        self.plot_layout = QtGui.QVBoxLayout()
        self.plot_layout.setMargin(10)
        self.plot_layout.setSpacing(5)
        self.plot_layout.setObjectName(_fromUtf8("plot_layout"))
        self.label_realtime = QtGui.QLabel(self.horizontalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_realtime.sizePolicy().hasHeightForWidth())
        self.label_realtime.setSizePolicy(sizePolicy)
        self.label_realtime.setMaximumSize(QtCore.QSize(16777215, 15))
        self.label_realtime.setFrameShape(QtGui.QFrame.Box)
        self.label_realtime.setObjectName(_fromUtf8("label_realtime"))
        self.plot_layout.addWidget(self.label_realtime)
        self.widget_real_time_plot = PlotWidget(self.horizontalLayoutWidget)
        self.widget_real_time_plot.setObjectName(_fromUtf8("widget_real_time_plot"))
        self.plot_layout.addWidget(self.widget_real_time_plot)
        self.widget_real_time_plot.setRange(xRange=(100,600),yRange=(-2,2))
        self.widget_real_time_plot.setLabel("left", "Amplitude")
        self.widget_real_time_plot.setLabel("bottom", "Time", "seconds")
        self.widget_real_time_plot.setTitle("Real Time Plot")
        self.widget_real_time_plot.setMouseEnabled(y = False)


        self.label_realtime_fourier = QtGui.QLabel(self.horizontalLayoutWidget)
        self.label_realtime_fourier.setMaximumSize(QtCore.QSize(16777215, 15))
        self.label_realtime_fourier.setFrameShape(QtGui.QFrame.Box)
        self.label_realtime_fourier.setObjectName(_fromUtf8("label_realtime_fourier"))
        self.plot_layout.addWidget(self.label_realtime_fourier)
        self.widget_fourier_plot = PlotWidget(self.horizontalLayoutWidget)
        self.widget_fourier_plot.setObjectName(_fromUtf8("widget_fourier_plot"))
        self.plot_layout.addWidget(self.widget_fourier_plot)
        self.widget_fourier_plot.setLabel("left", "Magnitude", "decibels")
        self.widget_fourier_plot.setLabel("bottom", "Frequency", "Hertz")
        self.widget_fourier_plot.setTitle("Real Time Plot - Fourier")
        self.widget_fourier_plot.setMouseEnabled (y = False)
        self.widget_fourier_plot.setRange(xRange=(0,2000),yRange=(0,100))


        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(0, 0, -1, -1)
        self.horizontalLayout_3.setSpacing(5)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.button_record_mic = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.button_record_mic.setObjectName(_fromUtf8("button_record_mic"))
        self.horizontalLayout_3.addWidget(self.button_record_mic)
        self.button_stop_record_mic = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.button_stop_record_mic.setObjectName(_fromUtf8("button_stop_record_mic"))
        self.horizontalLayout_3.addWidget(self.button_stop_record_mic)
        self.plot_layout.addLayout(self.horizontalLayout_3)
        self.label_recording_device = QtGui.QLabel(self.horizontalLayoutWidget)
        self.label_recording_device.setObjectName(_fromUtf8("label_recording_device"))
        self.plot_layout.addWidget(self.label_recording_device)
        self.horizontalLayout.addLayout(self.plot_layout)
        self.setCentralWidget(self.centralwidget)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        #DTMF Buttons Connections
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
            self.button_load_file_name.setEnabled(False)
            self.button_record_mic.setEnabled(False)
            self.button_stop_record_mic.setEnabled(False)
            self.button_save_audio_file.setEnabled(False)
            self.input_save_audio.setEnabled(False)
            self.input_save_graph1.setEnabled(False)
            self.input_save_graph2.setEnabled(False)
            self.button_save_graphs.setEnabled(False)
            self.console("Selected Mode:")
            self.console("    ______                     __")
            self.console("   / ____/___  _________  ____/ /__  _____")
            self.console("  / __/ / __ \/ ___/ __ \/ __  / _ \/ ___/")
            self.console(" / /___/ / / / /__/ /_/ / /_/ /  __/ /")
            self.console("/_____/_/ /_/\___/\____/\__,_/\___/_/")
            self.console("͏͏͏͏          ")
            self.console("͏͏͏͏          ")

        self.radio_mode_decoder.toggled.connect(lambda: self.modeChange("Decoder"))

        #Load Audio File
        self.button_load_file_name.clicked.connect(lambda: self.loadFile())

        self.label_recording_device.setText("Recording Device: {}".format(self.getRecordingDevice()))


    def retranslateUi(self):
        self.setWindowTitle(_translate("MainWindow", "MPMF", None))
        self.label_settings.setText(_translate("MainWindow", "Settings", None))
        self.label_select_mode.setText(_translate("MainWindow", "Select Mode", None))
        self.radio_mode_encoder.setText(_translate("MainWindow", "Encoder", None))
        self.radio_mode_decoder.setText(_translate("MainWindow", "Decoder", None))
        self.checkBox_saveDTMF.setText(_translate("MainWindow", "Save DTMF Tone Audio", None))
        self.checkBox_saveDTMF_chart.setText(_translate("MainWindow", "Save DTMF Tone Chart", None))
        self.button_load_file_name.setText(_translate("MainWindow", "Load audio file", None))
        self.loaded_file_name.setPlaceholderText(_translate("MainWindow", "audio_file.wav", None))
        self.input_save_audio.setPlaceholderText(_translate("MainWindow", "audio_file.wav", None))
        self.button_save_audio_file.setText(_translate("MainWindow", "Save", None))
        self.label_save_charts.setText(_translate("MainWindow", "Save charts", None))
        self.input_save_graph1.setPlaceholderText(_translate("MainWindow", "graph_audio.png", None))
        self.input_save_graph2.setPlaceholderText(_translate("MainWindow", "fourier_audio.png", None))
        self.button_save_graphs.setText(_translate("MainWindow", "Save", None))
        self.dtmf_label.setText(_translate("MainWindow", "DTMF", None))
        self.dtmf_button_4.setText(_translate("MainWindow", "4", None))
        self.dtmf_button_3.setText(_translate("MainWindow", "3", None))
        self.dtmf_button_0.setText(_translate("MainWindow", "0", None))
        self.dtmf_button_9.setText(_translate("MainWindow", "9", None))
        self.dtmf_button_2.setText(_translate("MainWindow", "2", None))
        self.dtmf_button_7.setText(_translate("MainWindow", "7", None))
        self.dtmf_button_8.setText(_translate("MainWindow", "8", None))
        self.dtmf_button_5.setText(_translate("MainWindow", "5", None))
        self.dtmf_button_1.setText(_translate("MainWindow", "1", None))
        self.dtmf_button_ast.setText(_translate("MainWindow", "*", None))
        self.dtmf_button_6.setText(_translate("MainWindow", "6", None))
        self.dtmf_button_hash.setText(_translate("MainWindow", "#", None))
        self.console_label.setText(_translate("MainWindow", "Console", None))
        self.label_realtime.setToolTip(_translate("MainWindow", "Real time data from the source (mic or audio file)", None))
        self.label_realtime.setText(_translate("MainWindow", "Real Time Plot", None))
        self.label_realtime_fourier.setToolTip(_translate("MainWindow", "Fourier transform from data source above", None))
        self.label_realtime_fourier.setText(_translate("MainWindow", "Real Time Plot - Fourier", None))
        self.button_record_mic.setText(_translate("MainWindow", "Record Mic", None))
        self.button_stop_record_mic.setText(_translate("MainWindow", "Stop Mic Recording", None))
        self.label_recording_device.setText(_translate("MainWindow", "Recording Device: ", None))

    def modeChange(self, mode):
        if self.radio_mode_encoder.isChecked():
            self.button_load_file_name.setEnabled(False)
            self.button_record_mic.setEnabled(False)
            self.button_stop_record_mic.setEnabled(False)
            self.unlockButtons()
            self.checkBox_saveDTMF.setEnabled(True)
            self.checkBox_saveDTMF_chart.setEnabled(True)
            self.button_save_audio_file.setEnabled(False)
            self.input_save_audio.setEnabled(False)
            self.input_save_graph1.setEnabled(False)
            self.input_save_graph2.setEnabled(False)
            self.button_save_graphs.setEnabled(False)

            self.cleanConsole()
            self.console("Selected Mode:")
            self.console("    ______                     __")
            self.console("   / ____/___  _________  ____/ /__  _____")
            self.console("  / __/ / __ \/ ___/ __ \/ __  / _ \/ ___/")
            self.console(" / /___/ / / / /__/ /_/ / /_/ /  __/ /")
            self.console("/_____/_/ /_/\___/\____/\__,_/\___/_/")
            self.console("͏͏͏͏          ")
            self.console("͏͏͏͏          ")

        if self.radio_mode_decoder.isChecked():
            self.button_load_file_name.setEnabled(True)
            self.button_record_mic.setEnabled(True)
            self.button_stop_record_mic.setEnabled(True)
            self.lockButtons()
            self.checkBox_saveDTMF.setEnabled(False)
            self.checkBox_saveDTMF_chart.setEnabled(False)
            self.button_save_audio_file.setEnabled(True)
            self.input_save_audio.setEnabled(True)
            self.input_save_graph1.setEnabled(True)
            self.input_save_graph2.setEnabled(True)
            self.button_save_graphs.setEnabled(True)

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
        self.plotData(audio_data)

    def saveFile(self, fileName, audio):
        fs = 44100
        if self.radio_mode_encoder.isChecked():
            if fileName == "*":
                fileName = "asterisk"
            if fileName == "#":
                fileName = "hashtag"

            filePath = "./audio/original/" + "tone_" + str(fileName) + ".wav"
            sf.write(filePath, audio, fs)
            self.console("Tone {0} was saved as: {1}".format(fileName, filePath))

        if self.radio_mode_decoder.isChecked():
            filePath = "./audio/received/" + str(fileName)
            sf.write(filePath, audio, fs, format="PCM_24")
            self.console("Recorded audio file saved as: {}").format(filePath) 

    def savePlotData(self, fileName, item_plot):
        exporter = pg.exporters.ImageExporter(item_plot.plotItem)
        if self.radio_mode_encoder.isChecked():
            if fileName == "*":
                fileName = "asterisk"
            if fileName == "#":
                fileName = "hashtag"

            filePath = "./img/encoder/original/" + "tone_" + str(fileName) + ".png"
            exporter.export(filePath)
            self.console("Tone {0} chart was saved as: {1}".format(fileName, filePath))

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
        self.fs = 44100
        created_tone = self.createToneWave(self.getTone(tone))
        self.lockButtons()
        sd.play(created_tone, self.fs)
        sd.wait()
        
        self.console("Tone {0} was reproduced".format(tone))

        if self.checkBox_saveDTMF.isChecked():
            self.saveFile(tone, created_tone)

        self.unlockButtons()
        self.plotData(created_tone)

        if self.checkBox_saveDTMF_chart.isChecked():
            self.savePlotData(tone, self.widget_real_time_plot)

    def createToneWave(self, tone):
        self.periodo = 1
        self.duration = 5
        self.fs = 44100
        
        x = np.linspace(0, self.periodo, self.fs * self.periodo)
        lower, higher = tone
        return np.sin(2 * np.pi * x * lower) + np.sin(2 * np.pi * x * higher)

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
        self.widget_real_time_plot.plot(data)
        self.plotDataFourier(data)


    def plotDataFourier(self, data):
        audio_fft = self.FFT(data)[0:len(data)//2]
        self.widget_fourier_plot.plot(abs(audio_fft), clear = True)
        self.getNotoriousPeaks(audio_fft)

    def getNotoriousPeaks(self, data):
        from scipy.signal import argrelextrema
        peaks = argrelextrema(data, np.greater) #array of indexes of the locals maxima
        print(peaks[0:2])
        
        
    def getRecordingDevice(self):
        record, play = sd.default.device
        record_device = sd.query_devices(record, "input").get("name")
        return(record_device)

    def recordMic(self):
        return()



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
    

if __name__ == '__main__':
    app = QtGui.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_() 
