# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Translate.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QLayout, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_TranslateInfoWin(object):
    def setupUi(self, TranslateInfoWin):
        if not TranslateInfoWin.objectName():
            TranslateInfoWin.setObjectName(u"TranslateInfoWin")
        TranslateInfoWin.resize(588, 267)
        self.gridLayout = QGridLayout(TranslateInfoWin)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.scrollArea = QScrollArea(TranslateInfoWin)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 560, 195))
        self.gridLayout_2 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.result = QLabel(self.scrollAreaWidgetContents)
        self.result.setObjectName(u"result")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.result.sizePolicy().hasHeightForWidth())
        self.result.setSizePolicy(sizePolicy)
        self.result.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.result.setWordWrap(True)

        self.gridLayout_2.addWidget(self.result, 0, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.translate_button = QPushButton(TranslateInfoWin)
        self.translate_button.setObjectName(u"translate_button")

        self.horizontalLayout.addWidget(self.translate_button)

        self.add_database_button = QPushButton(TranslateInfoWin)
        self.add_database_button.setObjectName(u"add_database_button")

        self.horizontalLayout.addWidget(self.add_database_button)


        self.horizontalLayout_2.addLayout(self.horizontalLayout)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.retranslateUi(TranslateInfoWin)

        QMetaObject.connectSlotsByName(TranslateInfoWin)
    # setupUi

    def retranslateUi(self, TranslateInfoWin):
        TranslateInfoWin.setWindowTitle(QCoreApplication.translate("TranslateInfoWin", u"Form", None))
        self.result.setText("")
        self.translate_button.setText(QCoreApplication.translate("TranslateInfoWin", u"\u7ffb\u8bd1", None))
        self.add_database_button.setText(QCoreApplication.translate("TranslateInfoWin", u"\u52a0\u5165\u5355\u8bcd\u672c", None))
    # retranslateUi

