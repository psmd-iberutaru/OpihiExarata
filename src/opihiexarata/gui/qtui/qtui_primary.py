# Form implementation generated from reading ui file '.\primary.ui'
#
# Created by: PyQt6 UI code generator 6.3.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_PrimaryWindow(object):
    def setupUi(self, PrimaryWindow):
        PrimaryWindow.setObjectName("PrimaryWindow")
        PrimaryWindow.resize(628, 884)
        font = QtGui.QFont()
        font.setFamily("Sylfaen")
        font.setPointSize(11)
        PrimaryWindow.setFont(font)
        PrimaryWindow.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        PrimaryWindow.setWindowOpacity(1.0)
        self.centralwidget = QtWidgets.QWidget(PrimaryWindow)
        self.centralwidget.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(10, 10, 601, 821))
        font = QtGui.QFont()
        font.setFamily("Sylfaen")
        font.setPointSize(11)
        self.verticalLayoutWidget_3.setFont(font)
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.vertical_layout_window = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.vertical_layout_window.setContentsMargins(0, 0, 0, 0)
        self.vertical_layout_window.setObjectName("vertical_layout_window")
        self.horizontal_layout_new_files = QtWidgets.QHBoxLayout()
        self.horizontal_layout_new_files.setObjectName("horizontal_layout_new_files")
        self.push_button_new_image_automatic = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        font = QtGui.QFont()
        font.setFamily("Sylfaen")
        font.setPointSize(11)
        self.push_button_new_image_automatic.setFont(font)
        self.push_button_new_image_automatic.setObjectName("push_button_new_image_automatic")
        self.horizontal_layout_new_files.addWidget(self.push_button_new_image_automatic)
        self.push_button_new_image_manual = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        font = QtGui.QFont()
        font.setFamily("Sylfaen")
        font.setPointSize(11)
        self.push_button_new_image_manual.setFont(font)
        self.push_button_new_image_manual.setObjectName("push_button_new_image_manual")
        self.horizontal_layout_new_files.addWidget(self.push_button_new_image_manual)
        self.line = QtWidgets.QFrame(self.verticalLayoutWidget_3)
        font = QtGui.QFont()
        font.setFamily("Sylfaen")
        font.setPointSize(11)
        self.line.setFont(font)
        self.line.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.horizontal_layout_new_files.addWidget(self.line)
        self.push_button_new_object = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        font = QtGui.QFont()
        font.setFamily("Sylfaen")
        font.setPointSize(11)
        self.push_button_new_object.setFont(font)
        self.push_button_new_object.setObjectName("push_button_new_object")
        self.horizontal_layout_new_files.addWidget(self.push_button_new_object)
        self.vertical_layout_window.addLayout(self.horizontal_layout_new_files)
        self.line_file_image = QtWidgets.QFrame(self.verticalLayoutWidget_3)
        font = QtGui.QFont()
        font.setFamily("Sylfaen")
        font.setPointSize(11)
        self.line_file_image.setFont(font)
        self.line_file_image.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_file_image.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_file_image.setObjectName("line_file_image")
        self.vertical_layout_window.addWidget(self.line_file_image)
        self.dummy_opihi_image = QtWidgets.QGraphicsView(self.verticalLayoutWidget_3)
        self.dummy_opihi_image.setMinimumSize(QtCore.QSize(400, 400))
        self.dummy_opihi_image.setMaximumSize(QtCore.QSize(400, 400))
        font = QtGui.QFont()
        font.setFamily("Sylfaen")
        font.setPointSize(11)
        self.dummy_opihi_image.setFont(font)
        self.dummy_opihi_image.setObjectName("dummy_opihi_image")
        self.vertical_layout_window.addWidget(self.dummy_opihi_image, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.vertical_layout_image = QtWidgets.QVBoxLayout()
        self.vertical_layout_image.setObjectName("vertical_layout_image")
        self.vertical_layout_window.addLayout(self.vertical_layout_image)
        self.line_image_solution = QtWidgets.QFrame(self.verticalLayoutWidget_3)
        font = QtGui.QFont()
        font.setFamily("Sylfaen")
        font.setPointSize(11)
        self.line_image_solution.setFont(font)
        self.line_image_solution.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_image_solution.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_image_solution.setObjectName("line_image_solution")
        self.vertical_layout_window.addWidget(self.line_image_solution)
        self.vertical_layout_solutions = QtWidgets.QVBoxLayout()
        self.vertical_layout_solutions.setObjectName("vertical_layout_solutions")
        self.tabs_solutions = QtWidgets.QTabWidget(self.verticalLayoutWidget_3)
        font = QtGui.QFont()
        font.setFamily("Sylfaen")
        font.setPointSize(11)
        self.tabs_solutions.setFont(font)
        self.tabs_solutions.setIconSize(QtCore.QSize(16, 16))
        self.tabs_solutions.setObjectName("tabs_solutions")
        self.tab_astrometry = QtWidgets.QWidget()
        self.tab_astrometry.setObjectName("tab_astrometry")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.tab_astrometry)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 571, 181))
        font = QtGui.QFont()
        font.setFamily("Sylfaen")
        font.setPointSize(11)
        self.verticalLayoutWidget.setFont(font)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.vertical_layout_astrometry = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.vertical_layout_astrometry.setContentsMargins(0, 0, 0, 0)
        self.vertical_layout_astrometry.setObjectName("vertical_layout_astrometry")
        self.horizontal_layout_solve_astrometry = QtWidgets.QHBoxLayout()
        self.horizontal_layout_solve_astrometry.setObjectName("horizontal_layout_solve_astrometry")
        self.push_button_solve_astrometry = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Sylfaen")
        font.setPointSize(11)
        self.push_button_solve_astrometry.setFont(font)
        self.push_button_solve_astrometry.setObjectName("push_button_solve_astrometry")
        self.horizontal_layout_solve_astrometry.addWidget(self.push_button_solve_astrometry)
        self.vertical_layout_astrometry.addLayout(self.horizontal_layout_solve_astrometry)
        self.line_2 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_2.setObjectName("line_2")
        self.vertical_layout_astrometry.addWidget(self.line_2)
        self.grid_layout_astrometry_results = QtWidgets.QGridLayout()
        self.grid_layout_astrometry_results.setObjectName("grid_layout_astrometry_results")
        self.label_dynamic_target_x = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_dynamic_target_x.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_dynamic_target_x.setObjectName("label_dynamic_target_x")
        self.grid_layout_astrometry_results.addWidget(self.label_dynamic_target_x, 1, 2, 1, 1)
        self.label_dynamic_target_y = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_dynamic_target_y.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_dynamic_target_y.setObjectName("label_dynamic_target_y")
        self.grid_layout_astrometry_results.addWidget(self.label_dynamic_target_y, 1, 3, 1, 1)
        self.label_static_target_coordinates = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_static_target_coordinates.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_static_target_coordinates.setObjectName("label_static_target_coordinates")
        self.grid_layout_astrometry_results.addWidget(self.label_static_target_coordinates, 1, 0, 1, 1)
        self.line_9 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_9.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_9.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_9.setObjectName("line_9")
        self.grid_layout_astrometry_results.addWidget(self.line_9, 0, 5, 3, 1)
        self.label_dynamic_center_ra = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_dynamic_center_ra.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_dynamic_center_ra.setObjectName("label_dynamic_center_ra")
        self.grid_layout_astrometry_results.addWidget(self.label_dynamic_center_ra, 0, 6, 1, 1)
        self.label_static_center_coordinates = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_static_center_coordinates.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_static_center_coordinates.setObjectName("label_static_center_coordinates")
        self.grid_layout_astrometry_results.addWidget(self.label_static_center_coordinates, 0, 0, 1, 1)
        self.label_dynamic_center_dec = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_dynamic_center_dec.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_dynamic_center_dec.setObjectName("label_dynamic_center_dec")
        self.grid_layout_astrometry_results.addWidget(self.label_dynamic_center_dec, 0, 7, 1, 1)
        self.label_dynamic_target_ra = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_dynamic_target_ra.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_dynamic_target_ra.setObjectName("label_dynamic_target_ra")
        self.grid_layout_astrometry_results.addWidget(self.label_dynamic_target_ra, 1, 6, 1, 1)
        self.label_dynamic_target_dec = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_dynamic_target_dec.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_dynamic_target_dec.setObjectName("label_dynamic_target_dec")
        self.grid_layout_astrometry_results.addWidget(self.label_dynamic_target_dec, 1, 7, 1, 1)
        self.label_dynamic_center_y = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_dynamic_center_y.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_dynamic_center_y.setObjectName("label_dynamic_center_y")
        self.grid_layout_astrometry_results.addWidget(self.label_dynamic_center_y, 0, 3, 1, 1)
        self.label_dynamic_center_x = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_dynamic_center_x.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_dynamic_center_x.setObjectName("label_dynamic_center_x")
        self.grid_layout_astrometry_results.addWidget(self.label_dynamic_center_x, 0, 2, 1, 1)
        self.line_8 = QtWidgets.QFrame(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line_8.sizePolicy().hasHeightForWidth())
        self.line_8.setSizePolicy(sizePolicy)
        self.line_8.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_8.setObjectName("line_8")
        self.grid_layout_astrometry_results.addWidget(self.line_8, 0, 1, 3, 1)
        self.line_edit_custom_x = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.line_edit_custom_x.setObjectName("line_edit_custom_x")
        self.grid_layout_astrometry_results.addWidget(self.line_edit_custom_x, 2, 2, 1, 1)
        self.line_edit_custom_y = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.line_edit_custom_y.setObjectName("line_edit_custom_y")
        self.grid_layout_astrometry_results.addWidget(self.line_edit_custom_y, 2, 3, 1, 1)
        self.line_edit_custom_ra = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.line_edit_custom_ra.setObjectName("line_edit_custom_ra")
        self.grid_layout_astrometry_results.addWidget(self.line_edit_custom_ra, 2, 6, 1, 1)
        self.line_edit_dec = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.line_edit_dec.setObjectName("line_edit_dec")
        self.grid_layout_astrometry_results.addWidget(self.line_edit_dec, 2, 7, 1, 1)
        self.push_button_custom_astrometry_solve = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.push_button_custom_astrometry_solve.setObjectName("push_button_custom_astrometry_solve")
        self.grid_layout_astrometry_results.addWidget(self.push_button_custom_astrometry_solve, 2, 0, 1, 1)
        self.vertical_layout_astrometry.addLayout(self.grid_layout_astrometry_results)
        self.tabs_solutions.addTab(self.tab_astrometry, "")
        self.tab_photometry = QtWidgets.QWidget()
        self.tab_photometry.setObjectName("tab_photometry")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.tab_photometry)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(10, 10, 701, 251))
        font = QtGui.QFont()
        font.setFamily("Sylfaen")
        font.setPointSize(11)
        self.verticalLayoutWidget_2.setFont(font)
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.vertical_layout_photometry = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.vertical_layout_photometry.setContentsMargins(0, 0, 0, 0)
        self.vertical_layout_photometry.setObjectName("vertical_layout_photometry")
        self.horizontal_layout_solve_photometry = QtWidgets.QHBoxLayout()
        self.horizontal_layout_solve_photometry.setObjectName("horizontal_layout_solve_photometry")
        self.push_button_solve_photometry = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Sylfaen")
        font.setPointSize(11)
        self.push_button_solve_photometry.setFont(font)
        self.push_button_solve_photometry.setObjectName("push_button_solve_photometry")
        self.horizontal_layout_solve_photometry.addWidget(self.push_button_solve_photometry)
        self.vertical_layout_photometry.addLayout(self.horizontal_layout_solve_photometry)
        self.line_3 = QtWidgets.QFrame(self.verticalLayoutWidget_2)
        self.line_3.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_3.setObjectName("line_3")
        self.vertical_layout_photometry.addWidget(self.line_3)
        self.horizonta_layout_photometry_results = QtWidgets.QHBoxLayout()
        self.horizonta_layout_photometry_results.setObjectName("horizonta_layout_photometry_results")
        self.vertical_layout_photometry.addLayout(self.horizonta_layout_photometry_results)
        self.tabs_solutions.addTab(self.tab_photometry, "")
        self.tab_propagate = QtWidgets.QWidget()
        self.tab_propagate.setObjectName("tab_propagate")
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.tab_propagate)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(10, 10, 701, 251))
        font = QtGui.QFont()
        font.setFamily("Sylfaen")
        font.setPointSize(11)
        self.verticalLayoutWidget_4.setFont(font)
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.vertical_layout_propagate = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.vertical_layout_propagate.setContentsMargins(0, 0, 0, 0)
        self.vertical_layout_propagate.setObjectName("vertical_layout_propagate")
        self.horizontal_layout_solve_photometry_2 = QtWidgets.QHBoxLayout()
        self.horizontal_layout_solve_photometry_2.setObjectName("horizontal_layout_solve_photometry_2")
        self.push_button_solve_propagation = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        font = QtGui.QFont()
        font.setFamily("Sylfaen")
        font.setPointSize(11)
        self.push_button_solve_propagation.setFont(font)
        self.push_button_solve_propagation.setObjectName("push_button_solve_propagation")
        self.horizontal_layout_solve_photometry_2.addWidget(self.push_button_solve_propagation)
        self.vertical_layout_propagate.addLayout(self.horizontal_layout_solve_photometry_2)
        self.line_4 = QtWidgets.QFrame(self.verticalLayoutWidget_4)
        self.line_4.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_4.setObjectName("line_4")
        self.vertical_layout_propagate.addWidget(self.line_4)
        self.horizontal_layout_propagate_results = QtWidgets.QHBoxLayout()
        self.horizontal_layout_propagate_results.setObjectName("horizontal_layout_propagate_results")
        self.vertical_layout_propagate.addLayout(self.horizontal_layout_propagate_results)
        self.tabs_solutions.addTab(self.tab_propagate, "")
        self.tab_orbit = QtWidgets.QWidget()
        self.tab_orbit.setObjectName("tab_orbit")
        self.verticalLayoutWidget_5 = QtWidgets.QWidget(self.tab_orbit)
        self.verticalLayoutWidget_5.setGeometry(QtCore.QRect(10, 10, 701, 251))
        font = QtGui.QFont()
        font.setFamily("Sylfaen")
        font.setPointSize(11)
        self.verticalLayoutWidget_5.setFont(font)
        self.verticalLayoutWidget_5.setObjectName("verticalLayoutWidget_5")
        self.vertical_layout_orbit = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_5)
        self.vertical_layout_orbit.setContentsMargins(0, 0, 0, 0)
        self.vertical_layout_orbit.setObjectName("vertical_layout_orbit")
        self.horizontal_layout_solve_orbit = QtWidgets.QHBoxLayout()
        self.horizontal_layout_solve_orbit.setObjectName("horizontal_layout_solve_orbit")
        self.push_button_solve_orbit = QtWidgets.QPushButton(self.verticalLayoutWidget_5)
        font = QtGui.QFont()
        font.setFamily("Sylfaen")
        font.setPointSize(11)
        self.push_button_solve_orbit.setFont(font)
        self.push_button_solve_orbit.setObjectName("push_button_solve_orbit")
        self.horizontal_layout_solve_orbit.addWidget(self.push_button_solve_orbit)
        self.vertical_layout_orbit.addLayout(self.horizontal_layout_solve_orbit)
        self.line_5 = QtWidgets.QFrame(self.verticalLayoutWidget_5)
        self.line_5.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_5.setObjectName("line_5")
        self.vertical_layout_orbit.addWidget(self.line_5)
        self.horizontal_layout_orbit_results = QtWidgets.QHBoxLayout()
        self.horizontal_layout_orbit_results.setObjectName("horizontal_layout_orbit_results")
        self.vertical_layout_orbit.addLayout(self.horizontal_layout_orbit_results)
        self.tabs_solutions.addTab(self.tab_orbit, "")
        self.tab_ephemeris = QtWidgets.QWidget()
        self.tab_ephemeris.setObjectName("tab_ephemeris")
        self.verticalLayoutWidget_6 = QtWidgets.QWidget(self.tab_ephemeris)
        self.verticalLayoutWidget_6.setGeometry(QtCore.QRect(10, 10, 701, 251))
        font = QtGui.QFont()
        font.setFamily("Sylfaen")
        font.setPointSize(11)
        self.verticalLayoutWidget_6.setFont(font)
        self.verticalLayoutWidget_6.setObjectName("verticalLayoutWidget_6")
        self.vertical_layout_ephemeris = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_6)
        self.vertical_layout_ephemeris.setContentsMargins(0, 0, 0, 0)
        self.vertical_layout_ephemeris.setObjectName("vertical_layout_ephemeris")
        self.horizontal_layout_solve_ephemeris = QtWidgets.QHBoxLayout()
        self.horizontal_layout_solve_ephemeris.setObjectName("horizontal_layout_solve_ephemeris")
        self.push_button_solve_ephemeris = QtWidgets.QPushButton(self.verticalLayoutWidget_6)
        font = QtGui.QFont()
        font.setFamily("Sylfaen")
        font.setPointSize(11)
        self.push_button_solve_ephemeris.setFont(font)
        self.push_button_solve_ephemeris.setObjectName("push_button_solve_ephemeris")
        self.horizontal_layout_solve_ephemeris.addWidget(self.push_button_solve_ephemeris)
        self.vertical_layout_ephemeris.addLayout(self.horizontal_layout_solve_ephemeris)
        self.line_6 = QtWidgets.QFrame(self.verticalLayoutWidget_6)
        self.line_6.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_6.setObjectName("line_6")
        self.vertical_layout_ephemeris.addWidget(self.line_6)
        self.horizontal_layout_ephemeris_results = QtWidgets.QHBoxLayout()
        self.horizontal_layout_ephemeris_results.setObjectName("horizontal_layout_ephemeris_results")
        self.vertical_layout_ephemeris.addLayout(self.horizontal_layout_ephemeris_results)
        self.tabs_solutions.addTab(self.tab_ephemeris, "")
        self.vertical_layout_solutions.addWidget(self.tabs_solutions)
        self.vertical_layout_window.addLayout(self.vertical_layout_solutions)
        PrimaryWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(PrimaryWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 628, 21))
        self.menubar.setObjectName("menubar")
        PrimaryWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(PrimaryWindow)
        self.statusbar.setObjectName("statusbar")
        PrimaryWindow.setStatusBar(self.statusbar)

        self.retranslateUi(PrimaryWindow)
        self.tabs_solutions.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(PrimaryWindow)

    def retranslateUi(self, PrimaryWindow):
        _translate = QtCore.QCoreApplication.translate
        PrimaryWindow.setWindowTitle(_translate("PrimaryWindow", "OpihiExarata"))
        self.push_button_new_image_automatic.setText(_translate("PrimaryWindow", "Automatic New Image"))
        self.push_button_new_image_manual.setText(_translate("PrimaryWindow", "Manual New Image"))
        self.push_button_new_object.setText(_translate("PrimaryWindow", "New Target"))
        self.push_button_solve_astrometry.setText(_translate("PrimaryWindow", "Solve Astrometry"))
        self.label_dynamic_target_x.setText(_translate("PrimaryWindow", "0000"))
        self.label_dynamic_target_y.setText(_translate("PrimaryWindow", "0000"))
        self.label_static_target_coordinates.setText(_translate("PrimaryWindow", "Target/Asteroid:"))
        self.label_dynamic_center_ra.setText(_translate("PrimaryWindow", "HH:MM:SS"))
        self.label_static_center_coordinates.setText(_translate("PrimaryWindow", "Opihi Center:"))
        self.label_dynamic_center_dec.setText(_translate("PrimaryWindow", "DD:MM:SS"))
        self.label_dynamic_target_ra.setText(_translate("PrimaryWindow", "HH:MM:SS"))
        self.label_dynamic_target_dec.setText(_translate("PrimaryWindow", "DD:MM:SS"))
        self.label_dynamic_center_y.setText(_translate("PrimaryWindow", "0000"))
        self.label_dynamic_center_x.setText(_translate("PrimaryWindow", "0000"))
        self.push_button_custom_astrometry_solve.setText(_translate("PrimaryWindow", "Custom Solve"))
        self.tabs_solutions.setTabText(self.tabs_solutions.indexOf(self.tab_astrometry), _translate("PrimaryWindow", "Astrometry"))
        self.push_button_solve_photometry.setText(_translate("PrimaryWindow", "Solve Photometry"))
        self.tabs_solutions.setTabText(self.tabs_solutions.indexOf(self.tab_photometry), _translate("PrimaryWindow", "Photometry"))
        self.push_button_solve_propagation.setText(_translate("PrimaryWindow", "Solve Propagation"))
        self.tabs_solutions.setTabText(self.tabs_solutions.indexOf(self.tab_propagate), _translate("PrimaryWindow", "Propagate"))
        self.push_button_solve_orbit.setText(_translate("PrimaryWindow", "Solve Orbit"))
        self.tabs_solutions.setTabText(self.tabs_solutions.indexOf(self.tab_orbit), _translate("PrimaryWindow", "Orbit"))
        self.push_button_solve_ephemeris.setText(_translate("PrimaryWindow", "Solve Ephemeris"))
        self.tabs_solutions.setTabText(self.tabs_solutions.indexOf(self.tab_ephemeris), _translate("PrimaryWindow", "Ephemeris"))
