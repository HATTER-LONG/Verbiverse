import os
import sys

from CContexMenu import CContexMenu
from Functions.WebChannelBridge import BridgeClass
from LoadPdfText import PdfReader
from PySide6.QtCore import QPoint, Qt, QUrl, Slot
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtWidgets import (
    QMessageBox,
)
from qfluentwidgets import isDarkTheme, qconfig
from qframelesswindow.webengine import FramelessWebEngineView


class CWebView(FramelessWebEngineView):
    """
    This class represents a web view for displaying PDF documents and url.

    @Attributes:
        m_fileDialog (QFileDialog): The file dialog used to open local PDF documents.
        pdf_js_path (str): The path to the PDF.js viewer HTML file.
        pdf_path (str): The path to the currently opened PDF document.
        pdf_current_page (int): The current page number of the PDF document.
        pdf_reader (PdfReader): The reader object used to read the PDF document.

    @Methods:
        initWebPdfView(self) -> None: Initializes the web view for displaying PDF documents.
        openLocalPdfDoc(self, doc_location: QUrl): Opens a local PDF document.
        updatePdfPageNum(self, page_num: int) -> None: Updates the current page number of the PDF document.
        ContextMenu(self, event: QPoint): Handles the custom context menu event.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initWebPdfView()
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.ContextMenu)

        qconfig.themeChanged.connect(self.themeChanged)

    def themeChanged(self):
        # TODO: https://github.com/shivaprsd/doq use this to support pdf dark mode
        if isDarkTheme():
            self.page().runJavaScript(
                'document.documentElement.classList.add("is-dark")'
            )
        else:
            self.reload()  # just reload to default light mode
            # self.page().runJavaScript(
            #     'document.documentElement.classList.add("is-light")'
            # )

    def initWebPdfView(self) -> None:
        """
        Initializes the web view for displaying PDF documents.
        """
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

    def openLocalPdfDoc(self, doc_location: QUrl) -> None:
        """
        Opens a local PDF document.

        @param:
            doc_location: The URL of the PDF document.
        """
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
        """
        Updates the current page number of the PDF document.

        @param:
            page_num: The new page number.
        """
        self.pdf_current_page = page_num

    def hasSelectedText(self) -> bool:
        if len(self.selectedText()) > 0:
            return True
        return False

    def setSelection(self, mode: int, len: int):
        self.page().triggerAction(QWebEnginePage.SelectAll)

    def text(self) -> str:
        return self.pdf_reader.getTextByPageNum(self.pdf_current_page - 1).page_content

    @Slot(QPoint)
    def ContextMenu(self, event: QPoint):
        """
        Handles the custom context menu event.

        @param:
            event: The context menu event.
        """
        menu = CContexMenu(parent=self)
        menu.exec(self.mapToGlobal(event))
