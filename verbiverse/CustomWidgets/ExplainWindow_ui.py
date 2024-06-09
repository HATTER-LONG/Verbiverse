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
    QVBoxLayout, QWidget)

from qfluentwidgets import (BodyLabel, SubtitleLabel, TransparentToolButton)

class Ui_ExplainWindow(object):
    def setupUi(self, ExplainWindow):
        if not ExplainWindow.objectName():
            ExplainWindow.setObjectName(u"ExplainWindow")
        ExplainWindow.resize(461, 341)
        self.gridLayout = QGridLayout(ExplainWindow)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(5, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(10, -1, -1, -1)
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

        self.close_button = TransparentToolButton(ExplainWindow)
        self.close_button.setObjectName(u"close_button")
        self.close_button.setArrowType(Qt.NoArrow)

        self.horizontalLayout.addWidget(self.close_button, 0, Qt.AlignTop)


        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)


        self.retranslateUi(ExplainWindow)

        QMetaObject.connectSlotsByName(ExplainWindow)
    # setupUi

    def retranslateUi(self, ExplainWindow):
        ExplainWindow.setWindowTitle(QCoreApplication.translate("ExplainWindow", u"Form", None))
        self.title_label.setText("")
        self.content_label.setText("")
        self.close_button.setText("")
    # retranslateUi

