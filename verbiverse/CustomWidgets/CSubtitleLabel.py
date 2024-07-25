import re

from ModuleLogger import logger
from PySide6.QtCore import QPoint, QSize, Qt, Signal, Slot
from PySide6.QtGui import QTextCharFormat, QTextCursor
from PySide6.QtWidgets import QTextBrowser


class CSubtitleLabel(QTextBrowser):
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
        self.select_word = None
        self.cursor = QTextCursor(self.document())
        self.highlight_format = QTextCharFormat()
        self.highlight_format.setBackground(Qt.gray)
        self.document().contentsChanged.connect(self.updateSize)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._onContextMenuRequested)

    def mouseDoubleClickEvent(self, event):
        if len(self.select_word) > 2 and self.isWord(self.select_word):
            logger.info(f"double click on word: {self.select_word}")
            self.explain_signal.emit(self.select_word)

        super().mouseDoubleClickEvent(event)

    @Slot(QPoint)
    def _onContextMenuRequested(self, event: QPoint) -> None:
        logger.info(f"context menu requested: [{event}]")

    def isWord(self, word: str):
        return bool(re.search(r"[a-zA-Z]", word)) and not bool(
            re.match(r"^[^\w\s]+$", word)
        )

    def updateSize(self):
        doc_size = self.document().size().toSize()
        new_size = QSize(
            doc_size.width() + 10,
            doc_size.height(),
        )
        self.setMaximumSize(new_size)
        self.setMinimumSize(new_size)

    def mouseMoveEvent(self, event):
        if event.pos().x() <= 2 or event.pos().y() <= 2:
            self.cursor.select(QTextCursor.Document)
            self.cursor.setCharFormat(QTextCharFormat())
            super().mouseMoveEvent(event)
            return

        text_cursor = self.cursorForPosition(event.pos())
        text_cursor.select(QTextCursor.WordUnderCursor)
        word = text_cursor.selectedText()
        if word is not None and (word != self.select_word or self.select_word is None):
            self.select_word = word
            self.cursor.select(QTextCursor.Document)
            self.cursor.setCharFormat(QTextCharFormat())
            text_cursor.setCharFormat(self.highlight_format)
            logger.debug(f"select word: [{self.select_word}]")
        super().mouseMoveEvent(event)
