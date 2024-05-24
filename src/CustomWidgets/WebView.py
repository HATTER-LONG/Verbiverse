import os
import sys

from Functions.WebChannelBridge import BridgeClass
from LoadPdfText import PdfReader
from PySide6.QtCore import QPoint, Qt, QUrl, Slot
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWidgets import (
    QMessageBox,
)
from qframelesswindow.webengine import FramelessWebEngineView


class WebView(FramelessWebEngineView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initWebPdfView()
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.pdfContextMenu)

    def initWebPdfView(self) -> None:
        self.m_fileDialog = None
        script_directory = os.path.dirname(os.path.abspath(__file__))
        self.pdf_js_path = os.path.join(
            script_directory, "PDF_js", "web", "viewer.html"
        ).replace("\\", "/")
        self.pdf_path = ""
        self.pdf_current_page = 1

        self.__channel = QWebChannel()
        self.__bridge_class = BridgeClass()
        self.__bridge_class.pageNumChangedSignal.connect(self.updatePdfPageNum)
        self.__channel.registerObject("bridgeClass", self.__bridge_class)

        self.page().setWebChannel(self.__channel)
        self.pdf_reader: PdfReader = None

    def openLocalPdfDoc(self, doc_location: QUrl):
        self.pdf_current_page = 1
        if doc_location.isLocalFile():
            self.pdf_path = doc_location.url()
            print(doc_location.toLocalFile())
            self.pdf_reader = PdfReader(doc_location.toLocalFile())
            self.load(
                QUrl.fromUserInput(
                    f"file:///{self.pdf_js_path}?file={self.pdf_path}#page={self.pdf_current_page}"
                )
            )
        else:
            message = f"{doc_location} is not a valid local file"
            print(message, file=sys.stderr)
            QMessageBox.critical(self, "Failed to open", message)

    @Slot(int)
    def updatePdfPageNum(self, page_num: int) -> None:
        self.pdf_current_page = page_num

    @Slot(QPoint)
    def ContextMenu(self, event: QPoint):
        print("custom context menu")

    # def contextMenuEvent(self, event):
    #     selected_text = self.selectedText()

    #     if len(selected_text) == 0:
    #         return
    #     all_text = ""

    #     self.menu = LabelMenu(self, selected_text, all_text)
    #     self.menu.popup(event.globalPos())

    # def gettext(self):
    #     print(self.page().selectedText())
    #     print(self.selectedText())
