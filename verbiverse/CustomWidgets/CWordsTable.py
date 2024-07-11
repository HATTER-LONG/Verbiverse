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
        self.tableView.setRowCount(30)
        self.tableView.setColumnCount(5)

        self.tableView.verticalHeader().hide()
        self.tableView.setHorizontalHeaderLabels(
            [
                self.tr("Word"),
                self.tr("Explain"),
                self.tr("Examples"),
                self.tr("AddTime"),
                self.tr("Review"),
            ]
        )
        self.tableView.resizeColumnsToContents()
        # self.tableView.horizontalHeader().setSectionResizeMode(
        #     QHeaderView.Custom
        # )
        # self.tableView.setSortingEnabled(True)

        # self.setStyleSheet("Demo{background: rgb(255, 255, 255)} ")
        self.hBoxLayout.setContentsMargins(10, 10, 10, 10)
        self.hBoxLayout.addWidget(self.tableView)
        self.db = WordsBookDatabase()
        self.updateTable()

    def getColumDataFromWord(self, index: int, word: Word):
        if index == 0:
            return word.word
        elif index == 1:
            return word.explain
        elif index == 2:
            return word.example
        elif index == 3:
            return word.added_on
        elif index == 4:
            return word.next_review_on

    def updateTable(self):
        words: map[Word] = self.db.getAllWords()
        for word in words:
            print(words[word])
        for i, word in enumerate(words):
            for j in range(5):
                self.tableView.setItem(
                    i, j, QTableWidgetItem(self.getColumDataFromWord(j, words[word]))
                )
