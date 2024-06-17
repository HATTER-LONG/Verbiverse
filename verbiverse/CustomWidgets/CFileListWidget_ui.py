# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CFileListWidget.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QListWidgetItem,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

from qfluentwidgets import (ListWidget, PushButton, SubtitleLabel)

class Ui_CFileListWidget(object):
    def setupUi(self, CFileListWidget):
        if not CFileListWidget.objectName():
            CFileListWidget.setObjectName(u"CFileListWidget")
        CFileListWidget.resize(667, 455)
        self.gridLayout = QGridLayout(CFileListWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_4 = QSpacerItem(30, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)

        self.filelist_label = SubtitleLabel(CFileListWidget)
        self.filelist_label.setObjectName(u"filelist_label")

        self.horizontalLayout_2.addWidget(self.filelist_label)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.filelist_clear = PushButton(CFileListWidget)
        self.filelist_clear.setObjectName(u"filelist_clear")
        self.filelist_clear.setAutoDefault(False)
        self.filelist_clear.setFlat(True)

        self.horizontalLayout_2.addWidget(self.filelist_clear)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.filelist_widget = ListWidget(CFileListWidget)
        self.filelist_widget.setObjectName(u"filelist_widget")

        self.horizontalLayout.addWidget(self.filelist_widget)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.retranslateUi(CFileListWidget)

        self.filelist_clear.setDefault(False)


        QMetaObject.connectSlotsByName(CFileListWidget)
    # setupUi

    def retranslateUi(self, CFileListWidget):
        CFileListWidget.setWindowTitle(QCoreApplication.translate("CFileListWidget", u"Form", None))
        self.filelist_label.setText(QCoreApplication.translate("CFileListWidget", u"Recently opened files", None))
        self.filelist_clear.setText(QCoreApplication.translate("CFileListWidget", u"Clear", None))
    # retranslateUi

