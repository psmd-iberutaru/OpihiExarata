# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'automatic.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class Ui_AutomaticWindow(object):
    def setupUi(self, AutomaticWindow):
        if not AutomaticWindow.objectName():
            AutomaticWindow.setObjectName("AutomaticWindow")
        AutomaticWindow.resize(600, 360)
        self.centralwidget = QWidget(AutomaticWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(9, 9, 581, 341))
        font = QFont()
        font.setFamilies(["Sylfaen"])
        font.setPointSize(12)
        self.verticalLayoutWidget.setFont(font)
        self.vertical_layout_automatic = QVBoxLayout(self.verticalLayoutWidget)
        self.vertical_layout_automatic.setObjectName("vertical_layout_automatic")
        self.vertical_layout_automatic.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout_directory = QHBoxLayout()
        self.horizontal_layout_directory.setObjectName("horizontal_layout_directory")
        self.label_static_fits_directory = QLabel(self.verticalLayoutWidget)
        self.label_static_fits_directory.setObjectName("label_static_fits_directory")
        self.label_static_fits_directory.setFont(font)

        self.horizontal_layout_directory.addWidget(self.label_static_fits_directory)

        self.label_dynamic_fits_directory = QLabel(self.verticalLayoutWidget)
        self.label_dynamic_fits_directory.setObjectName("label_dynamic_fits_directory")
        self.label_dynamic_fits_directory.setFont(font)

        self.horizontal_layout_directory.addWidget(self.label_dynamic_fits_directory)

        self.line_4 = QFrame(self.verticalLayoutWidget)
        self.line_4.setObjectName("line_4")
        self.line_4.setFrameShape(QFrame.VLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.horizontal_layout_directory.addWidget(self.line_4)

        self.push_button_change_directory = QPushButton(self.verticalLayoutWidget)
        self.push_button_change_directory.setObjectName("push_button_change_directory")
        self.push_button_change_directory.setFont(font)

        self.horizontal_layout_directory.addWidget(self.push_button_change_directory)

        self.vertical_layout_automatic.addLayout(self.horizontal_layout_directory)

        self.line_7 = QFrame(self.verticalLayoutWidget)
        self.line_7.setObjectName("line_7")
        self.line_7.setFrameShape(QFrame.HLine)
        self.line_7.setFrameShadow(QFrame.Sunken)

        self.vertical_layout_automatic.addWidget(self.line_7)

        self.horizontal_layout_engines = QHBoxLayout()
        self.horizontal_layout_engines.setObjectName("horizontal_layout_engines")
        self.label_static_engines = QLabel(self.verticalLayoutWidget)
        self.label_static_engines.setObjectName("label_static_engines")

        self.horizontal_layout_engines.addWidget(self.label_static_engines)

        self.combo_box_astrometry_engine = QComboBox(self.verticalLayoutWidget)
        self.combo_box_astrometry_engine.addItem("")
        self.combo_box_astrometry_engine.addItem("")
        self.combo_box_astrometry_engine.setObjectName("combo_box_astrometry_engine")

        self.horizontal_layout_engines.addWidget(self.combo_box_astrometry_engine)

        self.combo_box_photometry_engine = QComboBox(self.verticalLayoutWidget)
        self.combo_box_photometry_engine.addItem("")
        self.combo_box_photometry_engine.setObjectName("combo_box_photometry_engine")

        self.horizontal_layout_engines.addWidget(self.combo_box_photometry_engine)

        self.vertical_layout_automatic.addLayout(self.horizontal_layout_engines)

        self.line_2 = QFrame(self.verticalLayoutWidget)
        self.line_2.setObjectName("line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.vertical_layout_automatic.addWidget(self.line_2)

        self.grid_layout_fits_filenames = QGridLayout()
        self.grid_layout_fits_filenames.setObjectName("grid_layout_fits_filenames")
        self.label_dynamic_results_filename = QLabel(self.verticalLayoutWidget)
        self.label_dynamic_results_filename.setObjectName(
            "label_dynamic_results_filename"
        )

        self.grid_layout_fits_filenames.addWidget(
            self.label_dynamic_results_filename, 1, 1, 1, 1
        )

        self.label_static_results_filename = QLabel(self.verticalLayoutWidget)
        self.label_static_results_filename.setObjectName(
            "label_static_results_filename"
        )

        self.grid_layout_fits_filenames.addWidget(
            self.label_static_results_filename, 1, 0, 1, 1
        )

        self.label_static_working_filename = QLabel(self.verticalLayoutWidget)
        self.label_static_working_filename.setObjectName(
            "label_static_working_filename"
        )

        self.grid_layout_fits_filenames.addWidget(
            self.label_static_working_filename, 0, 0, 1, 1
        )

        self.label_dynamic_working_filename = QLabel(self.verticalLayoutWidget)
        self.label_dynamic_working_filename.setObjectName(
            "label_dynamic_working_filename"
        )

        self.grid_layout_fits_filenames.addWidget(
            self.label_dynamic_working_filename, 0, 1, 1, 1
        )

        self.vertical_layout_automatic.addLayout(self.grid_layout_fits_filenames)

        self.horizontal_layout_astrometry_results = QHBoxLayout()
        self.horizontal_layout_astrometry_results.setObjectName(
            "horizontal_layout_astrometry_results"
        )
        self.label_static_ra_dec = QLabel(self.verticalLayoutWidget)
        self.label_static_ra_dec.setObjectName("label_static_ra_dec")

        self.horizontal_layout_astrometry_results.addWidget(self.label_static_ra_dec)

        self.label_dynamic_ra = QLabel(self.verticalLayoutWidget)
        self.label_dynamic_ra.setObjectName("label_dynamic_ra")

        self.horizontal_layout_astrometry_results.addWidget(self.label_dynamic_ra)

        self.label_dynamic_dec = QLabel(self.verticalLayoutWidget)
        self.label_dynamic_dec.setObjectName("label_dynamic_dec")

        self.horizontal_layout_astrometry_results.addWidget(self.label_dynamic_dec)

        self.line_9 = QFrame(self.verticalLayoutWidget)
        self.line_9.setObjectName("line_9")
        self.line_9.setFrameShape(QFrame.VLine)
        self.line_9.setFrameShadow(QFrame.Sunken)

        self.horizontal_layout_astrometry_results.addWidget(self.line_9)

        self.label_dynamic_date = QLabel(self.verticalLayoutWidget)
        self.label_dynamic_date.setObjectName("label_dynamic_date")
        self.label_dynamic_date.setAlignment(Qt.AlignCenter)

        self.horizontal_layout_astrometry_results.addWidget(self.label_dynamic_date)

        self.label_dynamic_time = QLabel(self.verticalLayoutWidget)
        self.label_dynamic_time.setObjectName("label_dynamic_time")
        self.label_dynamic_time.setAlignment(Qt.AlignCenter)

        self.horizontal_layout_astrometry_results.addWidget(self.label_dynamic_time)

        self.vertical_layout_automatic.addLayout(
            self.horizontal_layout_astrometry_results
        )

        self.horizontal_layout_photometry_results = QHBoxLayout()
        self.horizontal_layout_photometry_results.setObjectName(
            "horizontal_layout_photometry_results"
        )
        self.label_static_zero_point = QLabel(self.verticalLayoutWidget)
        self.label_static_zero_point.setObjectName("label_static_zero_point")

        self.horizontal_layout_photometry_results.addWidget(
            self.label_static_zero_point
        )

        self.label_dynamic_zero_point = QLabel(self.verticalLayoutWidget)
        self.label_dynamic_zero_point.setObjectName("label_dynamic_zero_point")

        self.horizontal_layout_photometry_results.addWidget(
            self.label_dynamic_zero_point
        )

        self.line_5 = QFrame(self.verticalLayoutWidget)
        self.line_5.setObjectName("line_5")
        self.line_5.setFrameShape(QFrame.VLine)
        self.line_5.setFrameShadow(QFrame.Sunken)

        self.horizontal_layout_photometry_results.addWidget(self.line_5)

        self.label_static_filter = QLabel(self.verticalLayoutWidget)
        self.label_static_filter.setObjectName("label_static_filter")

        self.horizontal_layout_photometry_results.addWidget(self.label_static_filter)

        self.label_dynamic_filter = QLabel(self.verticalLayoutWidget)
        self.label_dynamic_filter.setObjectName("label_dynamic_filter")

        self.horizontal_layout_photometry_results.addWidget(self.label_dynamic_filter)

        self.vertical_layout_automatic.addLayout(
            self.horizontal_layout_photometry_results
        )

        self.line = QFrame(self.verticalLayoutWidget)
        self.line.setObjectName("line")
        self.line.setFont(font)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.vertical_layout_automatic.addWidget(self.line)

        self.horizontal_layout_start_stop = QHBoxLayout()
        self.horizontal_layout_start_stop.setObjectName("horizontal_layout_start_stop")
        self.label_static_operational_status = QLabel(self.verticalLayoutWidget)
        self.label_static_operational_status.setObjectName(
            "label_static_operational_status"
        )

        self.horizontal_layout_start_stop.addWidget(
            self.label_static_operational_status
        )

        self.label_dynamic_operational_status = QLabel(self.verticalLayoutWidget)
        self.label_dynamic_operational_status.setObjectName(
            "label_dynamic_operational_status"
        )
        self.label_dynamic_operational_status.setAlignment(Qt.AlignCenter)

        self.horizontal_layout_start_stop.addWidget(
            self.label_dynamic_operational_status
        )

        self.push_button_start = QPushButton(self.verticalLayoutWidget)
        self.push_button_start.setObjectName("push_button_start")

        self.horizontal_layout_start_stop.addWidget(self.push_button_start)

        self.push_button_stop = QPushButton(self.verticalLayoutWidget)
        self.push_button_stop.setObjectName("push_button_stop")

        self.horizontal_layout_start_stop.addWidget(self.push_button_stop)

        self.line_3 = QFrame(self.verticalLayoutWidget)
        self.line_3.setObjectName("line_3")
        self.line_3.setFrameShape(QFrame.VLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.horizontal_layout_start_stop.addWidget(self.line_3)

        self.push_button_trigger = QPushButton(self.verticalLayoutWidget)
        self.push_button_trigger.setObjectName("push_button_trigger")

        self.horizontal_layout_start_stop.addWidget(self.push_button_trigger)

        self.vertical_layout_automatic.addLayout(self.horizontal_layout_start_stop)

        AutomaticWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(AutomaticWindow)

        QMetaObject.connectSlotsByName(AutomaticWindow)

    # setupUi

    def retranslateUi(self, AutomaticWindow):
        AutomaticWindow.setWindowTitle(
            QCoreApplication.translate(
                "AutomaticWindow", "OpihiExarata Automatic Mode", None
            )
        )
        self.label_static_fits_directory.setText(
            QCoreApplication.translate("AutomaticWindow", "Fetch Directory:", None)
        )
        self.label_dynamic_fits_directory.setText(
            QCoreApplication.translate(
                "AutomaticWindow", "/path/to/fits/directory/", None
            )
        )
        self.push_button_change_directory.setText(
            QCoreApplication.translate("AutomaticWindow", "Change", None)
        )
        self.label_static_engines.setText(
            QCoreApplication.translate("AutomaticWindow", "Engines (A, P)", None)
        )
        self.combo_box_astrometry_engine.setItemText(
            0,
            QCoreApplication.translate("AutomaticWindow", "Astrometry.net Nova", None),
        )
        self.combo_box_astrometry_engine.setItemText(
            1,
            QCoreApplication.translate("AutomaticWindow", "Astrometry.net Host", None),
        )

        self.combo_box_photometry_engine.setItemText(
            0,
            QCoreApplication.translate(
                "AutomaticWindow", "Pan-STARRS 3pi DR2 MAST", None
            ),
        )

        self.label_dynamic_results_filename.setText(
            QCoreApplication.translate(
                "AutomaticWindow", "opi.20XXA999.YYMMDD.AAAAAAAAA.00001.b.fits", None
            )
        )
        self.label_static_results_filename.setText(
            QCoreApplication.translate("AutomaticWindow", "Results:", None)
        )
        self.label_static_working_filename.setText(
            QCoreApplication.translate("AutomaticWindow", "Working:", None)
        )
        self.label_dynamic_working_filename.setText(
            QCoreApplication.translate(
                "AutomaticWindow", "opi.20XXA999.YYMMDD.AAAAAAAAA.00001.a.fits", None
            )
        )
        self.label_static_ra_dec.setText(
            QCoreApplication.translate("AutomaticWindow", "Coordinates", None)
        )
        self.label_dynamic_ra.setText(
            QCoreApplication.translate("AutomaticWindow", "RR:RR:RR.RRR", None)
        )
        self.label_dynamic_dec.setText(
            QCoreApplication.translate("AutomaticWindow", "+DD:DD:DD.DDD", None)
        )
        self.label_dynamic_date.setText(
            QCoreApplication.translate("AutomaticWindow", "YYYY-MM-DD", None)
        )
        self.label_dynamic_time.setText(
            QCoreApplication.translate("AutomaticWindow", "HH:MM:SS.S", None)
        )
        self.label_static_zero_point.setText(
            QCoreApplication.translate("AutomaticWindow", "Zero Point", None)
        )
        self.label_dynamic_zero_point.setText(
            QCoreApplication.translate("AutomaticWindow", "ZZZ.ZZZ", None)
        )
        self.label_static_filter.setText(
            QCoreApplication.translate("AutomaticWindow", "Filter", None)
        )
        self.label_dynamic_filter.setText(
            QCoreApplication.translate("AutomaticWindow", "FF", None)
        )
        self.label_static_operational_status.setText(
            QCoreApplication.translate("AutomaticWindow", "Loop Status", None)
        )
        self.label_dynamic_operational_status.setText(
            QCoreApplication.translate("AutomaticWindow", "Default", None)
        )
        self.push_button_start.setText(
            QCoreApplication.translate("AutomaticWindow", "Start", None)
        )
        self.push_button_stop.setText(
            QCoreApplication.translate("AutomaticWindow", "Stop", None)
        )
        self.push_button_trigger.setText(
            QCoreApplication.translate("AutomaticWindow", "Trigger", None)
        )

    # retranslateUi
