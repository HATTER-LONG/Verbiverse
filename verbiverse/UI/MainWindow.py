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
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QHeaderView,
    QLabel, QMainWindow, QMenuBar, QPushButton,
    QScrollArea, QSizePolicy, QSplitter, QTabWidget,
    QTextEdit, QTreeView, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(968, 700)
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
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.splitter_2 = QSplitter(self.centralwidget)
        self.splitter_2.setObjectName(u"splitter_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(30)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.splitter_2.sizePolicy().hasHeightForWidth())
        self.splitter_2.setSizePolicy(sizePolicy1)
        self.splitter_2.setAcceptDrops(False)
        self.splitter_2.setOrientation(Qt.Orientation.Horizontal)
        self.tabWidget_4 = QTabWidget(self.splitter_2)
        self.tabWidget_4.setObjectName(u"tabWidget_4")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.tabWidget_4.sizePolicy().hasHeightForWidth())
        self.tabWidget_4.setSizePolicy(sizePolicy2)
        self.tabWidget_4.setTabPosition(QTabWidget.TabPosition.West)
        self.tabWidget_4.setDocumentMode(False)
        self.bookmarkTab_4 = QWidget()
        self.bookmarkTab_4.setObjectName(u"bookmarkTab_4")
        self.verticalLayout_8 = QVBoxLayout(self.bookmarkTab_4)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(2, 2, 2, 2)
        self.bookmarkView_4 = QTreeView(self.bookmarkTab_4)
        self.bookmarkView_4.setObjectName(u"bookmarkView_4")
        sizePolicy2.setHeightForWidth(self.bookmarkView_4.sizePolicy().hasHeightForWidth())
        self.bookmarkView_4.setSizePolicy(sizePolicy2)
        self.bookmarkView_4.setMinimumSize(QSize(150, 0))
        self.bookmarkView_4.setHeaderHidden(True)

        self.verticalLayout_8.addWidget(self.bookmarkView_4)

        self.tabWidget_4.addTab(self.bookmarkTab_4, "")
        self.pagesTab_4 = QWidget()
        self.pagesTab_4.setObjectName(u"pagesTab_4")
        self.tabWidget_4.addTab(self.pagesTab_4, "")
        self.splitter_2.addWidget(self.tabWidget_4)
        self.pdfView_4 = QPdfView(self.splitter_2)
        self.pdfView_4.setObjectName(u"pdfView_4")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy3.setHorizontalStretch(10)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.pdfView_4.sizePolicy().hasHeightForWidth())
        self.pdfView_4.setSizePolicy(sizePolicy3)
        self.pdfView_4.setMinimumSize(QSize(300, 0))
        self.splitter_2.addWidget(self.pdfView_4)

        self.horizontalLayout.addWidget(self.splitter_2)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.chat_scroll_area = QScrollArea(self.centralwidget)
        self.chat_scroll_area.setObjectName(u"chat_scroll_area")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.chat_scroll_area.sizePolicy().hasHeightForWidth())
        self.chat_scroll_area.setSizePolicy(sizePolicy4)
        font = QFont()
        font.setFamilies([u".AppleSystemUIFont"])
        self.chat_scroll_area.setFont(font)
        self.chat_scroll_area.setWidgetResizable(False)
        self.chat_scroll_area.setAlignment(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 677, 392))
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.chat_scroll_area.setWidget(self.scrollAreaWidgetContents_2)

        self.verticalLayout_5.addWidget(self.chat_scroll_area)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.user_text_edit = QTextEdit(self.centralwidget)
        self.user_text_edit.setObjectName(u"user_text_edit")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.user_text_edit.sizePolicy().hasHeightForWidth())
        self.user_text_edit.setSizePolicy(sizePolicy5)
        self.user_text_edit.setMinimumSize(QSize(40, 80))
        self.user_text_edit.setMaximumSize(QSize(16777215, 200))

        self.horizontalLayout_5.addWidget(self.user_text_edit)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.user_send_button = QPushButton(self.centralwidget)
        self.user_send_button.setObjectName(u"user_send_button")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.user_send_button.sizePolicy().hasHeightForWidth())
        self.user_send_button.setSizePolicy(sizePolicy6)
        self.user_send_button.setMinimumSize(QSize(0, 40))
        self.user_send_button.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_2.addWidget(self.user_send_button)

        self.user_check_button = QPushButton(self.centralwidget)
        self.user_check_button.setObjectName(u"user_check_button")
        sizePolicy6.setHeightForWidth(self.user_check_button.sizePolicy().hasHeightForWidth())
        self.user_check_button.setSizePolicy(sizePolicy6)
        self.user_check_button.setMinimumSize(QSize(0, 40))

        self.verticalLayout_2.addWidget(self.user_check_button)


        self.horizontalLayout_5.addLayout(self.verticalLayout_2)


        self.verticalLayout_5.addLayout(self.horizontalLayout_5)

        self.check_result = QLabel(self.centralwidget)
        self.check_result.setObjectName(u"check_result")
        sizePolicy6.setHeightForWidth(self.check_result.sizePolicy().hasHeightForWidth())
        self.check_result.setSizePolicy(sizePolicy6)
        self.check_result.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.check_result.setWordWrap(True)
        self.check_result.setMargin(0)

        self.verticalLayout_5.addWidget(self.check_result)


        self.horizontalLayout.addLayout(self.verticalLayout_5)

        self.horizontalLayout.setStretch(0, 6)
        self.horizontalLayout.setStretch(1, 2)

        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setEnabled(False)
        self.menubar.setGeometry(QRect(0, 0, 968, 24))
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)

        self.tabWidget_4.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.tabWidget_4.setTabText(self.tabWidget_4.indexOf(self.bookmarkTab_4), QCoreApplication.translate("MainWindow", u"Bookmarks", None))
        self.tabWidget_4.setTabText(self.tabWidget_4.indexOf(self.pagesTab_4), QCoreApplication.translate("MainWindow", u"Pages", None))
        self.user_send_button.setText(QCoreApplication.translate("MainWindow", u"Send", None))
        self.user_check_button.setText(QCoreApplication.translate("MainWindow", u"check", None))
        self.check_result.setText("")
    # retranslateUi

