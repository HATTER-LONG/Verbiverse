from ModuleLogger import logger
from PySide6.QtCore import QPoint, QSize, Qt, Slot
from PySide6.QtGui import QContextMenuEvent, QTextCharFormat, QTextCursor
from PySide6.QtWidgets import QTextBrowser


class CSubtitleLabel(QTextBrowser):
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

        self.cursor = QTextCursor(self.document())
        self.highlight_format = QTextCharFormat()
        self.highlight_format.setBackground(Qt.gray)
        self.document().contentsChanged.connect(self.updateSize)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._onContextMenuRequested)

    @Slot(QPoint)
    def _onContextMenuRequested(self, event: QPoint) -> None:
        logger.info(f"context menu requested: [{event}]")

    def contextMenuEvent(self, event: QContextMenuEvent):
        event.ignore()

    def updateSize(self):
        doc_size = self.document().size().toSize()
        new_size = QSize(
            doc_size.width() + 10,
            doc_size.height() + 10,
        )
        self.setMaximumSize(new_size)
        self.setMinimumSize(new_size)

    def mouseMoveEvent(self, event):
        logger.info(f"mouse move event: [{event}]")
        if event.pos().x() <= 10 or event.pos().y() <= 10:
            self.cursor.select(QTextCursor.Document)
            self.cursor.setCharFormat(QTextCharFormat())
            super().mouseMoveEvent(event)
            return
        self.cursor.select(QTextCursor.Document)
        self.cursor.setCharFormat(QTextCharFormat())

        text_cursor = self.cursorForPosition(event.pos())
        text_cursor.select(QTextCursor.WordUnderCursor)
        select_word = text_cursor.selectedText()
        if select_word:
            text_cursor.setCharFormat(self.highlight_format)

        logger.info(f"select word: [{select_word}]")
        super().mouseMoveEvent(event)
