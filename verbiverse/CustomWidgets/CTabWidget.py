from PySide6.QtWidgets import (
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)
from qfluentwidgets import ListWidget, SegmentedWidget


class CTabWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.pivot = SegmentedWidget(self)
        self.stackedWidget = QStackedWidget(self)
        self.vBoxLayout = QVBoxLayout(self)

        self.subtitle = ListWidget(self)
        self.file_list = ListWidget(self)

        # add items to pivot
        self.addSubInterface(self.subtitle, "SubTitleInterface", self.tr("SubTitle"))
        self.addSubInterface(
            self.file_list, "videoFileInterface", self.tr("Video List")
        )

        self.vBoxLayout.addWidget(self.pivot)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setContentsMargins(15, 10, 15, 30)

        self.stackedWidget.setCurrentWidget(self.subtitle)
        self.pivot.setCurrentItem(self.subtitle.objectName())
        self.pivot.currentItemChanged.connect(
            lambda k: self.stackedWidget.setCurrentWidget(self.findChild(QWidget, k))
        )

    def addSubInterface(self, widget: QWidget, objectName, text):
        widget.setObjectName(objectName)
        self.stackedWidget.addWidget(widget)
        self.pivot.addItem(routeKey=objectName, text=text)
