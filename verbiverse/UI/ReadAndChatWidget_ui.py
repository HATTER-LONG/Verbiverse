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

from CReadPageTabWidget import CReadPageTabWidget
from CustomWidgets import CWebView

class Ui_ReadAndChatWidget(object):
    def setupUi(self, ReadAndChatWidget):
        if not ReadAndChatWidget.objectName():
            ReadAndChatWidget.setObjectName(u"ReadAndChatWidget")
        ReadAndChatWidget.resize(915, 563)
        self.gridLayout = QGridLayout(ReadAndChatWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.splitter = QSplitter(ReadAndChatWidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter.setHandleWidth(5)
        self.web_view = CWebView(self.splitter)
        self.web_view.setObjectName(u"web_view")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.web_view.sizePolicy().hasHeightForWidth())
        self.web_view.setSizePolicy(sizePolicy)
        self.web_view.setMinimumSize(QSize(500, 0))
        self.web_view.setUrl(QUrl(u"about:blank"))
        self.splitter.addWidget(self.web_view)
        self.tab_widget = CReadPageTabWidget(self.splitter)
        self.tab_widget.setObjectName(u"tab_widget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tab_widget.sizePolicy().hasHeightForWidth())
        self.tab_widget.setSizePolicy(sizePolicy1)
        self.tab_widget.setMinimumSize(QSize(300, 0))
        self.splitter.addWidget(self.tab_widget)

        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)


        self.retranslateUi(ReadAndChatWidget)

        QMetaObject.connectSlotsByName(ReadAndChatWidget)
    # setupUi

    def retranslateUi(self, ReadAndChatWidget):
        ReadAndChatWidget.setWindowTitle(QCoreApplication.translate("ReadAndChatWidget", u"Form", None))
    # retranslateUi

