# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'VideoInterface.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QSizePolicy, QWidget)

from qfluentwidgets.multimedia import VideoWidget

class Ui_VideoInterface(object):
    def setupUi(self, VideoInterface):
        if not VideoInterface.objectName():
            VideoInterface.setObjectName(u"VideoInterface")
        VideoInterface.resize(487, 368)
        self.gridLayout = QGridLayout(VideoInterface)
        self.gridLayout.setObjectName(u"gridLayout")
        self.video_widget = VideoWidget(VideoInterface)
        self.video_widget.setObjectName(u"video_widget")

        self.gridLayout.addWidget(self.video_widget, 0, 0, 1, 1)


        self.retranslateUi(VideoInterface)

        QMetaObject.connectSlotsByName(VideoInterface)
    # setupUi

    def retranslateUi(self, VideoInterface):
        VideoInterface.setWindowTitle(QCoreApplication.translate("VideoInterface", u"Form", None))
    # retranslateUi

