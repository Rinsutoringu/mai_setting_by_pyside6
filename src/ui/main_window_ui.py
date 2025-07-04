# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QComboBox,
    QDialogButtonBox, QGroupBox, QLabel, QLineEdit,
    QPushButton, QRadioButton, QSizePolicy, QTabWidget,
    QTextBrowser, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(683, 375)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QSize(683, 375))
        Form.setMaximumSize(QSize(683, 375))
        Form.setSizeIncrement(QSize(750, 650))
        Form.setBaseSize(QSize(750, 650))
        self.dialog_button = QDialogButtonBox(Form)
        self.dialog_button.setObjectName(u"dialog_button")
        self.dialog_button.setGeometry(QRect(510, 333, 156, 31))
        self.dialog_button.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        self.dialog_button.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.tabWidget = QTabWidget(Form)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(10, 90, 451, 231))
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.label = QLabel(self.tab)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, -10, 231, 50))
        font = QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.textBrowser = QTextBrowser(self.tab)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setEnabled(True)
        self.textBrowser.setGeometry(QRect(15, 30, 241, 130))
        self.textBrowser.setMouseTracking(True)
        self.textBrowser.setTabletTracking(False)
        self.textBrowser.setTabChangesFocus(True)
        self.textBrowser.setReadOnly(True)
        self.textBrowser.setOverwriteMode(True)
        self.textBrowser.setOpenExternalLinks(False)
        self.textBrowser.setOpenLinks(False)
        self.groupBox_6 = QGroupBox(self.tab)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.groupBox_6.setGeometry(QRect(270, 10, 171, 171))
        self.verticalLayoutWidget = QWidget(self.groupBox_6)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 20, 151, 141))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.port_setting = QPushButton(self.verticalLayoutWidget)
        self.port_setting.setObjectName(u"port_setting")

        self.verticalLayout_2.addWidget(self.port_setting)

        self.Sensitivity = QPushButton(self.verticalLayoutWidget)
        self.Sensitivity.setObjectName(u"Sensitivity")

        self.verticalLayout_2.addWidget(self.Sensitivity)

        self.pushButton_1_3 = QPushButton(self.verticalLayoutWidget)
        self.pushButton_1_3.setObjectName(u"pushButton_1_3")

        self.verticalLayout_2.addWidget(self.pushButton_1_3)

        self.lineEdit = QLineEdit(self.tab)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(20, 170, 191, 21))
        self.pushButton = QPushButton(self.tab)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(210, 163, 41, 31))
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.groupBox_7 = QGroupBox(self.tab_2)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.groupBox_7.setGeometry(QRect(20, 10, 411, 171))
        self.radioButton = QRadioButton(self.groupBox_7)
        self.radioButton.setObjectName(u"radioButton")
        self.radioButton.setGeometry(QRect(20, 70, 92, 20))
        self.radioButton.setChecked(True)
        self.radioButton_2 = QRadioButton(self.groupBox_7)
        self.radioButton_2.setObjectName(u"radioButton_2")
        self.radioButton_2.setGeometry(QRect(20, 100, 92, 20))
        self.radioButton_2.setAcceptDrops(False)
        self.label_5 = QLabel(self.groupBox_7)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(30, 40, 71, 16))
        self.tabWidget.addTab(self.tab_2, "")
        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(0, 10, 691, 81))
        self.label_3.setFont(font)
        self.groupBox_5 = QGroupBox(Form)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.groupBox_5.setGeometry(QRect(490, 110, 161, 201))
        self.device_selector = QComboBox(self.groupBox_5)
        self.device_selector.addItem("")
        self.device_selector.setObjectName(u"device_selector")
        self.device_selector.setGeometry(QRect(10, 30, 141, 31))
        self.reconfirm_button = QPushButton(self.groupBox_5)
        self.reconfirm_button.setObjectName(u"reconfirm_button")
        self.reconfirm_button.setGeometry(QRect(40, 170, 81, 21))
        self.checkadmin = QCheckBox(self.groupBox_5)
        self.checkadmin.setObjectName(u"checkadmin")
        self.checkadmin.setEnabled(False)
        self.checkadmin.setGeometry(QRect(20, 74, 121, 20))
        self.checkadmin.setCheckable(True)
        self.checkdevice = QCheckBox(self.groupBox_5)
        self.checkdevice.setObjectName(u"checkdevice")
        self.checkdevice.setEnabled(False)
        self.checkdevice.setGeometry(QRect(20, 94, 121, 20))
        self.checklink = QCheckBox(self.groupBox_5)
        self.checklink.setObjectName(u"checklink")
        self.checklink.setEnabled(False)
        self.checklink.setGeometry(QRect(20, 114, 121, 20))
        self.checkhandshake = QCheckBox(self.groupBox_5)
        self.checkhandshake.setObjectName(u"checkhandshake")
        self.checkhandshake.setEnabled(False)
        self.checkhandshake.setGeometry(QRect(20, 134, 121, 20))
        self.label_8 = QLabel(self.groupBox_5)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(50, 74, 91, 21))
        self.label_9 = QLabel(self.groupBox_5)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(50, 94, 91, 21))
        self.label_10 = QLabel(self.groupBox_5)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(50, 114, 91, 21))
        self.label_11 = QLabel(self.groupBox_5)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(50, 134, 91, 21))
        self.admin_button = QPushButton(Form)
        self.admin_button.setObjectName(u"admin_button")
        self.admin_button.setGeometry(QRect(30, 330, 136, 31))
        self.admin_button.setStyleSheet(u"\n"
"color: rgb(255, 58, 58);")

        self.retranslateUi(Form)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-size:18pt;\">Terminal</span></p></body></html>", None))
        self.textBrowser.setHtml(QCoreApplication.translate("Form", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Connect Success !</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Fail to Connect</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("Form", u"Settings", None))
        self.port_setting.setText(QCoreApplication.translate("Form", u"Port", None))
        self.Sensitivity.setText(QCoreApplication.translate("Form", u"Sensitivity", None))
        self.pushButton_1_3.setText(QCoreApplication.translate("Form", u"Overload", None))
        self.pushButton.setText(QCoreApplication.translate("Form", u"Sent", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Form", u"Tab 1", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("Form", u"Device Select", None))
        self.radioButton.setText(QCoreApplication.translate("Form", u"USB (Defult)", None))
        self.radioButton_2.setText(QCoreApplication.translate("Form", u"Registry", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"\u8fd0\u884c\u6a21\u5f0f\u5207\u6362", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Form", u"Tab 2", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"center\"><span style=\" font-size:36pt;\">Oniimai Assistant</span></p></body></html>", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("Form", u"Device Select", None))
        self.device_selector.setItemText(0, QCoreApplication.translate("Form", u"\u8bbe\u59071", None))

        self.reconfirm_button.setText(QCoreApplication.translate("Form", u"OK", None))
        self.checkadmin.setText("")
        self.checkdevice.setText("")
        self.checklink.setText("")
        self.checkhandshake.setText("")
        self.label_8.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"center\">Admin</p></body></html>", None))
        self.label_9.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"center\">Device</p></body></html>", None))
        self.label_10.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"center\">Link</p></body></html>", None))
        self.label_11.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"center\">Hand Shake</p></body></html>", None))
        self.admin_button.setText(QCoreApplication.translate("Form", u"Active Admin", None))
    # retranslateUi

