from PySide6.QtWidgets import QWidget
from UI import Ui_WordsTableInterface


class WordsTableInterface(QWidget, Ui_WordsTableInterface):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
