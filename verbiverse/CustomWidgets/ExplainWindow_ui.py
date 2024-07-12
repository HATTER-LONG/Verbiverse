# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ExplainWindow.ui'
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

from qfluentwidgets import (BodyLabel, PrimaryToolButton, SubtitleLabel, TransparentToolButton)

class Ui_ExplainWindow(object):
    def setupUi(self, ExplainWindow):
        if not ExplainWindow.objectName():
            ExplainWindow.setObjectName(u"ExplainWindow")
        ExplainWindow.resize(466, 341)
        self.gridLayout = QGridLayout(ExplainWindow)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, 10, -1, -1)
        self.title_label = SubtitleLabel(ExplainWindow)
        self.title_label.setObjectName(u"title_label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.title_label.sizePolicy().hasHeightForWidth())
        self.title_label.setSizePolicy(sizePolicy)
        self.title_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.verticalLayout.addWidget(self.title_label)

        self.content_label = BodyLabel(ExplainWindow)
        self.content_label.setObjectName(u"content_label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.content_label.sizePolicy().hasHeightForWidth())
        self.content_label.setSizePolicy(sizePolicy1)
        self.content_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.content_label.setWordWrap(True)
        self.content_label.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)

        self.verticalLayout.addWidget(self.content_label)

        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 8)

        self.horizontalLayout.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.close_button = TransparentToolButton(ExplainWindow)
        self.close_button.setObjectName(u"close_button")
        self.close_button.setArrowType(Qt.NoArrow)

        self.verticalLayout_2.addWidget(self.close_button)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.add_button = PrimaryToolButton(ExplainWindow)
        self.add_button.setObjectName(u"add_button")

        self.verticalLayout_2.addWidget(self.add_button)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.horizontalLayout.setStretch(0, 20)
        self.horizontalLayout.setStretch(1, 1)

        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)


        self.retranslateUi(ExplainWindow)

        QMetaObject.connectSlotsByName(ExplainWindow)
    # setupUi

    def retranslateUi(self, ExplainWindow):
        ExplainWindow.setWindowTitle(QCoreApplication.translate("ExplainWindow", u"Form", None))
        self.title_label.setText("")
        self.content_label.setText("")
        self.close_button.setText("")
        self.add_button.setText("")
    # retranslateUi

