# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'primary.ui'
##
## Created by: Qt User Interface Compiler version 6.2.3
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDateTimeEdit, QFrame,
    QGraphicsView, QGridLayout, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QPushButton, QSizePolicy,
    QStatusBar, QTabWidget, QTextBrowser, QVBoxLayout,
    QWidget)

class Ui_PrimaryWindow(object):
    def setupUi(self, PrimaryWindow):
        if not PrimaryWindow.objectName():
            PrimaryWindow.setObjectName(u"PrimaryWindow")
        PrimaryWindow.resize(623, 873)
        font = QFont()
        font.setFamilies([u"Sylfaen"])
        font.setPointSize(11)
        PrimaryWindow.setFont(font)
        PrimaryWindow.setCursor(QCursor(Qt.ArrowCursor))
        PrimaryWindow.setWindowOpacity(1.000000000000000)
        self.centralwidget = QWidget(PrimaryWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.verticalLayoutWidget_3 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.verticalLayoutWidget_3.setGeometry(QRect(10, 10, 601, 831))
        self.verticalLayoutWidget_3.setFont(font)
        self.vertical_layout_window = QVBoxLayout(self.verticalLayoutWidget_3)
        self.vertical_layout_window.setObjectName(u"vertical_layout_window")
        self.vertical_layout_window.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout_new_files = QHBoxLayout()
        self.horizontal_layout_new_files.setObjectName(u"horizontal_layout_new_files")
        self.push_button_new_target = QPushButton(self.verticalLayoutWidget_3)
        self.push_button_new_target.setObjectName(u"push_button_new_target")
        self.push_button_new_target.setFont(font)

        self.horizontal_layout_new_files.addWidget(self.push_button_new_target)

        self.line = QFrame(self.verticalLayoutWidget_3)
        self.line.setObjectName(u"line")
        self.line.setFont(font)
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontal_layout_new_files.addWidget(self.line)

        self.push_button_new_image_automatic = QPushButton(self.verticalLayoutWidget_3)
        self.push_button_new_image_automatic.setObjectName(u"push_button_new_image_automatic")
        self.push_button_new_image_automatic.setFont(font)

        self.horizontal_layout_new_files.addWidget(self.push_button_new_image_automatic)

        self.push_button_new_image_manual = QPushButton(self.verticalLayoutWidget_3)
        self.push_button_new_image_manual.setObjectName(u"push_button_new_image_manual")
        self.push_button_new_image_manual.setFont(font)

        self.horizontal_layout_new_files.addWidget(self.push_button_new_image_manual)


        self.vertical_layout_window.addLayout(self.horizontal_layout_new_files)

        self.line_file_image = QFrame(self.verticalLayoutWidget_3)
        self.line_file_image.setObjectName(u"line_file_image")
        self.line_file_image.setFont(font)
        self.line_file_image.setFrameShape(QFrame.HLine)
        self.line_file_image.setFrameShadow(QFrame.Sunken)

        self.vertical_layout_window.addWidget(self.line_file_image)

        self.vertical_layout_image = QVBoxLayout()
        self.vertical_layout_image.setObjectName(u"vertical_layout_image")
        self.vertical_layout_image.setContentsMargins(0, -1, -1, -1)
        self.dummy_opihi_image = QGraphicsView(self.verticalLayoutWidget_3)
        self.dummy_opihi_image.setObjectName(u"dummy_opihi_image")
        self.dummy_opihi_image.setMinimumSize(QSize(400, 400))
        self.dummy_opihi_image.setMaximumSize(QSize(16777215, 400))
        font1 = QFont()
        font1.setFamilies([u"Sylfaen"])
        font1.setPointSize(11)
        font1.setKerning(True)
        self.dummy_opihi_image.setFont(font1)

        self.vertical_layout_image.addWidget(self.dummy_opihi_image)

        self.dummy_opihi_navbar = QLabel(self.verticalLayoutWidget_3)
        self.dummy_opihi_navbar.setObjectName(u"dummy_opihi_navbar")
        self.dummy_opihi_navbar.setMinimumSize(QSize(0, 25))
        self.dummy_opihi_navbar.setAlignment(Qt.AlignCenter)

        self.vertical_layout_image.addWidget(self.dummy_opihi_navbar)


        self.vertical_layout_window.addLayout(self.vertical_layout_image)

        self.push_button_refresh_window = QPushButton(self.verticalLayoutWidget_3)
        self.push_button_refresh_window.setObjectName(u"push_button_refresh_window")

        self.vertical_layout_window.addWidget(self.push_button_refresh_window)

        self.line_image_solution = QFrame(self.verticalLayoutWidget_3)
        self.line_image_solution.setObjectName(u"line_image_solution")
        self.line_image_solution.setFont(font)
        self.line_image_solution.setFrameShadow(QFrame.Sunken)
        self.line_image_solution.setFrameShape(QFrame.HLine)

        self.vertical_layout_window.addWidget(self.line_image_solution)

        self.vertical_layout_solutions = QVBoxLayout()
        self.vertical_layout_solutions.setObjectName(u"vertical_layout_solutions")
        self.tabs_solutions = QTabWidget(self.verticalLayoutWidget_3)
        self.tabs_solutions.setObjectName(u"tabs_solutions")
        self.tabs_solutions.setFont(font)
        self.tabs_solutions.setIconSize(QSize(16, 16))
        self.tab_summary = QWidget()
        self.tab_summary.setObjectName(u"tab_summary")
        self.tabs_solutions.addTab(self.tab_summary, "")
        self.tab_astrometry = QWidget()
        self.tab_astrometry.setObjectName(u"tab_astrometry")
        self.verticalLayoutWidget = QWidget(self.tab_astrometry)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 10, 571, 241))
        self.verticalLayoutWidget.setFont(font)
        self.vertical_layout_astrometry = QVBoxLayout(self.verticalLayoutWidget)
        self.vertical_layout_astrometry.setObjectName(u"vertical_layout_astrometry")
        self.vertical_layout_astrometry.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout_solve_astrometry = QHBoxLayout()
        self.horizontal_layout_solve_astrometry.setObjectName(u"horizontal_layout_solve_astrometry")
        self.push_button_astrometry_solve_astrometry = QPushButton(self.verticalLayoutWidget)
        self.push_button_astrometry_solve_astrometry.setObjectName(u"push_button_astrometry_solve_astrometry")
        self.push_button_astrometry_solve_astrometry.setFont(font)

        self.horizontal_layout_solve_astrometry.addWidget(self.push_button_astrometry_solve_astrometry)


        self.vertical_layout_astrometry.addLayout(self.horizontal_layout_solve_astrometry)

        self.line_2 = QFrame(self.verticalLayoutWidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.vertical_layout_astrometry.addWidget(self.line_2)

        self.grid_layout_astrometry_results = QGridLayout()
        self.grid_layout_astrometry_results.setObjectName(u"grid_layout_astrometry_results")
        self.label_dynamic_astrometry_target_x = QLabel(self.verticalLayoutWidget)
        self.label_dynamic_astrometry_target_x.setObjectName(u"label_dynamic_astrometry_target_x")
        self.label_dynamic_astrometry_target_x.setAlignment(Qt.AlignCenter)

        self.grid_layout_astrometry_results.addWidget(self.label_dynamic_astrometry_target_x, 1, 2, 1, 1)

        self.label_dynamic_astrometry_target_y = QLabel(self.verticalLayoutWidget)
        self.label_dynamic_astrometry_target_y.setObjectName(u"label_dynamic_astrometry_target_y")
        self.label_dynamic_astrometry_target_y.setAlignment(Qt.AlignCenter)

        self.grid_layout_astrometry_results.addWidget(self.label_dynamic_astrometry_target_y, 1, 3, 1, 1)

        self.label_static_astrometry_target_coordinates = QLabel(self.verticalLayoutWidget)
        self.label_static_astrometry_target_coordinates.setObjectName(u"label_static_astrometry_target_coordinates")
        self.label_static_astrometry_target_coordinates.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.grid_layout_astrometry_results.addWidget(self.label_static_astrometry_target_coordinates, 1, 0, 1, 1)

        self.line_9 = QFrame(self.verticalLayoutWidget)
        self.line_9.setObjectName(u"line_9")
        self.line_9.setFrameShape(QFrame.VLine)
        self.line_9.setFrameShadow(QFrame.Sunken)

        self.grid_layout_astrometry_results.addWidget(self.line_9, 0, 5, 3, 1)

        self.label_dynamic_astrometry_center_ra = QLabel(self.verticalLayoutWidget)
        self.label_dynamic_astrometry_center_ra.setObjectName(u"label_dynamic_astrometry_center_ra")
        self.label_dynamic_astrometry_center_ra.setAlignment(Qt.AlignCenter)

        self.grid_layout_astrometry_results.addWidget(self.label_dynamic_astrometry_center_ra, 0, 6, 1, 1)

        self.label_static_astrometry_center_coordinates = QLabel(self.verticalLayoutWidget)
        self.label_static_astrometry_center_coordinates.setObjectName(u"label_static_astrometry_center_coordinates")
        self.label_static_astrometry_center_coordinates.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.grid_layout_astrometry_results.addWidget(self.label_static_astrometry_center_coordinates, 0, 0, 1, 1)

        self.label_dynamic_astrometry_center_dec = QLabel(self.verticalLayoutWidget)
        self.label_dynamic_astrometry_center_dec.setObjectName(u"label_dynamic_astrometry_center_dec")
        self.label_dynamic_astrometry_center_dec.setAlignment(Qt.AlignCenter)

        self.grid_layout_astrometry_results.addWidget(self.label_dynamic_astrometry_center_dec, 0, 7, 1, 1)

        self.label_dynamic_astrometry_target_ra = QLabel(self.verticalLayoutWidget)
        self.label_dynamic_astrometry_target_ra.setObjectName(u"label_dynamic_astrometry_target_ra")
        self.label_dynamic_astrometry_target_ra.setAlignment(Qt.AlignCenter)

        self.grid_layout_astrometry_results.addWidget(self.label_dynamic_astrometry_target_ra, 1, 6, 1, 1)

        self.label_dynamic_astrometry_target_dec = QLabel(self.verticalLayoutWidget)
        self.label_dynamic_astrometry_target_dec.setObjectName(u"label_dynamic_astrometry_target_dec")
        self.label_dynamic_astrometry_target_dec.setAlignment(Qt.AlignCenter)

        self.grid_layout_astrometry_results.addWidget(self.label_dynamic_astrometry_target_dec, 1, 7, 1, 1)

        self.label_dynamic_astrometry_center_y = QLabel(self.verticalLayoutWidget)
        self.label_dynamic_astrometry_center_y.setObjectName(u"label_dynamic_astrometry_center_y")
        self.label_dynamic_astrometry_center_y.setAlignment(Qt.AlignCenter)

        self.grid_layout_astrometry_results.addWidget(self.label_dynamic_astrometry_center_y, 0, 3, 1, 1)

        self.label_dynamic_astrometry_center_x = QLabel(self.verticalLayoutWidget)
        self.label_dynamic_astrometry_center_x.setObjectName(u"label_dynamic_astrometry_center_x")
        self.label_dynamic_astrometry_center_x.setAlignment(Qt.AlignCenter)

        self.grid_layout_astrometry_results.addWidget(self.label_dynamic_astrometry_center_x, 0, 2, 1, 1)

        self.line_8 = QFrame(self.verticalLayoutWidget)
        self.line_8.setObjectName(u"line_8")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.line_8.sizePolicy().hasHeightForWidth())
        self.line_8.setSizePolicy(sizePolicy1)
        self.line_8.setFrameShape(QFrame.VLine)
        self.line_8.setFrameShadow(QFrame.Sunken)

        self.grid_layout_astrometry_results.addWidget(self.line_8, 0, 1, 3, 1)

        self.line_edit_astrometry_custom_x = QLineEdit(self.verticalLayoutWidget)
        self.line_edit_astrometry_custom_x.setObjectName(u"line_edit_astrometry_custom_x")

        self.grid_layout_astrometry_results.addWidget(self.line_edit_astrometry_custom_x, 2, 2, 1, 1)

        self.line_edit_astrometry_custom_y = QLineEdit(self.verticalLayoutWidget)
        self.line_edit_astrometry_custom_y.setObjectName(u"line_edit_astrometry_custom_y")

        self.grid_layout_astrometry_results.addWidget(self.line_edit_astrometry_custom_y, 2, 3, 1, 1)

        self.line_edit_astrometry_custom_ra = QLineEdit(self.verticalLayoutWidget)
        self.line_edit_astrometry_custom_ra.setObjectName(u"line_edit_astrometry_custom_ra")

        self.grid_layout_astrometry_results.addWidget(self.line_edit_astrometry_custom_ra, 2, 6, 1, 1)

        self.line_edit_astrometry_custom_dec = QLineEdit(self.verticalLayoutWidget)
        self.line_edit_astrometry_custom_dec.setObjectName(u"line_edit_astrometry_custom_dec")

        self.grid_layout_astrometry_results.addWidget(self.line_edit_astrometry_custom_dec, 2, 7, 1, 1)

        self.push_button_astrometry_custom_solve = QPushButton(self.verticalLayoutWidget)
        self.push_button_astrometry_custom_solve.setObjectName(u"push_button_astrometry_custom_solve")

        self.grid_layout_astrometry_results.addWidget(self.push_button_astrometry_custom_solve, 2, 0, 1, 1)


        self.vertical_layout_astrometry.addLayout(self.grid_layout_astrometry_results)

        self.tabs_solutions.addTab(self.tab_astrometry, "")
        self.tab_photometry = QWidget()
        self.tab_photometry.setObjectName(u"tab_photometry")
        self.verticalLayoutWidget_2 = QWidget(self.tab_photometry)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(10, 10, 571, 241))
        self.verticalLayoutWidget_2.setFont(font)
        self.vertical_layout_photometry = QVBoxLayout(self.verticalLayoutWidget_2)
        self.vertical_layout_photometry.setObjectName(u"vertical_layout_photometry")
        self.vertical_layout_photometry.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout_solve_photometry = QHBoxLayout()
        self.horizontal_layout_solve_photometry.setObjectName(u"horizontal_layout_solve_photometry")
        self.push_button_photometry_solve_photometry = QPushButton(self.verticalLayoutWidget_2)
        self.push_button_photometry_solve_photometry.setObjectName(u"push_button_photometry_solve_photometry")
        self.push_button_photometry_solve_photometry.setFont(font)

        self.horizontal_layout_solve_photometry.addWidget(self.push_button_photometry_solve_photometry)


        self.vertical_layout_photometry.addLayout(self.horizontal_layout_solve_photometry)

        self.line_3 = QFrame(self.verticalLayoutWidget_2)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.vertical_layout_photometry.addWidget(self.line_3)

        self.horizonta_layout_photometry_results = QHBoxLayout()
        self.horizonta_layout_photometry_results.setObjectName(u"horizonta_layout_photometry_results")

        self.vertical_layout_photometry.addLayout(self.horizonta_layout_photometry_results)

        self.tabs_solutions.addTab(self.tab_photometry, "")
        self.tab_orbit = QWidget()
        self.tab_orbit.setObjectName(u"tab_orbit")
        self.verticalLayoutWidget_5 = QWidget(self.tab_orbit)
        self.verticalLayoutWidget_5.setObjectName(u"verticalLayoutWidget_5")
        self.verticalLayoutWidget_5.setGeometry(QRect(10, 10, 571, 241))
        self.verticalLayoutWidget_5.setFont(font)
        self.vertical_layout_orbit = QVBoxLayout(self.verticalLayoutWidget_5)
        self.vertical_layout_orbit.setObjectName(u"vertical_layout_orbit")
        self.vertical_layout_orbit.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout_solve_orbit = QHBoxLayout()
        self.horizontal_layout_solve_orbit.setObjectName(u"horizontal_layout_solve_orbit")
        self.push_button_orbit_solve_orbit = QPushButton(self.verticalLayoutWidget_5)
        self.push_button_orbit_solve_orbit.setObjectName(u"push_button_orbit_solve_orbit")
        self.push_button_orbit_solve_orbit.setFont(font)

        self.horizontal_layout_solve_orbit.addWidget(self.push_button_orbit_solve_orbit)


        self.vertical_layout_orbit.addLayout(self.horizontal_layout_solve_orbit)

        self.line_5 = QFrame(self.verticalLayoutWidget_5)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.HLine)
        self.line_5.setFrameShadow(QFrame.Sunken)

        self.vertical_layout_orbit.addWidget(self.line_5)

        self.horizontal_layout_orbit_results = QHBoxLayout()
        self.horizontal_layout_orbit_results.setObjectName(u"horizontal_layout_orbit_results")

        self.vertical_layout_orbit.addLayout(self.horizontal_layout_orbit_results)

        self.tabs_solutions.addTab(self.tab_orbit, "")
        self.tab_ephemeris = QWidget()
        self.tab_ephemeris.setObjectName(u"tab_ephemeris")
        self.verticalLayoutWidget_6 = QWidget(self.tab_ephemeris)
        self.verticalLayoutWidget_6.setObjectName(u"verticalLayoutWidget_6")
        self.verticalLayoutWidget_6.setGeometry(QRect(10, 10, 571, 241))
        self.verticalLayoutWidget_6.setFont(font)
        self.vertical_layout_ephemeris = QVBoxLayout(self.verticalLayoutWidget_6)
        self.vertical_layout_ephemeris.setObjectName(u"vertical_layout_ephemeris")
        self.vertical_layout_ephemeris.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout_solve_ephemeris = QHBoxLayout()
        self.horizontal_layout_solve_ephemeris.setObjectName(u"horizontal_layout_solve_ephemeris")
        self.push_button_ephemeris_solve_ephemeris = QPushButton(self.verticalLayoutWidget_6)
        self.push_button_ephemeris_solve_ephemeris.setObjectName(u"push_button_ephemeris_solve_ephemeris")
        self.push_button_ephemeris_solve_ephemeris.setFont(font)

        self.horizontal_layout_solve_ephemeris.addWidget(self.push_button_ephemeris_solve_ephemeris)


        self.vertical_layout_ephemeris.addLayout(self.horizontal_layout_solve_ephemeris)

        self.line_6 = QFrame(self.verticalLayoutWidget_6)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShape(QFrame.HLine)
        self.line_6.setFrameShadow(QFrame.Sunken)

        self.vertical_layout_ephemeris.addWidget(self.line_6)

        self.horizontal_layout_ephemeris_results = QHBoxLayout()
        self.horizontal_layout_ephemeris_results.setObjectName(u"horizontal_layout_ephemeris_results")

        self.vertical_layout_ephemeris.addLayout(self.horizontal_layout_ephemeris_results)

        self.tabs_solutions.addTab(self.tab_ephemeris, "")
        self.tab_propagate = QWidget()
        self.tab_propagate.setObjectName(u"tab_propagate")
        self.verticalLayoutWidget_4 = QWidget(self.tab_propagate)
        self.verticalLayoutWidget_4.setObjectName(u"verticalLayoutWidget_4")
        self.verticalLayoutWidget_4.setGeometry(QRect(10, 10, 571, 251))
        self.verticalLayoutWidget_4.setFont(font)
        self.vertical_layout_propagate = QVBoxLayout(self.verticalLayoutWidget_4)
        self.vertical_layout_propagate.setObjectName(u"vertical_layout_propagate")
        self.vertical_layout_propagate.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout_solve_propagation = QHBoxLayout()
        self.horizontal_layout_solve_propagation.setObjectName(u"horizontal_layout_solve_propagation")
        self.push_button_propagate_solve_propagation = QPushButton(self.verticalLayoutWidget_4)
        self.push_button_propagate_solve_propagation.setObjectName(u"push_button_propagate_solve_propagation")
        self.push_button_propagate_solve_propagation.setFont(font)

        self.horizontal_layout_solve_propagation.addWidget(self.push_button_propagate_solve_propagation)


        self.vertical_layout_propagate.addLayout(self.horizontal_layout_solve_propagation)

        self.line_7 = QFrame(self.verticalLayoutWidget_4)
        self.line_7.setObjectName(u"line_7")
        self.line_7.setFrameShape(QFrame.HLine)
        self.line_7.setFrameShadow(QFrame.Sunken)

        self.vertical_layout_propagate.addWidget(self.line_7)

        self.grid_layout_propagate_rate_results = QGridLayout()
        self.grid_layout_propagate_rate_results.setObjectName(u"grid_layout_propagate_rate_results")
        self.line_12 = QFrame(self.verticalLayoutWidget_4)
        self.line_12.setObjectName(u"line_12")
        self.line_12.setFrameShape(QFrame.VLine)
        self.line_12.setFrameShadow(QFrame.Sunken)

        self.grid_layout_propagate_rate_results.addWidget(self.line_12, 0, 5, 1, 1)

        self.label_dynamic_propagate_ra_acceleration = QLabel(self.verticalLayoutWidget_4)
        self.label_dynamic_propagate_ra_acceleration.setObjectName(u"label_dynamic_propagate_ra_acceleration")
        self.label_dynamic_propagate_ra_acceleration.setAlignment(Qt.AlignCenter)

        self.grid_layout_propagate_rate_results.addWidget(self.label_dynamic_propagate_ra_acceleration, 0, 6, 1, 1)

        self.label_dynamic_propagate_dec_acceleration = QLabel(self.verticalLayoutWidget_4)
        self.label_dynamic_propagate_dec_acceleration.setObjectName(u"label_dynamic_propagate_dec_acceleration")
        self.label_dynamic_propagate_dec_acceleration.setAlignment(Qt.AlignCenter)

        self.grid_layout_propagate_rate_results.addWidget(self.label_dynamic_propagate_dec_acceleration, 0, 7, 1, 1)

        self.label_dynamic_propagate_dec_velocity = QLabel(self.verticalLayoutWidget_4)
        self.label_dynamic_propagate_dec_velocity.setObjectName(u"label_dynamic_propagate_dec_velocity")
        self.label_dynamic_propagate_dec_velocity.setAlignment(Qt.AlignCenter)

        self.grid_layout_propagate_rate_results.addWidget(self.label_dynamic_propagate_dec_velocity, 0, 4, 1, 1)

        self.line_11 = QFrame(self.verticalLayoutWidget_4)
        self.line_11.setObjectName(u"line_11")
        self.line_11.setFrameShape(QFrame.VLine)
        self.line_11.setFrameShadow(QFrame.Sunken)

        self.grid_layout_propagate_rate_results.addWidget(self.line_11, 0, 2, 1, 1)

        self.label_dynamic_propagate_ra_velocity = QLabel(self.verticalLayoutWidget_4)
        self.label_dynamic_propagate_ra_velocity.setObjectName(u"label_dynamic_propagate_ra_velocity")
        self.label_dynamic_propagate_ra_velocity.setAlignment(Qt.AlignCenter)

        self.grid_layout_propagate_rate_results.addWidget(self.label_dynamic_propagate_ra_velocity, 0, 3, 1, 1)

        self.label_static_propagate_rate = QLabel(self.verticalLayoutWidget_4)
        self.label_static_propagate_rate.setObjectName(u"label_static_propagate_rate")

        self.grid_layout_propagate_rate_results.addWidget(self.label_static_propagate_rate, 0, 0, 1, 1)


        self.vertical_layout_propagate.addLayout(self.grid_layout_propagate_rate_results)

        self.line_10 = QFrame(self.verticalLayoutWidget_4)
        self.line_10.setObjectName(u"line_10")
        self.line_10.setFrameShape(QFrame.HLine)
        self.line_10.setFrameShadow(QFrame.Sunken)

        self.vertical_layout_propagate.addWidget(self.line_10)

        self.text_browser_propagate_future_results = QTextBrowser(self.verticalLayoutWidget_4)
        self.text_browser_propagate_future_results.setObjectName(u"text_browser_propagate_future_results")
        self.text_browser_propagate_future_results.setAcceptRichText(True)

        self.vertical_layout_propagate.addWidget(self.text_browser_propagate_future_results)

        self.line_4 = QFrame(self.verticalLayoutWidget_4)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.vertical_layout_propagate.addWidget(self.line_4)

        self.grid_layout_propagate_custom_entry = QGridLayout()
        self.grid_layout_propagate_custom_entry.setObjectName(u"grid_layout_propagate_custom_entry")
        self.date_time_edit_propagate_date_time = QDateTimeEdit(self.verticalLayoutWidget_4)
        self.date_time_edit_propagate_date_time.setObjectName(u"date_time_edit_propagate_date_time")
        self.date_time_edit_propagate_date_time.setTimeSpec(Qt.LocalTime)

        self.grid_layout_propagate_custom_entry.addWidget(self.date_time_edit_propagate_date_time, 0, 0, 1, 1)

        self.label_dynamic_propagate_custom_dec = QLabel(self.verticalLayoutWidget_4)
        self.label_dynamic_propagate_custom_dec.setObjectName(u"label_dynamic_propagate_custom_dec")
        self.label_dynamic_propagate_custom_dec.setAlignment(Qt.AlignCenter)

        self.grid_layout_propagate_custom_entry.addWidget(self.label_dynamic_propagate_custom_dec, 0, 4, 1, 1)

        self.label_dynamic_propagate_custom_ra = QLabel(self.verticalLayoutWidget_4)
        self.label_dynamic_propagate_custom_ra.setObjectName(u"label_dynamic_propagate_custom_ra")
        self.label_dynamic_propagate_custom_ra.setAlignment(Qt.AlignCenter)

        self.grid_layout_propagate_custom_entry.addWidget(self.label_dynamic_propagate_custom_ra, 0, 3, 1, 1)

        self.push_button_propagate_custom_solve = QPushButton(self.verticalLayoutWidget_4)
        self.push_button_propagate_custom_solve.setObjectName(u"push_button_propagate_custom_solve")

        self.grid_layout_propagate_custom_entry.addWidget(self.push_button_propagate_custom_solve, 0, 2, 1, 1)

        self.combo_box_propagate_timezone = QComboBox(self.verticalLayoutWidget_4)
        self.combo_box_propagate_timezone.addItem("")
        self.combo_box_propagate_timezone.addItem("")
        self.combo_box_propagate_timezone.setObjectName(u"combo_box_propagate_timezone")
        self.combo_box_propagate_timezone.setLayoutDirection(Qt.LeftToRight)
        self.combo_box_propagate_timezone.setMinimumContentsLength(0)
        self.combo_box_propagate_timezone.setDuplicatesEnabled(False)

        self.grid_layout_propagate_custom_entry.addWidget(self.combo_box_propagate_timezone, 0, 1, 1, 1)


        self.vertical_layout_propagate.addLayout(self.grid_layout_propagate_custom_entry)

        self.tabs_solutions.addTab(self.tab_propagate, "")

        self.vertical_layout_solutions.addWidget(self.tabs_solutions)


        self.vertical_layout_window.addLayout(self.vertical_layout_solutions)

        PrimaryWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(PrimaryWindow)
        self.statusbar.setObjectName(u"statusbar")
        PrimaryWindow.setStatusBar(self.statusbar)

        self.retranslateUi(PrimaryWindow)

        self.tabs_solutions.setCurrentIndex(5)


        QMetaObject.connectSlotsByName(PrimaryWindow)
    # setupUi

    def retranslateUi(self, PrimaryWindow):
        PrimaryWindow.setWindowTitle(QCoreApplication.translate("PrimaryWindow", u"OpihiExarata", None))
        self.push_button_new_target.setText(QCoreApplication.translate("PrimaryWindow", u"New Target", None))
        self.push_button_new_image_automatic.setText(QCoreApplication.translate("PrimaryWindow", u"Automatic New Image", None))
        self.push_button_new_image_manual.setText(QCoreApplication.translate("PrimaryWindow", u"Manual New Image", None))
        self.dummy_opihi_navbar.setText(QCoreApplication.translate("PrimaryWindow", u"DUMMY OPIHI IMAGE NAVIGATION BAR.", None))
        self.push_button_refresh_window.setText(QCoreApplication.translate("PrimaryWindow", u"Refresh Window", None))
        self.tabs_solutions.setTabText(self.tabs_solutions.indexOf(self.tab_summary), QCoreApplication.translate("PrimaryWindow", u"Summary", None))
        self.push_button_astrometry_solve_astrometry.setText(QCoreApplication.translate("PrimaryWindow", u"Solve Astrometry", None))
        self.label_dynamic_astrometry_target_x.setText(QCoreApplication.translate("PrimaryWindow", u"0000", None))
        self.label_dynamic_astrometry_target_y.setText(QCoreApplication.translate("PrimaryWindow", u"0000", None))
        self.label_static_astrometry_target_coordinates.setText(QCoreApplication.translate("PrimaryWindow", u"Target/Asteroid:", None))
        self.label_dynamic_astrometry_center_ra.setText(QCoreApplication.translate("PrimaryWindow", u"HH:MM:SS.SS", None))
        self.label_static_astrometry_center_coordinates.setText(QCoreApplication.translate("PrimaryWindow", u"Opihi Center:", None))
        self.label_dynamic_astrometry_center_dec.setText(QCoreApplication.translate("PrimaryWindow", u"+DD:MM:SS.SS", None))
        self.label_dynamic_astrometry_target_ra.setText(QCoreApplication.translate("PrimaryWindow", u"HH:MM:SS.SS", None))
        self.label_dynamic_astrometry_target_dec.setText(QCoreApplication.translate("PrimaryWindow", u"+DD:MM:SS.SS", None))
        self.label_dynamic_astrometry_center_y.setText(QCoreApplication.translate("PrimaryWindow", u"0000", None))
        self.label_dynamic_astrometry_center_x.setText(QCoreApplication.translate("PrimaryWindow", u"0000", None))
        self.push_button_astrometry_custom_solve.setText(QCoreApplication.translate("PrimaryWindow", u"Custom Solve", None))
        self.tabs_solutions.setTabText(self.tabs_solutions.indexOf(self.tab_astrometry), QCoreApplication.translate("PrimaryWindow", u"Astrometry", None))
        self.push_button_photometry_solve_photometry.setText(QCoreApplication.translate("PrimaryWindow", u"Solve Photometry", None))
        self.tabs_solutions.setTabText(self.tabs_solutions.indexOf(self.tab_photometry), QCoreApplication.translate("PrimaryWindow", u"Photometry", None))
        self.push_button_orbit_solve_orbit.setText(QCoreApplication.translate("PrimaryWindow", u"Solve Orbit", None))
        self.tabs_solutions.setTabText(self.tabs_solutions.indexOf(self.tab_orbit), QCoreApplication.translate("PrimaryWindow", u"Orbit", None))
        self.push_button_ephemeris_solve_ephemeris.setText(QCoreApplication.translate("PrimaryWindow", u"Solve Ephemeris", None))
        self.tabs_solutions.setTabText(self.tabs_solutions.indexOf(self.tab_ephemeris), QCoreApplication.translate("PrimaryWindow", u"Ephemeris", None))
        self.push_button_propagate_solve_propagation.setText(QCoreApplication.translate("PrimaryWindow", u"Solve Propagation", None))
        self.label_dynamic_propagate_ra_acceleration.setText(QCoreApplication.translate("PrimaryWindow", u"+AA.AAA", None))
        self.label_dynamic_propagate_dec_acceleration.setText(QCoreApplication.translate("PrimaryWindow", u"+AA.AAA", None))
        self.label_dynamic_propagate_dec_velocity.setText(QCoreApplication.translate("PrimaryWindow", u"+VV.VVV", None))
        self.label_dynamic_propagate_ra_velocity.setText(QCoreApplication.translate("PrimaryWindow", u"+VV.VVV", None))
        self.label_static_propagate_rate.setText(QCoreApplication.translate("PrimaryWindow", u"<html><head/><body><p>Propagate Rate [ &quot;/s | &quot;/s<span style=\" vertical-align:super;\">2</span> ]</p></body></html>", None))
        self.text_browser_propagate_future_results.setHtml(QCoreApplication.translate("PrimaryWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Sylfaen'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">YYYY-MM-DD  HH:MM:SS  Z   |   HH:MM:SS.SS    +DD:MM:SS.SS</p></body></html>", None))
        self.date_time_edit_propagate_date_time.setDisplayFormat(QCoreApplication.translate("PrimaryWindow", u"yyyy-MM-dd HH:mm:ss", None))
        self.label_dynamic_propagate_custom_dec.setText(QCoreApplication.translate("PrimaryWindow", u"+DD:MM:SS.SS", None))
        self.label_dynamic_propagate_custom_ra.setText(QCoreApplication.translate("PrimaryWindow", u"HH:MM:SS.SS", None))
        self.push_button_propagate_custom_solve.setText(QCoreApplication.translate("PrimaryWindow", u"Custom Solve", None))
        self.combo_box_propagate_timezone.setItemText(0, QCoreApplication.translate("PrimaryWindow", u"UTC+00:00", None))
        self.combo_box_propagate_timezone.setItemText(1, QCoreApplication.translate("PrimaryWindow", u"HST-10:00", None))

        self.tabs_solutions.setTabText(self.tabs_solutions.indexOf(self.tab_propagate), QCoreApplication.translate("PrimaryWindow", u"Propagate", None))
    # retranslateUi

