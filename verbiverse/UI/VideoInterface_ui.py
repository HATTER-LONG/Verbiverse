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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

from CustomWidgets import CVideoWidget
from qfluentwidgets import (BodyLabel, TransparentToolButton)

class Ui_VideoInterface(object):
    def setupUi(self, VideoInterface):
        if not VideoInterface.objectName():
            VideoInterface.setObjectName(u"VideoInterface")
        VideoInterface.resize(629, 497)
        self.gridLayout_2 = QGridLayout(VideoInterface)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.video_widget = CVideoWidget(VideoInterface)
        self.video_widget.setObjectName(u"video_widget")

        self.verticalLayout.addWidget(self.video_widget)

        self.widget = QWidget(VideoInterface)
        self.widget.setObjectName(u"widget")
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.subtitle_label = BodyLabel(self.widget)
        self.subtitle_label.setObjectName(u"subtitle_label")
        self.subtitle_label.setMinimumSize(QSize(0, 42))
        font = QFont()
        font.setPointSize(20)
        self.subtitle_label.setFont(font)

        self.horizontalLayout_2.addWidget(self.subtitle_label)


        self.horizontalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.horizontalLayout_3.addLayout(self.horizontalLayout)

        self.parse_button = TransparentToolButton(self.widget)
        self.parse_button.setObjectName(u"parse_button")

        self.horizontalLayout_3.addWidget(self.parse_button)


        self.gridLayout.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.widget)

        self.verticalLayout.setStretch(0, 8)

        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.retranslateUi(VideoInterface)

        QMetaObject.connectSlotsByName(VideoInterface)
    # setupUi

    def retranslateUi(self, VideoInterface):
        VideoInterface.setWindowTitle(QCoreApplication.translate("VideoInterface", u"Form", None))
        self.subtitle_label.setText("")
        self.parse_button.setText("")
    # retranslateUi

