from PySide6.QtWidgets import (
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)
from qfluentwidgets import SegmentedWidget

from UI import ChatWidget
from AudioPlayer import AudioPlayer


class CReadPageTabWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.pivot = SegmentedWidget(self)
        self.stackedWidget = QStackedWidget(self)
        self.vBoxLayout = QVBoxLayout(self)

        self.chat_widget = ChatWidget(self)
        self.audio_player = AudioPlayer(self)

        # add items to pivot
        self.addSubInterface(
            self.chat_widget, "ChatInterface", self.tr("Chat with LLM")
        )
        self.addSubInterface(
            self.audio_player, "AudioPlayerInterface", self.tr("Audio Player")
        )

        self.vBoxLayout.addWidget(self.pivot)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.stackedWidget.setCurrentWidget(self.chat_widget)
        self.pivot.setCurrentItem(self.chat_widget.objectName())
        self.pivot.currentItemChanged.connect(
            lambda k: self.stackedWidget.setCurrentWidget(self.findChild(QWidget, k))
        )

    def addSubInterface(self, widget: QWidget, objectName, text):
        widget.setObjectName(objectName)
        self.stackedWidget.addWidget(widget)
        self.pivot.addItem(routeKey=objectName, text=text)
