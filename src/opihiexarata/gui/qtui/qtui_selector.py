# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'selector.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QGraphicsView,
    QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_SelectorWindow(object):
    def setupUi(self, SelectorWindow):
        if not SelectorWindow.objectName():
            SelectorWindow.setObjectName(u"SelectorWindow")
        SelectorWindow.resize(623, 868)
        self.verticalLayoutWidget = QWidget(SelectorWindow)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 10, 604, 846))
        font = QFont()
        font.setFamilies([u"Cantarell"])
        font.setPointSize(12)
        self.verticalLayoutWidget.setFont(font)
        self.vertical_layout_selector = QVBoxLayout(self.verticalLayoutWidget)
        self.vertical_layout_selector.setObjectName(u"vertical_layout_selector")
        self.vertical_layout_selector.setContentsMargins(0, 0, 0, 0)
        self.grid_layout_file_selection = QGridLayout()
        self.grid_layout_file_selection.setObjectName(u"grid_layout_file_selection")
        self.label_dynamic_current_fits_filename = QLabel(self.verticalLayoutWidget)
        self.label_dynamic_current_fits_filename.setObjectName(u"label_dynamic_current_fits_filename")
        self.label_dynamic_current_fits_filename.setMinimumSize(QSize(400, 0))
        font1 = QFont()
        font1.setFamilies([u"Cantarell"])
        self.label_dynamic_current_fits_filename.setFont(font1)

        self.grid_layout_file_selection.addWidget(self.label_dynamic_current_fits_filename, 0, 1, 1, 1)

        self.label_dynamic_reference_fits_filename = QLabel(self.verticalLayoutWidget)
        self.label_dynamic_reference_fits_filename.setObjectName(u"label_dynamic_reference_fits_filename")
        self.label_dynamic_reference_fits_filename.setMinimumSize(QSize(400, 0))
        self.label_dynamic_reference_fits_filename.setFont(font1)

        self.grid_layout_file_selection.addWidget(self.label_dynamic_reference_fits_filename, 1, 1, 1, 1)

        self.push_button_change_reference_filename = QPushButton(self.verticalLayoutWidget)
        self.push_button_change_reference_filename.setObjectName(u"push_button_change_reference_filename")
        self.push_button_change_reference_filename.setFont(font1)

        self.grid_layout_file_selection.addWidget(self.push_button_change_reference_filename, 1, 2, 1, 1)

        self.label_static_current_fits_filename = QLabel(self.verticalLayoutWidget)
        self.label_static_current_fits_filename.setObjectName(u"label_static_current_fits_filename")
        self.label_static_current_fits_filename.setFont(font1)

        self.grid_layout_file_selection.addWidget(self.label_static_current_fits_filename, 0, 0, 1, 1)

        self.label_static_reference_fits_filename = QLabel(self.verticalLayoutWidget)
        self.label_static_reference_fits_filename.setObjectName(u"label_static_reference_fits_filename")
        self.label_static_reference_fits_filename.setFont(font1)

        self.grid_layout_file_selection.addWidget(self.label_static_reference_fits_filename, 1, 0, 1, 1)


        self.vertical_layout_selector.addLayout(self.grid_layout_file_selection)

        self.line_2 = QFrame(self.verticalLayoutWidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFont(font1)
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.vertical_layout_selector.addWidget(self.line_2)

        self.vertical_layout_image = QVBoxLayout()
        self.vertical_layout_image.setObjectName(u"vertical_layout_image")
        self.dummy_selector_image = QGraphicsView(self.verticalLayoutWidget)
        self.dummy_selector_image.setObjectName(u"dummy_selector_image")
        self.dummy_selector_image.setMinimumSize(QSize(600, 600))
        self.dummy_selector_image.setMaximumSize(QSize(600, 600))
        self.dummy_selector_image.setFont(font1)

        self.vertical_layout_image.addWidget(self.dummy_selector_image)

        self.dummy_selector_navbar = QLabel(self.verticalLayoutWidget)
        self.dummy_selector_navbar.setObjectName(u"dummy_selector_navbar")
        self.dummy_selector_navbar.setMinimumSize(QSize(0, 25))
        self.dummy_selector_navbar.setMaximumSize(QSize(16777215, 25))
        self.dummy_selector_navbar.setFont(font1)
        self.dummy_selector_navbar.setAlignment(Qt.AlignCenter)

        self.vertical_layout_image.addWidget(self.dummy_selector_navbar)


        self.vertical_layout_selector.addLayout(self.vertical_layout_image)

        self.horizonta_layout_subtraction_mode = QHBoxLayout()
        self.horizonta_layout_subtraction_mode.setObjectName(u"horizonta_layout_subtraction_mode")
        self.label_static_subtraction_mode = QLabel(self.verticalLayoutWidget)
        self.label_static_subtraction_mode.setObjectName(u"label_static_subtraction_mode")
        self.label_static_subtraction_mode.setFont(font1)

        self.horizonta_layout_subtraction_mode.addWidget(self.label_static_subtraction_mode)

        self.line_3 = QFrame(self.verticalLayoutWidget)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFont(font1)
        self.line_3.setFrameShape(QFrame.VLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.horizonta_layout_subtraction_mode.addWidget(self.line_3)

        self.push_button_mode_none = QPushButton(self.verticalLayoutWidget)
        self.push_button_mode_none.setObjectName(u"push_button_mode_none")
        self.push_button_mode_none.setFont(font1)

        self.horizonta_layout_subtraction_mode.addWidget(self.push_button_mode_none)

        self.push_button_mode_reference = QPushButton(self.verticalLayoutWidget)
        self.push_button_mode_reference.setObjectName(u"push_button_mode_reference")
        self.push_button_mode_reference.setFont(font1)

        self.horizonta_layout_subtraction_mode.addWidget(self.push_button_mode_reference)

        self.push_button_mode_sidereal = QPushButton(self.verticalLayoutWidget)
        self.push_button_mode_sidereal.setObjectName(u"push_button_mode_sidereal")
        self.push_button_mode_sidereal.setFont(font1)

        self.horizonta_layout_subtraction_mode.addWidget(self.push_button_mode_sidereal)

        self.push_button_mode_non_sidereal = QPushButton(self.verticalLayoutWidget)
        self.push_button_mode_non_sidereal.setObjectName(u"push_button_mode_non_sidereal")
        self.push_button_mode_non_sidereal.setFont(font1)

        self.horizonta_layout_subtraction_mode.addWidget(self.push_button_mode_non_sidereal)


        self.vertical_layout_selector.addLayout(self.horizonta_layout_subtraction_mode)

        self.horizontal_layout_colorbar_scale = QHBoxLayout()
        self.horizontal_layout_colorbar_scale.setObjectName(u"horizontal_layout_colorbar_scale")
        self.label_static_scale = QLabel(self.verticalLayoutWidget)
        self.label_static_scale.setObjectName(u"label_static_scale")
        self.label_static_scale.setFont(font1)

        self.horizontal_layout_colorbar_scale.addWidget(self.label_static_scale)

        self.line_edit_dynamic_scale_low = QLineEdit(self.verticalLayoutWidget)
        self.line_edit_dynamic_scale_low.setObjectName(u"line_edit_dynamic_scale_low")
        self.line_edit_dynamic_scale_low.setFont(font1)

        self.horizontal_layout_colorbar_scale.addWidget(self.line_edit_dynamic_scale_low)

        self.line_edit_dynamic_scale_high = QLineEdit(self.verticalLayoutWidget)
        self.line_edit_dynamic_scale_high.setObjectName(u"line_edit_dynamic_scale_high")
        self.line_edit_dynamic_scale_high.setFont(font1)

        self.horizontal_layout_colorbar_scale.addWidget(self.line_edit_dynamic_scale_high)

        self.push_button_scale_1_99 = QPushButton(self.verticalLayoutWidget)
        self.push_button_scale_1_99.setObjectName(u"push_button_scale_1_99")
        self.push_button_scale_1_99.setFont(font1)

        self.horizontal_layout_colorbar_scale.addWidget(self.push_button_scale_1_99)

        self.check_box_autoscale_1_99 = QCheckBox(self.verticalLayoutWidget)
        self.check_box_autoscale_1_99.setObjectName(u"check_box_autoscale_1_99")
        self.check_box_autoscale_1_99.setFont(font1)

        self.horizontal_layout_colorbar_scale.addWidget(self.check_box_autoscale_1_99)


        self.vertical_layout_selector.addLayout(self.horizontal_layout_colorbar_scale)

        self.line = QFrame(self.verticalLayoutWidget)
        self.line.setObjectName(u"line")
        self.line.setFont(font)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.vertical_layout_selector.addWidget(self.line)

        self.horizontal_layout_target_pixel_entry = QHBoxLayout()
        self.horizontal_layout_target_pixel_entry.setObjectName(u"horizontal_layout_target_pixel_entry")
        self.label_static_target_x = QLabel(self.verticalLayoutWidget)
        self.label_static_target_x.setObjectName(u"label_static_target_x")
        self.label_static_target_x.setFont(font)

        self.horizontal_layout_target_pixel_entry.addWidget(self.label_static_target_x)

        self.line_edit_dynamic_target_x = QLineEdit(self.verticalLayoutWidget)
        self.line_edit_dynamic_target_x.setObjectName(u"line_edit_dynamic_target_x")
        self.line_edit_dynamic_target_x.setFont(font)

        self.horizontal_layout_target_pixel_entry.addWidget(self.line_edit_dynamic_target_x)

        self.label_static_target_y = QLabel(self.verticalLayoutWidget)
        self.label_static_target_y.setObjectName(u"label_static_target_y")
        self.label_static_target_y.setFont(font)

        self.horizontal_layout_target_pixel_entry.addWidget(self.label_static_target_y)

        self.line_edit_dynamic_target_y = QLineEdit(self.verticalLayoutWidget)
        self.line_edit_dynamic_target_y.setObjectName(u"line_edit_dynamic_target_y")
        self.line_edit_dynamic_target_y.setFont(font)

        self.horizontal_layout_target_pixel_entry.addWidget(self.line_edit_dynamic_target_y)

        self.push_button_submit_target = QPushButton(self.verticalLayoutWidget)
        self.push_button_submit_target.setObjectName(u"push_button_submit_target")
        self.push_button_submit_target.setFont(font)

        self.horizontal_layout_target_pixel_entry.addWidget(self.push_button_submit_target)


        self.vertical_layout_selector.addLayout(self.horizontal_layout_target_pixel_entry)


        self.retranslateUi(SelectorWindow)

        QMetaObject.connectSlotsByName(SelectorWindow)
    # setupUi

    def retranslateUi(self, SelectorWindow):
        SelectorWindow.setWindowTitle(QCoreApplication.translate("SelectorWindow", u"OpihiExarata Target Selector", None))
        self.label_dynamic_current_fits_filename.setText(QCoreApplication.translate("SelectorWindow", u"opi.20XXA999.YYMMDD.AAAAAAAAA.00001.a.fits", None))
        self.label_dynamic_reference_fits_filename.setText(QCoreApplication.translate("SelectorWindow", u"opi.20XXA999.YYMMDD.AAAAAAAAA.00001.b.fits", None))
        self.push_button_change_reference_filename.setText(QCoreApplication.translate("SelectorWindow", u"Change", None))
        self.label_static_current_fits_filename.setText(QCoreApplication.translate("SelectorWindow", u"Current:", None))
        self.label_static_reference_fits_filename.setText(QCoreApplication.translate("SelectorWindow", u"Reference:", None))
        self.dummy_selector_navbar.setText(QCoreApplication.translate("SelectorWindow", u"DUMMY NAVIGATION BAR", None))
        self.label_static_subtraction_mode.setText(QCoreApplication.translate("SelectorWindow", u"Subtraction Method", None))
        self.push_button_mode_none.setText(QCoreApplication.translate("SelectorWindow", u"None", None))
        self.push_button_mode_reference.setText(QCoreApplication.translate("SelectorWindow", u"Reference", None))
        self.push_button_mode_sidereal.setText(QCoreApplication.translate("SelectorWindow", u"Sidereal", None))
        self.push_button_mode_non_sidereal.setText(QCoreApplication.translate("SelectorWindow", u"Non-sidereal", None))
        self.label_static_scale.setText(QCoreApplication.translate("SelectorWindow", u"Scale [Low High]", None))
        self.push_button_scale_1_99.setText(QCoreApplication.translate("SelectorWindow", u"1 - 99 %", None))
        self.check_box_autoscale_1_99.setText(QCoreApplication.translate("SelectorWindow", u"Auto", None))
        self.label_static_target_x.setText(QCoreApplication.translate("SelectorWindow", u"Target X:", None))
        self.line_edit_dynamic_target_x.setText(QCoreApplication.translate("SelectorWindow", u"XXXX", None))
        self.label_static_target_y.setText(QCoreApplication.translate("SelectorWindow", u"Target Y:", None))
        self.line_edit_dynamic_target_y.setText(QCoreApplication.translate("SelectorWindow", u"YYYY", None))
        self.push_button_submit_target.setText(QCoreApplication.translate("SelectorWindow", u"Submit", None))
    # retranslateUi

