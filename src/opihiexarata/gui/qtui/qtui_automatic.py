# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'automatic.ui'
##
## Created by: Qt User Interface Compiler version 6.3.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QMainWindow, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_AutomaticWindow(object):
    def setupUi(self, AutomaticWindow):
        if not AutomaticWindow.objectName():
            AutomaticWindow.setObjectName(u"AutomaticWindow")
        AutomaticWindow.resize(621, 360)
        self.centralwidget = QWidget(AutomaticWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(9, 9, 601, 341))
        font = QFont()
        font.setFamilies([u"Cantarell"])
        font.setPointSize(12)
        self.verticalLayoutWidget.setFont(font)
        self.vertical_layout_automatic = QVBoxLayout(self.verticalLayoutWidget)
        self.vertical_layout_automatic.setObjectName(u"vertical_layout_automatic")
        self.vertical_layout_automatic.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout_directory = QHBoxLayout()
        self.horizontal_layout_directory.setObjectName(u"horizontal_layout_directory")
        self.label_static_fits_directory = QLabel(self.verticalLayoutWidget)
        self.label_static_fits_directory.setObjectName(u"label_static_fits_directory")
        self.label_static_fits_directory.setFont(font)

        self.horizontal_layout_directory.addWidget(self.label_static_fits_directory)

        self.label_dynamic_fits_directory = QLabel(self.verticalLayoutWidget)
        self.label_dynamic_fits_directory.setObjectName(u"label_dynamic_fits_directory")
        self.label_dynamic_fits_directory.setFont(font)

        self.horizontal_layout_directory.addWidget(self.label_dynamic_fits_directory)

        self.line_4 = QFrame(self.verticalLayoutWidget)
        self.line_4.setObjectName(u"line_4")
        font1 = QFont()
        font1.setFamilies([u"Cantarell"])
        self.line_4.setFont(font1)
        self.line_4.setFrameShape(QFrame.VLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.horizontal_layout_directory.addWidget(self.line_4)

        self.push_button_change_directory = QPushButton(self.verticalLayoutWidget)
        self.push_button_change_directory.setObjectName(u"push_button_change_directory")
        self.push_button_change_directory.setFont(font)

        self.horizontal_layout_directory.addWidget(self.push_button_change_directory)


        self.vertical_layout_automatic.addLayout(self.horizontal_layout_directory)

        self.line_7 = QFrame(self.verticalLayoutWidget)
        self.line_7.setObjectName(u"line_7")
        self.line_7.setFont(font1)
        self.line_7.setFrameShape(QFrame.HLine)
        self.line_7.setFrameShadow(QFrame.Sunken)

        self.vertical_layout_automatic.addWidget(self.line_7)

        self.horizontal_layout_engines = QHBoxLayout()
        self.horizontal_layout_engines.setObjectName(u"horizontal_layout_engines")
        self.label_static_engines = QLabel(self.verticalLayoutWidget)
        self.label_static_engines.setObjectName(u"label_static_engines")
        self.label_static_engines.setFont(font1)

        self.horizontal_layout_engines.addWidget(self.label_static_engines)

        self.combo_box_astrometry_engine = QComboBox(self.verticalLayoutWidget)
        self.combo_box_astrometry_engine.addItem("")
        self.combo_box_astrometry_engine.addItem("")
        self.combo_box_astrometry_engine.setObjectName(u"combo_box_astrometry_engine")
        self.combo_box_astrometry_engine.setFont(font1)

        self.horizontal_layout_engines.addWidget(self.combo_box_astrometry_engine)

        self.combo_box_photometry_engine = QComboBox(self.verticalLayoutWidget)
        self.combo_box_photometry_engine.addItem("")
        self.combo_box_photometry_engine.setObjectName(u"combo_box_photometry_engine")
        self.combo_box_photometry_engine.setFont(font1)

        self.horizontal_layout_engines.addWidget(self.combo_box_photometry_engine)


        self.vertical_layout_automatic.addLayout(self.horizontal_layout_engines)

        self.line_2 = QFrame(self.verticalLayoutWidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFont(font1)
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.vertical_layout_automatic.addWidget(self.line_2)

        self.grid_layout_fits_filenames = QGridLayout()
        self.grid_layout_fits_filenames.setObjectName(u"grid_layout_fits_filenames")
        self.label_dynamic_results_filename = QLabel(self.verticalLayoutWidget)
        self.label_dynamic_results_filename.setObjectName(u"label_dynamic_results_filename")
        self.label_dynamic_results_filename.setFont(font1)

        self.grid_layout_fits_filenames.addWidget(self.label_dynamic_results_filename, 1, 1, 1, 1)

        self.label_static_results_filename = QLabel(self.verticalLayoutWidget)
        self.label_static_results_filename.setObjectName(u"label_static_results_filename")
        self.label_static_results_filename.setFont(font1)

        self.grid_layout_fits_filenames.addWidget(self.label_static_results_filename, 1, 0, 1, 1)

        self.label_static_working_filename = QLabel(self.verticalLayoutWidget)
        self.label_static_working_filename.setObjectName(u"label_static_working_filename")
        self.label_static_working_filename.setFont(font1)

        self.grid_layout_fits_filenames.addWidget(self.label_static_working_filename, 0, 0, 1, 1)

        self.label_dynamic_working_filename = QLabel(self.verticalLayoutWidget)
        self.label_dynamic_working_filename.setObjectName(u"label_dynamic_working_filename")
        self.label_dynamic_working_filename.setFont(font1)

        self.grid_layout_fits_filenames.addWidget(self.label_dynamic_working_filename, 0, 1, 1, 1)


        self.vertical_layout_automatic.addLayout(self.grid_layout_fits_filenames)

        self.horizontal_layout_astrometry_results = QHBoxLayout()
        self.horizontal_layout_astrometry_results.setObjectName(u"horizontal_layout_astrometry_results")
        self.label_static_ra_dec = QLabel(self.verticalLayoutWidget)
        self.label_static_ra_dec.setObjectName(u"label_static_ra_dec")
        self.label_static_ra_dec.setFont(font1)

        self.horizontal_layout_astrometry_results.addWidget(self.label_static_ra_dec)

        self.label_dynamic_ra = QLabel(self.verticalLayoutWidget)
        self.label_dynamic_ra.setObjectName(u"label_dynamic_ra")
        self.label_dynamic_ra.setFont(font1)

        self.horizontal_layout_astrometry_results.addWidget(self.label_dynamic_ra)

        self.label_dynamic_dec = QLabel(self.verticalLayoutWidget)
        self.label_dynamic_dec.setObjectName(u"label_dynamic_dec")
        self.label_dynamic_dec.setFont(font1)

        self.horizontal_layout_astrometry_results.addWidget(self.label_dynamic_dec)

        self.line_9 = QFrame(self.verticalLayoutWidget)
        self.line_9.setObjectName(u"line_9")
        self.line_9.setFont(font1)
        self.line_9.setFrameShape(QFrame.VLine)
        self.line_9.setFrameShadow(QFrame.Sunken)

        self.horizontal_layout_astrometry_results.addWidget(self.line_9)

        self.label_dynamic_date = QLabel(self.verticalLayoutWidget)
        self.label_dynamic_date.setObjectName(u"label_dynamic_date")
        self.label_dynamic_date.setFont(font1)
        self.label_dynamic_date.setAlignment(Qt.AlignCenter)

        self.horizontal_layout_astrometry_results.addWidget(self.label_dynamic_date)

        self.label_dynamic_time = QLabel(self.verticalLayoutWidget)
        self.label_dynamic_time.setObjectName(u"label_dynamic_time")
        self.label_dynamic_time.setFont(font1)
        self.label_dynamic_time.setAlignment(Qt.AlignCenter)

        self.horizontal_layout_astrometry_results.addWidget(self.label_dynamic_time)


        self.vertical_layout_automatic.addLayout(self.horizontal_layout_astrometry_results)

        self.horizontal_layout_photometry_results = QHBoxLayout()
        self.horizontal_layout_photometry_results.setObjectName(u"horizontal_layout_photometry_results")
        self.label_static_zero_point = QLabel(self.verticalLayoutWidget)
        self.label_static_zero_point.setObjectName(u"label_static_zero_point")
        self.label_static_zero_point.setFont(font1)

        self.horizontal_layout_photometry_results.addWidget(self.label_static_zero_point)

        self.label_dynamic_zero_point = QLabel(self.verticalLayoutWidget)
        self.label_dynamic_zero_point.setObjectName(u"label_dynamic_zero_point")
        self.label_dynamic_zero_point.setFont(font1)

        self.horizontal_layout_photometry_results.addWidget(self.label_dynamic_zero_point)

        self.line_5 = QFrame(self.verticalLayoutWidget)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFont(font1)
        self.line_5.setFrameShape(QFrame.VLine)
        self.line_5.setFrameShadow(QFrame.Sunken)

        self.horizontal_layout_photometry_results.addWidget(self.line_5)

        self.label_static_filter = QLabel(self.verticalLayoutWidget)
        self.label_static_filter.setObjectName(u"label_static_filter")
        self.label_static_filter.setFont(font1)

        self.horizontal_layout_photometry_results.addWidget(self.label_static_filter)

        self.label_dynamic_filter = QLabel(self.verticalLayoutWidget)
        self.label_dynamic_filter.setObjectName(u"label_dynamic_filter")
        self.label_dynamic_filter.setFont(font1)

        self.horizontal_layout_photometry_results.addWidget(self.label_dynamic_filter)


        self.vertical_layout_automatic.addLayout(self.horizontal_layout_photometry_results)

        self.line = QFrame(self.verticalLayoutWidget)
        self.line.setObjectName(u"line")
        self.line.setFont(font)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.vertical_layout_automatic.addWidget(self.line)

        self.horizontal_layout_start_stop = QHBoxLayout()
        self.horizontal_layout_start_stop.setObjectName(u"horizontal_layout_start_stop")
        self.label_static_operational_status = QLabel(self.verticalLayoutWidget)
        self.label_static_operational_status.setObjectName(u"label_static_operational_status")
        self.label_static_operational_status.setFont(font1)

        self.horizontal_layout_start_stop.addWidget(self.label_static_operational_status)

        self.label_dynamic_operational_status = QLabel(self.verticalLayoutWidget)
        self.label_dynamic_operational_status.setObjectName(u"label_dynamic_operational_status")
        self.label_dynamic_operational_status.setFont(font1)
        self.label_dynamic_operational_status.setAlignment(Qt.AlignCenter)

        self.horizontal_layout_start_stop.addWidget(self.label_dynamic_operational_status)

        self.push_button_start = QPushButton(self.verticalLayoutWidget)
        self.push_button_start.setObjectName(u"push_button_start")
        self.push_button_start.setFont(font1)

        self.horizontal_layout_start_stop.addWidget(self.push_button_start)

        self.push_button_stop = QPushButton(self.verticalLayoutWidget)
        self.push_button_stop.setObjectName(u"push_button_stop")
        self.push_button_stop.setFont(font1)

        self.horizontal_layout_start_stop.addWidget(self.push_button_stop)

        self.line_3 = QFrame(self.verticalLayoutWidget)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFont(font1)
        self.line_3.setFrameShape(QFrame.VLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.horizontal_layout_start_stop.addWidget(self.line_3)

        self.push_button_trigger = QPushButton(self.verticalLayoutWidget)
        self.push_button_trigger.setObjectName(u"push_button_trigger")
        self.push_button_trigger.setFont(font1)

        self.horizontal_layout_start_stop.addWidget(self.push_button_trigger)


        self.vertical_layout_automatic.addLayout(self.horizontal_layout_start_stop)

        AutomaticWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(AutomaticWindow)

        QMetaObject.connectSlotsByName(AutomaticWindow)
    # setupUi

    def retranslateUi(self, AutomaticWindow):
        AutomaticWindow.setWindowTitle(QCoreApplication.translate("AutomaticWindow", u"OpihiExarata Automatic Mode", None))
        self.label_static_fits_directory.setText(QCoreApplication.translate("AutomaticWindow", u"Fetch Directory:", None))
        self.label_dynamic_fits_directory.setText(QCoreApplication.translate("AutomaticWindow", u"/path/to/fits/directory/", None))
        self.push_button_change_directory.setText(QCoreApplication.translate("AutomaticWindow", u"Change", None))
        self.label_static_engines.setText(QCoreApplication.translate("AutomaticWindow", u"Engines (A, P)", None))
        self.combo_box_astrometry_engine.setItemText(0, QCoreApplication.translate("AutomaticWindow", u"Astrometry.net Nova", None))
        self.combo_box_astrometry_engine.setItemText(1, QCoreApplication.translate("AutomaticWindow", u"Astrometry.net Host", None))

        self.combo_box_photometry_engine.setItemText(0, QCoreApplication.translate("AutomaticWindow", u"Pan-STARRS 3pi DR2 MAST", None))

        self.label_dynamic_results_filename.setText(QCoreApplication.translate("AutomaticWindow", u"opi.20XXA999.YYMMDD.AAAAAAAAA.00001.b.fits", None))
        self.label_static_results_filename.setText(QCoreApplication.translate("AutomaticWindow", u"Results:", None))
        self.label_static_working_filename.setText(QCoreApplication.translate("AutomaticWindow", u"Working:", None))
        self.label_dynamic_working_filename.setText(QCoreApplication.translate("AutomaticWindow", u"opi.20XXA999.YYMMDD.AAAAAAAAA.00001.a.fits", None))
        self.label_static_ra_dec.setText(QCoreApplication.translate("AutomaticWindow", u"Coordinates", None))
        self.label_dynamic_ra.setText(QCoreApplication.translate("AutomaticWindow", u"RR:RR:RR.RRR", None))
        self.label_dynamic_dec.setText(QCoreApplication.translate("AutomaticWindow", u"+DD:DD:DD.DDD", None))
        self.label_dynamic_date.setText(QCoreApplication.translate("AutomaticWindow", u"YYYY-MM-DD", None))
        self.label_dynamic_time.setText(QCoreApplication.translate("AutomaticWindow", u"HH:MM:SS.S", None))
        self.label_static_zero_point.setText(QCoreApplication.translate("AutomaticWindow", u"Zero Point", None))
        self.label_dynamic_zero_point.setText(QCoreApplication.translate("AutomaticWindow", u"ZZZ.ZZZ", None))
        self.label_static_filter.setText(QCoreApplication.translate("AutomaticWindow", u"Filter", None))
        self.label_dynamic_filter.setText(QCoreApplication.translate("AutomaticWindow", u"FF", None))
        self.label_static_operational_status.setText(QCoreApplication.translate("AutomaticWindow", u"Loop Status", None))
        self.label_dynamic_operational_status.setText(QCoreApplication.translate("AutomaticWindow", u"Default", None))
        self.push_button_start.setText(QCoreApplication.translate("AutomaticWindow", u"Start", None))
        self.push_button_stop.setText(QCoreApplication.translate("AutomaticWindow", u"Stop", None))
        self.push_button_trigger.setText(QCoreApplication.translate("AutomaticWindow", u"Trigger", None))
    # retranslateUi

