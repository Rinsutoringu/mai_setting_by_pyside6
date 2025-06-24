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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialogButtonBox, QGraphicsView,
    QPushButton, QSizePolicy, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(623, 538)
        Form.setMinimumSize(QSize(623, 538))
        Form.setMaximumSize(QSize(623, 538))
        Form.setSizeIncrement(QSize(623, 538))
        Form.setBaseSize(QSize(623, 538))
        self.buttonBox = QDialogButtonBox(Form)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(530, 30, 81, 241))
        self.buttonBox.setMouseTracking(False)
        self.buttonBox.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.buttonBox.setOrientation(Qt.Orientation.Vertical)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Apply|QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Help|QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setCenterButtons(False)
        self.screenView = QGraphicsView(Form)
        self.screenView.setObjectName(u"screenView")
        self.screenView.setGeometry(QRect(20, 20, 500, 500))
        self.test123 = QPushButton(Form)
        self.test123.setObjectName(u"test123")
        self.test123.setGeometry(QRect(530, 230, 75, 24))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.test123.setText(QCoreApplication.translate("Form", u"test123", None))
    # retranslateUi

