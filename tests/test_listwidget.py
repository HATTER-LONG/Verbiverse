import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from verbiverse.CustomWidgets import CFileListWidget


class FileListWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("File List")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.listWidget = CFileListWidget()
        self.listWidget.itemDoubleClicked.connect(self.openFile)
        self.layout.addWidget(self.listWidget)

        self.button = QPushButton("Download")
        self.button.clicked.connect(self.onDownload)
        self.layout.addWidget(self.button)

    def openFile(self, item: QListWidgetItem):
        print(item.text())
        print(item.data(Qt.UserRole))

    def addFile(self, file_path):
        self.listWidget.addFile(file_path)

    def onDownload(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open file", "/")

        if filename:
            self.addFile(filename)


def main():
    app = QApplication(sys.argv)

    widget = FileListWidget()
    widget.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
