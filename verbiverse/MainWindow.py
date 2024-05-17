import os
import sys

from ChatLLM import ChatChain
from ChatLLMWithHistory import ChatLLMWithCustomHistory
from ChatWorkerThread import ChatWorkThread
from CustomLabelMenu import LabelMenu
from LoadPdfText import PdfReader
from MessageBoxWidget import MessageBox
from PySide6.QtCore import QPoint, QStandardPaths, Qt, QUrl, Slot
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFileDialog,
    QMainWindow,
    QMessageBox,
    QVBoxLayout,
    QWidget,
)
from resources import resources_rc  # noqa: F401
from UI import Ui_MainWindow
from WebChannelBridge import BridgeClass


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Set window title
        # self.setWindowTitle("聊天界面")

        # Set chat scroll arean laytou
        self.messages_list_widget = QWidget(self.chat_scroll_area)
        self.messages_list = QVBoxLayout(self.messages_list_widget)
        self.messages_list.setAlignment(Qt.AlignTop)
        self.messages_list_widget.setContentsMargins(0, 0, 0, 0)

        # Link messages list to scroll arean
        self.chat_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.chat_scroll_area.setWidgetResizable(True)
        self.chat_scroll_area.setWidget(self.messages_list_widget)

        # Set user input widget
        self.user_text_edit.setPlaceholderText("输入消息")
        self.user_send_button.clicked.connect(self.sendMessage)
        self.user_check_button.clicked.connect(self.checkMessage)

        # LLM Chat chain
        self.chat_chain = ChatChain()
        self.checker = ChatLLMWithCustomHistory()

        self.chat_worker = ChatWorkThread()
        self.chat_worker.finished.connect(self.updateFinish)
        self.chat_worker.started.connect(self.updateStart)
        self.chat_worker.setChain(self.chat_chain)
        self.chat_worker.messageCallBackSignal.connect(self.update_label)

        self.check_worker = ChatWorkThread()
        self.check_worker.finished.connect(self.checkFinish)
        self.check_worker.started.connect(self.checkStart)
        self.check_worker.setChain(self.checker)
        self.check_worker.messageCallBackSignal.connect(self.update_label)

        # will updated by chat worker thread
        self.need_update_label = None

        self.initWebView()
        # Test code
        # self.message_label1 = MessageBox("image", "User")
        # self.message_label1.setMessageText(
        #     "This is a test message, it's helpful to dev new function avoid input ever time"
        # )
        # self.messages_list.addWidget(self.message_label1)  # Add to QVBoxLayout

    def initWebView(self) -> None:
        self.m_fileDialog = None
        script_directory = os.path.dirname(os.path.abspath(__file__))
        self.pdf_js_path = os.path.join(
            script_directory, "PDF_js", "web", "viewer.html"
        ).replace("\\", "/")
        self.pdf_path = ""
        self.current_page = 1

        self.channel = QWebChannel()
        self.bridgeClass = BridgeClass()
        self.bridgeClass.pageNumChangedSignal.connect(self.updatePageNum)
        self.channel.registerObject("bridgeClass", self.bridgeClass)

        self.viewer_widget.page().setWebChannel(self.channel)
        self.viewer_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.viewer_widget.customContextMenuRequested.connect(self.pdfContextMenu)

        self.pdf_reader: PdfReader = None

        #### TEST CODE
        self.open(
            QUrl(
                "file:///Users/caolei/Downloads/01 Dinosaurs Before Dark - Mary Pope Osborne.pdf"
            )
        )

    @Slot(int)
    def updatePageNum(self, page_num: int) -> None:
        self.current_page = page_num

    @Slot(QPoint)
    def pdfContextMenu(self, event: QPoint):
        selected_text = self.viewer_widget.selectedText()

        if len(selected_text) == 0:
            return
        all_text = self.pdf_reader.getTextByPageNum(self.current_page - 1)

        menu = LabelMenu(self, selected_text, all_text)
        menu.popup(self.mapToGlobal(event))

    @Slot()
    def updateFinish(self) -> None:
        self.user_send_button.setEnabled(True)
        self.messages_list.update()
        self.need_update_label = None

    @Slot()
    def updateStart(self) -> None:
        self.messages_list.update()
        # QApplication.processEvents()
        # self.vscrollbar.setValue(self.vscrollbar.maximum())

    @Slot()
    def sendMessage(self) -> None:
        if self.need_update_label is not None:
            return
        self.user_send_button.setEnabled(False)
        message_text = self.user_text_edit.toPlainText()
        self.user_text_edit.setText("")
        if message_text:
            message_label = MessageBox("image", "User")
            message_label.setMessageText(message_text)
            self.messages_list.addWidget(message_label)  # Add to QVBoxLayout

            self.need_update_label = MessageBox("image", "Robot")
            self.messages_list.addWidget(self.need_update_label)  # Add to QVBoxLayout

            self.chat_worker.setMessage(message_text)
            self.chat_worker.start()

    @Slot(str)
    def update_label(self, message: str) -> None:
        if self.need_update_label is not None:
            self.need_update_label.setMessageText(
                self.need_update_label.getMessageText() + message
            )

    @Slot()
    def checkMessage(self) -> None:
        if self.need_update_label is not None:
            return
        if len(self.user_text_edit.toPlainText()) == 0:
            return
        self.checker.setChatHistoryForChain(
            self.chat_chain.demo_ephemeral_chat_history_for_chain
        )

        self.need_update_label = MessageBox("image", "Robot")
        self.messages_list.addWidget(self.need_update_label)  # Add to QVBoxLayout

        self.check_worker.setChain(self.checker)
        self.check_worker.setMessage(self.user_text_edit.toPlainText())
        self.check_worker.start()

    @Slot()
    def checkStart(self) -> None:
        pass

    @Slot()
    def checkFinish(self) -> None:
        self.need_update_label = None

    def open(self, doc_location: QUrl):
        if doc_location.isLocalFile():
            self.pdf_path = doc_location.url()
            print(doc_location.toLocalFile())
            self.pdf_reader = PdfReader(doc_location.toLocalFile())
            self.viewer_widget.load(
                QUrl.fromUserInput(
                    f"file:///{self.pdf_js_path}?file={self.pdf_path}#page={self.current_page}"
                )
            )
        else:
            message = f"{doc_location} is not a valid local file"
            print(message, file=sys.stderr)
            QMessageBox.critical(self, "Failed to open", message)

    @Slot()
    def on_actionPrevious_Page_triggered(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.viewer_widget.load(
                QUrl.fromUserInput(
                    f"file:///{self.pdf_js_path}?file={self.pdf_path}#page={self.current_page}"
                )
            )

    @Slot()
    def on_actionNext_Page_triggered(self):
        self.current_page += 1
        self.viewer_widget.load(
            QUrl.fromUserInput(
                f"file:///{self.pdf_js_path}?file={self.pdf_path}#page={self.current_page}"
            )
        )

    @Slot()
    def on_actionOpen_triggered(self):
        if not self.m_fileDialog:
            directory = QStandardPaths.writableLocation(
                QStandardPaths.DocumentsLocation
            )
            self.m_fileDialog = QFileDialog(self, "Choose a PDF", directory)
            self.m_fileDialog.setAcceptMode(QFileDialog.AcceptOpen)
            self.m_fileDialog.setMimeTypeFilters(["application/pdf"])
        if self.m_fileDialog.exec() == QDialog.Accepted:
            to_open = self.m_fileDialog.selectedUrls()[0]
            if to_open.isValid():
                self.open(to_open)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec()


if __name__ == "__main__":
    main()
