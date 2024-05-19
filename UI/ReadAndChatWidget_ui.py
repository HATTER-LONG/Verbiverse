# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ReadAndChatWidget.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
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
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QApplication, QGridLayout, QSizePolicy, QSplitter,
    QWidget)

from CustomWidgets import WebView
from UI import ChatWidget

class Ui_ReadAndChatWidget(object):
    def setupUi(self, ReadAndChatWidget):
        if not ReadAndChatWidget.objectName():
            ReadAndChatWidget.setObjectName(u"ReadAndChatWidget")
        ReadAndChatWidget.resize(696, 563)
        self.gridLayout = QGridLayout(ReadAndChatWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.splitter = QSplitter(ReadAndChatWidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter.setHandleWidth(15)
        self.web_view = WebView(self.splitter)
        self.web_view.setObjectName(u"web_view")
        self.web_view.setMinimumSize(QSize(500, 0))
        self.web_view.setUrl(QUrl(u"about:blank"))
        self.splitter.addWidget(self.web_view)
        self.chat_widget = ChatWidget(self.splitter)
        self.chat_widget.setObjectName(u"chat_widget")
        self.splitter.addWidget(self.chat_widget)

        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)


        self.retranslateUi(ReadAndChatWidget)

        QMetaObject.connectSlotsByName(ReadAndChatWidget)
    # setupUi

    def retranslateUi(self, ReadAndChatWidget):
        ReadAndChatWidget.setWindowTitle(QCoreApplication.translate("ReadAndChatWidget", u"Form", None))
    # retranslateUi

