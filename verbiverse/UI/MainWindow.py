# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
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
    QMainWindow, QMenuBar, QPushButton, QScrollArea,
    QSizePolicy, QTextEdit, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(900, 700)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(900, 700))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.chat_scroll_area = QScrollArea(self.centralwidget)
        self.chat_scroll_area.setObjectName(u"chat_scroll_area")
        font = QFont()
        font.setFamilies([u".AppleSystemUIFont"])
        self.chat_scroll_area.setFont(font)
        self.chat_scroll_area.setWidgetResizable(False)
        self.chat_scroll_area.setAlignment(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(98, 0, 677, 392))
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.chat_scroll_area.setWidget(self.scrollAreaWidgetContents_2)

        self.verticalLayout_5.addWidget(self.chat_scroll_area)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.user_text_edit = QTextEdit(self.centralwidget)
        self.user_text_edit.setObjectName(u"user_text_edit")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.user_text_edit.sizePolicy().hasHeightForWidth())
        self.user_text_edit.setSizePolicy(sizePolicy1)
        self.user_text_edit.setMinimumSize(QSize(600, 80))
        self.user_text_edit.setMaximumSize(QSize(16777215, 200))

        self.horizontalLayout_5.addWidget(self.user_text_edit)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.user_send_button = QPushButton(self.centralwidget)
        self.user_send_button.setObjectName(u"user_send_button")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.user_send_button.sizePolicy().hasHeightForWidth())
        self.user_send_button.setSizePolicy(sizePolicy2)
        self.user_send_button.setMinimumSize(QSize(0, 40))
        self.user_send_button.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_2.addWidget(self.user_send_button)

        self.user_check_button = QPushButton(self.centralwidget)
        self.user_check_button.setObjectName(u"user_check_button")
        sizePolicy2.setHeightForWidth(self.user_check_button.sizePolicy().hasHeightForWidth())
        self.user_check_button.setSizePolicy(sizePolicy2)
        self.user_check_button.setMinimumSize(QSize(0, 40))

        self.verticalLayout_2.addWidget(self.user_check_button)


        self.horizontalLayout_5.addLayout(self.verticalLayout_2)


        self.verticalLayout_5.addLayout(self.horizontalLayout_5)

        self.check_result = QLabel(self.centralwidget)
        self.check_result.setObjectName(u"check_result")
        self.check_result.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.check_result.setWordWrap(True)
        self.check_result.setMargin(0)

        self.verticalLayout_5.addWidget(self.check_result)


        self.gridLayout.addLayout(self.verticalLayout_5, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setEnabled(False)
        self.menubar.setGeometry(QRect(0, 0, 900, 24))
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.user_send_button.setText(QCoreApplication.translate("MainWindow", u"Send", None))
        self.user_check_button.setText(QCoreApplication.translate("MainWindow", u"check", None))
        self.check_result.setText("")
    # retranslateUi

