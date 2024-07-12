# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'WordsTableInterface.ui'
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

from CustomWidgets import WordsTable

class Ui_WordsTableInterface(object):
    def setupUi(self, WordsTableInterface):
        if not WordsTableInterface.objectName():
            WordsTableInterface.setObjectName(u"WordsTableInterface")
        WordsTableInterface.resize(505, 416)
        self.gridLayout = QGridLayout(WordsTableInterface)
        self.gridLayout.setObjectName(u"gridLayout")
        self.words_table = WordsTable(WordsTableInterface)
        self.words_table.setObjectName(u"words_table")

        self.gridLayout.addWidget(self.words_table, 0, 0, 1, 1)


        self.retranslateUi(WordsTableInterface)

        QMetaObject.connectSlotsByName(WordsTableInterface)
    # setupUi

    def retranslateUi(self, WordsTableInterface):
        WordsTableInterface.setWindowTitle(QCoreApplication.translate("WordsTableInterface", u"Form", None))
    # retranslateUi

