# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'AudioPlayer.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QListWidgetItem, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

from qfluentwidgets import (ListWidget, PrimaryPushButton)
from qfluentwidgets.multimedia import SimpleMediaPlayBar

class Ui_PlayerAudio(object):
    def setupUi(self, PlayerAudio):
        if not PlayerAudio.objectName():
            PlayerAudio.setObjectName(u"PlayerAudio")
        PlayerAudio.resize(505, 407)
        self.gridLayout = QGridLayout(PlayerAudio)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.player_title = QLabel(PlayerAudio)
        self.player_title.setObjectName(u"player_title")
        self.player_title.setWordWrap(True)

        self.verticalLayout.addWidget(self.player_title)

        self.player_bar = SimpleMediaPlayBar(PlayerAudio)
        self.player_bar.setObjectName(u"player_bar")

        self.verticalLayout.addWidget(self.player_bar)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.clear_button = PrimaryPushButton(PlayerAudio)
        self.clear_button.setObjectName(u"clear_button")

        self.horizontalLayout.addWidget(self.clear_button)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.listWidget = ListWidget(PlayerAudio)
        self.listWidget.setObjectName(u"listWidget")

        self.verticalLayout.addWidget(self.listWidget)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.retranslateUi(PlayerAudio)

        QMetaObject.connectSlotsByName(PlayerAudio)
    # setupUi

    def retranslateUi(self, PlayerAudio):
        PlayerAudio.setWindowTitle(QCoreApplication.translate("PlayerAudio", u"Form", None))
        self.player_title.setText(QCoreApplication.translate("PlayerAudio", u"TextLabel", None))
        self.clear_button.setText("")
    # retranslateUi

