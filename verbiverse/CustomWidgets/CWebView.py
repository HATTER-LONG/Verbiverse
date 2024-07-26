import os
import sys
import urllib.parse

from CContexMenu import CContexMenu
from ExplainWindow import ExplainWindow
from Functions.LanguageType import ExplainLanguage
from Functions.LoadPdfText import PdfReader
from Functions.SignalBus import signalBus
from Functions.WebChannelBridge import BridgeClass
from LLM.ExplainWorkerThread import ExplainWorkerThread
from ModuleLogger import logger
from PySide6.QtCore import QMutex, QPoint, Qt, QUrl, Slot
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtWidgets import QMessageBox
from qfluentwidgets import Flyout, isDarkTheme, qconfig
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
        contextMenu(self, event: QPoint): Handles the custom context menu event.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initWebPdfView()
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.contextMenu)

        qconfig.themeChanged.connect(self.themeChanged)

    def initWebPdfView(self) -> None:
        """
        Initializes the web view for displaying PDF documents.
        """
        self.m_fileDialog = None
        script_directory = ""
        if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
            script_directory = sys._MEIPASS
        else:
            script_directory = os.getcwd()
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

        self.pdf_path = None
        self.pdf_current_page = 1
        self.pdf_reader: PdfReader = None
        self.error_message = None

        self.already_connect_loadprocess_signal = False

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
        self.error_message = None
        self.pdf_current_page = 1
        self.pdf_path = None
        self.pdf_reader = None
        self.mutex.unlock()

    def openLocalPdfDoc(self, doc_location: QUrl, page: int = 0):
        """
        Opens a local PDF document.

        @param:
            doc_location: The URL of the PDF document.
        """
        self.clean()
        if doc_location.isLocalFile():
            self.pdf_path = doc_location
            self.pdf_current_page = page
            path = urllib.parse.quote(doc_location.url().encode("utf-8"))
            # Test error load code
            # path = doc_location.url().encode("utf-8")
            logger.info(
                f"open url: [file:///{self.pdf_js_path}?file={path}#page={self.pdf_current_page}]"
            )

            if not self.already_connect_loadprocess_signal:
                self.loadStarted.connect(
                    lambda: signalBus.load_localfile_signal.emit(0)
                )
                self.loadFinished.connect(
                    lambda: signalBus.load_localfile_signal.emit(100)
                )
                self.already_connect_loadprocess_signal = True

            url = QUrl.fromUserInput(
                f"file:///{self.pdf_js_path}?file={path}#page={self.pdf_current_page}"
            )
            self.load(url)
        else:
            message = f"{doc_location} is not a valid local file"
            logger.error(message)
            QMessageBox.critical(self, "Failed to open", message)

    @Slot(int)
    def updatePdfPageNum(self, page_num: int) -> None:
        """
        Updates the current page number of the PDF document.

        @param:
            page_num: The new page number.
        """
        self.pdf_current_page = page_num
        signalBus.update_file_schedule_signal.emit(
            self.pdf_path.toLocalFile(), page_num
        )

    def hasSelectedText(self) -> bool:
        if len(self.selectedText()) > 0:
            return True
        return False

    def setSelection(self, mode: int, len: int):
        self.page().triggerAction(QWebEnginePage.SelectAll)

    def setPdfReader(self, pdf_reader: PdfReader):
        self.pdf_reader = pdf_reader

    def text(self) -> str:
        if self.pdf_reader is None:
            raise Exception("PDF reader not init finished")
        return self.pdf_reader.getTextByPageNum(self.pdf_current_page - 1).page_content

    @Slot(QPoint)
    def contextMenu(self, event: QPoint):
        """
        Handles the custom context menu event.

        @param:
            event: The context menu event.
        """
        menu = CContexMenu(parent=self)
        menu.explain_signal.connect(self.explainSelectText)
        menu.exec(self.mapToGlobal(event))

    @Slot(Flyout, str, ExplainLanguage)
    def explainSelectText(
        self, explain_flyout: Flyout, selected_text: str, type: ExplainLanguage
    ):
        if hasattr(self, "worker") and self.worker is not None:
            logger.warning("flyout explain thread is not done")
            return
        self.explain_flyout = explain_flyout
        self.explain_flyout.view.setTextResource(
            self.pdf_path.toLocalFile() + " -> " + str(self.pdf_current_page)
        )
        self.explain_flyout.closed.connect(self.explainClose)
        self.explain_flyout.view.pin_explain_signal.connect(self.pinFlyout)

        self.explain_window = None

        # TODO: 优化all text 为单词关联语句
        self.worker = ExplainWorkerThread(
            selected_text=selected_text,
            all_text=self.pdf_reader.getTextByPageNum(self.pdf_current_page - 1),
            language_type=type,
        )
        self.worker.messageCallBackSignal.connect(self.onExplainResultUpdate)
        self.worker.finished.connect(self.finishedExplain)
        self.worker.start()

    @Slot()
    def finishedExplain(self):
        self.explain_flyout = None
        self.explain_window = None
        self.worker = None

    @Slot(str)
    def onExplainResultUpdate(self, explain: str):
        if self.explain_flyout is not None:
            self.explain_flyout.view.setContent(
                self.explain_flyout.view.getContent() + explain
            )
        elif self.explain_window is not None:
            self.explain_window.setContent(self.explain_window.getContent() + explain)

    def explainClose(self):
        logger.debug("flyout close")
        self.explain_flyout = None
        if self.explain_window is None:
            self.stopWorker()

    @Slot(str, str, bool)
    def pinFlyout(self, title: str, content: str, already_add: bool):
        logger.debug(f"pin flyout {title} \n content{content}")
        self.explain_window = ExplainWindow(
            title,
            content,
            self.pdf_path.toLocalFile() + " -> " + str(self.pdf_current_page),
            already_add,
        )
        self.explain_window.show()
        self.explain_window.close_signal.connect(self.pinWindowClose)

    @Slot()
    def pinWindowClose(self):
        logger.debug("webview window close")
        self.explain_window = None
        if self.explain_flyout is None:
            self.stopWorker()

    def stopWorker(self):
        if self.worker is not None:
            logger.debug("close webview explain thread ... ")
            self.worker.stop()
            self.worker.wait()
            logger.debug("close webview explain thread done !!! ")
