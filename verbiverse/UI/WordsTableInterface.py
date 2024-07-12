from PySide6.QtWidgets import QWidget
from qfluentwidgets import FluentIcon as FIF
from UI import Ui_WordsTableInterface


class WordsTableInterface(QWidget, Ui_WordsTableInterface):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.refresh.setIcon(FIF.SYNC)
        self.refresh.clicked.connect(self.words_table.updateTable)
