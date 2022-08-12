# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'manual.ui'
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
    QCheckBox,
    QComboBox,
    QDateTimeEdit,
    QFrame,
    QGraphicsView,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QStatusBar,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)


class Ui_ManualWindow(object):
    def setupUi(self, ManualWindow):
        if not ManualWindow.objectName():
            ManualWindow.setObjectName("ManualWindow")
        ManualWindow.resize(634, 873)
        font = QFont()
        font.setFamilies(["Sylfaen"])
        font.setPointSize(11)
        ManualWindow.setFont(font)
        ManualWindow.setCursor(QCursor(Qt.ArrowCursor))
        ManualWindow.setWindowOpacity(1.000000000000000)
        self.centralwidget = QWidget(ManualWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.centralwidget.sizePolicy().hasHeightForWidth()
        )
        self.centralwidget.setSizePolicy(sizePolicy)
        self.verticalLayoutWidget_3 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayoutWidget_3.setGeometry(QRect(10, 10, 611, 831))
        self.verticalLayoutWidget_3.setFont(font)
        self.vertical_layout_window = QVBoxLayout(self.verticalLayoutWidget_3)
        self.vertical_layout_window.setObjectName("vertical_layout_window")
        self.vertical_layout_window.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout_new_files = QHBoxLayout()
        self.horizontal_layout_new_files.setObjectName("horizontal_layout_new_files")
        self.push_button_new_target = QPushButton(self.verticalLayoutWidget_3)
        self.push_button_new_target.setObjectName("push_button_new_target")
        self.push_button_new_target.setFont(font)

        self.horizontal_layout_new_files.addWidget(self.push_button_new_target)

        self.line = QFrame(self.verticalLayoutWidget_3)
        self.line.setObjectName("line")
        self.line.setFont(font)
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontal_layout_new_files.addWidget(self.line)

        self.push_button_new_image_automatic = QPushButton(self.verticalLayoutWidget_3)
        self.push_button_new_image_automatic.setObjectName(
            "push_button_new_image_automatic"
        )
        self.push_button_new_image_automatic.setFont(font)

        self.horizontal_layout_new_files.addWidget(self.push_button_new_image_automatic)

        self.push_button_new_image_manual = QPushButton(self.verticalLayoutWidget_3)
        self.push_button_new_image_manual.setObjectName("push_button_new_image_manual")
        self.push_button_new_image_manual.setFont(font)

        self.horizontal_layout_new_files.addWidget(self.push_button_new_image_manual)

        self.vertical_layout_window.addLayout(self.horizontal_layout_new_files)

        self.line_file_image = QFrame(self.verticalLayoutWidget_3)
        self.line_file_image.setObjectName("line_file_image")
        self.line_file_image.setFont(font)
        self.line_file_image.setFrameShape(QFrame.HLine)
        self.line_file_image.setFrameShadow(QFrame.Sunken)

        self.vertical_layout_window.addWidget(self.line_file_image)

        self.vertical_layout_image = QVBoxLayout()
        self.vertical_layout_image.setObjectName("vertical_layout_image")
        self.vertical_layout_image.setContentsMargins(0, -1, -1, -1)
        self.dummy_opihi_image = QGraphicsView(self.verticalLayoutWidget_3)
        self.dummy_opihi_image.setObjectName("dummy_opihi_image")
        self.dummy_opihi_image.setMinimumSize(QSize(400, 400))
        self.dummy_opihi_image.setMaximumSize(QSize(16777215, 400))
        font1 = QFont()
        font1.setFamilies(["Sylfaen"])
        font1.setPointSize(11)
        font1.setKerning(True)
        self.dummy_opihi_image.setFont(font1)

        self.vertical_layout_image.addWidget(self.dummy_opihi_image)

        self.dummy_opihi_navbar = QLabel(self.verticalLayoutWidget_3)
        self.dummy_opihi_navbar.setObjectName("dummy_opihi_navbar")
        self.dummy_opihi_navbar.setMinimumSize(QSize(0, 25))
        self.dummy_opihi_navbar.setAlignment(Qt.AlignCenter)

        self.vertical_layout_image.addWidget(self.dummy_opihi_navbar)

        self.vertical_layout_window.addLayout(self.vertical_layout_image)

        self.push_button_refresh_window = QPushButton(self.verticalLayoutWidget_3)
        self.push_button_refresh_window.setObjectName("push_button_refresh_window")

        self.vertical_layout_window.addWidget(self.push_button_refresh_window)

        self.line_image_solution = QFrame(self.verticalLayoutWidget_3)
        self.line_image_solution.setObjectName("line_image_solution")
        self.line_image_solution.setFont(font)
        self.line_image_solution.setFrameShadow(QFrame.Sunken)
        self.line_image_solution.setFrameShape(QFrame.HLine)

        self.vertical_layout_window.addWidget(self.line_image_solution)

        self.vertical_layout_solutions = QVBoxLayout()
        self.vertical_layout_solutions.setObjectName("vertical_layout_solutions")
        self.tabs_solutions = QTabWidget(self.verticalLayoutWidget_3)
        self.tabs_solutions.setObjectName("tabs_solutions")
        self.tabs_solutions.setFont(font)
        self.tabs_solutions.setIconSize(QSize(16, 16))
        self.tab_summary = QWidget()
        self.tab_summary.setObjectName("tab_summary")
        self.verticalLayoutWidget_7 = QWidget(self.tab_summary)
        self.verticalLayoutWidget_7.setObjectName("verticalLayoutWidget_7")
        self.verticalLayoutWidget_7.setGeometry(QRect(10, 10, 581, 251))
        self.vertical_layout_summary = QVBoxLayout(self.verticalLayoutWidget_7)
        self.vertical_layout_summary.setObjectName("vertical_layout_summary")
        self.vertical_layout_summary.setContentsMargins(0, 0, 0, 0)
        self.grid_layout_target_image_names = QGridLayout()
        self.grid_layout_target_image_names.setObjectName(
            "grid_layout_target_image_names"
        )
        self.label_static_summary_target_name = QLabel(self.verticalLayoutWidget_7)
        self.label_static_summary_target_name.setObjectName(
            "label_static_summary_target_name"
        )

        self.grid_layout_target_image_names.addWidget(
            self.label_static_summary_target_name, 0, 0, 1, 1
        )

        self.label_static_summary_fits_file = QLabel(self.verticalLayoutWidget_7)
        self.label_static_summary_fits_file.setObjectName(
            "label_static_summary_fits_file"
        )

        self.grid_layout_target_image_names.addWidget(
            self.label_static_summary_fits_file, 2, 0, 1, 1
        )

        self.label_dynamic_summary_target_name = QLabel(self.verticalLayoutWidget_7)
        self.label_dynamic_summary_target_name.setObjectName(
            "label_dynamic_summary_target_name"
        )

        self.grid_layout_target_image_names.addWidget(
            self.label_dynamic_summary_target_name, 0, 1, 1, 1
        )

        self.label_dynamic_summary_fits_file = QLabel(self.verticalLayoutWidget_7)
        self.label_dynamic_summary_fits_file.setObjectName(
            "label_dynamic_summary_fits_file"
        )

        self.grid_layout_target_image_names.addWidget(
            self.label_dynamic_summary_fits_file, 2, 1, 1, 1
        )

        self.label_static_summary_directory = QLabel(self.verticalLayoutWidget_7)
        self.label_static_summary_directory.setObjectName(
            "label_static_summary_directory"
        )

        self.grid_layout_target_image_names.addWidget(
            self.label_static_summary_directory, 1, 0, 1, 1
        )

        self.label_dynamic_summary_directory = QLabel(self.verticalLayoutWidget_7)
        self.label_dynamic_summary_directory.setObjectName(
            "label_dynamic_summary_directory"
        )

        self.grid_layout_target_image_names.addWidget(
            self.label_dynamic_summary_directory, 1, 1, 1, 1
        )

        self.vertical_layout_summary.addLayout(self.grid_layout_target_image_names)

        self.push_button_send_target_to_tcs = QPushButton(self.verticalLayoutWidget_7)
        self.push_button_send_target_to_tcs.setObjectName(
            "push_button_send_target_to_tcs"
        )

        self.vertical_layout_summary.addWidget(self.push_button_send_target_to_tcs)

        self.horizontal_layout_save_file = QHBoxLayout()
        self.horizontal_layout_save_file.setObjectName("horizontal_layout_save_file")
        self.line_edit_summary_save_filename = QLineEdit(self.verticalLayoutWidget_7)
        self.line_edit_summary_save_filename.setObjectName(
            "line_edit_summary_save_filename"
        )

        self.horizontal_layout_save_file.addWidget(self.line_edit_summary_save_filename)

        self.check_box_summary_autosave = QCheckBox(self.verticalLayoutWidget_7)
        self.check_box_summary_autosave.setObjectName("check_box_summary_autosave")
        self.check_box_summary_autosave.setChecked(True)

        self.horizontal_layout_save_file.addWidget(self.check_box_summary_autosave)

        self.push_button_summary_save = QPushButton(self.verticalLayoutWidget_7)
        self.push_button_summary_save.setObjectName("push_button_summary_save")

        self.horizontal_layout_save_file.addWidget(self.push_button_summary_save)

        self.vertical_layout_summary.addLayout(self.horizontal_layout_save_file)

        self.tabs_solutions.addTab(self.tab_summary, "")
        self.tab_astrometry = QWidget()
        self.tab_astrometry.setObjectName("tab_astrometry")
        self.verticalLayoutWidget = QWidget(self.tab_astrometry)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 10, 581, 251))
        self.verticalLayoutWidget.setFont(font)
        self.vertical_layout_astrometry = QVBoxLayout(self.verticalLayoutWidget)
        self.vertical_layout_astrometry.setObjectName("vertical_layout_astrometry")
        self.vertical_layout_astrometry.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout_solve_astrometry = QHBoxLayout()
        self.horizontal_layout_solve_astrometry.setObjectName(
            "horizontal_layout_solve_astrometry"
        )
        self.combo_box_astrometry_solve_engine = QComboBox(self.verticalLayoutWidget)
        self.combo_box_astrometry_solve_engine.addItem("")
        self.combo_box_astrometry_solve_engine.addItem("")
        self.combo_box_astrometry_solve_engine.setObjectName(
            "combo_box_astrometry_solve_engine"
        )

        self.horizontal_layout_solve_astrometry.addWidget(
            self.combo_box_astrometry_solve_engine
        )

        self.push_button_astrometry_solve_astrometry = QPushButton(
            self.verticalLayoutWidget
        )
        self.push_button_astrometry_solve_astrometry.setObjectName(
            "push_button_astrometry_solve_astrometry"
        )
        self.push_button_astrometry_solve_astrometry.setFont(font)

        self.horizontal_layout_solve_astrometry.addWidget(
            self.push_button_astrometry_solve_astrometry
        )

        self.vertical_layout_astrometry.addLayout(
            self.horizontal_layout_solve_astrometry
        )

        self.line_2 = QFrame(self.verticalLayoutWidget)
        self.line_2.setObjectName("line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.vertical_layout_astrometry.addWidget(self.line_2)

        self.grid_layout_astrometry_results = QGridLayout()
        self.grid_layout_astrometry_results.setObjectName(
            "grid_layout_astrometry_results"
        )
        self.label_dynamic_astrometry_target_x = QLabel(self.verticalLayoutWidget)
        self.label_dynamic_astrometry_target_x.setObjectName(
            "label_dynamic_astrometry_target_x"
        )
        self.label_dynamic_astrometry_target_x.setAlignment(Qt.AlignCenter)

        self.grid_layout_astrometry_results.addWidget(
            self.label_dynamic_astrometry_target_x, 1, 2, 1, 1
        )

        self.label_dynamic_astrometry_target_y = QLabel(self.verticalLayoutWidget)
        self.label_dynamic_astrometry_target_y.setObjectName(
            "label_dynamic_astrometry_target_y"
        )
        self.label_dynamic_astrometry_target_y.setAlignment(Qt.AlignCenter)

        self.grid_layout_astrometry_results.addWidget(
            self.label_dynamic_astrometry_target_y, 1, 3, 1, 1
        )

        self.label_static_astrometry_target_coordinates = QLabel(
            self.verticalLayoutWidget
        )
        self.label_static_astrometry_target_coordinates.setObjectName(
            "label_static_astrometry_target_coordinates"
        )
        self.label_static_astrometry_target_coordinates.setAlignment(
            Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter
        )

        self.grid_layout_astrometry_results.addWidget(
            self.label_static_astrometry_target_coordinates, 1, 0, 1, 1
        )

        self.line_9 = QFrame(self.verticalLayoutWidget)
        self.line_9.setObjectName("line_9")
        self.line_9.setFrameShape(QFrame.VLine)
        self.line_9.setFrameShadow(QFrame.Sunken)

        self.grid_layout_astrometry_results.addWidget(self.line_9, 0, 5, 3, 1)

        self.label_dynamic_astrometry_center_ra = QLabel(self.verticalLayoutWidget)
        self.label_dynamic_astrometry_center_ra.setObjectName(
            "label_dynamic_astrometry_center_ra"
        )
        self.label_dynamic_astrometry_center_ra.setAlignment(Qt.AlignCenter)

        self.grid_layout_astrometry_results.addWidget(
            self.label_dynamic_astrometry_center_ra, 0, 6, 1, 1
        )

        self.label_static_astrometry_center_coordinates = QLabel(
            self.verticalLayoutWidget
        )
        self.label_static_astrometry_center_coordinates.setObjectName(
            "label_static_astrometry_center_coordinates"
        )
        self.label_static_astrometry_center_coordinates.setAlignment(
            Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter
        )

        self.grid_layout_astrometry_results.addWidget(
            self.label_static_astrometry_center_coordinates, 0, 0, 1, 1
        )

        self.label_dynamic_astrometry_center_dec = QLabel(self.verticalLayoutWidget)
        self.label_dynamic_astrometry_center_dec.setObjectName(
            "label_dynamic_astrometry_center_dec"
        )
        self.label_dynamic_astrometry_center_dec.setAlignment(Qt.AlignCenter)

        self.grid_layout_astrometry_results.addWidget(
            self.label_dynamic_astrometry_center_dec, 0, 7, 1, 1
        )

        self.label_dynamic_astrometry_target_ra = QLabel(self.verticalLayoutWidget)
        self.label_dynamic_astrometry_target_ra.setObjectName(
            "label_dynamic_astrometry_target_ra"
        )
        self.label_dynamic_astrometry_target_ra.setAlignment(Qt.AlignCenter)

        self.grid_layout_astrometry_results.addWidget(
            self.label_dynamic_astrometry_target_ra, 1, 6, 1, 1
        )

        self.label_dynamic_astrometry_target_dec = QLabel(self.verticalLayoutWidget)
        self.label_dynamic_astrometry_target_dec.setObjectName(
            "label_dynamic_astrometry_target_dec"
        )
        self.label_dynamic_astrometry_target_dec.setAlignment(Qt.AlignCenter)

        self.grid_layout_astrometry_results.addWidget(
            self.label_dynamic_astrometry_target_dec, 1, 7, 1, 1
        )

        self.label_dynamic_astrometry_center_y = QLabel(self.verticalLayoutWidget)
        self.label_dynamic_astrometry_center_y.setObjectName(
            "label_dynamic_astrometry_center_y"
        )
        self.label_dynamic_astrometry_center_y.setAlignment(Qt.AlignCenter)

        self.grid_layout_astrometry_results.addWidget(
            self.label_dynamic_astrometry_center_y, 0, 3, 1, 1
        )

        self.label_dynamic_astrometry_center_x = QLabel(self.verticalLayoutWidget)
        self.label_dynamic_astrometry_center_x.setObjectName(
            "label_dynamic_astrometry_center_x"
        )
        self.label_dynamic_astrometry_center_x.setAlignment(Qt.AlignCenter)

        self.grid_layout_astrometry_results.addWidget(
            self.label_dynamic_astrometry_center_x, 0, 2, 1, 1
        )

        self.line_8 = QFrame(self.verticalLayoutWidget)
        self.line_8.setObjectName("line_8")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.line_8.sizePolicy().hasHeightForWidth())
        self.line_8.setSizePolicy(sizePolicy1)
        self.line_8.setFrameShape(QFrame.VLine)
        self.line_8.setFrameShadow(QFrame.Sunken)

        self.grid_layout_astrometry_results.addWidget(self.line_8, 0, 1, 3, 1)

        self.line_edit_astrometry_custom_x = QLineEdit(self.verticalLayoutWidget)
        self.line_edit_astrometry_custom_x.setObjectName(
            "line_edit_astrometry_custom_x"
        )

        self.grid_layout_astrometry_results.addWidget(
            self.line_edit_astrometry_custom_x, 2, 2, 1, 1
        )

        self.line_edit_astrometry_custom_y = QLineEdit(self.verticalLayoutWidget)
        self.line_edit_astrometry_custom_y.setObjectName(
            "line_edit_astrometry_custom_y"
        )

        self.grid_layout_astrometry_results.addWidget(
            self.line_edit_astrometry_custom_y, 2, 3, 1, 1
        )

        self.line_edit_astrometry_custom_ra = QLineEdit(self.verticalLayoutWidget)
        self.line_edit_astrometry_custom_ra.setObjectName(
            "line_edit_astrometry_custom_ra"
        )

        self.grid_layout_astrometry_results.addWidget(
            self.line_edit_astrometry_custom_ra, 2, 6, 1, 1
        )

        self.line_edit_astrometry_custom_dec = QLineEdit(self.verticalLayoutWidget)
        self.line_edit_astrometry_custom_dec.setObjectName(
            "line_edit_astrometry_custom_dec"
        )

        self.grid_layout_astrometry_results.addWidget(
            self.line_edit_astrometry_custom_dec, 2, 7, 1, 1
        )

        self.push_button_astrometry_custom_solve = QPushButton(
            self.verticalLayoutWidget
        )
        self.push_button_astrometry_custom_solve.setObjectName(
            "push_button_astrometry_custom_solve"
        )

        self.grid_layout_astrometry_results.addWidget(
            self.push_button_astrometry_custom_solve, 2, 0, 1, 1
        )

        self.vertical_layout_astrometry.addLayout(self.grid_layout_astrometry_results)

        self.tabs_solutions.addTab(self.tab_astrometry, "")
        self.tab_photometry = QWidget()
        self.tab_photometry.setObjectName("tab_photometry")
        self.verticalLayoutWidget_2 = QWidget(self.tab_photometry)
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(10, 10, 581, 251))
        self.verticalLayoutWidget_2.setFont(font)
        self.vertical_layout_photometry = QVBoxLayout(self.verticalLayoutWidget_2)
        self.vertical_layout_photometry.setObjectName("vertical_layout_photometry")
        self.vertical_layout_photometry.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout_solve_photometry = QHBoxLayout()
        self.horizontal_layout_solve_photometry.setObjectName(
            "horizontal_layout_solve_photometry"
        )
        self.combo_box_photometry_solve_engine = QComboBox(self.verticalLayoutWidget_2)
        self.combo_box_photometry_solve_engine.addItem("")
        self.combo_box_photometry_solve_engine.setObjectName(
            "combo_box_photometry_solve_engine"
        )

        self.horizontal_layout_solve_photometry.addWidget(
            self.combo_box_photometry_solve_engine
        )

        self.push_button_photometry_solve_photometry = QPushButton(
            self.verticalLayoutWidget_2
        )
        self.push_button_photometry_solve_photometry.setObjectName(
            "push_button_photometry_solve_photometry"
        )
        self.push_button_photometry_solve_photometry.setFont(font)

        self.horizontal_layout_solve_photometry.addWidget(
            self.push_button_photometry_solve_photometry
        )

        self.vertical_layout_photometry.addLayout(
            self.horizontal_layout_solve_photometry
        )

        self.line_3 = QFrame(self.verticalLayoutWidget_2)
        self.line_3.setObjectName("line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.vertical_layout_photometry.addWidget(self.line_3)

        self.horizonta_layout_photometry_results = QHBoxLayout()
        self.horizonta_layout_photometry_results.setObjectName(
            "horizonta_layout_photometry_results"
        )
        self.label_static_photometry_filter_label = QLabel(self.verticalLayoutWidget_2)
        self.label_static_photometry_filter_label.setObjectName(
            "label_static_photometry_filter_label"
        )

        self.horizonta_layout_photometry_results.addWidget(
            self.label_static_photometry_filter_label
        )

        self.label_dynamic_photometry_filter_name = QLabel(self.verticalLayoutWidget_2)
        self.label_dynamic_photometry_filter_name.setObjectName(
            "label_dynamic_photometry_filter_name"
        )

        self.horizonta_layout_photometry_results.addWidget(
            self.label_dynamic_photometry_filter_name
        )

        self.line_13 = QFrame(self.verticalLayoutWidget_2)
        self.line_13.setObjectName("line_13")
        self.line_13.setFrameShape(QFrame.VLine)
        self.line_13.setFrameShadow(QFrame.Sunken)

        self.horizonta_layout_photometry_results.addWidget(self.line_13)

        self.label_static_photometry_magnitude = QLabel(self.verticalLayoutWidget_2)
        self.label_static_photometry_magnitude.setObjectName(
            "label_static_photometry_magnitude"
        )

        self.horizonta_layout_photometry_results.addWidget(
            self.label_static_photometry_magnitude
        )

        self.label_dynamic_photometry_magnitude = QLabel(self.verticalLayoutWidget_2)
        self.label_dynamic_photometry_magnitude.setObjectName(
            "label_dynamic_photometry_magnitude"
        )

        self.horizonta_layout_photometry_results.addWidget(
            self.label_dynamic_photometry_magnitude
        )

        self.line_4 = QFrame(self.verticalLayoutWidget_2)
        self.line_4.setObjectName("line_4")
        self.line_4.setFrameShape(QFrame.VLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.horizonta_layout_photometry_results.addWidget(self.line_4)

        self.label_static_photometry_zero_point_label = QLabel(
            self.verticalLayoutWidget_2
        )
        self.label_static_photometry_zero_point_label.setObjectName(
            "label_static_photometry_zero_point_label"
        )

        self.horizonta_layout_photometry_results.addWidget(
            self.label_static_photometry_zero_point_label
        )

        self.label_dynamic_photometry_zero_point_value = QLabel(
            self.verticalLayoutWidget_2
        )
        self.label_dynamic_photometry_zero_point_value.setObjectName(
            "label_dynamic_photometry_zero_point_value"
        )

        self.horizonta_layout_photometry_results.addWidget(
            self.label_dynamic_photometry_zero_point_value
        )

        self.vertical_layout_photometry.addLayout(
            self.horizonta_layout_photometry_results
        )

        self.line_14 = QFrame(self.verticalLayoutWidget_2)
        self.line_14.setObjectName("line_14")
        self.line_14.setFrameShape(QFrame.HLine)
        self.line_14.setFrameShadow(QFrame.Sunken)

        self.vertical_layout_photometry.addWidget(self.line_14)

        self.tabs_solutions.addTab(self.tab_photometry, "")
        self.tab_orbit = QWidget()
        self.tab_orbit.setObjectName("tab_orbit")
        self.verticalLayoutWidget_5 = QWidget(self.tab_orbit)
        self.verticalLayoutWidget_5.setObjectName("verticalLayoutWidget_5")
        self.verticalLayoutWidget_5.setGeometry(QRect(10, 10, 581, 251))
        self.verticalLayoutWidget_5.setFont(font)
        self.vertical_layout_orbit = QVBoxLayout(self.verticalLayoutWidget_5)
        self.vertical_layout_orbit.setObjectName("vertical_layout_orbit")
        self.vertical_layout_orbit.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout_solve_orbit = QHBoxLayout()
        self.horizontal_layout_solve_orbit.setObjectName(
            "horizontal_layout_solve_orbit"
        )
        self.combo_box_orbit_solve_engine = QComboBox(self.verticalLayoutWidget_5)
        self.combo_box_orbit_solve_engine.addItem("")
        self.combo_box_orbit_solve_engine.addItem("")
        self.combo_box_orbit_solve_engine.setObjectName("combo_box_orbit_solve_engine")

        self.horizontal_layout_solve_orbit.addWidget(self.combo_box_orbit_solve_engine)

        self.push_button_orbit_solve_orbit = QPushButton(self.verticalLayoutWidget_5)
        self.push_button_orbit_solve_orbit.setObjectName(
            "push_button_orbit_solve_orbit"
        )
        self.push_button_orbit_solve_orbit.setFont(font)

        self.horizontal_layout_solve_orbit.addWidget(self.push_button_orbit_solve_orbit)

        self.vertical_layout_orbit.addLayout(self.horizontal_layout_solve_orbit)

        self.line_5 = QFrame(self.verticalLayoutWidget_5)
        self.line_5.setObjectName("line_5")
        self.line_5.setFrameShape(QFrame.HLine)
        self.line_5.setFrameShadow(QFrame.Sunken)

        self.vertical_layout_orbit.addWidget(self.line_5)

        self.grid_layout_orbit_elements = QGridLayout()
        self.grid_layout_orbit_elements.setObjectName("grid_layout_orbit_elements")
        self.line_edit_orbit_inclination = QLineEdit(self.verticalLayoutWidget_5)
        self.line_edit_orbit_inclination.setObjectName("line_edit_orbit_inclination")

        self.grid_layout_orbit_elements.addWidget(
            self.line_edit_orbit_inclination, 1, 1, 1, 1
        )

        self.line_edit_orbit_perihelion = QLineEdit(self.verticalLayoutWidget_5)
        self.line_edit_orbit_perihelion.setObjectName("line_edit_orbit_perihelion")

        self.grid_layout_orbit_elements.addWidget(
            self.line_edit_orbit_perihelion, 2, 1, 1, 1
        )

        self.line_edit_orbit_epoch = QLineEdit(self.verticalLayoutWidget_5)
        self.line_edit_orbit_epoch.setObjectName("line_edit_orbit_epoch")

        self.grid_layout_orbit_elements.addWidget(
            self.line_edit_orbit_epoch, 3, 1, 1, 1
        )

        self.label_static_orbit_inclination = QLabel(self.verticalLayoutWidget_5)
        self.label_static_orbit_inclination.setObjectName(
            "label_static_orbit_inclination"
        )
        font2 = QFont()
        font2.setItalic(False)
        self.label_static_orbit_inclination.setFont(font2)

        self.grid_layout_orbit_elements.addWidget(
            self.label_static_orbit_inclination, 1, 0, 1, 1
        )

        self.label_static_orbit_perihelion = QLabel(self.verticalLayoutWidget_5)
        self.label_static_orbit_perihelion.setObjectName(
            "label_static_orbit_perihelion"
        )
        self.label_static_orbit_perihelion.setFont(font2)

        self.grid_layout_orbit_elements.addWidget(
            self.label_static_orbit_perihelion, 2, 0, 1, 1
        )

        self.label_static_orbit_epoch = QLabel(self.verticalLayoutWidget_5)
        self.label_static_orbit_epoch.setObjectName("label_static_orbit_epoch")

        self.grid_layout_orbit_elements.addWidget(
            self.label_static_orbit_epoch, 3, 0, 1, 1
        )

        self.line_edit_orbit_semimajor_axis = QLineEdit(self.verticalLayoutWidget_5)
        self.line_edit_orbit_semimajor_axis.setObjectName(
            "line_edit_orbit_semimajor_axis"
        )

        self.grid_layout_orbit_elements.addWidget(
            self.line_edit_orbit_semimajor_axis, 0, 1, 1, 1
        )

        self.label_static_orbit_semimajor_axis = QLabel(self.verticalLayoutWidget_5)
        self.label_static_orbit_semimajor_axis.setObjectName(
            "label_static_orbit_semimajor_axis"
        )
        font3 = QFont()
        font3.setBold(False)
        font3.setItalic(False)
        self.label_static_orbit_semimajor_axis.setFont(font3)

        self.grid_layout_orbit_elements.addWidget(
            self.label_static_orbit_semimajor_axis, 0, 0, 1, 1
        )

        self.line_16 = QFrame(self.verticalLayoutWidget_5)
        self.line_16.setObjectName("line_16")
        self.line_16.setFrameShape(QFrame.VLine)
        self.line_16.setFrameShadow(QFrame.Sunken)

        self.grid_layout_orbit_elements.addWidget(self.line_16, 0, 2, 4, 1)

        self.label_static_orbit_eccentricity = QLabel(self.verticalLayoutWidget_5)
        self.label_static_orbit_eccentricity.setObjectName(
            "label_static_orbit_eccentricity"
        )
        self.label_static_orbit_eccentricity.setFont(font2)

        self.grid_layout_orbit_elements.addWidget(
            self.label_static_orbit_eccentricity, 0, 3, 1, 1
        )

        self.line_edit_orbit_eccentricity = QLineEdit(self.verticalLayoutWidget_5)
        self.line_edit_orbit_eccentricity.setObjectName("line_edit_orbit_eccentricity")

        self.grid_layout_orbit_elements.addWidget(
            self.line_edit_orbit_eccentricity, 0, 4, 1, 1
        )

        self.label_static_orbit_ascending_node = QLabel(self.verticalLayoutWidget_5)
        self.label_static_orbit_ascending_node.setObjectName(
            "label_static_orbit_ascending_node"
        )
        self.label_static_orbit_ascending_node.setFont(font2)

        self.grid_layout_orbit_elements.addWidget(
            self.label_static_orbit_ascending_node, 1, 3, 1, 1
        )

        self.line_edit_orbit_ascending_node = QLineEdit(self.verticalLayoutWidget_5)
        self.line_edit_orbit_ascending_node.setObjectName(
            "line_edit_orbit_ascending_node"
        )

        self.grid_layout_orbit_elements.addWidget(
            self.line_edit_orbit_ascending_node, 1, 4, 1, 1
        )

        self.label_static_orbit_mean_anomaly = QLabel(self.verticalLayoutWidget_5)
        self.label_static_orbit_mean_anomaly.setObjectName(
            "label_static_orbit_mean_anomaly"
        )
        self.label_static_orbit_mean_anomaly.setFont(font2)

        self.grid_layout_orbit_elements.addWidget(
            self.label_static_orbit_mean_anomaly, 2, 3, 1, 1
        )

        self.line_edit_orbit_mean_anomaly = QLineEdit(self.verticalLayoutWidget_5)
        self.line_edit_orbit_mean_anomaly.setObjectName("line_edit_orbit_mean_anomaly")

        self.grid_layout_orbit_elements.addWidget(
            self.line_edit_orbit_mean_anomaly, 2, 4, 1, 1
        )

        self.vertical_layout_orbit.addLayout(self.grid_layout_orbit_elements)

        self.line_15 = QFrame(self.verticalLayoutWidget_5)
        self.line_15.setObjectName("line_15")
        self.line_15.setFrameShape(QFrame.HLine)
        self.line_15.setFrameShadow(QFrame.Sunken)

        self.vertical_layout_orbit.addWidget(self.line_15)

        self.horizontal_layout_orbit_results = QHBoxLayout()
        self.horizontal_layout_orbit_results.setObjectName(
            "horizontal_layout_orbit_results"
        )

        self.vertical_layout_orbit.addLayout(self.horizontal_layout_orbit_results)

        self.tabs_solutions.addTab(self.tab_orbit, "")
        self.tab_ephemeris = QWidget()
        self.tab_ephemeris.setObjectName("tab_ephemeris")
        self.verticalLayoutWidget_6 = QWidget(self.tab_ephemeris)
        self.verticalLayoutWidget_6.setObjectName("verticalLayoutWidget_6")
        self.verticalLayoutWidget_6.setGeometry(QRect(10, 10, 581, 251))
        self.verticalLayoutWidget_6.setFont(font)
        self.vertical_layout_ephemeris = QVBoxLayout(self.verticalLayoutWidget_6)
        self.vertical_layout_ephemeris.setObjectName("vertical_layout_ephemeris")
        self.vertical_layout_ephemeris.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout_solve_ephemeris = QHBoxLayout()
        self.horizontal_layout_solve_ephemeris.setObjectName(
            "horizontal_layout_solve_ephemeris"
        )
        self.combo_box_ephemeris_solve_engine = QComboBox(self.verticalLayoutWidget_6)
        self.combo_box_ephemeris_solve_engine.addItem("")
        self.combo_box_ephemeris_solve_engine.setObjectName(
            "combo_box_ephemeris_solve_engine"
        )

        self.horizontal_layout_solve_ephemeris.addWidget(
            self.combo_box_ephemeris_solve_engine
        )

        self.push_button_ephemeris_solve_ephemeris = QPushButton(
            self.verticalLayoutWidget_6
        )
        self.push_button_ephemeris_solve_ephemeris.setObjectName(
            "push_button_ephemeris_solve_ephemeris"
        )
        self.push_button_ephemeris_solve_ephemeris.setFont(font)

        self.horizontal_layout_solve_ephemeris.addWidget(
            self.push_button_ephemeris_solve_ephemeris
        )

        self.vertical_layout_ephemeris.addLayout(self.horizontal_layout_solve_ephemeris)

        self.line_19 = QFrame(self.verticalLayoutWidget_6)
        self.line_19.setObjectName("line_19")
        self.line_19.setFrameShape(QFrame.HLine)
        self.line_19.setFrameShadow(QFrame.Sunken)

        self.vertical_layout_ephemeris.addWidget(self.line_19)

        self.grid_layout_ephemeris_rate_results = QGridLayout()
        self.grid_layout_ephemeris_rate_results.setObjectName(
            "grid_layout_ephemeris_rate_results"
        )
        self.line_17 = QFrame(self.verticalLayoutWidget_6)
        self.line_17.setObjectName("line_17")
        self.line_17.setFrameShape(QFrame.VLine)
        self.line_17.setFrameShadow(QFrame.Sunken)

        self.grid_layout_ephemeris_rate_results.addWidget(self.line_17, 0, 5, 1, 1)

        self.label_dynamic_ephemeris_ra_acceleration = QLabel(
            self.verticalLayoutWidget_6
        )
        self.label_dynamic_ephemeris_ra_acceleration.setObjectName(
            "label_dynamic_ephemeris_ra_acceleration"
        )
        self.label_dynamic_ephemeris_ra_acceleration.setAlignment(Qt.AlignCenter)

        self.grid_layout_ephemeris_rate_results.addWidget(
            self.label_dynamic_ephemeris_ra_acceleration, 0, 6, 1, 1
        )

        self.label_dynamic_ephemeris_dec_acceleration = QLabel(
            self.verticalLayoutWidget_6
        )
        self.label_dynamic_ephemeris_dec_acceleration.setObjectName(
            "label_dynamic_ephemeris_dec_acceleration"
        )
        self.label_dynamic_ephemeris_dec_acceleration.setAlignment(Qt.AlignCenter)

        self.grid_layout_ephemeris_rate_results.addWidget(
            self.label_dynamic_ephemeris_dec_acceleration, 0, 7, 1, 1
        )

        self.label_dynamic_ephemeris_dec_velocity = QLabel(self.verticalLayoutWidget_6)
        self.label_dynamic_ephemeris_dec_velocity.setObjectName(
            "label_dynamic_ephemeris_dec_velocity"
        )
        self.label_dynamic_ephemeris_dec_velocity.setAlignment(Qt.AlignCenter)

        self.grid_layout_ephemeris_rate_results.addWidget(
            self.label_dynamic_ephemeris_dec_velocity, 0, 4, 1, 1
        )

        self.line_18 = QFrame(self.verticalLayoutWidget_6)
        self.line_18.setObjectName("line_18")
        self.line_18.setFrameShape(QFrame.VLine)
        self.line_18.setFrameShadow(QFrame.Sunken)

        self.grid_layout_ephemeris_rate_results.addWidget(self.line_18, 0, 2, 1, 1)

        self.label_dynamic_ephemeris_ra_velocity = QLabel(self.verticalLayoutWidget_6)
        self.label_dynamic_ephemeris_ra_velocity.setObjectName(
            "label_dynamic_ephemeris_ra_velocity"
        )
        self.label_dynamic_ephemeris_ra_velocity.setAlignment(Qt.AlignCenter)

        self.grid_layout_ephemeris_rate_results.addWidget(
            self.label_dynamic_ephemeris_ra_velocity, 0, 3, 1, 1
        )

        self.label_static_ephemeris_rate = QLabel(self.verticalLayoutWidget_6)
        self.label_static_ephemeris_rate.setObjectName("label_static_ephemeris_rate")

        self.grid_layout_ephemeris_rate_results.addWidget(
            self.label_static_ephemeris_rate, 0, 0, 1, 1
        )

        self.vertical_layout_ephemeris.addLayout(
            self.grid_layout_ephemeris_rate_results
        )

        self.push_button_ephemeris_update_tcs_rate = QPushButton(
            self.verticalLayoutWidget_6
        )
        self.push_button_ephemeris_update_tcs_rate.setObjectName(
            "push_button_ephemeris_update_tcs_rate"
        )

        self.vertical_layout_ephemeris.addWidget(
            self.push_button_ephemeris_update_tcs_rate
        )

        self.line_6 = QFrame(self.verticalLayoutWidget_6)
        self.line_6.setObjectName("line_6")
        self.line_6.setFrameShape(QFrame.HLine)
        self.line_6.setFrameShadow(QFrame.Sunken)

        self.vertical_layout_ephemeris.addWidget(self.line_6)

        self.grid_layout_ephemeris_custom_entry = QGridLayout()
        self.grid_layout_ephemeris_custom_entry.setObjectName(
            "grid_layout_ephemeris_custom_entry"
        )
        self.label_dynamic_ephemeris_custom_ra = QLabel(self.verticalLayoutWidget_6)
        self.label_dynamic_ephemeris_custom_ra.setObjectName(
            "label_dynamic_ephemeris_custom_ra"
        )
        self.label_dynamic_ephemeris_custom_ra.setAlignment(Qt.AlignCenter)

        self.grid_layout_ephemeris_custom_entry.addWidget(
            self.label_dynamic_ephemeris_custom_ra, 0, 3, 1, 1
        )

        self.date_time_edit_ephemeris_date_time = QDateTimeEdit(
            self.verticalLayoutWidget_6
        )
        self.date_time_edit_ephemeris_date_time.setObjectName(
            "date_time_edit_ephemeris_date_time"
        )
        self.date_time_edit_ephemeris_date_time.setTimeSpec(Qt.LocalTime)

        self.grid_layout_ephemeris_custom_entry.addWidget(
            self.date_time_edit_ephemeris_date_time, 0, 0, 1, 1
        )

        self.label_dynamic_ephemeris_custom_dec = QLabel(self.verticalLayoutWidget_6)
        self.label_dynamic_ephemeris_custom_dec.setObjectName(
            "label_dynamic_ephemeris_custom_dec"
        )
        self.label_dynamic_ephemeris_custom_dec.setAlignment(Qt.AlignCenter)

        self.grid_layout_ephemeris_custom_entry.addWidget(
            self.label_dynamic_ephemeris_custom_dec, 0, 4, 1, 1
        )

        self.combo_box_ephemeris_timezone = QComboBox(self.verticalLayoutWidget_6)
        self.combo_box_ephemeris_timezone.addItem("")
        self.combo_box_ephemeris_timezone.addItem("")
        self.combo_box_ephemeris_timezone.setObjectName("combo_box_ephemeris_timezone")
        self.combo_box_ephemeris_timezone.setLayoutDirection(Qt.LeftToRight)
        self.combo_box_ephemeris_timezone.setMinimumContentsLength(0)
        self.combo_box_ephemeris_timezone.setDuplicatesEnabled(False)

        self.grid_layout_ephemeris_custom_entry.addWidget(
            self.combo_box_ephemeris_timezone, 0, 1, 1, 1
        )

        self.push_button_ephemeris_custom_solve = QPushButton(
            self.verticalLayoutWidget_6
        )
        self.push_button_ephemeris_custom_solve.setObjectName(
            "push_button_ephemeris_custom_solve"
        )

        self.grid_layout_ephemeris_custom_entry.addWidget(
            self.push_button_ephemeris_custom_solve, 0, 2, 1, 1
        )

        self.vertical_layout_ephemeris.addLayout(
            self.grid_layout_ephemeris_custom_entry
        )

        self.tabs_solutions.addTab(self.tab_ephemeris, "")
        self.tab_propagate = QWidget()
        self.tab_propagate.setObjectName("tab_propagate")
        self.verticalLayoutWidget_4 = QWidget(self.tab_propagate)
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayoutWidget_4.setGeometry(QRect(10, 10, 581, 251))
        self.verticalLayoutWidget_4.setFont(font)
        self.vertical_layout_propagate = QVBoxLayout(self.verticalLayoutWidget_4)
        self.vertical_layout_propagate.setObjectName("vertical_layout_propagate")
        self.vertical_layout_propagate.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout_solve_propagation = QHBoxLayout()
        self.horizontal_layout_solve_propagation.setObjectName(
            "horizontal_layout_solve_propagation"
        )
        self.combo_box_propagate_solve_engine = QComboBox(self.verticalLayoutWidget_4)
        self.combo_box_propagate_solve_engine.addItem("")
        self.combo_box_propagate_solve_engine.addItem("")
        self.combo_box_propagate_solve_engine.setObjectName(
            "combo_box_propagate_solve_engine"
        )

        self.horizontal_layout_solve_propagation.addWidget(
            self.combo_box_propagate_solve_engine
        )

        self.push_button_propagate_solve_propagation = QPushButton(
            self.verticalLayoutWidget_4
        )
        self.push_button_propagate_solve_propagation.setObjectName(
            "push_button_propagate_solve_propagation"
        )
        self.push_button_propagate_solve_propagation.setFont(font)

        self.horizontal_layout_solve_propagation.addWidget(
            self.push_button_propagate_solve_propagation
        )

        self.vertical_layout_propagate.addLayout(
            self.horizontal_layout_solve_propagation
        )

        self.line_7 = QFrame(self.verticalLayoutWidget_4)
        self.line_7.setObjectName("line_7")
        self.line_7.setFrameShape(QFrame.HLine)
        self.line_7.setFrameShadow(QFrame.Sunken)

        self.vertical_layout_propagate.addWidget(self.line_7)

        self.grid_layout_propagate_rate_results = QGridLayout()
        self.grid_layout_propagate_rate_results.setObjectName(
            "grid_layout_propagate_rate_results"
        )
        self.line_12 = QFrame(self.verticalLayoutWidget_4)
        self.line_12.setObjectName("line_12")
        self.line_12.setFrameShape(QFrame.VLine)
        self.line_12.setFrameShadow(QFrame.Sunken)

        self.grid_layout_propagate_rate_results.addWidget(self.line_12, 0, 5, 1, 1)

        self.label_dynamic_propagate_ra_acceleration = QLabel(
            self.verticalLayoutWidget_4
        )
        self.label_dynamic_propagate_ra_acceleration.setObjectName(
            "label_dynamic_propagate_ra_acceleration"
        )
        self.label_dynamic_propagate_ra_acceleration.setAlignment(Qt.AlignCenter)

        self.grid_layout_propagate_rate_results.addWidget(
            self.label_dynamic_propagate_ra_acceleration, 0, 6, 1, 1
        )

        self.label_dynamic_propagate_dec_acceleration = QLabel(
            self.verticalLayoutWidget_4
        )
        self.label_dynamic_propagate_dec_acceleration.setObjectName(
            "label_dynamic_propagate_dec_acceleration"
        )
        self.label_dynamic_propagate_dec_acceleration.setAlignment(Qt.AlignCenter)

        self.grid_layout_propagate_rate_results.addWidget(
            self.label_dynamic_propagate_dec_acceleration, 0, 7, 1, 1
        )

        self.label_dynamic_propagate_dec_velocity = QLabel(self.verticalLayoutWidget_4)
        self.label_dynamic_propagate_dec_velocity.setObjectName(
            "label_dynamic_propagate_dec_velocity"
        )
        self.label_dynamic_propagate_dec_velocity.setAlignment(Qt.AlignCenter)

        self.grid_layout_propagate_rate_results.addWidget(
            self.label_dynamic_propagate_dec_velocity, 0, 4, 1, 1
        )

        self.line_11 = QFrame(self.verticalLayoutWidget_4)
        self.line_11.setObjectName("line_11")
        self.line_11.setFrameShape(QFrame.VLine)
        self.line_11.setFrameShadow(QFrame.Sunken)

        self.grid_layout_propagate_rate_results.addWidget(self.line_11, 0, 2, 1, 1)

        self.label_dynamic_propagate_ra_velocity = QLabel(self.verticalLayoutWidget_4)
        self.label_dynamic_propagate_ra_velocity.setObjectName(
            "label_dynamic_propagate_ra_velocity"
        )
        self.label_dynamic_propagate_ra_velocity.setAlignment(Qt.AlignCenter)

        self.grid_layout_propagate_rate_results.addWidget(
            self.label_dynamic_propagate_ra_velocity, 0, 3, 1, 1
        )

        self.label_static_propagate_rate = QLabel(self.verticalLayoutWidget_4)
        self.label_static_propagate_rate.setObjectName("label_static_propagate_rate")

        self.grid_layout_propagate_rate_results.addWidget(
            self.label_static_propagate_rate, 0, 0, 1, 1
        )

        self.vertical_layout_propagate.addLayout(
            self.grid_layout_propagate_rate_results
        )

        self.push_button_propagate_update_tcs_rate = QPushButton(
            self.verticalLayoutWidget_4
        )
        self.push_button_propagate_update_tcs_rate.setObjectName(
            "push_button_propagate_update_tcs_rate"
        )

        self.vertical_layout_propagate.addWidget(
            self.push_button_propagate_update_tcs_rate
        )

        self.line_10 = QFrame(self.verticalLayoutWidget_4)
        self.line_10.setObjectName("line_10")
        self.line_10.setFrameShape(QFrame.HLine)
        self.line_10.setFrameShadow(QFrame.Sunken)

        self.vertical_layout_propagate.addWidget(self.line_10)

        self.grid_layout_propagate_custom_entry = QGridLayout()
        self.grid_layout_propagate_custom_entry.setObjectName(
            "grid_layout_propagate_custom_entry"
        )
        self.date_time_edit_propagate_date_time = QDateTimeEdit(
            self.verticalLayoutWidget_4
        )
        self.date_time_edit_propagate_date_time.setObjectName(
            "date_time_edit_propagate_date_time"
        )
        self.date_time_edit_propagate_date_time.setTimeSpec(Qt.LocalTime)

        self.grid_layout_propagate_custom_entry.addWidget(
            self.date_time_edit_propagate_date_time, 0, 0, 1, 1
        )

        self.label_dynamic_propagate_custom_dec = QLabel(self.verticalLayoutWidget_4)
        self.label_dynamic_propagate_custom_dec.setObjectName(
            "label_dynamic_propagate_custom_dec"
        )
        self.label_dynamic_propagate_custom_dec.setAlignment(Qt.AlignCenter)

        self.grid_layout_propagate_custom_entry.addWidget(
            self.label_dynamic_propagate_custom_dec, 0, 4, 1, 1
        )

        self.label_dynamic_propagate_custom_ra = QLabel(self.verticalLayoutWidget_4)
        self.label_dynamic_propagate_custom_ra.setObjectName(
            "label_dynamic_propagate_custom_ra"
        )
        self.label_dynamic_propagate_custom_ra.setAlignment(Qt.AlignCenter)

        self.grid_layout_propagate_custom_entry.addWidget(
            self.label_dynamic_propagate_custom_ra, 0, 3, 1, 1
        )

        self.push_button_propagate_custom_solve = QPushButton(
            self.verticalLayoutWidget_4
        )
        self.push_button_propagate_custom_solve.setObjectName(
            "push_button_propagate_custom_solve"
        )

        self.grid_layout_propagate_custom_entry.addWidget(
            self.push_button_propagate_custom_solve, 0, 2, 1, 1
        )

        self.combo_box_propagate_timezone = QComboBox(self.verticalLayoutWidget_4)
        self.combo_box_propagate_timezone.addItem("")
        self.combo_box_propagate_timezone.addItem("")
        self.combo_box_propagate_timezone.setObjectName("combo_box_propagate_timezone")
        self.combo_box_propagate_timezone.setLayoutDirection(Qt.LeftToRight)
        self.combo_box_propagate_timezone.setMinimumContentsLength(0)
        self.combo_box_propagate_timezone.setDuplicatesEnabled(False)

        self.grid_layout_propagate_custom_entry.addWidget(
            self.combo_box_propagate_timezone, 0, 1, 1, 1
        )

        self.vertical_layout_propagate.addLayout(
            self.grid_layout_propagate_custom_entry
        )

        self.tabs_solutions.addTab(self.tab_propagate, "")

        self.vertical_layout_solutions.addWidget(self.tabs_solutions)

        self.vertical_layout_window.addLayout(self.vertical_layout_solutions)

        ManualWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(ManualWindow)
        self.statusbar.setObjectName("statusbar")
        ManualWindow.setStatusBar(self.statusbar)

        self.retranslateUi(ManualWindow)

        self.tabs_solutions.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(ManualWindow)

    # setupUi

    def retranslateUi(self, ManualWindow):
        ManualWindow.setWindowTitle(
            QCoreApplication.translate("ManualWindow", "OpihiExarata Manual Mode", None)
        )
        self.push_button_new_target.setText(
            QCoreApplication.translate("ManualWindow", "New Target", None)
        )
        self.push_button_new_image_automatic.setText(
            QCoreApplication.translate("ManualWindow", "Automatic New Image", None)
        )
        self.push_button_new_image_manual.setText(
            QCoreApplication.translate("ManualWindow", "Manual New Image", None)
        )
        self.dummy_opihi_navbar.setText(
            QCoreApplication.translate(
                "ManualWindow", "DUMMY OPIHI IMAGE NAVIGATION BAR.", None
            )
        )
        self.push_button_refresh_window.setText(
            QCoreApplication.translate("ManualWindow", "Refresh Window", None)
        )
        self.label_static_summary_target_name.setText(
            QCoreApplication.translate("ManualWindow", "Target Name:", None)
        )
        self.label_static_summary_fits_file.setText(
            QCoreApplication.translate("ManualWindow", "FITS File:", None)
        )
        self.label_dynamic_summary_target_name.setText(
            QCoreApplication.translate("ManualWindow", "DEFAULT", None)
        )
        self.label_dynamic_summary_fits_file.setText(
            QCoreApplication.translate(
                "ManualWindow", "opi.20XXA999.YYMMDD.AAAAAAAAA.00001.a.fits", None
            )
        )
        self.label_static_summary_directory.setText(
            QCoreApplication.translate("ManualWindow", "Directory:", None)
        )
        self.label_dynamic_summary_directory.setText(
            QCoreApplication.translate("ManualWindow", "/path/to/dir/", None)
        )
        self.push_button_send_target_to_tcs.setText(
            QCoreApplication.translate("ManualWindow", "Send Target to TCS", None)
        )
        self.check_box_summary_autosave.setText(
            QCoreApplication.translate("ManualWindow", "Auto", None)
        )
        self.push_button_summary_save.setText(
            QCoreApplication.translate("ManualWindow", "Save", None)
        )
        self.tabs_solutions.setTabText(
            self.tabs_solutions.indexOf(self.tab_summary),
            QCoreApplication.translate("ManualWindow", "Summary", None),
        )
        self.combo_box_astrometry_solve_engine.setItemText(
            0, QCoreApplication.translate("ManualWindow", "Astrometry.net Nova", None)
        )
        self.combo_box_astrometry_solve_engine.setItemText(
            1, QCoreApplication.translate("ManualWindow", "Astrometry.net Host", None)
        )

        self.push_button_astrometry_solve_astrometry.setText(
            QCoreApplication.translate("ManualWindow", "Solve Astrometry", None)
        )
        self.label_dynamic_astrometry_target_x.setText(
            QCoreApplication.translate("ManualWindow", "0000", None)
        )
        self.label_dynamic_astrometry_target_y.setText(
            QCoreApplication.translate("ManualWindow", "0000", None)
        )
        self.label_static_astrometry_target_coordinates.setText(
            QCoreApplication.translate("ManualWindow", "Target/Asteroid:", None)
        )
        self.label_dynamic_astrometry_center_ra.setText(
            QCoreApplication.translate("ManualWindow", "HH:MM:SS.SS", None)
        )
        self.label_static_astrometry_center_coordinates.setText(
            QCoreApplication.translate("ManualWindow", "Opihi Center:", None)
        )
        self.label_dynamic_astrometry_center_dec.setText(
            QCoreApplication.translate("ManualWindow", "+DD:MM:SS.SS", None)
        )
        self.label_dynamic_astrometry_target_ra.setText(
            QCoreApplication.translate("ManualWindow", "HH:MM:SS.SS", None)
        )
        self.label_dynamic_astrometry_target_dec.setText(
            QCoreApplication.translate("ManualWindow", "+DD:MM:SS.SS", None)
        )
        self.label_dynamic_astrometry_center_y.setText(
            QCoreApplication.translate("ManualWindow", "0000", None)
        )
        self.label_dynamic_astrometry_center_x.setText(
            QCoreApplication.translate("ManualWindow", "0000", None)
        )
        self.push_button_astrometry_custom_solve.setText(
            QCoreApplication.translate("ManualWindow", "Custom Solve", None)
        )
        self.tabs_solutions.setTabText(
            self.tabs_solutions.indexOf(self.tab_astrometry),
            QCoreApplication.translate("ManualWindow", "Astrometry", None),
        )
        self.combo_box_photometry_solve_engine.setItemText(
            0,
            QCoreApplication.translate("ManualWindow", "Pan-STARRS 3pi DR2 MAST", None),
        )

        self.push_button_photometry_solve_photometry.setText(
            QCoreApplication.translate("ManualWindow", "Solve Photometry", None)
        )
        self.label_static_photometry_filter_label.setText(
            QCoreApplication.translate("ManualWindow", "Filter", None)
        )
        self.label_dynamic_photometry_filter_name.setText(
            QCoreApplication.translate("ManualWindow", "FF", None)
        )
        self.label_static_photometry_magnitude.setText(
            QCoreApplication.translate("ManualWindow", "Magnitude", None)
        )
        self.label_dynamic_photometry_magnitude.setText(
            QCoreApplication.translate("ManualWindow", "MM.MM + E.EEE", None)
        )
        self.label_static_photometry_zero_point_label.setText(
            QCoreApplication.translate("ManualWindow", "Zero Point ", None)
        )
        self.label_dynamic_photometry_zero_point_value.setText(
            QCoreApplication.translate("ManualWindow", "ZZ.ZZ + E.EEE", None)
        )
        self.tabs_solutions.setTabText(
            self.tabs_solutions.indexOf(self.tab_photometry),
            QCoreApplication.translate("ManualWindow", "Photometry", None),
        )
        self.combo_box_orbit_solve_engine.setItemText(
            0, QCoreApplication.translate("ManualWindow", "OrbFit", None)
        )
        self.combo_box_orbit_solve_engine.setItemText(
            1, QCoreApplication.translate("ManualWindow", "Custom Orbit", None)
        )

        self.push_button_orbit_solve_orbit.setText(
            QCoreApplication.translate("ManualWindow", "Solve Orbit", None)
        )
        self.line_edit_orbit_inclination.setText(
            QCoreApplication.translate("ManualWindow", "VV.VVV + EE.EEE", None)
        )
        self.line_edit_orbit_perihelion.setText(
            QCoreApplication.translate("ManualWindow", "VV.VVV + EE.EEE", None)
        )
        self.line_edit_orbit_epoch.setText(
            QCoreApplication.translate("ManualWindow", "EEEEEEE.EEEEE", None)
        )
        self.label_static_orbit_inclination.setText(
            QCoreApplication.translate("ManualWindow", "Incli.", None)
        )
        self.label_static_orbit_perihelion.setText(
            QCoreApplication.translate("ManualWindow", "Peri.", None)
        )
        self.label_static_orbit_epoch.setText(
            QCoreApplication.translate("ManualWindow", "Epoch", None)
        )
        self.line_edit_orbit_semimajor_axis.setText(
            QCoreApplication.translate("ManualWindow", "VV.VVV + EE.EEE", None)
        )
        self.label_static_orbit_semimajor_axis.setText(
            QCoreApplication.translate("ManualWindow", "SM-Axis", None)
        )
        self.label_static_orbit_eccentricity.setText(
            QCoreApplication.translate("ManualWindow", "Ecc.", None)
        )
        self.line_edit_orbit_eccentricity.setText(
            QCoreApplication.translate("ManualWindow", "VV.VVV + EE.EEE", None)
        )
        self.label_static_orbit_ascending_node.setText(
            QCoreApplication.translate("ManualWindow", "As-Node", None)
        )
        self.line_edit_orbit_ascending_node.setText(
            QCoreApplication.translate("ManualWindow", "VV.VVV + EE.EEE", None)
        )
        self.label_static_orbit_mean_anomaly.setText(
            QCoreApplication.translate("ManualWindow", "M-Anom.", None)
        )
        self.line_edit_orbit_mean_anomaly.setText(
            QCoreApplication.translate("ManualWindow", "VV.VVV + EE.EEE", None)
        )
        self.tabs_solutions.setTabText(
            self.tabs_solutions.indexOf(self.tab_orbit),
            QCoreApplication.translate("ManualWindow", "Orbit", None),
        )
        self.combo_box_ephemeris_solve_engine.setItemText(
            0, QCoreApplication.translate("ManualWindow", "JPL Horizons", None)
        )

        self.push_button_ephemeris_solve_ephemeris.setText(
            QCoreApplication.translate("ManualWindow", "Solve Ephemeris", None)
        )
        self.label_dynamic_ephemeris_ra_acceleration.setText(
            QCoreApplication.translate("ManualWindow", "+AA.AAAeXX", None)
        )
        self.label_dynamic_ephemeris_dec_acceleration.setText(
            QCoreApplication.translate("ManualWindow", "+AA.AAAeXX", None)
        )
        self.label_dynamic_ephemeris_dec_velocity.setText(
            QCoreApplication.translate("ManualWindow", "+VV.VVV", None)
        )
        self.label_dynamic_ephemeris_ra_velocity.setText(
            QCoreApplication.translate("ManualWindow", "+VV.VVV", None)
        )
        self.label_static_ephemeris_rate.setText(
            QCoreApplication.translate(
                "ManualWindow",
                "<html><head/><body><p>Ephemeris Rate [ &quot;/s | &quot;/s<span"
                ' style=" vertical-align:super;">2</span> ]</p></body></html>',
                None,
            )
        )
        self.push_button_ephemeris_update_tcs_rate.setText(
            QCoreApplication.translate("ManualWindow", "Update TCS Rate", None)
        )
        self.label_dynamic_ephemeris_custom_ra.setText(
            QCoreApplication.translate("ManualWindow", "HH:MM:SS.SS", None)
        )
        self.date_time_edit_ephemeris_date_time.setDisplayFormat(
            QCoreApplication.translate("ManualWindow", "yyyy-MM-dd HH:mm:ss", None)
        )
        self.label_dynamic_ephemeris_custom_dec.setText(
            QCoreApplication.translate("ManualWindow", "+DD:MM:SS.SS", None)
        )
        self.combo_box_ephemeris_timezone.setItemText(
            0, QCoreApplication.translate("ManualWindow", "UTC+00:00", None)
        )
        self.combo_box_ephemeris_timezone.setItemText(
            1, QCoreApplication.translate("ManualWindow", "HST-10:00", None)
        )

        self.push_button_ephemeris_custom_solve.setText(
            QCoreApplication.translate("ManualWindow", "Custom Solve", None)
        )
        self.tabs_solutions.setTabText(
            self.tabs_solutions.indexOf(self.tab_ephemeris),
            QCoreApplication.translate("ManualWindow", "Ephemeris", None),
        )
        self.combo_box_propagate_solve_engine.setItemText(
            0, QCoreApplication.translate("ManualWindow", "Linear", None)
        )
        self.combo_box_propagate_solve_engine.setItemText(
            1, QCoreApplication.translate("ManualWindow", "Quadratic", None)
        )

        self.push_button_propagate_solve_propagation.setText(
            QCoreApplication.translate("ManualWindow", "Solve Propagation", None)
        )
        self.label_dynamic_propagate_ra_acceleration.setText(
            QCoreApplication.translate("ManualWindow", "+AA.AAAeXX", None)
        )
        self.label_dynamic_propagate_dec_acceleration.setText(
            QCoreApplication.translate("ManualWindow", "+AA.AAAeXX", None)
        )
        self.label_dynamic_propagate_dec_velocity.setText(
            QCoreApplication.translate("ManualWindow", "+VV.VVV", None)
        )
        self.label_dynamic_propagate_ra_velocity.setText(
            QCoreApplication.translate("ManualWindow", "+VV.VVV", None)
        )
        self.label_static_propagate_rate.setText(
            QCoreApplication.translate(
                "ManualWindow",
                "<html><head/><body><p>Propagate Rate [ &quot;/s | &quot;/s<span"
                ' style=" vertical-align:super;">2</span> ]</p></body></html>',
                None,
            )
        )
        self.push_button_propagate_update_tcs_rate.setText(
            QCoreApplication.translate("ManualWindow", "Update TCS Rate", None)
        )
        self.date_time_edit_propagate_date_time.setDisplayFormat(
            QCoreApplication.translate("ManualWindow", "yyyy-MM-dd HH:mm:ss", None)
        )
        self.label_dynamic_propagate_custom_dec.setText(
            QCoreApplication.translate("ManualWindow", "+DD:MM:SS.SS", None)
        )
        self.label_dynamic_propagate_custom_ra.setText(
            QCoreApplication.translate("ManualWindow", "HH:MM:SS.SS", None)
        )
        self.push_button_propagate_custom_solve.setText(
            QCoreApplication.translate("ManualWindow", "Custom Solve", None)
        )
        self.combo_box_propagate_timezone.setItemText(
            0, QCoreApplication.translate("ManualWindow", "UTC+00:00", None)
        )
        self.combo_box_propagate_timezone.setItemText(
            1, QCoreApplication.translate("ManualWindow", "HST-10:00", None)
        )

        self.tabs_solutions.setTabText(
            self.tabs_solutions.indexOf(self.tab_propagate),
            QCoreApplication.translate("ManualWindow", "Propagate", None),
        )

    # retranslateUi
