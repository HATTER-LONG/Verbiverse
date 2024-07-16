from concurrent.futures import CancelledError

from Functions.LoadPdfText import PdfReader
from Functions.SignalBus import signalBus
from ModuleLogger import logger
from PySide6.QtCore import (
    QThread,
    QUrl,
    Signal,
    Slot,
)
from PySide6.QtWidgets import QApplication, QWidget
from ReadAndChatWidget_ui import Ui_ReadAndChatWidget


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
            error_message = f"load pdf file to analyse error: [{error}], please check pdf file type."
            logger.error(error_message)
            signalBus.error_signal.emit(error_message)
        else:
            logger.info(f"finish pdf load: [{self.pdf_loc_path}]")


class ReadAndChatWidget(QWidget, Ui_ReadAndChatWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setupUi(self)

        # #### TEST CODE
        # self.web_view.openLocalPdfDoc(
        #     QUrl(
        #         "file:///Users/caolei/Downloads/01 Dinosaurs Before Dark - Mary Pope Osborne.pdf"
        #     )
        # )

        self.loader: LoadPdfText = None
        self.pdf_reader = None
        self.local_file_path = None
        signalBus.open_localfile_signal.connect(self.openLocalPdfDoc)

    def clean(self):
        if self.loader is not None and self.loader.isRunning():
            self.loader.stopLoad()
            signalBus.warning_signal.emit(
                self.tr("Need wait last loader stop, maybe cost some time!!!")
            )
            while not self.loader.wait(100):
                QApplication.processEvents()

        self.loader = None
        self.pdf_reader = None
        self.local_file_path = None

    @Slot(QUrl)
    def openLocalPdfDoc(self, doc_location: QUrl):
        self.clean()

        self.local_file_path = doc_location
        self.loader = LoadPdfText(doc_location.toLocalFile())
        self.loader.load_pdf_finish.connect(self.updatePdfReader)
        self.loader.start()
        self.web_view.openLocalPdfDoc(doc_location)

    @Slot(PdfReader)
    def updatePdfReader(self, reader: PdfReader):
        self.pdf_reader = reader
        self.web_view.setPdfReader(reader)
        path = self.local_file_path.toLocalFile()
        logger.info(
            f"read pdf [{path}] finish get [{len(self.pdf_reader.pages)}] pages"
        )
