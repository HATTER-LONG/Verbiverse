from PySide6.QtGui import QAction
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (
    QMenu,
)


class QWebPdfView(QWebEngineView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def contextMenuEvent(self, event):
        self.menus = QMenu()

        self.action3 = QAction("get text", self)
        self.action3.triggered.connect(self.gettext)
        self.menus.addAction(self.action3)
        self.menus.popup(event.globalPos())
        self.selectionChanged.connect(self.gettext)

    def gettext(self):
        print(self.page().selectedText())
        print(self.selectedText())
