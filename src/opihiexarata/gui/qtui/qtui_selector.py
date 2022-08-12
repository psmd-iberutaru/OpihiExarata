# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'selector.ui'
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
    QFrame,
    QGraphicsView,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class Ui_SelectorWindow(object):
    def setupUi(self, SelectorWindow):
        if not SelectorWindow.objectName():
            SelectorWindow.setObjectName("SelectorWindow")
        SelectorWindow.resize(623, 868)
        self.verticalLayoutWidget = QWidget(SelectorWindow)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 10, 604, 846))
        font = QFont()
        font.setFamilies(["Sylfaen"])
        font.setPointSize(12)
        self.verticalLayoutWidget.setFont(font)
        self.vertical_layout_selector = QVBoxLayout(self.verticalLayoutWidget)
        self.vertical_layout_selector.setObjectName("vertical_layout_selector")
        self.vertical_layout_selector.setContentsMargins(0, 0, 0, 0)
        self.grid_layout_file_selection = QGridLayout()
        self.grid_layout_file_selection.setObjectName("grid_layout_file_selection")
        self.label_dynamic_current_fits_filename = QLabel(self.verticalLayoutWidget)
        self.label_dynamic_current_fits_filename.setObjectName(
            "label_dynamic_current_fits_filename"
        )
        self.label_dynamic_current_fits_filename.setMinimumSize(QSize(400, 0))

        self.grid_layout_file_selection.addWidget(
            self.label_dynamic_current_fits_filename, 0, 1, 1, 1
        )

        self.label_dynamic_reference_fits_filename = QLabel(self.verticalLayoutWidget)
        self.label_dynamic_reference_fits_filename.setObjectName(
            "label_dynamic_reference_fits_filename"
        )
        self.label_dynamic_reference_fits_filename.setMinimumSize(QSize(400, 0))

        self.grid_layout_file_selection.addWidget(
            self.label_dynamic_reference_fits_filename, 1, 1, 1, 1
        )

        self.push_button_change_reference_filename = QPushButton(
            self.verticalLayoutWidget
        )
        self.push_button_change_reference_filename.setObjectName(
            "push_button_change_reference_filename"
        )

        self.grid_layout_file_selection.addWidget(
            self.push_button_change_reference_filename, 1, 2, 1, 1
        )

        self.label_static_current_fits_filename = QLabel(self.verticalLayoutWidget)
        self.label_static_current_fits_filename.setObjectName(
            "label_static_current_fits_filename"
        )

        self.grid_layout_file_selection.addWidget(
            self.label_static_current_fits_filename, 0, 0, 1, 1
        )

        self.label_static_reference_fits_filename = QLabel(self.verticalLayoutWidget)
        self.label_static_reference_fits_filename.setObjectName(
            "label_static_reference_fits_filename"
        )

        self.grid_layout_file_selection.addWidget(
            self.label_static_reference_fits_filename, 1, 0, 1, 1
        )

        self.vertical_layout_selector.addLayout(self.grid_layout_file_selection)

        self.line_2 = QFrame(self.verticalLayoutWidget)
        self.line_2.setObjectName("line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.vertical_layout_selector.addWidget(self.line_2)

        self.vertical_layout_image = QVBoxLayout()
        self.vertical_layout_image.setObjectName("vertical_layout_image")
        self.dummy_selector_image = QGraphicsView(self.verticalLayoutWidget)
        self.dummy_selector_image.setObjectName("dummy_selector_image")
        self.dummy_selector_image.setMinimumSize(QSize(600, 600))
        self.dummy_selector_image.setMaximumSize(QSize(600, 600))

        self.vertical_layout_image.addWidget(self.dummy_selector_image)

        self.dummy_selector_navbar = QLabel(self.verticalLayoutWidget)
        self.dummy_selector_navbar.setObjectName("dummy_selector_navbar")
        self.dummy_selector_navbar.setMinimumSize(QSize(0, 30))
        self.dummy_selector_navbar.setAlignment(Qt.AlignCenter)

        self.vertical_layout_image.addWidget(self.dummy_selector_navbar)

        self.vertical_layout_selector.addLayout(self.vertical_layout_image)

        self.horizonta_layout_subtraction_mode = QHBoxLayout()
        self.horizonta_layout_subtraction_mode.setObjectName(
            "horizonta_layout_subtraction_mode"
        )
        self.label_static_subtraction_mode = QLabel(self.verticalLayoutWidget)
        self.label_static_subtraction_mode.setObjectName(
            "label_static_subtraction_mode"
        )

        self.horizonta_layout_subtraction_mode.addWidget(
            self.label_static_subtraction_mode
        )

        self.line_3 = QFrame(self.verticalLayoutWidget)
        self.line_3.setObjectName("line_3")
        self.line_3.setFrameShape(QFrame.VLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.horizonta_layout_subtraction_mode.addWidget(self.line_3)

        self.push_button_mode_none = QPushButton(self.verticalLayoutWidget)
        self.push_button_mode_none.setObjectName("push_button_mode_none")

        self.horizonta_layout_subtraction_mode.addWidget(self.push_button_mode_none)

        self.push_button_mode_reference = QPushButton(self.verticalLayoutWidget)
        self.push_button_mode_reference.setObjectName("push_button_mode_reference")

        self.horizonta_layout_subtraction_mode.addWidget(
            self.push_button_mode_reference
        )

        self.push_button_mode_sidereal = QPushButton(self.verticalLayoutWidget)
        self.push_button_mode_sidereal.setObjectName("push_button_mode_sidereal")

        self.horizonta_layout_subtraction_mode.addWidget(self.push_button_mode_sidereal)

        self.push_button_mode_non_sidereal = QPushButton(self.verticalLayoutWidget)
        self.push_button_mode_non_sidereal.setObjectName(
            "push_button_mode_non_sidereal"
        )

        self.horizonta_layout_subtraction_mode.addWidget(
            self.push_button_mode_non_sidereal
        )

        self.vertical_layout_selector.addLayout(self.horizonta_layout_subtraction_mode)

        self.horizontal_layout_colorbar_scale = QHBoxLayout()
        self.horizontal_layout_colorbar_scale.setObjectName(
            "horizontal_layout_colorbar_scale"
        )
        self.label_static_scale = QLabel(self.verticalLayoutWidget)
        self.label_static_scale.setObjectName("label_static_scale")

        self.horizontal_layout_colorbar_scale.addWidget(self.label_static_scale)

        self.line_edit_dynamic_scale_low = QLineEdit(self.verticalLayoutWidget)
        self.line_edit_dynamic_scale_low.setObjectName("line_edit_dynamic_scale_low")

        self.horizontal_layout_colorbar_scale.addWidget(
            self.line_edit_dynamic_scale_low
        )

        self.line_edit_dynamic_scale_high = QLineEdit(self.verticalLayoutWidget)
        self.line_edit_dynamic_scale_high.setObjectName("line_edit_dynamic_scale_high")

        self.horizontal_layout_colorbar_scale.addWidget(
            self.line_edit_dynamic_scale_high
        )

        self.push_button_scale_1_99 = QPushButton(self.verticalLayoutWidget)
        self.push_button_scale_1_99.setObjectName("push_button_scale_1_99")

        self.horizontal_layout_colorbar_scale.addWidget(self.push_button_scale_1_99)

        self.check_box_autoscale_1_99 = QCheckBox(self.verticalLayoutWidget)
        self.check_box_autoscale_1_99.setObjectName("check_box_autoscale_1_99")

        self.horizontal_layout_colorbar_scale.addWidget(self.check_box_autoscale_1_99)

        self.vertical_layout_selector.addLayout(self.horizontal_layout_colorbar_scale)

        self.line = QFrame(self.verticalLayoutWidget)
        self.line.setObjectName("line")
        self.line.setFont(font)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.vertical_layout_selector.addWidget(self.line)

        self.horizontal_layout_target_pixel_entry = QHBoxLayout()
        self.horizontal_layout_target_pixel_entry.setObjectName(
            "horizontal_layout_target_pixel_entry"
        )
        self.label_static_target_x = QLabel(self.verticalLayoutWidget)
        self.label_static_target_x.setObjectName("label_static_target_x")
        self.label_static_target_x.setFont(font)

        self.horizontal_layout_target_pixel_entry.addWidget(self.label_static_target_x)

        self.line_edit_dynamic_target_x = QLineEdit(self.verticalLayoutWidget)
        self.line_edit_dynamic_target_x.setObjectName("line_edit_dynamic_target_x")
        self.line_edit_dynamic_target_x.setFont(font)

        self.horizontal_layout_target_pixel_entry.addWidget(
            self.line_edit_dynamic_target_x
        )

        self.label_static_target_y = QLabel(self.verticalLayoutWidget)
        self.label_static_target_y.setObjectName("label_static_target_y")
        self.label_static_target_y.setFont(font)

        self.horizontal_layout_target_pixel_entry.addWidget(self.label_static_target_y)

        self.line_edit_dynamic_target_y = QLineEdit(self.verticalLayoutWidget)
        self.line_edit_dynamic_target_y.setObjectName("line_edit_dynamic_target_y")
        self.line_edit_dynamic_target_y.setFont(font)

        self.horizontal_layout_target_pixel_entry.addWidget(
            self.line_edit_dynamic_target_y
        )

        self.push_button_submit_target = QPushButton(self.verticalLayoutWidget)
        self.push_button_submit_target.setObjectName("push_button_submit_target")
        self.push_button_submit_target.setFont(font)

        self.horizontal_layout_target_pixel_entry.addWidget(
            self.push_button_submit_target
        )

        self.vertical_layout_selector.addLayout(
            self.horizontal_layout_target_pixel_entry
        )

        self.retranslateUi(SelectorWindow)

        QMetaObject.connectSlotsByName(SelectorWindow)

    # setupUi

    def retranslateUi(self, SelectorWindow):
        SelectorWindow.setWindowTitle(
            QCoreApplication.translate(
                "SelectorWindow", "OpihiExarata Target Selector", None
            )
        )
        self.label_dynamic_current_fits_filename.setText(
            QCoreApplication.translate(
                "SelectorWindow", "opi.20XXA999.YYMMDD.AAAAAAAAA.00001.a.fits", None
            )
        )
        self.label_dynamic_reference_fits_filename.setText(
            QCoreApplication.translate(
                "SelectorWindow", "opi.20XXA999.YYMMDD.AAAAAAAAA.00001.b.fits", None
            )
        )
        self.push_button_change_reference_filename.setText(
            QCoreApplication.translate("SelectorWindow", "Change", None)
        )
        self.label_static_current_fits_filename.setText(
            QCoreApplication.translate("SelectorWindow", "Current:", None)
        )
        self.label_static_reference_fits_filename.setText(
            QCoreApplication.translate("SelectorWindow", "Reference:", None)
        )
        self.dummy_selector_navbar.setText(
            QCoreApplication.translate("SelectorWindow", "DUMMY NAVIGATION BAR", None)
        )
        self.label_static_subtraction_mode.setText(
            QCoreApplication.translate("SelectorWindow", "Subtraction Method", None)
        )
        self.push_button_mode_none.setText(
            QCoreApplication.translate("SelectorWindow", "None", None)
        )
        self.push_button_mode_reference.setText(
            QCoreApplication.translate("SelectorWindow", "Reference", None)
        )
        self.push_button_mode_sidereal.setText(
            QCoreApplication.translate("SelectorWindow", "Sidereal", None)
        )
        self.push_button_mode_non_sidereal.setText(
            QCoreApplication.translate("SelectorWindow", "Non-sidereal", None)
        )
        self.label_static_scale.setText(
            QCoreApplication.translate("SelectorWindow", "Scale [Low High]", None)
        )
        self.push_button_scale_1_99.setText(
            QCoreApplication.translate("SelectorWindow", "1 - 99 %", None)
        )
        self.check_box_autoscale_1_99.setText(
            QCoreApplication.translate("SelectorWindow", "Auto", None)
        )
        self.label_static_target_x.setText(
            QCoreApplication.translate("SelectorWindow", "Target X:", None)
        )
        self.line_edit_dynamic_target_x.setText(
            QCoreApplication.translate("SelectorWindow", "XXXX", None)
        )
        self.label_static_target_y.setText(
            QCoreApplication.translate("SelectorWindow", "Target Y:", None)
        )
        self.line_edit_dynamic_target_y.setText(
            QCoreApplication.translate("SelectorWindow", "YYYY", None)
        )
        self.push_button_submit_target.setText(
            QCoreApplication.translate("SelectorWindow", "Submit", None)
        )

    # retranslateUi
