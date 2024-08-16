import os

from Functions.WordBookDatabase import Word, WordsBookDatabase
from PySide6.QtCore import QModelIndex, Qt
from PySide6.QtGui import QPalette
from PySide6.QtWidgets import (
    QHBoxLayout,
    QHeaderView,
    QStyleOptionViewItem,
    QTableWidgetItem,
    QWidget,
)
from qfluentwidgets import (
    TableItemDelegate,
    TableWidget,
    isDarkTheme,
)


class CustomTableItemDelegate(TableItemDelegate):
    """Custom table item delegate"""

    def initStyleOption(self, option: QStyleOptionViewItem, index: QModelIndex):
        super().initStyleOption(option, index)
        if index.column() != 1:
            return

        if isDarkTheme():
            option.palette.setColor(QPalette.Text, Qt.white)
            option.palette.setColor(QPalette.HighlightedText, Qt.white)
        else:
            option.palette.setColor(QPalette.Text, Qt.red)
            option.palette.setColor(QPalette.HighlightedText, Qt.red)


class WordsTable(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.hBoxLayout = QHBoxLayout(self)
        self.tableView = TableWidget(self)
        self.tableView.setBorderVisible(True)
        self.tableView.setBorderRadius(8)

        self.tableView.setWordWrap(False)
        # self.tableView.setRowCount(1000000)
        self.tableView.setColumnCount(6)

        self.tableView.verticalHeader().hide()
        self.tableView.setHorizontalHeaderLabels(
            [
                self.tr("Word"),
                self.tr("Explain"),
                self.tr("Examples"),
                self.tr("AddTime"),
                self.tr("Review"),
                self.tr("Resource"),
            ]
        )
        self.tableView.resizeColumnsToContents()
        self.tableView.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )
        # self.tableView.setSortingEnabled(True)

        # self.setStyleSheet("Demo{background: rgb(255, 255, 255)} ")
        self.hBoxLayout.setContentsMargins(10, 10, 10, 10)
        self.hBoxLayout.addWidget(self.tableView)

    def addWord(self, word, explain, example, added_on, next_review_on, resource):
        rowPosition = self.tableView.rowCount()
        self.tableView.insertRow(rowPosition)

        self.tableView.setItem(rowPosition, 0, QTableWidgetItem(word))
        self.tableView.setItem(rowPosition, 1, QTableWidgetItem(explain))
        self.tableView.setItem(rowPosition, 2, QTableWidgetItem(example))
        self.tableView.setItem(rowPosition, 3, QTableWidgetItem(added_on))
        self.tableView.setItem(rowPosition, 4, QTableWidgetItem(next_review_on))
        self.tableView.setItem(rowPosition, 5, QTableWidgetItem(resource))

    def updateTable(self):
        db = WordsBookDatabase()
        words: map[Word] = db.updateWordsMap()
        self.tableView.setRowCount(0)
        for word in words:
            wordobj = words[word]
            self.addWord(
                wordobj.word,
                wordobj.explain,
                wordobj.example,
                wordobj.added_on,
                wordobj.next_review_on,
                os.path.basename(wordobj.resource),
            )
