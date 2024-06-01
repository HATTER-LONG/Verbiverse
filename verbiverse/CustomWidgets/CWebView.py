import os
import sys
import urllib.parse
from concurrent.futures import CancelledError

from CContexMenu import CContexMenu
from Functions.LoadPdfText import PdfReader
from Functions.SignalBus import signalBus
from Functions.WebChannelBridge import BridgeClass
from ModuleLogger import logger
from PySide6.QtCore import QMutex, QPoint, Qt, QThread, QUrl, Signal, Slot
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtWidgets import QApplication, QMessageBox
from qfluentwidgets import isDarkTheme, qconfig
from qframelesswindow.webengine import FramelessWebEngineView


class LoadPdfText(QThread):
    """Signal to load pdf text"""

    load_pdf_finish = Signal(PdfReader)

    def __init__(self, pdf_loc_path: str):
        super().__init__()
        self.pdf_loc_path = pdf_loc_path
        self.stop = False

    def stopLoad(self):
        logger.info(f"stop load pdf: [{self.pdf_loc_path}]")
        self.loader.cancel()

    def run(self):
        logger.info(f"ready to load pdf by new process: [{self.pdf_loc_path}]")
        try:
            self.loader = PdfReader(self.pdf_loc_path)
            self.loader.load()
            self.load_pdf_finish.emit(self.loader)
        except CancelledError:
            logger.info(f"already cancel current load: [{self.pdf_loc_path}]")
        except Exception as error:
            logger.error(f"load pdf error: [{error}]")
        else:
            logger.info(f"finish pdf load: [{self.pdf_loc_path}]")


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

    def initWebPdfView(self) -> None:
        """
        Initializes the web view for displaying PDF documents.
        """
        self.m_fileDialog = None
        script_directory = os.path.dirname(os.path.abspath(__file__))
        self.pdf_js_path = os.path.join(
            script_directory, "PDF_js", "web", "viewer.html"
        ).replace("\\", "/")

        self.__channel = QWebChannel()
        self.__bridge_class = BridgeClass()
        self.__bridge_class.pageNumChangedSignal.connect(self.updatePdfPageNum)
        self.__bridge_class.pageOpenErrorSignal.connect(self.updateOpenStatus)
        self.__channel.registerObject("bridgeClass", self.__bridge_class)
        self.page().setWebChannel(self.__channel)
        self.mutex = QMutex()

        self.loader: LoadPdfText = None
        self.pdf_path = None
        self.pdf_current_page = 1
        self.pdf_reader: PdfReader = None
        self.error_message = None

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

    @Slot(str)
    def updateOpenStatus(self, error_message):
        if self.error_message != error_message:
            signalBus.error_signal.emit(error_message)
            logger.error(
                f"get a new error which need to clean webview: [{error_message}]"
            )
            self.clean()
            self.error_message = error_message

    def clean(self):
        self.mutex.lock()
        if self.loader is not None and self.loader.isRunning():
            self.loader.stopLoad()
            signalBus.warning_signal.emit(
                self.tr("Need wait last loader stop, maybe cost some time!!!")
            )
            while not self.loader.wait(100):
                QApplication.processEvents()

        self.loader = None
        self.error_message = None
        self.pdf_current_page = 1
        self.pdf_path = None
        self.pdf_reader = None
        self.mutex.unlock()

    def openLocalPdfDoc(self, doc_location: QUrl):
        """
        Opens a local PDF document.

        @param:
            doc_location: The URL of the PDF document.
        """
        self.clean()
        if doc_location.isLocalFile():
            self.pdf_path = urllib.parse.quote(doc_location.url().encode("utf-8"))
            # Test error load code
            # self.pdf_path = doc_location.url().encode("utf-8")
            self.loader = LoadPdfText(doc_location.toLocalFile())
            self.loader.load_pdf_finish.connect(self.updatePdfReader)
            self.loader.start()
            logger.info(
                f"open url: [file:///{self.pdf_js_path}?file={self.pdf_path}#page={self.pdf_current_page}]"
            )

            self.loadStarted.connect(lambda: signalBus.load_localfile_signal.emit(0))
            self.loadFinished.connect(lambda: signalBus.load_localfile_signal.emit(100))

            url = QUrl.fromUserInput(
                f"file:///{self.pdf_js_path}?file={self.pdf_path}#page={self.pdf_current_page}"
            )
            self.load(url)
        else:
            message = f"{doc_location} is not a valid local file"
            logger.error(message)
            QMessageBox.critical(self, "Failed to open", message)

    @Slot(PdfReader)
    def updatePdfReader(self, reader: PdfReader):
        self.pdf_reader = reader
        logger.info(
            f"read pdf [{self.pdf_path}] finish get [{len(self.pdf_reader.pages)}] pages"
        )

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
