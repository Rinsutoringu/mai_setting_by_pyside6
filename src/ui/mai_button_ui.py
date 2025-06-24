# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mai_button.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialogButtonBox, QPushButton,
    QSizePolicy, QWidget)
import 1_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(744, 902)
        Form.setMinimumSize(QSize(744, 902))
        Form.setMaximumSize(QSize(744, 902))
        Form.setSizeIncrement(QSize(744, 902))
        Form.setBaseSize(QSize(744, 902))
        self.buttonBox = QDialogButtonBox(Form)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(650, 260, 81, 241))
        self.buttonBox.setMouseTracking(False)
        self.buttonBox.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.buttonBox.setOrientation(Qt.Orientation.Vertical)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Apply|QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Help|QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setCenterButtons(False)
        self.test123 = QPushButton(Form)
        self.test123.setObjectName(u"test123")
        self.test123.setGeometry(QRect(650, 470, 75, 24))
        self.test123_2 = QPushButton(Form)
        self.test123_2.setObjectName(u"test123_2")
        self.test123_2.setGeometry(QRect(650, 500, 75, 24))
        self.test123_3 = QPushButton(Form)
        self.test123_3.setObjectName(u"test123_3")
        self.test123_3.setGeometry(QRect(650, 530, 75, 24))
        self.test123_4 = QPushButton(Form)
        self.test123_4.setObjectName(u"test123_4")
        self.test123_4.setGeometry(QRect(650, 560, 75, 24))
        self.test123_5 = QPushButton(Form)
        self.test123_5.setObjectName(u"test123_5")
        self.test123_5.setGeometry(QRect(650, 590, 75, 24))
        self.bgweight = QWidget(Form)
        self.bgweight.setObjectName(u"bgweight")
        self.bgweight.setGeometry(QRect(0, 10, 651, 881))
        self.bgweight.setStyleSheet(u"")
        self.buttonview = QWidget(self.bgweight)
        self.buttonview.setObjectName(u"buttonview")
        self.buttonview.setGeometry(QRect(80, 330, 490, 496))
        self.buttonview.setAutoFillBackground(False)
        self.buttonview.setStyleSheet(u"background-color: rgb(201, 208, 255);")
        self.bgweight.raise_()
        self.buttonBox.raise_()
        self.test123.raise_()
        self.test123_2.raise_()
        self.test123_3.raise_()
        self.test123_4.raise_()
        self.test123_5.raise_()

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.test123.setText(QCoreApplication.translate("Form", u"test123", None))
        self.test123_2.setText(QCoreApplication.translate("Form", u"test123", None))
        self.test123_3.setText(QCoreApplication.translate("Form", u"test123", None))
        self.test123_4.setText(QCoreApplication.translate("Form", u"test123", None))
        self.test123_5.setText(QCoreApplication.translate("Form", u"test123", None))
    # retranslateUi

