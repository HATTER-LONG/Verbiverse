# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ChatWidget.ui'
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
    QLayout, QSizePolicy, QVBoxLayout, QWidget)

from qfluentwidgets import (PushButton, ScrollArea, TextEdit)

class Ui_ChatWidget(object):
    def setupUi(self, ChatWidget):
        if not ChatWidget.objectName():
            ChatWidget.setObjectName(u"ChatWidget")
        ChatWidget.resize(582, 500)
        self.gridLayout = QGridLayout(ChatWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.chat_scroll_area = ScrollArea(ChatWidget)
        self.chat_scroll_area.setObjectName(u"chat_scroll_area")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chat_scroll_area.sizePolicy().hasHeightForWidth())
        self.chat_scroll_area.setSizePolicy(sizePolicy)
        self.chat_scroll_area.setStyleSheet(u"")
        self.chat_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.chat_scroll_area.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.chat_scroll_area.setWidgetResizable(True)
        self.chat_scroll_area.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.scroll_area_widget = QWidget()
        self.scroll_area_widget.setObjectName(u"scroll_area_widget")
        self.scroll_area_widget.setGeometry(QRect(0, 0, 553, 332))
        sizePolicy.setHeightForWidth(self.scroll_area_widget.sizePolicy().hasHeightForWidth())
        self.scroll_area_widget.setSizePolicy(sizePolicy)
        self.scroll_area_widget.setMinimumSize(QSize(0, 332))
        self.scroll_area_widget.setLayoutDirection(Qt.LeftToRight)
        self.scroll_area_widget.setAutoFillBackground(True)
        self.messages_list = QVBoxLayout(self.scroll_area_widget)
        self.messages_list.setSpacing(5)
        self.messages_list.setObjectName(u"messages_list")
        self.messages_list.setSizeConstraint(QLayout.SetNoConstraint)
        self.messages_list.setContentsMargins(0, 0, 0, 0)
        self.chat_scroll_area.setWidget(self.scroll_area_widget)

        self.verticalLayout_5.addWidget(self.chat_scroll_area)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.user_text_edit = TextEdit(ChatWidget)
        self.user_text_edit.setObjectName(u"user_text_edit")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.user_text_edit.sizePolicy().hasHeightForWidth())
        self.user_text_edit.setSizePolicy(sizePolicy1)
        self.user_text_edit.setMinimumSize(QSize(40, 80))
        self.user_text_edit.setMaximumSize(QSize(16777215, 200))

        self.horizontalLayout_5.addWidget(self.user_text_edit)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.user_send_button = PushButton(ChatWidget)
        self.user_send_button.setObjectName(u"user_send_button")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.user_send_button.sizePolicy().hasHeightForWidth())
        self.user_send_button.setSizePolicy(sizePolicy2)
        self.user_send_button.setMinimumSize(QSize(0, 40))
        self.user_send_button.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_2.addWidget(self.user_send_button)

        self.user_check_button = PushButton(ChatWidget)
        self.user_check_button.setObjectName(u"user_check_button")
        sizePolicy2.setHeightForWidth(self.user_check_button.sizePolicy().hasHeightForWidth())
        self.user_check_button.setSizePolicy(sizePolicy2)
        self.user_check_button.setMinimumSize(QSize(0, 40))

        self.verticalLayout_2.addWidget(self.user_check_button)


        self.horizontalLayout_5.addLayout(self.verticalLayout_2)


        self.verticalLayout_5.addLayout(self.horizontalLayout_5)


        self.gridLayout.addLayout(self.verticalLayout_5, 0, 0, 1, 1)


        self.retranslateUi(ChatWidget)

        QMetaObject.connectSlotsByName(ChatWidget)
    # setupUi

    def retranslateUi(self, ChatWidget):
        ChatWidget.setWindowTitle(QCoreApplication.translate("ChatWidget", u"Form", None))
        self.user_send_button.setText(QCoreApplication.translate("ChatWidget", u"Send", None))
        self.user_check_button.setText(QCoreApplication.translate("ChatWidget", u"check", None))
    # retranslateUi

