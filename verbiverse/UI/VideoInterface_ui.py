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
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QGridLayout, QHBoxLayout,
    QSizePolicy, QSpacerItem, QSplitter, QTextEdit,
    QVBoxLayout, QWidget)

from CustomWidgets import (CSubtitleLabel, CTabWidget, CVideoWidget)
from qfluentwidgets import TransparentToolButton

class Ui_VideoInterface(object):
    def setupUi(self, VideoInterface):
        if not VideoInterface.objectName():
            VideoInterface.setObjectName(u"VideoInterface")
        VideoInterface.resize(839, 544)
        VideoInterface.setContextMenuPolicy(Qt.CustomContextMenu)
        self.gridLayout_2 = QGridLayout(VideoInterface)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.splitter = QSplitter(VideoInterface)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.widget = QWidget(self.splitter)
        self.widget.setObjectName(u"widget")
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.video_widget = CVideoWidget(self.widget)
        self.video_widget.setObjectName(u"video_widget")
        self.video_widget.setMinimumSize(QSize(500, 0))
        self.video_widget.setContextMenuPolicy(Qt.ActionsContextMenu)

        self.verticalLayout.addWidget(self.video_widget)

        self.subtitle_widget = QWidget(self.widget)
        self.subtitle_widget.setObjectName(u"subtitle_widget")
        self.gridLayout = QGridLayout(self.subtitle_widget)
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

        self.horizontalLayout.addLayout(self.horizontalLayout_2)

        self.subtitel_browser = CSubtitleLabel(self.subtitle_widget)
        self.subtitel_browser.setObjectName(u"subtitel_browser")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subtitel_browser.sizePolicy().hasHeightForWidth())
        self.subtitel_browser.setSizePolicy(sizePolicy)
        self.subtitel_browser.setMinimumSize(QSize(0, 40))
        self.subtitel_browser.setMaximumSize(QSize(16777215, 42))
        font = QFont()
        font.setPointSize(20)
        self.subtitel_browser.setFont(font)
        self.subtitel_browser.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.subtitel_browser.setAcceptDrops(False)
        self.subtitel_browser.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.subtitel_browser.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.subtitel_browser.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.subtitel_browser.setLineWrapMode(QTextEdit.NoWrap)
        self.subtitel_browser.setTextInteractionFlags(Qt.NoTextInteraction)

        self.horizontalLayout.addWidget(self.subtitel_browser)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.horizontalLayout_3.addLayout(self.horizontalLayout)

        self.parse_button = TransparentToolButton(self.subtitle_widget)
        self.parse_button.setObjectName(u"parse_button")

        self.horizontalLayout_3.addWidget(self.parse_button)


        self.gridLayout.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 30, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout.addItem(self.verticalSpacer, 1, 0, 1, 1)


        self.verticalLayout.addWidget(self.subtitle_widget)

        self.verticalLayout.setStretch(0, 8)
        self.splitter.addWidget(self.widget)
        self.tab_widget = CTabWidget(self.splitter)
        self.tab_widget.setObjectName(u"tab_widget")
        self.tab_widget.setMinimumSize(QSize(200, 0))
        self.splitter.addWidget(self.tab_widget)

        self.gridLayout_2.addWidget(self.splitter, 0, 0, 1, 1)


        self.retranslateUi(VideoInterface)

        QMetaObject.connectSlotsByName(VideoInterface)
    # setupUi

    def retranslateUi(self, VideoInterface):
        VideoInterface.setWindowTitle(QCoreApplication.translate("VideoInterface", u"Form", None))
        self.parse_button.setText("")
    # retranslateUi

