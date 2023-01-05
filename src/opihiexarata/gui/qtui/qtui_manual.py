# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'manual.ui'
##
## Created by: Qt User Interface Compiler version 6.3.2
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
    QButtonGroup,
    QComboBox,
    QDateTimeEdit,
    QFrame,
    QGraphicsView,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLayout,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QRadioButton,
    QSizePolicy,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)


class Ui_ManualWindow(object):
    def setupUi(self, ManualWindow):
        if not ManualWindow.objectName():
            ManualWindow.setObjectName("ManualWindow")
        ManualWindow.resize(930, 821)
        self.central_widget = QWidget(ManualWindow)
        self.central_widget.setObjectName("central_widget")
        self.verticalLayoutWidget = QWidget(self.central_widget)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 10, 911, 801))
        font = QFont()
        font.setFamilies(["Cantarell"])
        font.setPointSize(12)
        self.verticalLayoutWidget.setFont(font)
        self.vertical_layout_window = QVBoxLayout(self.verticalLayoutWidget)
        self.vertical_layout_window.setObjectName("vertical_layout_window")
        self.vertical_layout_window.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout_image_file = QHBoxLayout()
        self.horizontal_layout_image_file.setObjectName("horizontal_layout_image_file")
        self.vertical_layout_image = QVBoxLayout()
        self.vertical_layout_image.setObjectName("vertical_layout_image")
        self.graphics_view_dummy_opihi_image = QGraphicsView(self.verticalLayoutWidget)
        self.graphics_view_dummy_opihi_image.setObjectName(
            "graphics_view_dummy_opihi_image"
        )
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.graphics_view_dummy_opihi_image.sizePolicy().hasHeightForWidth()
        )
        self.graphics_view_dummy_opihi_image.setSizePolicy(sizePolicy)
        self.graphics_view_dummy_opihi_image.setMinimumSize(QSize(400, 400))
        self.graphics_view_dummy_opihi_image.setMaximumSize(QSize(400, 400))
        self.graphics_view_dummy_opihi_image.setFont(font)

        self.vertical_layout_image.addWidget(self.graphics_view_dummy_opihi_image)

        self.label_static_dummy_opihi_navbar = QLabel(self.verticalLayoutWidget)
        self.label_static_dummy_opihi_navbar.setObjectName(
            "label_static_dummy_opihi_navbar"
        )
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(
            self.label_static_dummy_opihi_navbar.sizePolicy().hasHeightForWidth()
        )
        self.label_static_dummy_opihi_navbar.setSizePolicy(sizePolicy1)
        self.label_static_dummy_opihi_navbar.setMinimumSize(QSize(0, 25))
        self.label_static_dummy_opihi_navbar.setBaseSize(QSize(0, 0))
        self.label_static_dummy_opihi_navbar.setFont(font)
        self.label_static_dummy_opihi_navbar.setAlignment(Qt.AlignCenter)

        self.vertical_layout_image.addWidget(self.label_static_dummy_opihi_navbar)

        self.horizontal_layout_image_file.addLayout(self.vertical_layout_image)

        self.line = QFrame(self.verticalLayoutWidget)
        self.line.setObjectName("line")
        self.line.setFont(font)
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontal_layout_image_file.addWidget(self.line)

        self.grid_layout_file_selector = QGridLayout()
        self.grid_layout_file_selector.setObjectName("grid_layout_file_selector")
        self.label_dynamic_target_4_pixel_location = QLabel(self.verticalLayoutWidget)
        self.label_dynamic_target_4_pixel_location.setObjectName(
            "label_dynamic_target_4_pixel_location"
        )
        self.label_dynamic_target_4_pixel_location.setAlignment(Qt.AlignCenter)

        self.grid_layout_file_selector.addWidget(
            self.label_dynamic_target_4_pixel_location, 12, 3, 1, 1
        )

        self.label_static_target_3_location = QLabel(self.verticalLayoutWidget)
        self.label_static_target_3_location.setObjectName(
            "label_static_target_3_location"
        )

        self.grid_layout_file_selector.addWidget(
            self.label_static_target_3_location, 9, 2, 1, 1
        )

        self.label_static_target_4_location = QLabel(self.verticalLayoutWidget)
        self.label_static_target_4_location.setObjectName(
            "label_static_target_4_location"
        )

        self.grid_layout_file_selector.addWidget(
            self.label_static_target_4_location, 12, 2, 1, 1
        )

        self.push_button_relocate_target_location_1 = QPushButton(
            self.verticalLayoutWidget
        )
        self.push_button_relocate_target_location_1.setObjectName(
            "push_button_relocate_target_location_1"
        )
        self.push_button_relocate_target_location_1.setFont(font)

        self.grid_layout_file_selector.addWidget(
            self.push_button_relocate_target_location_1, 3, 4, 1, 1
        )

        self.label_dynamic_target_1_pixel_location = QLabel(self.verticalLayoutWidget)
        self.label_dynamic_target_1_pixel_location.setObjectName(
            "label_dynamic_target_1_pixel_location"
        )
        self.label_dynamic_target_1_pixel_location.setAlignment(Qt.AlignCenter)

        self.grid_layout_file_selector.addWidget(
            self.label_dynamic_target_1_pixel_location, 3, 3, 1, 1
        )

        self.push_button_load_filename_3 = QPushButton(self.verticalLayoutWidget)
        self.push_button_load_filename_3.setObjectName("push_button_load_filename_3")

        self.grid_layout_file_selector.addWidget(
            self.push_button_load_filename_3, 8, 4, 1, 1
        )

        self.label_dynamic_filename_3 = QLabel(self.verticalLayoutWidget)
        self.label_dynamic_filename_3.setObjectName("label_dynamic_filename_3")

        self.grid_layout_file_selector.addWidget(
            self.label_dynamic_filename_3, 8, 0, 1, 4
        )

        self.label_dynamic_filename_1 = QLabel(self.verticalLayoutWidget)
        self.label_dynamic_filename_1.setObjectName("label_dynamic_filename_1")
        self.label_dynamic_filename_1.setFont(font)

        self.grid_layout_file_selector.addWidget(
            self.label_dynamic_filename_1, 2, 0, 1, 4
        )

        self.label_dynamic_filename_2 = QLabel(self.verticalLayoutWidget)
        self.label_dynamic_filename_2.setObjectName("label_dynamic_filename_2")

        self.grid_layout_file_selector.addWidget(
            self.label_dynamic_filename_2, 5, 0, 1, 4
        )

        self.line_35 = QFrame(self.verticalLayoutWidget)
        self.line_35.setObjectName("line_35")
        self.line_35.setFrameShape(QFrame.VLine)
        self.line_35.setFrameShadow(QFrame.Sunken)

        self.grid_layout_file_selector.addWidget(self.line_35, 6, 1, 1, 1)

        self.line_37 = QFrame(self.verticalLayoutWidget)
        self.line_37.setObjectName("line_37")
        self.line_37.setFrameShape(QFrame.VLine)
        self.line_37.setFrameShadow(QFrame.Sunken)

        self.grid_layout_file_selector.addWidget(self.line_37, 12, 1, 1, 1)

        self.label_dynamic_filename_4 = QLabel(self.verticalLayoutWidget)
        self.label_dynamic_filename_4.setObjectName("label_dynamic_filename_4")

        self.grid_layout_file_selector.addWidget(
            self.label_dynamic_filename_4, 11, 0, 1, 4
        )

        self.radio_button_primary_file_3 = QRadioButton(self.verticalLayoutWidget)
        self.button_group_primary_working_file = QButtonGroup(ManualWindow)
        self.button_group_primary_working_file.setObjectName(
            "button_group_primary_working_file"
        )
        self.button_group_primary_working_file.addButton(
            self.radio_button_primary_file_3
        )
        self.radio_button_primary_file_3.setObjectName("radio_button_primary_file_3")
        self.radio_button_primary_file_3.setEnabled(True)
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(
            self.radio_button_primary_file_3.sizePolicy().hasHeightForWidth()
        )
        self.radio_button_primary_file_3.setSizePolicy(sizePolicy2)
        self.radio_button_primary_file_3.setMaximumSize(QSize(30, 16777215))

        self.grid_layout_file_selector.addWidget(
            self.radio_button_primary_file_3, 9, 0, 1, 1
        )

        self.line_36 = QFrame(self.verticalLayoutWidget)
        self.line_36.setObjectName("line_36")
        self.line_36.setFrameShape(QFrame.VLine)
        self.line_36.setFrameShadow(QFrame.Sunken)

        self.grid_layout_file_selector.addWidget(self.line_36, 9, 1, 1, 1)

        self.line_34 = QFrame(self.verticalLayoutWidget)
        self.line_34.setObjectName("line_34")
        self.line_34.setFrameShape(QFrame.VLine)
        self.line_34.setFrameShadow(QFrame.Sunken)

        self.grid_layout_file_selector.addWidget(self.line_34, 3, 1, 1, 1)

        self.radio_button_primary_file_4 = QRadioButton(self.verticalLayoutWidget)
        self.button_group_primary_working_file.addButton(
            self.radio_button_primary_file_4
        )
        self.radio_button_primary_file_4.setObjectName("radio_button_primary_file_4")
        self.radio_button_primary_file_4.setEnabled(True)
        sizePolicy2.setHeightForWidth(
            self.radio_button_primary_file_4.sizePolicy().hasHeightForWidth()
        )
        self.radio_button_primary_file_4.setSizePolicy(sizePolicy2)
        self.radio_button_primary_file_4.setMaximumSize(QSize(30, 16777215))

        self.grid_layout_file_selector.addWidget(
            self.radio_button_primary_file_4, 12, 0, 1, 1
        )

        self.label_dynamic_target_2_pixel_location = QLabel(self.verticalLayoutWidget)
        self.label_dynamic_target_2_pixel_location.setObjectName(
            "label_dynamic_target_2_pixel_location"
        )
        self.label_dynamic_target_2_pixel_location.setAlignment(Qt.AlignCenter)

        self.grid_layout_file_selector.addWidget(
            self.label_dynamic_target_2_pixel_location, 6, 3, 1, 1
        )

        self.push_button_relocate_target_location_3 = QPushButton(
            self.verticalLayoutWidget
        )
        self.push_button_relocate_target_location_3.setObjectName(
            "push_button_relocate_target_location_3"
        )

        self.grid_layout_file_selector.addWidget(
            self.push_button_relocate_target_location_3, 9, 4, 1, 1
        )

        self.radio_button_primary_file_1 = QRadioButton(self.verticalLayoutWidget)
        self.button_group_primary_working_file.addButton(
            self.radio_button_primary_file_1
        )
        self.radio_button_primary_file_1.setObjectName("radio_button_primary_file_1")
        sizePolicy2.setHeightForWidth(
            self.radio_button_primary_file_1.sizePolicy().hasHeightForWidth()
        )
        self.radio_button_primary_file_1.setSizePolicy(sizePolicy2)
        self.radio_button_primary_file_1.setMaximumSize(QSize(30, 16777215))
        self.radio_button_primary_file_1.setChecked(True)

        self.grid_layout_file_selector.addWidget(
            self.radio_button_primary_file_1, 3, 0, 1, 1
        )

        self.label_dynamic_target_3_pixel_location = QLabel(self.verticalLayoutWidget)
        self.label_dynamic_target_3_pixel_location.setObjectName(
            "label_dynamic_target_3_pixel_location"
        )
        self.label_dynamic_target_3_pixel_location.setAlignment(Qt.AlignCenter)

        self.grid_layout_file_selector.addWidget(
            self.label_dynamic_target_3_pixel_location, 9, 3, 1, 1
        )

        self.radio_button_primary_file_2 = QRadioButton(self.verticalLayoutWidget)
        self.button_group_primary_working_file.addButton(
            self.radio_button_primary_file_2
        )
        self.radio_button_primary_file_2.setObjectName("radio_button_primary_file_2")
        sizePolicy2.setHeightForWidth(
            self.radio_button_primary_file_2.sizePolicy().hasHeightForWidth()
        )
        self.radio_button_primary_file_2.setSizePolicy(sizePolicy2)
        self.radio_button_primary_file_2.setMaximumSize(QSize(30, 16777215))

        self.grid_layout_file_selector.addWidget(
            self.radio_button_primary_file_2, 6, 0, 1, 1
        )

        self.label_static_target_2_location = QLabel(self.verticalLayoutWidget)
        self.label_static_target_2_location.setObjectName(
            "label_static_target_2_location"
        )

        self.grid_layout_file_selector.addWidget(
            self.label_static_target_2_location, 6, 2, 1, 1
        )

        self.push_button_relocate_target_location_2 = QPushButton(
            self.verticalLayoutWidget
        )
        self.push_button_relocate_target_location_2.setObjectName(
            "push_button_relocate_target_location_2"
        )

        self.grid_layout_file_selector.addWidget(
            self.push_button_relocate_target_location_2, 6, 4, 1, 1
        )

        self.push_button_load_filename_1 = QPushButton(self.verticalLayoutWidget)
        self.push_button_load_filename_1.setObjectName("push_button_load_filename_1")
        self.push_button_load_filename_1.setFont(font)

        self.grid_layout_file_selector.addWidget(
            self.push_button_load_filename_1, 2, 4, 1, 1
        )

        self.push_button_load_filename_2 = QPushButton(self.verticalLayoutWidget)
        self.push_button_load_filename_2.setObjectName("push_button_load_filename_2")

        self.grid_layout_file_selector.addWidget(
            self.push_button_load_filename_2, 5, 4, 1, 1
        )

        self.label_static_target_1_location = QLabel(self.verticalLayoutWidget)
        self.label_static_target_1_location.setObjectName(
            "label_static_target_1_location"
        )
        self.label_static_target_1_location.setFont(font)

        self.grid_layout_file_selector.addWidget(
            self.label_static_target_1_location, 3, 2, 1, 1
        )

        self.push_button_load_filename_4 = QPushButton(self.verticalLayoutWidget)
        self.push_button_load_filename_4.setObjectName("push_button_load_filename_4")

        self.grid_layout_file_selector.addWidget(
            self.push_button_load_filename_4, 11, 4, 1, 1
        )

        self.push_button_relocate_target_location_4 = QPushButton(
            self.verticalLayoutWidget
        )
        self.push_button_relocate_target_location_4.setObjectName(
            "push_button_relocate_target_location_4"
        )

        self.grid_layout_file_selector.addWidget(
            self.push_button_relocate_target_location_4, 12, 4, 1, 1
        )

        self.push_button_force_reset = QPushButton(self.verticalLayoutWidget)
        self.push_button_force_reset.setObjectName("push_button_force_reset")

        self.grid_layout_file_selector.addWidget(
            self.push_button_force_reset, 0, 4, 1, 1
        )

        self.push_button_save_and_reset = QPushButton(self.verticalLayoutWidget)
        self.push_button_save_and_reset.setObjectName("push_button_save_and_reset")
        sizePolicy3 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(
            self.push_button_save_and_reset.sizePolicy().hasHeightForWidth()
        )
        self.push_button_save_and_reset.setSizePolicy(sizePolicy3)

        self.grid_layout_file_selector.addWidget(
            self.push_button_save_and_reset, 0, 0, 1, 4
        )

        self.line_38 = QFrame(self.verticalLayoutWidget)
        self.line_38.setObjectName("line_38")
        self.line_38.setFrameShape(QFrame.HLine)
        self.line_38.setFrameShadow(QFrame.Sunken)

        self.grid_layout_file_selector.addWidget(self.line_38, 1, 0, 1, 5)

        self.line_2 = QFrame(self.verticalLayoutWidget)
        self.line_2.setObjectName("line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.grid_layout_file_selector.addWidget(self.line_2, 4, 1, 1, 4)

        self.line_3 = QFrame(self.verticalLayoutWidget)
        self.line_3.setObjectName("line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.grid_layout_file_selector.addWidget(self.line_3, 7, 1, 1, 4)

        self.line_4 = QFrame(self.verticalLayoutWidget)
        self.line_4.setObjectName("line_4")
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.grid_layout_file_selector.addWidget(self.line_4, 10, 1, 1, 4)

        self.horizontal_layout_image_file.addLayout(self.grid_layout_file_selector)

        self.vertical_layout_window.addLayout(self.horizontal_layout_image_file)

        self.line_5 = QFrame(self.verticalLayoutWidget)
        self.line_5.setObjectName("line_5")
        self.line_5.setFrameShape(QFrame.HLine)
        self.line_5.setFrameShadow(QFrame.Sunken)

        self.vertical_layout_window.addWidget(self.line_5)

        self.tab_widget_solutions = QTabWidget(self.verticalLayoutWidget)
        self.tab_widget_solutions.setObjectName("tab_widget_solutions")
        sizePolicy4 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(
            self.tab_widget_solutions.sizePolicy().hasHeightForWidth()
        )
        self.tab_widget_solutions.setSizePolicy(sizePolicy4)
        self.tab_widget_solutions.setFont(font)
        self.tab_summary = QWidget()
        self.tab_summary.setObjectName("tab_summary")
        self.verticalLayoutWidget_2 = QWidget(self.tab_summary)
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(9, 9, 881, 291))
        self.vertical_layout_summary = QVBoxLayout(self.verticalLayoutWidget_2)
        self.vertical_layout_summary.setObjectName("vertical_layout_summary")
        self.vertical_layout_summary.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout_target_name = QHBoxLayout()
        self.horizontal_layout_target_name.setObjectName(
            "horizontal_layout_target_name"
        )
        self.label_static_detected_target_name = QLabel(self.verticalLayoutWidget_2)
        self.label_static_detected_target_name.setObjectName(
            "label_static_detected_target_name"
        )

        self.horizontal_layout_target_name.addWidget(
            self.label_static_detected_target_name
        )

        self.line_edit_detected_target_name = QLineEdit(self.verticalLayoutWidget_2)
        self.line_edit_detected_target_name.setObjectName(
            "line_edit_detected_target_name"
        )

        self.horizontal_layout_target_name.addWidget(
            self.line_edit_detected_target_name
        )

        self.push_button_change_target_name = QPushButton(self.verticalLayoutWidget_2)
        self.push_button_change_target_name.setObjectName(
            "push_button_change_target_name"
        )

        self.horizontal_layout_target_name.addWidget(
            self.push_button_change_target_name
        )

        self.line_33 = QFrame(self.verticalLayoutWidget_2)
        self.line_33.setObjectName("line_33")
        self.line_33.setFrameShape(QFrame.VLine)
        self.line_33.setFrameShadow(QFrame.Sunken)

        self.horizontal_layout_target_name.addWidget(self.line_33)

        self.push_button_send_target_to_tcs = QPushButton(self.verticalLayoutWidget_2)
        self.push_button_send_target_to_tcs.setObjectName(
            "push_button_send_target_to_tcs"
        )

        self.horizontal_layout_target_name.addWidget(
            self.push_button_send_target_to_tcs
        )

        self.vertical_layout_summary.addLayout(self.horizontal_layout_target_name)

        self.label = QLabel(self.verticalLayoutWidget_2)
        self.label.setObjectName("label")

        self.vertical_layout_summary.addWidget(self.label)

        self.tab_widget_solutions.addTab(self.tab_summary, "")
        self.tab_astrometry = QWidget()
        self.tab_astrometry.setObjectName("tab_astrometry")
        self.verticalLayoutWidget_3 = QWidget(self.tab_astrometry)
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayoutWidget_3.setGeometry(QRect(10, 10, 881, 291))
        self.vertical_layout_astrometry = QVBoxLayout(self.verticalLayoutWidget_3)
        self.vertical_layout_astrometry.setObjectName("vertical_layout_astrometry")
        self.vertical_layout_astrometry.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout_astrometry_solve = QHBoxLayout()
        self.horizontal_layout_astrometry_solve.setObjectName(
            "horizontal_layout_astrometry_solve"
        )
        self.horizontal_layout_astrometry_solve.setSizeConstraint(
            QLayout.SetDefaultConstraint
        )
        self.label_static_astrometry_engine = QLabel(self.verticalLayoutWidget_3)
        self.label_static_astrometry_engine.setObjectName(
            "label_static_astrometry_engine"
        )

        self.horizontal_layout_astrometry_solve.addWidget(
            self.label_static_astrometry_engine
        )

        self.combo_box_astrometry_engine = QComboBox(self.verticalLayoutWidget_3)
        self.combo_box_astrometry_engine.addItem("")
        self.combo_box_astrometry_engine.addItem("")
        self.combo_box_astrometry_engine.setObjectName("combo_box_astrometry_engine")

        self.horizontal_layout_astrometry_solve.addWidget(
            self.combo_box_astrometry_engine
        )

        self.push_button_solve_astrometry = QPushButton(self.verticalLayoutWidget_3)
        self.push_button_solve_astrometry.setObjectName("push_button_solve_astrometry")

        self.horizontal_layout_astrometry_solve.addWidget(
            self.push_button_solve_astrometry
        )

        self.vertical_layout_astrometry.addLayout(
            self.horizontal_layout_astrometry_solve
        )

        self.line_6 = QFrame(self.verticalLayoutWidget_3)
        self.line_6.setObjectName("line_6")
        self.line_6.setFrameShape(QFrame.HLine)
        self.line_6.setFrameShadow(QFrame.Sunken)

        self.vertical_layout_astrometry.addWidget(self.line_6)

        self.grid_layout_astrometry_results = QGridLayout()
        self.grid_layout_astrometry_results.setObjectName(
            "grid_layout_astrometry_results"
        )
        self.label_static_astrometry_results_center_dec = QLabel(
            self.verticalLayoutWidget_3
        )
        self.label_static_astrometry_results_center_dec.setObjectName(
            "label_static_astrometry_results_center_dec"
        )
        self.label_static_astrometry_results_center_dec.setAlignment(Qt.AlignCenter)

        self.grid_layout_astrometry_results.addWidget(
            self.label_static_astrometry_results_center_dec, 1, 3, 1, 1
        )

        self.label_dynamic_astrometry_file_3_target_ra = QLabel(
            self.verticalLayoutWidget_3
        )
        self.label_dynamic_astrometry_file_3_target_ra.setObjectName(
            "label_dynamic_astrometry_file_3_target_ra"
        )
        self.label_dynamic_astrometry_file_3_target_ra.setAlignment(Qt.AlignCenter)

        self.grid_layout_astrometry_results.addWidget(
            self.label_dynamic_astrometry_file_3_target_ra, 5, 5, 1, 1
        )

        self.label_static_astrometry_results_center_ra = QLabel(
            self.verticalLayoutWidget_3
        )
        self.label_static_astrometry_results_center_ra.setObjectName(
            "label_static_astrometry_results_center_ra"
        )
        self.label_static_astrometry_results_center_ra.setAlignment(Qt.AlignCenter)

        self.grid_layout_astrometry_results.addWidget(
            self.label_static_astrometry_results_center_ra, 1, 2, 1, 1
        )

        self.label_dynamic_astrometry_file_4_center_ra = QLabel(
            self.verticalLayoutWidget_3
        )
        self.label_dynamic_astrometry_file_4_center_ra.setObjectName(
            "label_dynamic_astrometry_file_4_center_ra"
        )
        self.label_dynamic_astrometry_file_4_center_ra.setAlignment(Qt.AlignCenter)

        self.grid_layout_astrometry_results.addWidget(
            self.label_dynamic_astrometry_file_4_center_ra, 6, 2, 1, 1
        )

        self.label_static_astrometry_results_center = QLabel(
            self.verticalLayoutWidget_3
        )
        self.label_static_astrometry_results_center.setObjectName(
            "label_static_astrometry_results_center"
        )
        self.label_static_astrometry_results_center.setAlignment(Qt.AlignCenter)

        self.grid_layout_astrometry_results.addWidget(
            self.label_static_astrometry_results_center, 0, 2, 1, 2
        )

        self.label_dynamic_astrometry_file_4_target_ra = QLabel(
            self.verticalLayoutWidget_3
        )
        self.label_dynamic_astrometry_file_4_target_ra.setObjectName(
            "label_dynamic_astrometry_file_4_target_ra"
        )
        self.label_dynamic_astrometry_file_4_target_ra.setAlignment(Qt.AlignCenter)

        self.grid_layout_astrometry_results.addWidget(
            self.label_dynamic_astrometry_file_4_target_ra, 6, 5, 1, 1
        )

        self.label_dynamic_astrometry_file_3_target_dec = QLabel(
            self.verticalLayoutWidget_3
        )
        self.label_dynamic_astrometry_file_3_target_dec.setObjectName(
            "label_dynamic_astrometry_file_3_target_dec"
        )
        self.label_dynamic_astrometry_file_3_target_dec.setAlignment(Qt.AlignCenter)

        self.grid_layout_astrometry_results.addWidget(
            self.label_dynamic_astrometry_file_3_target_dec, 5, 6, 1, 1
        )

        self.label_dynamic_astrometry_file_4_target_dec = QLabel(
            self.verticalLayoutWidget_3
        )
        self.label_dynamic_astrometry_file_4_target_dec.setObjectName(
            "label_dynamic_astrometry_file_4_target_dec"
        )
        self.label_dynamic_astrometry_file_4_target_dec.setAlignment(Qt.AlignCenter)

        self.grid_layout_astrometry_results.addWidget(
            self.label_dynamic_astrometry_file_4_target_dec, 6, 6, 1, 1
        )

        self.label_dynamic_astrometry_file_2_target_ra = QLabel(
            self.verticalLayoutWidget_3
        )
        self.label_dynamic_astrometry_file_2_target_ra.setObjectName(
            "label_dynamic_astrometry_file_2_target_ra"
        )
        self.label_dynamic_astrometry_file_2_target_ra.setAlignment(Qt.AlignCenter)

        self.grid_layout_astrometry_results.addWidget(
            self.label_dynamic_astrometry_file_2_target_ra, 4, 5, 1, 1
        )

        self.label_dynamic_astrometry_file_3_center_dec = QLabel(
            self.verticalLayoutWidget_3
        )
        self.label_dynamic_astrometry_file_3_center_dec.setObjectName(
            "label_dynamic_astrometry_file_3_center_dec"
        )
        self.label_dynamic_astrometry_file_3_center_dec.setAlignment(Qt.AlignCenter)

        self.grid_layout_astrometry_results.addWidget(
            self.label_dynamic_astrometry_file_3_center_dec, 5, 3, 1, 1
        )

        self.label_dynamic_astrometry_file_4_center_dec = QLabel(
            self.verticalLayoutWidget_3
        )
        self.label_dynamic_astrometry_file_4_center_dec.setObjectName(
            "label_dynamic_astrometry_file_4_center_dec"
        )
        self.label_dynamic_astrometry_file_4_center_dec.setAlignment(Qt.AlignCenter)

        self.grid_layout_astrometry_results.addWidget(
            self.label_dynamic_astrometry_file_4_center_dec, 6, 3, 1, 1
        )

        self.label_dynamic_astrometry_file_2_center_dec = QLabel(
            self.verticalLayoutWidget_3
        )
        self.label_dynamic_astrometry_file_2_center_dec.setObjectName(
            "label_dynamic_astrometry_file_2_center_dec"
        )
        self.label_dynamic_astrometry_file_2_center_dec.setAlignment(Qt.AlignCenter)

        self.grid_layout_astrometry_results.addWidget(
            self.label_dynamic_astrometry_file_2_center_dec, 4, 3, 1, 1
        )

        self.label_static_astrometry_results_target_dec = QLabel(
            self.verticalLayoutWidget_3
        )
        self.label_static_astrometry_results_target_dec.setObjectName(
            "label_static_astrometry_results_target_dec"
        )
        self.label_static_astrometry_results_target_dec.setAlignment(Qt.AlignCenter)

        self.grid_layout_astrometry_results.addWidget(
            self.label_static_astrometry_results_target_dec, 1, 6, 1, 1
        )

        self.label_static_astrometry_results_target_ra = QLabel(
            self.verticalLayoutWidget_3
        )
        self.label_static_astrometry_results_target_ra.setObjectName(
            "label_static_astrometry_results_target_ra"
        )
        self.label_static_astrometry_results_target_ra.setAlignment(Qt.AlignCenter)

        self.grid_layout_astrometry_results.addWidget(
            self.label_static_astrometry_results_target_ra, 1, 5, 1, 1
        )

        self.label_dynamic_astrometry_file_2_target_dec = QLabel(
            self.verticalLayoutWidget_3
        )
        self.label_dynamic_astrometry_file_2_target_dec.setObjectName(
            "label_dynamic_astrometry_file_2_target_dec"
        )
        self.label_dynamic_astrometry_file_2_target_dec.setAlignment(Qt.AlignCenter)

        self.grid_layout_astrometry_results.addWidget(
            self.label_dynamic_astrometry_file_2_target_dec, 4, 6, 1, 1
        )

        self.label_dynamic_astrometry_file_3_center_ra = QLabel(
            self.verticalLayoutWidget_3
        )
        self.label_dynamic_astrometry_file_3_center_ra.setObjectName(
            "label_dynamic_astrometry_file_3_center_ra"
        )
        self.label_dynamic_astrometry_file_3_center_ra.setAlignment(Qt.AlignCenter)

        self.grid_layout_astrometry_results.addWidget(
            self.label_dynamic_astrometry_file_3_center_ra, 5, 2, 1, 1
        )

        self.label_dynamic_astrometry_file_2_center_ra = QLabel(
            self.verticalLayoutWidget_3
        )
        self.label_dynamic_astrometry_file_2_center_ra.setObjectName(
            "label_dynamic_astrometry_file_2_center_ra"
        )
        self.label_dynamic_astrometry_file_2_center_ra.setAlignment(Qt.AlignCenter)

        self.grid_layout_astrometry_results.addWidget(
            self.label_dynamic_astrometry_file_2_center_ra, 4, 2, 1, 1
        )

        self.label_static_astrometry_results_target = QLabel(
            self.verticalLayoutWidget_3
        )
        self.label_static_astrometry_results_target.setObjectName(
            "label_static_astrometry_results_target"
        )
        self.label_static_astrometry_results_target.setAlignment(Qt.AlignCenter)

        self.grid_layout_astrometry_results.addWidget(
            self.label_static_astrometry_results_target, 0, 5, 1, 2
        )

        self.label_dynamic_astrometry_file_1_center_dec = QLabel(
            self.verticalLayoutWidget_3
        )
        self.label_dynamic_astrometry_file_1_center_dec.setObjectName(
            "label_dynamic_astrometry_file_1_center_dec"
        )
        self.label_dynamic_astrometry_file_1_center_dec.setAlignment(Qt.AlignCenter)

        self.grid_layout_astrometry_results.addWidget(
            self.label_dynamic_astrometry_file_1_center_dec, 3, 3, 1, 1
        )

        self.label_static_astrometry_results_file_1 = QLabel(
            self.verticalLayoutWidget_3
        )
        self.label_static_astrometry_results_file_1.setObjectName(
            "label_static_astrometry_results_file_1"
        )
        self.label_static_astrometry_results_file_1.setMinimumSize(QSize(50, 0))
        self.label_static_astrometry_results_file_1.setMaximumSize(QSize(50, 16777215))
        self.label_static_astrometry_results_file_1.setAlignment(Qt.AlignCenter)

        self.grid_layout_astrometry_results.addWidget(
            self.label_static_astrometry_results_file_1, 3, 0, 1, 1
        )

        self.label_dynamic_astrometry_file_1_target_dec = QLabel(
            self.verticalLayoutWidget_3
        )
        self.label_dynamic_astrometry_file_1_target_dec.setObjectName(
            "label_dynamic_astrometry_file_1_target_dec"
        )
        self.label_dynamic_astrometry_file_1_target_dec.setAlignment(Qt.AlignCenter)

        self.grid_layout_astrometry_results.addWidget(
            self.label_dynamic_astrometry_file_1_target_dec, 3, 6, 1, 1
        )

        self.label_dynamic_astrometry_file_1_target_ra = QLabel(
            self.verticalLayoutWidget_3
        )
        self.label_dynamic_astrometry_file_1_target_ra.setObjectName(
            "label_dynamic_astrometry_file_1_target_ra"
        )
        self.label_dynamic_astrometry_file_1_target_ra.setAlignment(Qt.AlignCenter)

        self.grid_layout_astrometry_results.addWidget(
            self.label_dynamic_astrometry_file_1_target_ra, 3, 5, 1, 1
        )

        self.label_static_astrometry_results_file = QLabel(self.verticalLayoutWidget_3)
        self.label_static_astrometry_results_file.setObjectName(
            "label_static_astrometry_results_file"
        )
        self.label_static_astrometry_results_file.setMinimumSize(QSize(50, 0))
        self.label_static_astrometry_results_file.setMaximumSize(QSize(50, 16777215))
        self.label_static_astrometry_results_file.setAlignment(Qt.AlignCenter)

        self.grid_layout_astrometry_results.addWidget(
            self.label_static_astrometry_results_file, 0, 0, 1, 1
        )

        self.label_dynamic_astrometry_file_1_center_ra = QLabel(
            self.verticalLayoutWidget_3
        )
        self.label_dynamic_astrometry_file_1_center_ra.setObjectName(
            "label_dynamic_astrometry_file_1_center_ra"
        )
        self.label_dynamic_astrometry_file_1_center_ra.setAlignment(Qt.AlignCenter)

        self.grid_layout_astrometry_results.addWidget(
            self.label_dynamic_astrometry_file_1_center_ra, 3, 2, 1, 1
        )

        self.label_static_astrometry_results_file_3 = QLabel(
            self.verticalLayoutWidget_3
        )
        self.label_static_astrometry_results_file_3.setObjectName(
            "label_static_astrometry_results_file_3"
        )
        self.label_static_astrometry_results_file_3.setMinimumSize(QSize(50, 0))
        self.label_static_astrometry_results_file_3.setMaximumSize(QSize(50, 16777215))
        self.label_static_astrometry_results_file_3.setAlignment(Qt.AlignCenter)

        self.grid_layout_astrometry_results.addWidget(
            self.label_static_astrometry_results_file_3, 5, 0, 1, 1
        )

        self.label_static_astrometry_results_file_2 = QLabel(
            self.verticalLayoutWidget_3
        )
        self.label_static_astrometry_results_file_2.setObjectName(
            "label_static_astrometry_results_file_2"
        )
        self.label_static_astrometry_results_file_2.setMinimumSize(QSize(50, 0))
        self.label_static_astrometry_results_file_2.setMaximumSize(QSize(50, 16777215))
        self.label_static_astrometry_results_file_2.setAlignment(Qt.AlignCenter)

        self.grid_layout_astrometry_results.addWidget(
            self.label_static_astrometry_results_file_2, 4, 0, 1, 1
        )

        self.label_static_astrometry_results_file_4 = QLabel(
            self.verticalLayoutWidget_3
        )
        self.label_static_astrometry_results_file_4.setObjectName(
            "label_static_astrometry_results_file_4"
        )
        self.label_static_astrometry_results_file_4.setMinimumSize(QSize(50, 0))
        self.label_static_astrometry_results_file_4.setMaximumSize(QSize(50, 16777215))
        self.label_static_astrometry_results_file_4.setAlignment(Qt.AlignCenter)

        self.grid_layout_astrometry_results.addWidget(
            self.label_static_astrometry_results_file_4, 6, 0, 1, 1
        )

        self.line_23 = QFrame(self.verticalLayoutWidget_3)
        self.line_23.setObjectName("line_23")
        self.line_23.setFrameShape(QFrame.HLine)
        self.line_23.setFrameShadow(QFrame.Sunken)

        self.grid_layout_astrometry_results.addWidget(self.line_23, 2, 2, 1, 2)

        self.line_26 = QFrame(self.verticalLayoutWidget_3)
        self.line_26.setObjectName("line_26")
        self.line_26.setFrameShape(QFrame.HLine)
        self.line_26.setFrameShadow(QFrame.Sunken)

        self.grid_layout_astrometry_results.addWidget(self.line_26, 2, 5, 1, 2)

        self.line_27 = QFrame(self.verticalLayoutWidget_3)
        self.line_27.setObjectName("line_27")
        self.line_27.setFrameShape(QFrame.HLine)
        self.line_27.setFrameShadow(QFrame.Sunken)

        self.grid_layout_astrometry_results.addWidget(self.line_27, 2, 0, 1, 1)

        self.line_7 = QFrame(self.verticalLayoutWidget_3)
        self.line_7.setObjectName("line_7")
        self.line_7.setFrameShape(QFrame.VLine)
        self.line_7.setFrameShadow(QFrame.Sunken)

        self.grid_layout_astrometry_results.addWidget(self.line_7, 0, 1, 7, 1)

        self.line_8 = QFrame(self.verticalLayoutWidget_3)
        self.line_8.setObjectName("line_8")
        self.line_8.setFrameShape(QFrame.VLine)
        self.line_8.setFrameShadow(QFrame.Sunken)

        self.grid_layout_astrometry_results.addWidget(self.line_8, 0, 4, 7, 1)

        self.vertical_layout_astrometry.addLayout(self.grid_layout_astrometry_results)

        self.line_9 = QFrame(self.verticalLayoutWidget_3)
        self.line_9.setObjectName("line_9")
        self.line_9.setFrameShape(QFrame.HLine)
        self.line_9.setFrameShadow(QFrame.Sunken)

        self.vertical_layout_astrometry.addWidget(self.line_9)

        self.grid_layout_astrometry_custom = QGridLayout()
        self.grid_layout_astrometry_custom.setObjectName(
            "grid_layout_astrometry_custom"
        )
        self.line_edit_astrometry_custom_pixel_y = QLineEdit(
            self.verticalLayoutWidget_3
        )
        self.line_edit_astrometry_custom_pixel_y.setObjectName(
            "line_edit_astrometry_custom_pixel_y"
        )

        self.grid_layout_astrometry_custom.addWidget(
            self.line_edit_astrometry_custom_pixel_y, 1, 2, 1, 1
        )

        self.line_edit_astrometry_custom_dec = QLineEdit(self.verticalLayoutWidget_3)
        self.line_edit_astrometry_custom_dec.setObjectName(
            "line_edit_astrometry_custom_dec"
        )

        self.grid_layout_astrometry_custom.addWidget(
            self.line_edit_astrometry_custom_dec, 1, 4, 1, 1
        )

        self.line_edit_astrometry_custom_ra = QLineEdit(self.verticalLayoutWidget_3)
        self.line_edit_astrometry_custom_ra.setObjectName(
            "line_edit_astrometry_custom_ra"
        )

        self.grid_layout_astrometry_custom.addWidget(
            self.line_edit_astrometry_custom_ra, 1, 3, 1, 1
        )

        self.line_edit_astrometry_custom_pixel_x = QLineEdit(
            self.verticalLayoutWidget_3
        )
        self.line_edit_astrometry_custom_pixel_x.setObjectName(
            "line_edit_astrometry_custom_pixel_x"
        )

        self.grid_layout_astrometry_custom.addWidget(
            self.line_edit_astrometry_custom_pixel_x, 1, 1, 1, 1
        )

        self.label_static_astrometry_custom_pixel_x = QLabel(
            self.verticalLayoutWidget_3
        )
        self.label_static_astrometry_custom_pixel_x.setObjectName(
            "label_static_astrometry_custom_pixel_x"
        )
        self.label_static_astrometry_custom_pixel_x.setAlignment(Qt.AlignCenter)

        self.grid_layout_astrometry_custom.addWidget(
            self.label_static_astrometry_custom_pixel_x, 0, 1, 1, 1
        )

        self.label_static_astrometry_coordinate_solve = QLabel(
            self.verticalLayoutWidget_3
        )
        self.label_static_astrometry_coordinate_solve.setObjectName(
            "label_static_astrometry_coordinate_solve"
        )

        self.grid_layout_astrometry_custom.addWidget(
            self.label_static_astrometry_coordinate_solve, 0, 0, 1, 1
        )

        self.label_static_astrometry_custom_pixel_y = QLabel(
            self.verticalLayoutWidget_3
        )
        self.label_static_astrometry_custom_pixel_y.setObjectName(
            "label_static_astrometry_custom_pixel_y"
        )
        self.label_static_astrometry_custom_pixel_y.setAlignment(Qt.AlignCenter)

        self.grid_layout_astrometry_custom.addWidget(
            self.label_static_astrometry_custom_pixel_y, 0, 2, 1, 1
        )

        self.label_static_astrometry_custom_ra = QLabel(self.verticalLayoutWidget_3)
        self.label_static_astrometry_custom_ra.setObjectName(
            "label_static_astrometry_custom_ra"
        )
        self.label_static_astrometry_custom_ra.setAlignment(Qt.AlignCenter)

        self.grid_layout_astrometry_custom.addWidget(
            self.label_static_astrometry_custom_ra, 0, 3, 1, 1
        )

        self.label_static_astrometry_custom_dec = QLabel(self.verticalLayoutWidget_3)
        self.label_static_astrometry_custom_dec.setObjectName(
            "label_static_astrometry_custom_dec"
        )
        self.label_static_astrometry_custom_dec.setAlignment(Qt.AlignCenter)

        self.grid_layout_astrometry_custom.addWidget(
            self.label_static_astrometry_custom_dec, 0, 4, 1, 1
        )

        self.push_button_astrometry_custom_solve = QPushButton(
            self.verticalLayoutWidget_3
        )
        self.push_button_astrometry_custom_solve.setObjectName(
            "push_button_astrometry_custom_solve"
        )

        self.grid_layout_astrometry_custom.addWidget(
            self.push_button_astrometry_custom_solve, 1, 0, 1, 1
        )

        self.vertical_layout_astrometry.addLayout(self.grid_layout_astrometry_custom)

        self.tab_widget_solutions.addTab(self.tab_astrometry, "")
        self.tab_photometry = QWidget()
        self.tab_photometry.setObjectName("tab_photometry")
        self.verticalLayoutWidget_4 = QWidget(self.tab_photometry)
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayoutWidget_4.setGeometry(QRect(10, 10, 881, 291))
        self.vertical_layout_photometry = QVBoxLayout(self.verticalLayoutWidget_4)
        self.vertical_layout_photometry.setObjectName("vertical_layout_photometry")
        self.vertical_layout_photometry.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout_photometry_solve = QHBoxLayout()
        self.horizontal_layout_photometry_solve.setObjectName(
            "horizontal_layout_photometry_solve"
        )
        self.label_static_photometry_engine = QLabel(self.verticalLayoutWidget_4)
        self.label_static_photometry_engine.setObjectName(
            "label_static_photometry_engine"
        )

        self.horizontal_layout_photometry_solve.addWidget(
            self.label_static_photometry_engine
        )

        self.combo_box_photometry_engine = QComboBox(self.verticalLayoutWidget_4)
        self.combo_box_photometry_engine.addItem("")
        self.combo_box_photometry_engine.setObjectName("combo_box_photometry_engine")

        self.horizontal_layout_photometry_solve.addWidget(
            self.combo_box_photometry_engine
        )

        self.push_button_solve_photometry = QPushButton(self.verticalLayoutWidget_4)
        self.push_button_solve_photometry.setObjectName("push_button_solve_photometry")

        self.horizontal_layout_photometry_solve.addWidget(
            self.push_button_solve_photometry
        )

        self.vertical_layout_photometry.addLayout(
            self.horizontal_layout_photometry_solve
        )

        self.line_10 = QFrame(self.verticalLayoutWidget_4)
        self.line_10.setObjectName("line_10")
        self.line_10.setFrameShape(QFrame.HLine)
        self.line_10.setFrameShadow(QFrame.Sunken)

        self.vertical_layout_photometry.addWidget(self.line_10)

        self.grid_layout_photometry_results = QGridLayout()
        self.grid_layout_photometry_results.setObjectName(
            "grid_layout_photometry_results"
        )
        self.label_static_photometry_results_file_1 = QLabel(
            self.verticalLayoutWidget_4
        )
        self.label_static_photometry_results_file_1.setObjectName(
            "label_static_photometry_results_file_1"
        )
        self.label_static_photometry_results_file_1.setMinimumSize(QSize(50, 0))
        self.label_static_photometry_results_file_1.setMaximumSize(QSize(50, 16777215))
        self.label_static_photometry_results_file_1.setAlignment(Qt.AlignCenter)

        self.grid_layout_photometry_results.addWidget(
            self.label_static_photometry_results_file_1, 2, 0, 1, 1
        )

        self.label_static_photometry_results_file = QLabel(self.verticalLayoutWidget_4)
        self.label_static_photometry_results_file.setObjectName(
            "label_static_photometry_results_file"
        )
        self.label_static_photometry_results_file.setMinimumSize(QSize(50, 0))
        self.label_static_photometry_results_file.setMaximumSize(QSize(50, 16777215))
        self.label_static_photometry_results_file.setAlignment(Qt.AlignCenter)

        self.grid_layout_photometry_results.addWidget(
            self.label_static_photometry_results_file, 0, 0, 1, 1
        )

        self.label_static_photometry_results_file_2 = QLabel(
            self.verticalLayoutWidget_4
        )
        self.label_static_photometry_results_file_2.setObjectName(
            "label_static_photometry_results_file_2"
        )
        self.label_static_photometry_results_file_2.setMinimumSize(QSize(50, 0))
        self.label_static_photometry_results_file_2.setMaximumSize(QSize(50, 16777215))
        self.label_static_photometry_results_file_2.setAlignment(Qt.AlignCenter)

        self.grid_layout_photometry_results.addWidget(
            self.label_static_photometry_results_file_2, 3, 0, 1, 1
        )

        self.label_static_photometry_results_file_4 = QLabel(
            self.verticalLayoutWidget_4
        )
        self.label_static_photometry_results_file_4.setObjectName(
            "label_static_photometry_results_file_4"
        )
        self.label_static_photometry_results_file_4.setMinimumSize(QSize(50, 0))
        self.label_static_photometry_results_file_4.setMaximumSize(QSize(50, 16777215))
        self.label_static_photometry_results_file_4.setAlignment(Qt.AlignCenter)

        self.grid_layout_photometry_results.addWidget(
            self.label_static_photometry_results_file_4, 5, 0, 1, 1
        )

        self.label_static_photometry_results_file_3 = QLabel(
            self.verticalLayoutWidget_4
        )
        self.label_static_photometry_results_file_3.setObjectName(
            "label_static_photometry_results_file_3"
        )
        self.label_static_photometry_results_file_3.setMinimumSize(QSize(50, 0))
        self.label_static_photometry_results_file_3.setMaximumSize(QSize(50, 16777215))
        self.label_static_photometry_results_file_3.setAlignment(Qt.AlignCenter)

        self.grid_layout_photometry_results.addWidget(
            self.label_static_photometry_results_file_3, 4, 0, 1, 1
        )

        self.label_static_photometry_results_zero_point = QLabel(
            self.verticalLayoutWidget_4
        )
        self.label_static_photometry_results_zero_point.setObjectName(
            "label_static_photometry_results_zero_point"
        )
        self.label_static_photometry_results_zero_point.setAlignment(Qt.AlignCenter)

        self.grid_layout_photometry_results.addWidget(
            self.label_static_photometry_results_zero_point, 0, 3, 1, 1
        )

        self.label_static_photometry_results_file_2_filter_name = QLabel(
            self.verticalLayoutWidget_4
        )
        self.label_static_photometry_results_file_2_filter_name.setObjectName(
            "label_static_photometry_results_file_2_filter_name"
        )
        self.label_static_photometry_results_file_2_filter_name.setAlignment(
            Qt.AlignCenter
        )

        self.grid_layout_photometry_results.addWidget(
            self.label_static_photometry_results_file_2_filter_name, 3, 2, 1, 1
        )

        self.label_static_photometry_results_aperture_magnitude = QLabel(
            self.verticalLayoutWidget_4
        )
        self.label_static_photometry_results_aperture_magnitude.setObjectName(
            "label_static_photometry_results_aperture_magnitude"
        )
        self.label_static_photometry_results_aperture_magnitude.setAlignment(
            Qt.AlignCenter
        )

        self.grid_layout_photometry_results.addWidget(
            self.label_static_photometry_results_aperture_magnitude, 0, 4, 1, 1
        )

        self.label_static_photometry_results_filter_name = QLabel(
            self.verticalLayoutWidget_4
        )
        self.label_static_photometry_results_filter_name.setObjectName(
            "label_static_photometry_results_filter_name"
        )
        self.label_static_photometry_results_filter_name.setAlignment(Qt.AlignCenter)

        self.grid_layout_photometry_results.addWidget(
            self.label_static_photometry_results_filter_name, 0, 2, 1, 1
        )

        self.label_static_photometry_results_file_4_filter_name = QLabel(
            self.verticalLayoutWidget_4
        )
        self.label_static_photometry_results_file_4_filter_name.setObjectName(
            "label_static_photometry_results_file_4_filter_name"
        )
        self.label_static_photometry_results_file_4_filter_name.setAlignment(
            Qt.AlignCenter
        )

        self.grid_layout_photometry_results.addWidget(
            self.label_static_photometry_results_file_4_filter_name, 5, 2, 1, 1
        )

        self.label_static_photometry_results_file_1_filter_name = QLabel(
            self.verticalLayoutWidget_4
        )
        self.label_static_photometry_results_file_1_filter_name.setObjectName(
            "label_static_photometry_results_file_1_filter_name"
        )
        self.label_static_photometry_results_file_1_filter_name.setAlignment(
            Qt.AlignCenter
        )

        self.grid_layout_photometry_results.addWidget(
            self.label_static_photometry_results_file_1_filter_name, 2, 2, 1, 1
        )

        self.label_static_photometry_results_file_3_filter_name = QLabel(
            self.verticalLayoutWidget_4
        )
        self.label_static_photometry_results_file_3_filter_name.setObjectName(
            "label_static_photometry_results_file_3_filter_name"
        )
        self.label_static_photometry_results_file_3_filter_name.setAlignment(
            Qt.AlignCenter
        )

        self.grid_layout_photometry_results.addWidget(
            self.label_static_photometry_results_file_3_filter_name, 4, 2, 1, 1
        )

        self.label_static_photometry_results_file_1_zero_point = QLabel(
            self.verticalLayoutWidget_4
        )
        self.label_static_photometry_results_file_1_zero_point.setObjectName(
            "label_static_photometry_results_file_1_zero_point"
        )
        self.label_static_photometry_results_file_1_zero_point.setAlignment(
            Qt.AlignCenter
        )

        self.grid_layout_photometry_results.addWidget(
            self.label_static_photometry_results_file_1_zero_point, 2, 3, 1, 1
        )

        self.label_static_photometry_results_file_4_zero_point = QLabel(
            self.verticalLayoutWidget_4
        )
        self.label_static_photometry_results_file_4_zero_point.setObjectName(
            "label_static_photometry_results_file_4_zero_point"
        )
        self.label_static_photometry_results_file_4_zero_point.setAlignment(
            Qt.AlignCenter
        )

        self.grid_layout_photometry_results.addWidget(
            self.label_static_photometry_results_file_4_zero_point, 5, 3, 1, 1
        )

        self.label_static_photometry_results_file_2_zero_point = QLabel(
            self.verticalLayoutWidget_4
        )
        self.label_static_photometry_results_file_2_zero_point.setObjectName(
            "label_static_photometry_results_file_2_zero_point"
        )
        self.label_static_photometry_results_file_2_zero_point.setAlignment(
            Qt.AlignCenter
        )

        self.grid_layout_photometry_results.addWidget(
            self.label_static_photometry_results_file_2_zero_point, 3, 3, 1, 1
        )

        self.label_static_photometry_results_file_3_zero_point = QLabel(
            self.verticalLayoutWidget_4
        )
        self.label_static_photometry_results_file_3_zero_point.setObjectName(
            "label_static_photometry_results_file_3_zero_point"
        )
        self.label_static_photometry_results_file_3_zero_point.setAlignment(
            Qt.AlignCenter
        )

        self.grid_layout_photometry_results.addWidget(
            self.label_static_photometry_results_file_3_zero_point, 4, 3, 1, 1
        )

        self.label_static_photometry_results_file_1_magnitude = QLabel(
            self.verticalLayoutWidget_4
        )
        self.label_static_photometry_results_file_1_magnitude.setObjectName(
            "label_static_photometry_results_file_1_magnitude"
        )
        self.label_static_photometry_results_file_1_magnitude.setAlignment(
            Qt.AlignCenter
        )

        self.grid_layout_photometry_results.addWidget(
            self.label_static_photometry_results_file_1_magnitude, 2, 4, 1, 1
        )

        self.label_static_photometry_results_file_2_magnitude = QLabel(
            self.verticalLayoutWidget_4
        )
        self.label_static_photometry_results_file_2_magnitude.setObjectName(
            "label_static_photometry_results_file_2_magnitude"
        )
        self.label_static_photometry_results_file_2_magnitude.setAlignment(
            Qt.AlignCenter
        )

        self.grid_layout_photometry_results.addWidget(
            self.label_static_photometry_results_file_2_magnitude, 3, 4, 1, 1
        )

        self.label_static_photometry_results_file_3_magnitude = QLabel(
            self.verticalLayoutWidget_4
        )
        self.label_static_photometry_results_file_3_magnitude.setObjectName(
            "label_static_photometry_results_file_3_magnitude"
        )
        self.label_static_photometry_results_file_3_magnitude.setAlignment(
            Qt.AlignCenter
        )

        self.grid_layout_photometry_results.addWidget(
            self.label_static_photometry_results_file_3_magnitude, 4, 4, 1, 1
        )

        self.label_static_photometry_results_file_4_magnitude = QLabel(
            self.verticalLayoutWidget_4
        )
        self.label_static_photometry_results_file_4_magnitude.setObjectName(
            "label_static_photometry_results_file_4_magnitude"
        )
        self.label_static_photometry_results_file_4_magnitude.setAlignment(
            Qt.AlignCenter
        )

        self.grid_layout_photometry_results.addWidget(
            self.label_static_photometry_results_file_4_magnitude, 5, 4, 1, 1
        )

        self.line_11 = QFrame(self.verticalLayoutWidget_4)
        self.line_11.setObjectName("line_11")
        self.line_11.setFrameShape(QFrame.VLine)
        self.line_11.setFrameShadow(QFrame.Sunken)

        self.grid_layout_photometry_results.addWidget(self.line_11, 0, 1, 6, 1)

        self.line_28 = QFrame(self.verticalLayoutWidget_4)
        self.line_28.setObjectName("line_28")
        self.line_28.setFrameShape(QFrame.HLine)
        self.line_28.setFrameShadow(QFrame.Sunken)

        self.grid_layout_photometry_results.addWidget(self.line_28, 1, 2, 1, 3)

        self.line_29 = QFrame(self.verticalLayoutWidget_4)
        self.line_29.setObjectName("line_29")
        self.line_29.setFrameShape(QFrame.HLine)
        self.line_29.setFrameShadow(QFrame.Sunken)

        self.grid_layout_photometry_results.addWidget(self.line_29, 1, 0, 1, 1)

        self.vertical_layout_photometry.addLayout(self.grid_layout_photometry_results)

        self.tab_widget_solutions.addTab(self.tab_photometry, "")
        self.tab_orbit = QWidget()
        self.tab_orbit.setObjectName("tab_orbit")
        self.verticalLayoutWidget_5 = QWidget(self.tab_orbit)
        self.verticalLayoutWidget_5.setObjectName("verticalLayoutWidget_5")
        self.verticalLayoutWidget_5.setGeometry(QRect(10, 10, 881, 291))
        self.vertical_layout_orbit = QVBoxLayout(self.verticalLayoutWidget_5)
        self.vertical_layout_orbit.setObjectName("vertical_layout_orbit")
        self.vertical_layout_orbit.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout_orbit_solve = QHBoxLayout()
        self.horizontal_layout_orbit_solve.setObjectName(
            "horizontal_layout_orbit_solve"
        )
        self.label_static_orbit_engine = QLabel(self.verticalLayoutWidget_5)
        self.label_static_orbit_engine.setObjectName("label_static_orbit_engine")

        self.horizontal_layout_orbit_solve.addWidget(self.label_static_orbit_engine)

        self.combo_box_orbit_engine = QComboBox(self.verticalLayoutWidget_5)
        self.combo_box_orbit_engine.addItem("")
        self.combo_box_orbit_engine.addItem("")
        self.combo_box_orbit_engine.setObjectName("combo_box_orbit_engine")

        self.horizontal_layout_orbit_solve.addWidget(self.combo_box_orbit_engine)

        self.push_button_solve_orbit = QPushButton(self.verticalLayoutWidget_5)
        self.push_button_solve_orbit.setObjectName("push_button_solve_orbit")

        self.horizontal_layout_orbit_solve.addWidget(self.push_button_solve_orbit)

        self.vertical_layout_orbit.addLayout(self.horizontal_layout_orbit_solve)

        self.line_12 = QFrame(self.verticalLayoutWidget_5)
        self.line_12.setObjectName("line_12")
        self.line_12.setFrameShape(QFrame.HLine)
        self.line_12.setFrameShadow(QFrame.Sunken)

        self.vertical_layout_orbit.addWidget(self.line_12)

        self.grid_layout_orbit_results = QGridLayout()
        self.grid_layout_orbit_results.setObjectName("grid_layout_orbit_results")
        self.line_edit_orbit_results_ascending_node_error = QLineEdit(
            self.verticalLayoutWidget_5
        )
        self.line_edit_orbit_results_ascending_node_error.setObjectName(
            "line_edit_orbit_results_ascending_node_error"
        )

        self.grid_layout_orbit_results.addWidget(
            self.line_edit_orbit_results_ascending_node_error, 3, 6, 1, 1
        )

        self.line_edit_orbit_results_ascending_node_value = QLineEdit(
            self.verticalLayoutWidget_5
        )
        self.line_edit_orbit_results_ascending_node_value.setObjectName(
            "line_edit_orbit_results_ascending_node_value"
        )

        self.grid_layout_orbit_results.addWidget(
            self.line_edit_orbit_results_ascending_node_value, 3, 5, 1, 1
        )

        self.line_edit_orbit_results_mean_anomaly_value = QLineEdit(
            self.verticalLayoutWidget_5
        )
        self.line_edit_orbit_results_mean_anomaly_value.setObjectName(
            "line_edit_orbit_results_mean_anomaly_value"
        )

        self.grid_layout_orbit_results.addWidget(
            self.line_edit_orbit_results_mean_anomaly_value, 4, 5, 1, 1
        )

        self.line_edit_orbit_results_mean_anomaly_error = QLineEdit(
            self.verticalLayoutWidget_5
        )
        self.line_edit_orbit_results_mean_anomaly_error.setObjectName(
            "line_edit_orbit_results_mean_anomaly_error"
        )

        self.grid_layout_orbit_results.addWidget(
            self.line_edit_orbit_results_mean_anomaly_error, 4, 6, 1, 1
        )

        self.line_edit_orbit_results_epoch_value = QLineEdit(
            self.verticalLayoutWidget_5
        )
        self.line_edit_orbit_results_epoch_value.setObjectName(
            "line_edit_orbit_results_epoch_value"
        )

        self.grid_layout_orbit_results.addWidget(
            self.line_edit_orbit_results_epoch_value, 0, 5, 1, 2
        )

        self.label_static_orbit_results_value = QLabel(self.verticalLayoutWidget_5)
        self.label_static_orbit_results_value.setObjectName(
            "label_static_orbit_results_value"
        )
        self.label_static_orbit_results_value.setAlignment(
            Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter
        )

        self.grid_layout_orbit_results.addWidget(
            self.label_static_orbit_results_value, 0, 1, 1, 1
        )

        self.label_static_orbit_results_error = QLabel(self.verticalLayoutWidget_5)
        self.label_static_orbit_results_error.setObjectName(
            "label_static_orbit_results_error"
        )

        self.grid_layout_orbit_results.addWidget(
            self.label_static_orbit_results_error, 0, 2, 1, 1
        )

        self.label_static_orbit_results_semimajor_axis = QLabel(
            self.verticalLayoutWidget_5
        )
        self.label_static_orbit_results_semimajor_axis.setObjectName(
            "label_static_orbit_results_semimajor_axis"
        )

        self.grid_layout_orbit_results.addWidget(
            self.label_static_orbit_results_semimajor_axis, 2, 0, 1, 1
        )

        self.label_static_orbit_results_eccentricity = QLabel(
            self.verticalLayoutWidget_5
        )
        self.label_static_orbit_results_eccentricity.setObjectName(
            "label_static_orbit_results_eccentricity"
        )

        self.grid_layout_orbit_results.addWidget(
            self.label_static_orbit_results_eccentricity, 2, 4, 1, 1
        )

        self.label_static_orbit_results_mean_anomaly = QLabel(
            self.verticalLayoutWidget_5
        )
        self.label_static_orbit_results_mean_anomaly.setObjectName(
            "label_static_orbit_results_mean_anomaly"
        )

        self.grid_layout_orbit_results.addWidget(
            self.label_static_orbit_results_mean_anomaly, 4, 4, 1, 1
        )

        self.label_static_orbit_results_inclination = QLabel(
            self.verticalLayoutWidget_5
        )
        self.label_static_orbit_results_inclination.setObjectName(
            "label_static_orbit_results_inclination"
        )

        self.grid_layout_orbit_results.addWidget(
            self.label_static_orbit_results_inclination, 3, 0, 1, 1
        )

        self.label_static_orbit_results_perihelion = QLabel(self.verticalLayoutWidget_5)
        self.label_static_orbit_results_perihelion.setObjectName(
            "label_static_orbit_results_perihelion"
        )

        self.grid_layout_orbit_results.addWidget(
            self.label_static_orbit_results_perihelion, 4, 0, 1, 1
        )

        self.line_edit_orbit_results_semimajor_axis_value = QLineEdit(
            self.verticalLayoutWidget_5
        )
        self.line_edit_orbit_results_semimajor_axis_value.setObjectName(
            "line_edit_orbit_results_semimajor_axis_value"
        )

        self.grid_layout_orbit_results.addWidget(
            self.line_edit_orbit_results_semimajor_axis_value, 2, 1, 1, 1
        )

        self.line_edit_orbit_results_perihelion_value = QLineEdit(
            self.verticalLayoutWidget_5
        )
        self.line_edit_orbit_results_perihelion_value.setObjectName(
            "line_edit_orbit_results_perihelion_value"
        )

        self.grid_layout_orbit_results.addWidget(
            self.line_edit_orbit_results_perihelion_value, 4, 1, 1, 1
        )

        self.label_static_orbit_results_ascending_node = QLabel(
            self.verticalLayoutWidget_5
        )
        self.label_static_orbit_results_ascending_node.setObjectName(
            "label_static_orbit_results_ascending_node"
        )

        self.grid_layout_orbit_results.addWidget(
            self.label_static_orbit_results_ascending_node, 3, 4, 1, 1
        )

        self.label_static_orbit_results_epoch = QLabel(self.verticalLayoutWidget_5)
        self.label_static_orbit_results_epoch.setObjectName(
            "label_static_orbit_results_epoch"
        )

        self.grid_layout_orbit_results.addWidget(
            self.label_static_orbit_results_epoch, 0, 4, 1, 1
        )

        self.line_edit_orbit_results_inclination_value = QLineEdit(
            self.verticalLayoutWidget_5
        )
        self.line_edit_orbit_results_inclination_value.setObjectName(
            "line_edit_orbit_results_inclination_value"
        )

        self.grid_layout_orbit_results.addWidget(
            self.line_edit_orbit_results_inclination_value, 3, 1, 1, 1
        )

        self.line_edit_orbit_results_eccentricity_error = QLineEdit(
            self.verticalLayoutWidget_5
        )
        self.line_edit_orbit_results_eccentricity_error.setObjectName(
            "line_edit_orbit_results_eccentricity_error"
        )

        self.grid_layout_orbit_results.addWidget(
            self.line_edit_orbit_results_eccentricity_error, 2, 6, 1, 1
        )

        self.line_edit_orbit_results_inclination_error = QLineEdit(
            self.verticalLayoutWidget_5
        )
        self.line_edit_orbit_results_inclination_error.setObjectName(
            "line_edit_orbit_results_inclination_error"
        )

        self.grid_layout_orbit_results.addWidget(
            self.line_edit_orbit_results_inclination_error, 3, 2, 1, 1
        )

        self.line_edit_orbit_results_perihelion_error = QLineEdit(
            self.verticalLayoutWidget_5
        )
        self.line_edit_orbit_results_perihelion_error.setObjectName(
            "line_edit_orbit_results_perihelion_error"
        )

        self.grid_layout_orbit_results.addWidget(
            self.line_edit_orbit_results_perihelion_error, 4, 2, 1, 1
        )

        self.line_edit_orbit_results_eccentricity_value = QLineEdit(
            self.verticalLayoutWidget_5
        )
        self.line_edit_orbit_results_eccentricity_value.setObjectName(
            "line_edit_orbit_results_eccentricity_value"
        )

        self.grid_layout_orbit_results.addWidget(
            self.line_edit_orbit_results_eccentricity_value, 2, 5, 1, 1
        )

        self.line_edit_orbit_results_semimajor_axis_error = QLineEdit(
            self.verticalLayoutWidget_5
        )
        self.line_edit_orbit_results_semimajor_axis_error.setObjectName(
            "line_edit_orbit_results_semimajor_axis_error"
        )

        self.grid_layout_orbit_results.addWidget(
            self.line_edit_orbit_results_semimajor_axis_error, 2, 2, 1, 1
        )

        self.line_30 = QFrame(self.verticalLayoutWidget_5)
        self.line_30.setObjectName("line_30")
        self.line_30.setFrameShape(QFrame.VLine)
        self.line_30.setFrameShadow(QFrame.Sunken)

        self.grid_layout_orbit_results.addWidget(self.line_30, 2, 3, 3, 1)

        self.line_31 = QFrame(self.verticalLayoutWidget_5)
        self.line_31.setObjectName("line_31")
        self.line_31.setFrameShape(QFrame.HLine)
        self.line_31.setFrameShadow(QFrame.Sunken)

        self.grid_layout_orbit_results.addWidget(self.line_31, 1, 0, 1, 7)

        self.line_32 = QFrame(self.verticalLayoutWidget_5)
        self.line_32.setObjectName("line_32")
        self.line_32.setFrameShape(QFrame.VLine)
        self.line_32.setFrameShadow(QFrame.Sunken)

        self.grid_layout_orbit_results.addWidget(self.line_32, 0, 3, 1, 1)

        self.vertical_layout_orbit.addLayout(self.grid_layout_orbit_results)

        self.tab_widget_solutions.addTab(self.tab_orbit, "")
        self.tab_ephemeris = QWidget()
        self.tab_ephemeris.setObjectName("tab_ephemeris")
        self.verticalLayoutWidget_6 = QWidget(self.tab_ephemeris)
        self.verticalLayoutWidget_6.setObjectName("verticalLayoutWidget_6")
        self.verticalLayoutWidget_6.setGeometry(QRect(10, 10, 881, 291))
        self.vertical_layout_ephemeris = QVBoxLayout(self.verticalLayoutWidget_6)
        self.vertical_layout_ephemeris.setObjectName("vertical_layout_ephemeris")
        self.vertical_layout_ephemeris.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout_ephemeris_solve = QHBoxLayout()
        self.horizontal_layout_ephemeris_solve.setObjectName(
            "horizontal_layout_ephemeris_solve"
        )
        self.label_static_ephemeris_engine = QLabel(self.verticalLayoutWidget_6)
        self.label_static_ephemeris_engine.setObjectName(
            "label_static_ephemeris_engine"
        )

        self.horizontal_layout_ephemeris_solve.addWidget(
            self.label_static_ephemeris_engine
        )

        self.combo_box_ephemeris_engine = QComboBox(self.verticalLayoutWidget_6)
        self.combo_box_ephemeris_engine.addItem("")
        self.combo_box_ephemeris_engine.setObjectName("combo_box_ephemeris_engine")

        self.horizontal_layout_ephemeris_solve.addWidget(
            self.combo_box_ephemeris_engine
        )

        self.push_button_solve_ephemeris = QPushButton(self.verticalLayoutWidget_6)
        self.push_button_solve_ephemeris.setObjectName("push_button_solve_ephemeris")

        self.horizontal_layout_ephemeris_solve.addWidget(
            self.push_button_solve_ephemeris
        )

        self.vertical_layout_ephemeris.addLayout(self.horizontal_layout_ephemeris_solve)

        self.line_13 = QFrame(self.verticalLayoutWidget_6)
        self.line_13.setObjectName("line_13")
        self.line_13.setFrameShape(QFrame.HLine)
        self.line_13.setFrameShadow(QFrame.Sunken)

        self.vertical_layout_ephemeris.addWidget(self.line_13)

        self.grid_layout_ephemeris_results = QGridLayout()
        self.grid_layout_ephemeris_results.setObjectName(
            "grid_layout_ephemeris_results"
        )
        self.label_static_ephemeris_results_nonsiderial_rates = QLabel(
            self.verticalLayoutWidget_6
        )
        self.label_static_ephemeris_results_nonsiderial_rates.setObjectName(
            "label_static_ephemeris_results_nonsiderial_rates"
        )
        self.label_static_ephemeris_results_nonsiderial_rates.setAlignment(
            Qt.AlignCenter
        )

        self.grid_layout_ephemeris_results.addWidget(
            self.label_static_ephemeris_results_nonsiderial_rates, 0, 1, 1, 9
        )

        self.push_button_ephemeris_results_update_tcs_rates = QPushButton(
            self.verticalLayoutWidget_6
        )
        self.push_button_ephemeris_results_update_tcs_rates.setObjectName(
            "push_button_ephemeris_results_update_tcs_rates"
        )

        self.grid_layout_ephemeris_results.addWidget(
            self.push_button_ephemeris_results_update_tcs_rates, 5, 1, 1, 9
        )

        self.label_dynamic_ephemeris_results_first_order_ra_error = QLabel(
            self.verticalLayoutWidget_6
        )
        self.label_dynamic_ephemeris_results_first_order_ra_error.setObjectName(
            "label_dynamic_ephemeris_results_first_order_ra_error"
        )
        self.label_dynamic_ephemeris_results_first_order_ra_error.setAlignment(
            Qt.AlignCenter
        )

        self.grid_layout_ephemeris_results.addWidget(
            self.label_dynamic_ephemeris_results_first_order_ra_error, 4, 2, 1, 1
        )

        self.label_static_ephemeris_results_second_order_dec = QLabel(
            self.verticalLayoutWidget_6
        )
        self.label_static_ephemeris_results_second_order_dec.setObjectName(
            "label_static_ephemeris_results_second_order_dec"
        )
        self.label_static_ephemeris_results_second_order_dec.setAlignment(
            Qt.AlignCenter
        )

        self.grid_layout_ephemeris_results.addWidget(
            self.label_static_ephemeris_results_second_order_dec, 2, 8, 1, 2
        )

        self.label_static_ephemeris_results_first_order_dec = QLabel(
            self.verticalLayoutWidget_6
        )
        self.label_static_ephemeris_results_first_order_dec.setObjectName(
            "label_static_ephemeris_results_first_order_dec"
        )
        self.label_static_ephemeris_results_first_order_dec.setAlignment(Qt.AlignCenter)

        self.grid_layout_ephemeris_results.addWidget(
            self.label_static_ephemeris_results_first_order_dec, 2, 3, 1, 2
        )

        self.label_static_ephemeris_results_second_order_ra = QLabel(
            self.verticalLayoutWidget_6
        )
        self.label_static_ephemeris_results_second_order_ra.setObjectName(
            "label_static_ephemeris_results_second_order_ra"
        )
        self.label_static_ephemeris_results_second_order_ra.setAlignment(Qt.AlignCenter)

        self.grid_layout_ephemeris_results.addWidget(
            self.label_static_ephemeris_results_second_order_ra, 2, 6, 1, 2
        )

        self.label_static_ephemeris_results_second_order = QLabel(
            self.verticalLayoutWidget_6
        )
        self.label_static_ephemeris_results_second_order.setObjectName(
            "label_static_ephemeris_results_second_order"
        )
        self.label_static_ephemeris_results_second_order.setAlignment(Qt.AlignCenter)

        self.grid_layout_ephemeris_results.addWidget(
            self.label_static_ephemeris_results_second_order, 1, 6, 1, 4
        )

        self.label_static_ephemeris_results_first_order_ra = QLabel(
            self.verticalLayoutWidget_6
        )
        self.label_static_ephemeris_results_first_order_ra.setObjectName(
            "label_static_ephemeris_results_first_order_ra"
        )
        self.label_static_ephemeris_results_first_order_ra.setAlignment(Qt.AlignCenter)

        self.grid_layout_ephemeris_results.addWidget(
            self.label_static_ephemeris_results_first_order_ra, 2, 1, 1, 2
        )

        self.label_dynamic_ephemeris_results_second_order_ra_error = QLabel(
            self.verticalLayoutWidget_6
        )
        self.label_dynamic_ephemeris_results_second_order_ra_error.setObjectName(
            "label_dynamic_ephemeris_results_second_order_ra_error"
        )
        self.label_dynamic_ephemeris_results_second_order_ra_error.setAlignment(
            Qt.AlignCenter
        )

        self.grid_layout_ephemeris_results.addWidget(
            self.label_dynamic_ephemeris_results_second_order_ra_error, 4, 7, 1, 1
        )

        self.label_dynamic_ephemeris_results_second_order_dec_error = QLabel(
            self.verticalLayoutWidget_6
        )
        self.label_dynamic_ephemeris_results_second_order_dec_error.setObjectName(
            "label_dynamic_ephemeris_results_second_order_dec_error"
        )
        self.label_dynamic_ephemeris_results_second_order_dec_error.setAlignment(
            Qt.AlignCenter
        )

        self.grid_layout_ephemeris_results.addWidget(
            self.label_dynamic_ephemeris_results_second_order_dec_error, 4, 9, 1, 1
        )

        self.label_dynamic_ephemeris_results_second_order_dec_rate = QLabel(
            self.verticalLayoutWidget_6
        )
        self.label_dynamic_ephemeris_results_second_order_dec_rate.setObjectName(
            "label_dynamic_ephemeris_results_second_order_dec_rate"
        )
        self.label_dynamic_ephemeris_results_second_order_dec_rate.setAlignment(
            Qt.AlignCenter
        )

        self.grid_layout_ephemeris_results.addWidget(
            self.label_dynamic_ephemeris_results_second_order_dec_rate, 4, 8, 1, 1
        )

        self.line_14 = QFrame(self.verticalLayoutWidget_6)
        self.line_14.setObjectName("line_14")
        self.line_14.setFrameShape(QFrame.VLine)
        self.line_14.setFrameShadow(QFrame.Sunken)

        self.grid_layout_ephemeris_results.addWidget(self.line_14, 1, 5, 4, 1)

        self.label_static_ephemeris_results_first_order = QLabel(
            self.verticalLayoutWidget_6
        )
        self.label_static_ephemeris_results_first_order.setObjectName(
            "label_static_ephemeris_results_first_order"
        )
        self.label_static_ephemeris_results_first_order.setAlignment(Qt.AlignCenter)

        self.grid_layout_ephemeris_results.addWidget(
            self.label_static_ephemeris_results_first_order, 1, 1, 1, 4
        )

        self.label_dynamic_ephemeris_results_first_order_dec_error = QLabel(
            self.verticalLayoutWidget_6
        )
        self.label_dynamic_ephemeris_results_first_order_dec_error.setObjectName(
            "label_dynamic_ephemeris_results_first_order_dec_error"
        )
        self.label_dynamic_ephemeris_results_first_order_dec_error.setAlignment(
            Qt.AlignCenter
        )

        self.grid_layout_ephemeris_results.addWidget(
            self.label_dynamic_ephemeris_results_first_order_dec_error, 4, 4, 1, 1
        )

        self.label_dynamic_ephemeris_results_first_order_dec_rate = QLabel(
            self.verticalLayoutWidget_6
        )
        self.label_dynamic_ephemeris_results_first_order_dec_rate.setObjectName(
            "label_dynamic_ephemeris_results_first_order_dec_rate"
        )
        self.label_dynamic_ephemeris_results_first_order_dec_rate.setAlignment(
            Qt.AlignCenter
        )

        self.grid_layout_ephemeris_results.addWidget(
            self.label_dynamic_ephemeris_results_first_order_dec_rate, 4, 3, 1, 1
        )

        self.label_dynamic_ephemeris_results_second_order_ra_rate = QLabel(
            self.verticalLayoutWidget_6
        )
        self.label_dynamic_ephemeris_results_second_order_ra_rate.setObjectName(
            "label_dynamic_ephemeris_results_second_order_ra_rate"
        )
        self.label_dynamic_ephemeris_results_second_order_ra_rate.setAlignment(
            Qt.AlignCenter
        )

        self.grid_layout_ephemeris_results.addWidget(
            self.label_dynamic_ephemeris_results_second_order_ra_rate, 4, 6, 1, 1
        )

        self.label_dynamic_ephemeris_results_first_order_ra_rate = QLabel(
            self.verticalLayoutWidget_6
        )
        self.label_dynamic_ephemeris_results_first_order_ra_rate.setObjectName(
            "label_dynamic_ephemeris_results_first_order_ra_rate"
        )
        self.label_dynamic_ephemeris_results_first_order_ra_rate.setAlignment(
            Qt.AlignCenter
        )

        self.grid_layout_ephemeris_results.addWidget(
            self.label_dynamic_ephemeris_results_first_order_ra_rate, 4, 1, 1, 1
        )

        self.line_15 = QFrame(self.verticalLayoutWidget_6)
        self.line_15.setObjectName("line_15")
        self.line_15.setFrameShape(QFrame.HLine)
        self.line_15.setFrameShadow(QFrame.Sunken)

        self.grid_layout_ephemeris_results.addWidget(self.line_15, 3, 1, 1, 4)

        self.line_16 = QFrame(self.verticalLayoutWidget_6)
        self.line_16.setObjectName("line_16")
        self.line_16.setFrameShape(QFrame.HLine)
        self.line_16.setFrameShadow(QFrame.Sunken)

        self.grid_layout_ephemeris_results.addWidget(self.line_16, 3, 6, 1, 4)

        self.vertical_layout_ephemeris.addLayout(self.grid_layout_ephemeris_results)

        self.line_17 = QFrame(self.verticalLayoutWidget_6)
        self.line_17.setObjectName("line_17")
        self.line_17.setFrameShape(QFrame.HLine)
        self.line_17.setFrameShadow(QFrame.Sunken)

        self.vertical_layout_ephemeris.addWidget(self.line_17)

        self.horizontal_layout_ephemeris_forward = QHBoxLayout()
        self.horizontal_layout_ephemeris_forward.setObjectName(
            "horizontal_layout_ephemeris_forward"
        )
        self.combo_box_ephemeris_forward_datetime = QDateTimeEdit(
            self.verticalLayoutWidget_6
        )
        self.combo_box_ephemeris_forward_datetime.setObjectName(
            "combo_box_ephemeris_forward_datetime"
        )
        self.combo_box_ephemeris_forward_datetime.setMinimumSize(QSize(200, 0))
        self.combo_box_ephemeris_forward_datetime.setMaximumSize(
            QSize(16777213, 16777215)
        )

        self.horizontal_layout_ephemeris_forward.addWidget(
            self.combo_box_ephemeris_forward_datetime
        )

        self.combo_box_ephemeris_forward_timezone = QComboBox(
            self.verticalLayoutWidget_6
        )
        self.combo_box_ephemeris_forward_timezone.addItem("")
        self.combo_box_ephemeris_forward_timezone.addItem("")
        self.combo_box_ephemeris_forward_timezone.setObjectName(
            "combo_box_ephemeris_forward_timezone"
        )

        self.horizontal_layout_ephemeris_forward.addWidget(
            self.combo_box_ephemeris_forward_timezone
        )

        self.push_button_ephemeris_forward_solve = QPushButton(
            self.verticalLayoutWidget_6
        )
        self.push_button_ephemeris_forward_solve.setObjectName(
            "push_button_ephemeris_forward_solve"
        )

        self.horizontal_layout_ephemeris_forward.addWidget(
            self.push_button_ephemeris_forward_solve
        )

        self.line_18 = QFrame(self.verticalLayoutWidget_6)
        self.line_18.setObjectName("line_18")
        self.line_18.setFrameShape(QFrame.VLine)
        self.line_18.setFrameShadow(QFrame.Sunken)

        self.horizontal_layout_ephemeris_forward.addWidget(self.line_18)

        self.label_dynamic_ephemeris_forward_ra = QLabel(self.verticalLayoutWidget_6)
        self.label_dynamic_ephemeris_forward_ra.setObjectName(
            "label_dynamic_ephemeris_forward_ra"
        )
        self.label_dynamic_ephemeris_forward_ra.setAlignment(Qt.AlignCenter)

        self.horizontal_layout_ephemeris_forward.addWidget(
            self.label_dynamic_ephemeris_forward_ra
        )

        self.label_dynamic_ephemeris_forward_dec = QLabel(self.verticalLayoutWidget_6)
        self.label_dynamic_ephemeris_forward_dec.setObjectName(
            "label_dynamic_ephemeris_forward_dec"
        )
        self.label_dynamic_ephemeris_forward_dec.setAlignment(Qt.AlignCenter)

        self.horizontal_layout_ephemeris_forward.addWidget(
            self.label_dynamic_ephemeris_forward_dec
        )

        self.vertical_layout_ephemeris.addLayout(
            self.horizontal_layout_ephemeris_forward
        )

        self.tab_widget_solutions.addTab(self.tab_ephemeris, "")
        self.tab_propagate = QWidget()
        self.tab_propagate.setObjectName("tab_propagate")
        self.verticalLayoutWidget_7 = QWidget(self.tab_propagate)
        self.verticalLayoutWidget_7.setObjectName("verticalLayoutWidget_7")
        self.verticalLayoutWidget_7.setGeometry(QRect(10, 10, 881, 291))
        self.vertical_layout_propagate = QVBoxLayout(self.verticalLayoutWidget_7)
        self.vertical_layout_propagate.setObjectName("vertical_layout_propagate")
        self.vertical_layout_propagate.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout_propagate_solve = QHBoxLayout()
        self.horizontal_layout_propagate_solve.setObjectName(
            "horizontal_layout_propagate_solve"
        )
        self.label_static_propagate_engine = QLabel(self.verticalLayoutWidget_7)
        self.label_static_propagate_engine.setObjectName(
            "label_static_propagate_engine"
        )

        self.horizontal_layout_propagate_solve.addWidget(
            self.label_static_propagate_engine
        )

        self.combo_box_propagate_engine = QComboBox(self.verticalLayoutWidget_7)
        self.combo_box_propagate_engine.addItem("")
        self.combo_box_propagate_engine.addItem("")
        self.combo_box_propagate_engine.setObjectName("combo_box_propagate_engine")

        self.horizontal_layout_propagate_solve.addWidget(
            self.combo_box_propagate_engine
        )

        self.push_button_solve_propagation = QPushButton(self.verticalLayoutWidget_7)
        self.push_button_solve_propagation.setObjectName(
            "push_button_solve_propagation"
        )

        self.horizontal_layout_propagate_solve.addWidget(
            self.push_button_solve_propagation
        )

        self.vertical_layout_propagate.addLayout(self.horizontal_layout_propagate_solve)

        self.line_22 = QFrame(self.verticalLayoutWidget_7)
        self.line_22.setObjectName("line_22")
        self.line_22.setFrameShape(QFrame.HLine)
        self.line_22.setFrameShadow(QFrame.Sunken)

        self.vertical_layout_propagate.addWidget(self.line_22)

        self.grid_layout_propagate_results = QGridLayout()
        self.grid_layout_propagate_results.setObjectName(
            "grid_layout_propagate_results"
        )
        self.label_static_propagate_results_nonsiderial_rates = QLabel(
            self.verticalLayoutWidget_7
        )
        self.label_static_propagate_results_nonsiderial_rates.setObjectName(
            "label_static_propagate_results_nonsiderial_rates"
        )
        self.label_static_propagate_results_nonsiderial_rates.setAlignment(
            Qt.AlignCenter
        )

        self.grid_layout_propagate_results.addWidget(
            self.label_static_propagate_results_nonsiderial_rates, 0, 1, 1, 9
        )

        self.push_button_propagate_results_update_tcs_rates = QPushButton(
            self.verticalLayoutWidget_7
        )
        self.push_button_propagate_results_update_tcs_rates.setObjectName(
            "push_button_propagate_results_update_tcs_rates"
        )

        self.grid_layout_propagate_results.addWidget(
            self.push_button_propagate_results_update_tcs_rates, 5, 1, 1, 9
        )

        self.label_dynamic_propagate_results_first_order_ra_error = QLabel(
            self.verticalLayoutWidget_7
        )
        self.label_dynamic_propagate_results_first_order_ra_error.setObjectName(
            "label_dynamic_propagate_results_first_order_ra_error"
        )
        self.label_dynamic_propagate_results_first_order_ra_error.setAlignment(
            Qt.AlignCenter
        )

        self.grid_layout_propagate_results.addWidget(
            self.label_dynamic_propagate_results_first_order_ra_error, 4, 2, 1, 1
        )

        self.label_static_propagate_results_second_order_dec = QLabel(
            self.verticalLayoutWidget_7
        )
        self.label_static_propagate_results_second_order_dec.setObjectName(
            "label_static_propagate_results_second_order_dec"
        )
        self.label_static_propagate_results_second_order_dec.setAlignment(
            Qt.AlignCenter
        )

        self.grid_layout_propagate_results.addWidget(
            self.label_static_propagate_results_second_order_dec, 2, 8, 1, 2
        )

        self.label_static_propagate_results_first_order_dec = QLabel(
            self.verticalLayoutWidget_7
        )
        self.label_static_propagate_results_first_order_dec.setObjectName(
            "label_static_propagate_results_first_order_dec"
        )
        self.label_static_propagate_results_first_order_dec.setAlignment(Qt.AlignCenter)

        self.grid_layout_propagate_results.addWidget(
            self.label_static_propagate_results_first_order_dec, 2, 3, 1, 2
        )

        self.label_static_propagate_results_second_order_ra = QLabel(
            self.verticalLayoutWidget_7
        )
        self.label_static_propagate_results_second_order_ra.setObjectName(
            "label_static_propagate_results_second_order_ra"
        )
        self.label_static_propagate_results_second_order_ra.setAlignment(Qt.AlignCenter)

        self.grid_layout_propagate_results.addWidget(
            self.label_static_propagate_results_second_order_ra, 2, 6, 1, 2
        )

        self.label_static_propagate_results_second_order = QLabel(
            self.verticalLayoutWidget_7
        )
        self.label_static_propagate_results_second_order.setObjectName(
            "label_static_propagate_results_second_order"
        )
        self.label_static_propagate_results_second_order.setAlignment(Qt.AlignCenter)

        self.grid_layout_propagate_results.addWidget(
            self.label_static_propagate_results_second_order, 1, 6, 1, 4
        )

        self.label_static_propagate_results_first_order_ra = QLabel(
            self.verticalLayoutWidget_7
        )
        self.label_static_propagate_results_first_order_ra.setObjectName(
            "label_static_propagate_results_first_order_ra"
        )
        self.label_static_propagate_results_first_order_ra.setAlignment(Qt.AlignCenter)

        self.grid_layout_propagate_results.addWidget(
            self.label_static_propagate_results_first_order_ra, 2, 1, 1, 2
        )

        self.label_dynamic_propagate_results_second_order_ra_error = QLabel(
            self.verticalLayoutWidget_7
        )
        self.label_dynamic_propagate_results_second_order_ra_error.setObjectName(
            "label_dynamic_propagate_results_second_order_ra_error"
        )
        self.label_dynamic_propagate_results_second_order_ra_error.setAlignment(
            Qt.AlignCenter
        )

        self.grid_layout_propagate_results.addWidget(
            self.label_dynamic_propagate_results_second_order_ra_error, 4, 7, 1, 1
        )

        self.label_dynamic_propagate_results_second_order_dec_error = QLabel(
            self.verticalLayoutWidget_7
        )
        self.label_dynamic_propagate_results_second_order_dec_error.setObjectName(
            "label_dynamic_propagate_results_second_order_dec_error"
        )
        self.label_dynamic_propagate_results_second_order_dec_error.setAlignment(
            Qt.AlignCenter
        )

        self.grid_layout_propagate_results.addWidget(
            self.label_dynamic_propagate_results_second_order_dec_error, 4, 9, 1, 1
        )

        self.label_dynamic_propagate_results_second_order_dec_rate = QLabel(
            self.verticalLayoutWidget_7
        )
        self.label_dynamic_propagate_results_second_order_dec_rate.setObjectName(
            "label_dynamic_propagate_results_second_order_dec_rate"
        )
        self.label_dynamic_propagate_results_second_order_dec_rate.setAlignment(
            Qt.AlignCenter
        )

        self.grid_layout_propagate_results.addWidget(
            self.label_dynamic_propagate_results_second_order_dec_rate, 4, 8, 1, 1
        )

        self.line_19 = QFrame(self.verticalLayoutWidget_7)
        self.line_19.setObjectName("line_19")
        self.line_19.setFrameShape(QFrame.VLine)
        self.line_19.setFrameShadow(QFrame.Sunken)

        self.grid_layout_propagate_results.addWidget(self.line_19, 1, 5, 4, 1)

        self.label_static_propagate_results_first_order = QLabel(
            self.verticalLayoutWidget_7
        )
        self.label_static_propagate_results_first_order.setObjectName(
            "label_static_propagate_results_first_order"
        )
        self.label_static_propagate_results_first_order.setAlignment(Qt.AlignCenter)

        self.grid_layout_propagate_results.addWidget(
            self.label_static_propagate_results_first_order, 1, 1, 1, 4
        )

        self.label_dynamic_propagate_results_first_order_dec_error = QLabel(
            self.verticalLayoutWidget_7
        )
        self.label_dynamic_propagate_results_first_order_dec_error.setObjectName(
            "label_dynamic_propagate_results_first_order_dec_error"
        )
        self.label_dynamic_propagate_results_first_order_dec_error.setAlignment(
            Qt.AlignCenter
        )

        self.grid_layout_propagate_results.addWidget(
            self.label_dynamic_propagate_results_first_order_dec_error, 4, 4, 1, 1
        )

        self.label_dynamic_propagate_results_first_order_dec_rate = QLabel(
            self.verticalLayoutWidget_7
        )
        self.label_dynamic_propagate_results_first_order_dec_rate.setObjectName(
            "label_dynamic_propagate_results_first_order_dec_rate"
        )
        self.label_dynamic_propagate_results_first_order_dec_rate.setAlignment(
            Qt.AlignCenter
        )

        self.grid_layout_propagate_results.addWidget(
            self.label_dynamic_propagate_results_first_order_dec_rate, 4, 3, 1, 1
        )

        self.label_dynamic_propagate_results_second_order_ra_rate = QLabel(
            self.verticalLayoutWidget_7
        )
        self.label_dynamic_propagate_results_second_order_ra_rate.setObjectName(
            "label_dynamic_propagate_results_second_order_ra_rate"
        )
        self.label_dynamic_propagate_results_second_order_ra_rate.setAlignment(
            Qt.AlignCenter
        )

        self.grid_layout_propagate_results.addWidget(
            self.label_dynamic_propagate_results_second_order_ra_rate, 4, 6, 1, 1
        )

        self.label_dynamic_propagate_results_first_order_ra_rate = QLabel(
            self.verticalLayoutWidget_7
        )
        self.label_dynamic_propagate_results_first_order_ra_rate.setObjectName(
            "label_dynamic_propagate_results_first_order_ra_rate"
        )
        self.label_dynamic_propagate_results_first_order_ra_rate.setAlignment(
            Qt.AlignCenter
        )

        self.grid_layout_propagate_results.addWidget(
            self.label_dynamic_propagate_results_first_order_ra_rate, 4, 1, 1, 1
        )

        self.line_20 = QFrame(self.verticalLayoutWidget_7)
        self.line_20.setObjectName("line_20")
        self.line_20.setFrameShape(QFrame.HLine)
        self.line_20.setFrameShadow(QFrame.Sunken)

        self.grid_layout_propagate_results.addWidget(self.line_20, 3, 1, 1, 4)

        self.line_21 = QFrame(self.verticalLayoutWidget_7)
        self.line_21.setObjectName("line_21")
        self.line_21.setFrameShape(QFrame.HLine)
        self.line_21.setFrameShadow(QFrame.Sunken)

        self.grid_layout_propagate_results.addWidget(self.line_21, 3, 6, 1, 4)

        self.vertical_layout_propagate.addLayout(self.grid_layout_propagate_results)

        self.line_25 = QFrame(self.verticalLayoutWidget_7)
        self.line_25.setObjectName("line_25")
        self.line_25.setFrameShape(QFrame.HLine)
        self.line_25.setFrameShadow(QFrame.Sunken)

        self.vertical_layout_propagate.addWidget(self.line_25)

        self.horizontal_layout_propagate_forward = QHBoxLayout()
        self.horizontal_layout_propagate_forward.setObjectName(
            "horizontal_layout_propagate_forward"
        )
        self.combo_box_propagate_forward_datetime = QDateTimeEdit(
            self.verticalLayoutWidget_7
        )
        self.combo_box_propagate_forward_datetime.setObjectName(
            "combo_box_propagate_forward_datetime"
        )
        self.combo_box_propagate_forward_datetime.setMinimumSize(QSize(200, 0))
        self.combo_box_propagate_forward_datetime.setMaximumSize(
            QSize(16777213, 16777215)
        )

        self.horizontal_layout_propagate_forward.addWidget(
            self.combo_box_propagate_forward_datetime
        )

        self.combo_box_propagate_forward_timezone = QComboBox(
            self.verticalLayoutWidget_7
        )
        self.combo_box_propagate_forward_timezone.addItem("")
        self.combo_box_propagate_forward_timezone.addItem("")
        self.combo_box_propagate_forward_timezone.setObjectName(
            "combo_box_propagate_forward_timezone"
        )

        self.horizontal_layout_propagate_forward.addWidget(
            self.combo_box_propagate_forward_timezone
        )

        self.push_button_propagate_forward_solve = QPushButton(
            self.verticalLayoutWidget_7
        )
        self.push_button_propagate_forward_solve.setObjectName(
            "push_button_propagate_forward_solve"
        )

        self.horizontal_layout_propagate_forward.addWidget(
            self.push_button_propagate_forward_solve
        )

        self.line_24 = QFrame(self.verticalLayoutWidget_7)
        self.line_24.setObjectName("line_24")
        self.line_24.setFrameShape(QFrame.VLine)
        self.line_24.setFrameShadow(QFrame.Sunken)

        self.horizontal_layout_propagate_forward.addWidget(self.line_24)

        self.label_dynamic_propagate_forward_ra = QLabel(self.verticalLayoutWidget_7)
        self.label_dynamic_propagate_forward_ra.setObjectName(
            "label_dynamic_propagate_forward_ra"
        )
        self.label_dynamic_propagate_forward_ra.setAlignment(Qt.AlignCenter)

        self.horizontal_layout_propagate_forward.addWidget(
            self.label_dynamic_propagate_forward_ra
        )

        self.label_dynamic_propagate_forward_dec = QLabel(self.verticalLayoutWidget_7)
        self.label_dynamic_propagate_forward_dec.setObjectName(
            "label_dynamic_propagate_forward_dec"
        )
        self.label_dynamic_propagate_forward_dec.setAlignment(Qt.AlignCenter)

        self.horizontal_layout_propagate_forward.addWidget(
            self.label_dynamic_propagate_forward_dec
        )

        self.vertical_layout_propagate.addLayout(
            self.horizontal_layout_propagate_forward
        )

        self.tab_widget_solutions.addTab(self.tab_propagate, "")

        self.vertical_layout_window.addWidget(self.tab_widget_solutions)

        ManualWindow.setCentralWidget(self.central_widget)

        self.retranslateUi(ManualWindow)

        self.tab_widget_solutions.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(ManualWindow)

    # setupUi

    def retranslateUi(self, ManualWindow):
        ManualWindow.setWindowTitle(
            QCoreApplication.translate("ManualWindow", "OpihiExarata Manual Mode", None)
        )
        self.label_static_dummy_opihi_navbar.setText(
            QCoreApplication.translate(
                "ManualWindow", "DUMMY OPIHI IMAGE NAVIGATION BAR", None
            )
        )
        self.label_dynamic_target_4_pixel_location.setText(
            QCoreApplication.translate("ManualWindow", "(XXXX, YYYY)", None)
        )
        self.label_static_target_3_location.setText(
            QCoreApplication.translate("ManualWindow", "Target 3 Location:", None)
        )
        self.label_static_target_4_location.setText(
            QCoreApplication.translate("ManualWindow", "Target 4 Location:", None)
        )
        self.push_button_relocate_target_location_1.setText(
            QCoreApplication.translate("ManualWindow", "Relocate", None)
        )
        self.label_dynamic_target_1_pixel_location.setText(
            QCoreApplication.translate("ManualWindow", "(XXXX, YYYY)", None)
        )
        self.push_button_load_filename_3.setText(
            QCoreApplication.translate("ManualWindow", "Load", None)
        )
        self.label_dynamic_filename_3.setText(
            QCoreApplication.translate(
                "ManualWindow", "opi.20XXA999.YYMMDD.AAAAAAAAAA.#####.a.fits", None
            )
        )
        self.label_dynamic_filename_1.setText(
            QCoreApplication.translate(
                "ManualWindow", "opi.20XXA999.YYMMDD.AAAAAAAAAA.#####.a.fits", None
            )
        )
        self.label_dynamic_filename_2.setText(
            QCoreApplication.translate(
                "ManualWindow", "opi.20XXA999.YYMMDD.AAAAAAAAAA.#####.a.fits", None
            )
        )
        self.label_dynamic_filename_4.setText(
            QCoreApplication.translate(
                "ManualWindow", "opi.20XXA999.YYMMDD.AAAAAAAAAA.#####.a.fits", None
            )
        )
        self.radio_button_primary_file_3.setText(
            QCoreApplication.translate("ManualWindow", "3", None)
        )
        self.radio_button_primary_file_4.setText(
            QCoreApplication.translate("ManualWindow", "4", None)
        )
        self.label_dynamic_target_2_pixel_location.setText(
            QCoreApplication.translate("ManualWindow", "(XXXX, YYYY)", None)
        )
        self.push_button_relocate_target_location_3.setText(
            QCoreApplication.translate("ManualWindow", "Relocate", None)
        )
        self.radio_button_primary_file_1.setText(
            QCoreApplication.translate("ManualWindow", "1", None)
        )
        self.label_dynamic_target_3_pixel_location.setText(
            QCoreApplication.translate("ManualWindow", "(XXXX, YYYY)", None)
        )
        self.radio_button_primary_file_2.setText(
            QCoreApplication.translate("ManualWindow", "2", None)
        )
        self.label_static_target_2_location.setText(
            QCoreApplication.translate("ManualWindow", "Target 2 Location:", None)
        )
        self.push_button_relocate_target_location_2.setText(
            QCoreApplication.translate("ManualWindow", "Relocate", None)
        )
        self.push_button_load_filename_1.setText(
            QCoreApplication.translate("ManualWindow", "Load", None)
        )
        self.push_button_load_filename_2.setText(
            QCoreApplication.translate("ManualWindow", "Load", None)
        )
        self.label_static_target_1_location.setText(
            QCoreApplication.translate("ManualWindow", "Target 1 Location:", None)
        )
        self.push_button_load_filename_4.setText(
            QCoreApplication.translate("ManualWindow", "Load", None)
        )
        self.push_button_relocate_target_location_4.setText(
            QCoreApplication.translate("ManualWindow", "Relocate", None)
        )
        self.push_button_force_reset.setText(
            QCoreApplication.translate("ManualWindow", "Reset", None)
        )
        self.push_button_save_and_reset.setText(
            QCoreApplication.translate("ManualWindow", "Save && Reset", None)
        )
        self.label_static_detected_target_name.setText(
            QCoreApplication.translate("ManualWindow", "(Detected) Target Name", None)
        )
        self.push_button_change_target_name.setText(
            QCoreApplication.translate("ManualWindow", "Change", None)
        )
        self.push_button_send_target_to_tcs.setText(
            QCoreApplication.translate("ManualWindow", "Send Target to TCS", None)
        )
        self.label.setText(
            QCoreApplication.translate("ManualWindow", "TextLabel", None)
        )
        self.tab_widget_solutions.setTabText(
            self.tab_widget_solutions.indexOf(self.tab_summary),
            QCoreApplication.translate("ManualWindow", "Summary", None),
        )
        self.label_static_astrometry_engine.setText(
            QCoreApplication.translate("ManualWindow", "Astrometry Engine", None)
        )
        self.combo_box_astrometry_engine.setItemText(
            0, QCoreApplication.translate("ManualWindow", "Astrometry.net Nova", None)
        )
        self.combo_box_astrometry_engine.setItemText(
            1, QCoreApplication.translate("ManualWindow", "Astrometry.net Host", None)
        )

        self.push_button_solve_astrometry.setText(
            QCoreApplication.translate("ManualWindow", "Solve Astrometry", None)
        )
        self.label_static_astrometry_results_center_dec.setText(
            QCoreApplication.translate("ManualWindow", "DEC", None)
        )
        self.label_dynamic_astrometry_file_3_target_ra.setText(
            QCoreApplication.translate("ManualWindow", "HH:MM:SS.SS", None)
        )
        self.label_static_astrometry_results_center_ra.setText(
            QCoreApplication.translate("ManualWindow", "RA", None)
        )
        self.label_dynamic_astrometry_file_4_center_ra.setText(
            QCoreApplication.translate("ManualWindow", "HH:MM:SS.SS", None)
        )
        self.label_static_astrometry_results_center.setText(
            QCoreApplication.translate("ManualWindow", "Center", None)
        )
        self.label_dynamic_astrometry_file_4_target_ra.setText(
            QCoreApplication.translate("ManualWindow", "HH:MM:SS.SS", None)
        )
        self.label_dynamic_astrometry_file_3_target_dec.setText(
            QCoreApplication.translate("ManualWindow", "+DD:MM:SS.SS", None)
        )
        self.label_dynamic_astrometry_file_4_target_dec.setText(
            QCoreApplication.translate("ManualWindow", "+DD:MM:SS.SS", None)
        )
        self.label_dynamic_astrometry_file_2_target_ra.setText(
            QCoreApplication.translate("ManualWindow", "HH:MM:SS.SS", None)
        )
        self.label_dynamic_astrometry_file_3_center_dec.setText(
            QCoreApplication.translate("ManualWindow", "+DD:MM:SS.SS", None)
        )
        self.label_dynamic_astrometry_file_4_center_dec.setText(
            QCoreApplication.translate("ManualWindow", "+DD:MM:SS.SS", None)
        )
        self.label_dynamic_astrometry_file_2_center_dec.setText(
            QCoreApplication.translate("ManualWindow", "+DD:MM:SS.SS", None)
        )
        self.label_static_astrometry_results_target_dec.setText(
            QCoreApplication.translate("ManualWindow", "DEC", None)
        )
        self.label_static_astrometry_results_target_ra.setText(
            QCoreApplication.translate("ManualWindow", "RA", None)
        )
        self.label_dynamic_astrometry_file_2_target_dec.setText(
            QCoreApplication.translate("ManualWindow", "+DD:MM:SS.SS", None)
        )
        self.label_dynamic_astrometry_file_3_center_ra.setText(
            QCoreApplication.translate("ManualWindow", "HH:MM:SS.SS", None)
        )
        self.label_dynamic_astrometry_file_2_center_ra.setText(
            QCoreApplication.translate("ManualWindow", "HH:MM:SS.SS", None)
        )
        self.label_static_astrometry_results_target.setText(
            QCoreApplication.translate("ManualWindow", "Target/Asteroid", None)
        )
        self.label_dynamic_astrometry_file_1_center_dec.setText(
            QCoreApplication.translate("ManualWindow", "+DD:MM:SS.SS", None)
        )
        self.label_static_astrometry_results_file_1.setText(
            QCoreApplication.translate("ManualWindow", "1", None)
        )
        self.label_dynamic_astrometry_file_1_target_dec.setText(
            QCoreApplication.translate("ManualWindow", "+DD:MM:SS.SS", None)
        )
        self.label_dynamic_astrometry_file_1_target_ra.setText(
            QCoreApplication.translate("ManualWindow", "HH:MM:SS.SS", None)
        )
        self.label_static_astrometry_results_file.setText(
            QCoreApplication.translate("ManualWindow", "File", None)
        )
        self.label_dynamic_astrometry_file_1_center_ra.setText(
            QCoreApplication.translate("ManualWindow", "HH:MM:SS.SS", None)
        )
        self.label_static_astrometry_results_file_3.setText(
            QCoreApplication.translate("ManualWindow", "3", None)
        )
        self.label_static_astrometry_results_file_2.setText(
            QCoreApplication.translate("ManualWindow", "2", None)
        )
        self.label_static_astrometry_results_file_4.setText(
            QCoreApplication.translate("ManualWindow", "4", None)
        )
        self.label_static_astrometry_custom_pixel_x.setText(
            QCoreApplication.translate("ManualWindow", "Pixel X", None)
        )
        self.label_static_astrometry_coordinate_solve.setText(
            QCoreApplication.translate("ManualWindow", "Coordinate Solve", None)
        )
        self.label_static_astrometry_custom_pixel_y.setText(
            QCoreApplication.translate("ManualWindow", "Pixel Y", None)
        )
        self.label_static_astrometry_custom_ra.setText(
            QCoreApplication.translate("ManualWindow", "RA", None)
        )
        self.label_static_astrometry_custom_dec.setText(
            QCoreApplication.translate("ManualWindow", "DEC", None)
        )
        self.push_button_astrometry_custom_solve.setText(
            QCoreApplication.translate("ManualWindow", "Solve", None)
        )
        self.tab_widget_solutions.setTabText(
            self.tab_widget_solutions.indexOf(self.tab_astrometry),
            QCoreApplication.translate("ManualWindow", "Astrometry", None),
        )
        self.label_static_photometry_engine.setText(
            QCoreApplication.translate("ManualWindow", "Photometry Engine", None)
        )
        self.combo_box_photometry_engine.setItemText(
            0,
            QCoreApplication.translate("ManualWindow", "Pan-STARRS 3pi DR2 MAST", None),
        )

        self.push_button_solve_photometry.setText(
            QCoreApplication.translate("ManualWindow", "Solve Photometry", None)
        )
        self.label_static_photometry_results_file_1.setText(
            QCoreApplication.translate("ManualWindow", "1", None)
        )
        self.label_static_photometry_results_file.setText(
            QCoreApplication.translate("ManualWindow", "File", None)
        )
        self.label_static_photometry_results_file_2.setText(
            QCoreApplication.translate("ManualWindow", "2", None)
        )
        self.label_static_photometry_results_file_4.setText(
            QCoreApplication.translate("ManualWindow", "4", None)
        )
        self.label_static_photometry_results_file_3.setText(
            QCoreApplication.translate("ManualWindow", "3", None)
        )
        self.label_static_photometry_results_zero_point.setText(
            QCoreApplication.translate("ManualWindow", "Zero Point", None)
        )
        self.label_static_photometry_results_file_2_filter_name.setText(
            QCoreApplication.translate("ManualWindow", "FF", None)
        )
        self.label_static_photometry_results_aperture_magnitude.setText(
            QCoreApplication.translate("ManualWindow", "Aperture Magnitude", None)
        )
        self.label_static_photometry_results_filter_name.setText(
            QCoreApplication.translate("ManualWindow", "Filter Name", None)
        )
        self.label_static_photometry_results_file_4_filter_name.setText(
            QCoreApplication.translate("ManualWindow", "FF", None)
        )
        self.label_static_photometry_results_file_1_filter_name.setText(
            QCoreApplication.translate("ManualWindow", "FF", None)
        )
        self.label_static_photometry_results_file_3_filter_name.setText(
            QCoreApplication.translate("ManualWindow", "FF", None)
        )
        self.label_static_photometry_results_file_1_zero_point.setText(
            QCoreApplication.translate("ManualWindow", "ZZ.ZZZ + E.EEE", None)
        )
        self.label_static_photometry_results_file_4_zero_point.setText(
            QCoreApplication.translate("ManualWindow", "ZZ.ZZZ + E.EEE", None)
        )
        self.label_static_photometry_results_file_2_zero_point.setText(
            QCoreApplication.translate("ManualWindow", "ZZ.ZZZ + E.EEE", None)
        )
        self.label_static_photometry_results_file_3_zero_point.setText(
            QCoreApplication.translate("ManualWindow", "ZZ.ZZZ + E.EEE", None)
        )
        self.label_static_photometry_results_file_1_magnitude.setText(
            QCoreApplication.translate("ManualWindow", "MM.MMM + E.EEE", None)
        )
        self.label_static_photometry_results_file_2_magnitude.setText(
            QCoreApplication.translate("ManualWindow", "MM.MMM + E.EEE", None)
        )
        self.label_static_photometry_results_file_3_magnitude.setText(
            QCoreApplication.translate("ManualWindow", "MM.MMM + E.EEE", None)
        )
        self.label_static_photometry_results_file_4_magnitude.setText(
            QCoreApplication.translate("ManualWindow", "MM.MMM + E.EEE", None)
        )
        self.tab_widget_solutions.setTabText(
            self.tab_widget_solutions.indexOf(self.tab_photometry),
            QCoreApplication.translate("ManualWindow", "Photometry", None),
        )
        self.label_static_orbit_engine.setText(
            QCoreApplication.translate("ManualWindow", "Orbit Engine", None)
        )
        self.combo_box_orbit_engine.setItemText(
            0, QCoreApplication.translate("ManualWindow", "OrbFit", None)
        )
        self.combo_box_orbit_engine.setItemText(
            1, QCoreApplication.translate("ManualWindow", "Custom Orbit", None)
        )

        self.push_button_solve_orbit.setText(
            QCoreApplication.translate("ManualWindow", "Solve Orbit", None)
        )
        self.line_edit_orbit_results_ascending_node_error.setText(
            QCoreApplication.translate("ManualWindow", "EE.EEEE", None)
        )
        self.line_edit_orbit_results_ascending_node_value.setText(
            QCoreApplication.translate("ManualWindow", "VV.VVVV", None)
        )
        self.line_edit_orbit_results_mean_anomaly_value.setText(
            QCoreApplication.translate("ManualWindow", "VV.VVVV", None)
        )
        self.line_edit_orbit_results_mean_anomaly_error.setText(
            QCoreApplication.translate("ManualWindow", "EE.EEEE", None)
        )
        self.line_edit_orbit_results_epoch_value.setText(
            QCoreApplication.translate("ManualWindow", "EEEEEEE.EEEEE", None)
        )
        self.label_static_orbit_results_value.setText(
            QCoreApplication.translate("ManualWindow", "Value", None)
        )
        self.label_static_orbit_results_error.setText(
            QCoreApplication.translate("ManualWindow", "\u00b1 Error", None)
        )
        self.label_static_orbit_results_semimajor_axis.setText(
            QCoreApplication.translate("ManualWindow", "Semi-major Axis [AU]", None)
        )
        self.label_static_orbit_results_eccentricity.setText(
            QCoreApplication.translate("ManualWindow", "Eccentricity [1]", None)
        )
        self.label_static_orbit_results_mean_anomaly.setText(
            QCoreApplication.translate("ManualWindow", "Mean Anomaly [deg]", None)
        )
        self.label_static_orbit_results_inclination.setText(
            QCoreApplication.translate("ManualWindow", "Inclination [deg]", None)
        )
        self.label_static_orbit_results_perihelion.setText(
            QCoreApplication.translate("ManualWindow", "Perihelion [deg]", None)
        )
        self.line_edit_orbit_results_semimajor_axis_value.setText(
            QCoreApplication.translate("ManualWindow", "VV.VVVV", None)
        )
        self.line_edit_orbit_results_perihelion_value.setText(
            QCoreApplication.translate("ManualWindow", "VV.VVVV", None)
        )
        self.label_static_orbit_results_ascending_node.setText(
            QCoreApplication.translate("ManualWindow", "Ascending Node [deg]", None)
        )
        self.label_static_orbit_results_epoch.setText(
            QCoreApplication.translate("ManualWindow", "Epoch [JD]", None)
        )
        self.line_edit_orbit_results_inclination_value.setText(
            QCoreApplication.translate("ManualWindow", "VV.VVVV", None)
        )
        self.line_edit_orbit_results_eccentricity_error.setText(
            QCoreApplication.translate("ManualWindow", "EE.EEEE", None)
        )
        self.line_edit_orbit_results_inclination_error.setText(
            QCoreApplication.translate("ManualWindow", "EE.EEEE", None)
        )
        self.line_edit_orbit_results_perihelion_error.setText(
            QCoreApplication.translate("ManualWindow", "EE.EEEE", None)
        )
        self.line_edit_orbit_results_eccentricity_value.setText(
            QCoreApplication.translate("ManualWindow", "VV.VVVV", None)
        )
        self.line_edit_orbit_results_semimajor_axis_error.setText(
            QCoreApplication.translate("ManualWindow", "EE.EEEE", None)
        )
        self.tab_widget_solutions.setTabText(
            self.tab_widget_solutions.indexOf(self.tab_orbit),
            QCoreApplication.translate("ManualWindow", "Orbit", None),
        )
        self.label_static_ephemeris_engine.setText(
            QCoreApplication.translate("ManualWindow", "Ephemeris Engine", None)
        )
        self.combo_box_ephemeris_engine.setItemText(
            0, QCoreApplication.translate("ManualWindow", "JPL Horizons", None)
        )

        self.push_button_solve_ephemeris.setText(
            QCoreApplication.translate("ManualWindow", "Solve Ephemeris", None)
        )
        self.label_static_ephemeris_results_nonsiderial_rates.setText(
            QCoreApplication.translate(
                "ManualWindow", "Ephemeris Non-Siderial Rates", None
            )
        )
        self.push_button_ephemeris_results_update_tcs_rates.setText(
            QCoreApplication.translate("ManualWindow", "Update TCS Rates", None)
        )
        self.label_dynamic_ephemeris_results_first_order_ra_error.setText(
            QCoreApplication.translate("ManualWindow", "+EE.EEEE", None)
        )
        self.label_static_ephemeris_results_second_order_dec.setText(
            QCoreApplication.translate("ManualWindow", "DEC", None)
        )
        self.label_static_ephemeris_results_first_order_dec.setText(
            QCoreApplication.translate("ManualWindow", "DEC", None)
        )
        self.label_static_ephemeris_results_second_order_ra.setText(
            QCoreApplication.translate("ManualWindow", "RA", None)
        )
        self.label_static_ephemeris_results_second_order.setText(
            QCoreApplication.translate(
                "ManualWindow",
                '<html><head/><body><p>2nd Order [&quot;/s<span style=" vertical-align:super;">2</span>]</p></body></html>',
                None,
            )
        )
        self.label_static_ephemeris_results_first_order_ra.setText(
            QCoreApplication.translate("ManualWindow", "RA", None)
        )
        self.label_dynamic_ephemeris_results_second_order_ra_error.setText(
            QCoreApplication.translate("ManualWindow", "+EE.EEEE", None)
        )
        self.label_dynamic_ephemeris_results_second_order_dec_error.setText(
            QCoreApplication.translate("ManualWindow", "+EE.EEEE", None)
        )
        self.label_dynamic_ephemeris_results_second_order_dec_rate.setText(
            QCoreApplication.translate("ManualWindow", "+AA.AAA", None)
        )
        self.label_static_ephemeris_results_first_order.setText(
            QCoreApplication.translate("ManualWindow", '1st Order ["/s]', None)
        )
        self.label_dynamic_ephemeris_results_first_order_dec_error.setText(
            QCoreApplication.translate("ManualWindow", "+EE.EEEE", None)
        )
        self.label_dynamic_ephemeris_results_first_order_dec_rate.setText(
            QCoreApplication.translate("ManualWindow", "+VV.VVV", None)
        )
        self.label_dynamic_ephemeris_results_second_order_ra_rate.setText(
            QCoreApplication.translate("ManualWindow", "+AA.AAA", None)
        )
        self.label_dynamic_ephemeris_results_first_order_ra_rate.setText(
            QCoreApplication.translate("ManualWindow", "+VV.VVV", None)
        )
        self.combo_box_ephemeris_forward_datetime.setDisplayFormat(
            QCoreApplication.translate("ManualWindow", "yyyy-MM-dd HH:mm:ss", None)
        )
        self.combo_box_ephemeris_forward_timezone.setItemText(
            0, QCoreApplication.translate("ManualWindow", "UTC+00:00", None)
        )
        self.combo_box_ephemeris_forward_timezone.setItemText(
            1, QCoreApplication.translate("ManualWindow", "HST-10:00", None)
        )

        self.push_button_ephemeris_forward_solve.setText(
            QCoreApplication.translate("ManualWindow", "Forward Solve", None)
        )
        self.label_dynamic_ephemeris_forward_ra.setText(
            QCoreApplication.translate("ManualWindow", "HH:MM:SS.SS", None)
        )
        self.label_dynamic_ephemeris_forward_dec.setText(
            QCoreApplication.translate("ManualWindow", "+DD:MM:SS.SS", None)
        )
        self.tab_widget_solutions.setTabText(
            self.tab_widget_solutions.indexOf(self.tab_ephemeris),
            QCoreApplication.translate("ManualWindow", "Ephemeris", None),
        )
        self.label_static_propagate_engine.setText(
            QCoreApplication.translate("ManualWindow", "Propagation Engine", None)
        )
        self.combo_box_propagate_engine.setItemText(
            0, QCoreApplication.translate("ManualWindow", "Linear", None)
        )
        self.combo_box_propagate_engine.setItemText(
            1, QCoreApplication.translate("ManualWindow", "Quadratic", None)
        )

        self.push_button_solve_propagation.setText(
            QCoreApplication.translate("ManualWindow", "Solve Propagation", None)
        )
        self.label_static_propagate_results_nonsiderial_rates.setText(
            QCoreApplication.translate(
                "ManualWindow", "Propagation Non-Siderial Rates", None
            )
        )
        self.push_button_propagate_results_update_tcs_rates.setText(
            QCoreApplication.translate("ManualWindow", "Update TCS Rates", None)
        )
        self.label_dynamic_propagate_results_first_order_ra_error.setText(
            QCoreApplication.translate("ManualWindow", "+EE.EEEE", None)
        )
        self.label_static_propagate_results_second_order_dec.setText(
            QCoreApplication.translate("ManualWindow", "DEC", None)
        )
        self.label_static_propagate_results_first_order_dec.setText(
            QCoreApplication.translate("ManualWindow", "DEC", None)
        )
        self.label_static_propagate_results_second_order_ra.setText(
            QCoreApplication.translate("ManualWindow", "RA", None)
        )
        self.label_static_propagate_results_second_order.setText(
            QCoreApplication.translate(
                "ManualWindow",
                '<html><head/><body><p>2nd Order [&quot;/s<span style=" vertical-align:super;">2</span>]</p></body></html>',
                None,
            )
        )
        self.label_static_propagate_results_first_order_ra.setText(
            QCoreApplication.translate("ManualWindow", "RA", None)
        )
        self.label_dynamic_propagate_results_second_order_ra_error.setText(
            QCoreApplication.translate("ManualWindow", "+EE.EEEE", None)
        )
        self.label_dynamic_propagate_results_second_order_dec_error.setText(
            QCoreApplication.translate("ManualWindow", "+EE.EEEE", None)
        )
        self.label_dynamic_propagate_results_second_order_dec_rate.setText(
            QCoreApplication.translate("ManualWindow", "+AA.AAA", None)
        )
        self.label_static_propagate_results_first_order.setText(
            QCoreApplication.translate("ManualWindow", '1st Order ["/s]', None)
        )
        self.label_dynamic_propagate_results_first_order_dec_error.setText(
            QCoreApplication.translate("ManualWindow", "+EE.EEEE", None)
        )
        self.label_dynamic_propagate_results_first_order_dec_rate.setText(
            QCoreApplication.translate("ManualWindow", "+VV.VVV", None)
        )
        self.label_dynamic_propagate_results_second_order_ra_rate.setText(
            QCoreApplication.translate("ManualWindow", "+AA.AAA", None)
        )
        self.label_dynamic_propagate_results_first_order_ra_rate.setText(
            QCoreApplication.translate("ManualWindow", "+VV.VVV", None)
        )
        self.combo_box_propagate_forward_datetime.setDisplayFormat(
            QCoreApplication.translate("ManualWindow", "yyyy-MM-dd HH:mm:ss", None)
        )
        self.combo_box_propagate_forward_timezone.setItemText(
            0, QCoreApplication.translate("ManualWindow", "UTC+00:00", None)
        )
        self.combo_box_propagate_forward_timezone.setItemText(
            1, QCoreApplication.translate("ManualWindow", "HST-10:00", None)
        )

        self.push_button_propagate_forward_solve.setText(
            QCoreApplication.translate("ManualWindow", "Forward Solve", None)
        )
        self.label_dynamic_propagate_forward_ra.setText(
            QCoreApplication.translate("ManualWindow", "HH:MM:SS.SS", None)
        )
        self.label_dynamic_propagate_forward_dec.setText(
            QCoreApplication.translate("ManualWindow", "+DD:MM:SS.SS", None)
        )
        self.tab_widget_solutions.setTabText(
            self.tab_widget_solutions.indexOf(self.tab_propagate),
            QCoreApplication.translate("ManualWindow", "Propagate", None),
        )

    # retranslateUi
