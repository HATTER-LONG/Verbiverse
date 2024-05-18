# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MessageBox.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_MessageBox(object):
    def setupUi(self, MessageBox):
        if not MessageBox.objectName():
            MessageBox.setObjectName(u"MessageBox")
        MessageBox.resize(365, 86)
        MessageBox.setStyleSheet(u"border: 1px solid #000000; border-radius: 5px; padding: 5px")
        MessageBox.setFrameShape(QFrame.Shape.NoFrame)
        MessageBox.setFrameShadow(QFrame.Shadow.Plain)
        MessageBox.setLineWidth(1)
        self.gridLayout = QGridLayout(MessageBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.user_image = QLabel(MessageBox)
        self.user_image.setObjectName(u"user_image")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.user_image.sizePolicy().hasHeightForWidth())
        self.user_image.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.user_image)

        self.user_name = QLabel(MessageBox)
        self.user_name.setObjectName(u"user_name")
        sizePolicy.setHeightForWidth(self.user_name.sizePolicy().hasHeightForWidth())
        self.user_name.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.user_name)


        self.horizontalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.user_message = QLabel(MessageBox)
        self.user_message.setObjectName(u"user_message")
        sizePolicy.setHeightForWidth(self.user_message.sizePolicy().hasHeightForWidth())
        self.user_message.setSizePolicy(sizePolicy)
        self.user_message.setMouseTracking(False)
        self.user_message.setWordWrap(True)
        self.user_message.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByKeyboard|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.horizontalLayout_3.addWidget(self.user_message)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.retranslateUi(MessageBox)

        QMetaObject.connectSlotsByName(MessageBox)
    # setupUi

    def retranslateUi(self, MessageBox):
        MessageBox.setWindowTitle(QCoreApplication.translate("MessageBox", u"Frame", None))
        self.user_image.setText("")
        self.user_name.setText("")
        self.user_message.setText("")
    # retranslateUi

