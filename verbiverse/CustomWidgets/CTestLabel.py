from PySide6.QtCore import Signal
from PySide6.QtWidgets import QTextBrowser


class CTestLabel(QTextBrowser):
    explain_signal = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(
            """
            QTextBrowser {
                color: black;
                border-radius: 10px;
                background-color: lightgray;
                border: 1px solid black;
            }
        """
        )
