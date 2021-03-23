# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'parameters.ui'
##
## Created by: Qt User Interface Compiler version 6.0.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(432, 291)
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 40, 121, 21))
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(20, 70, 121, 21))
        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(0, 110, 381, 21))
        self.label_3.setAlignment(Qt.AlignCenter)
        self.p1_name = QLineEdit(Form)
        self.p1_name.setObjectName(u"p1_name")
        self.p1_name.setGeometry(QRect(110, 40, 121, 21))
        self.p2_name = QLineEdit(Form)
        self.p2_name.setObjectName(u"p2_name")
        self.p2_name.setGeometry(QRect(110, 70, 121, 21))
        self.p1_value = QLineEdit(Form)
        self.p1_value.setObjectName(u"p1_value")
        self.p1_value.setGeometry(QRect(240, 40, 121, 21))
        self.p2_value = QLineEdit(Form)
        self.p2_value.setObjectName(u"p2_value")
        self.p2_value.setGeometry(QRect(240, 70, 121, 21))
        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(110, 10, 121, 21))
        self.label_4.setFrameShape(QFrame.NoFrame)
        self.label_4.setAlignment(Qt.AlignCenter)
        self.label_5 = QLabel(Form)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(240, 10, 121, 21))
        self.label_5.setFrameShape(QFrame.NoFrame)
        self.label_5.setAlignment(Qt.AlignCenter)
        self.mass_display = QLCDNumber(Form)
        self.mass_display.setObjectName(u"mass_display")
        self.mass_display.setGeometry(QRect(140, 140, 111, 23))
        self.mass_display.setSmallDecimalPoint(False)
        self.mass_display.setMode(QLCDNumber.Dec)
        self.mass_display.setProperty("value", 3.450000000000000)
        self.button = QPushButton(Form)
        self.button.setObjectName(u"button")
        self.button.setGeometry(QRect(80, 190, 100, 32))
        self.refresh = QPushButton(Form)
        self.refresh.setObjectName(u"refresh")
        self.refresh.setGeometry(QRect(230, 190, 100, 32))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"Parameter 1", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Parameter 2", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Mass", None))
        self.p1_name.setText(QCoreApplication.translate("Form", u"length", None))
        self.p2_name.setText(QCoreApplication.translate("Form", u"width", None))
        self.p1_value.setText(QCoreApplication.translate("Form", u"2", None))
        self.p2_value.setText(QCoreApplication.translate("Form", u"3", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Name", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Value", None))
        self.button.setText(QCoreApplication.translate("Form", u"Send", None))
        self.refresh.setText(QCoreApplication.translate("Form", u"Refresh", None))
    # retranslateUi

