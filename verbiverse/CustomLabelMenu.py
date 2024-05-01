from PySide6.QtCore import Slot
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu
from TranslateInfoWindow import TranslateInfoWin, TranslationType


class LabelMenu(QMenu):
    def __init__(self, parent, selected_text, all_text):
        super().__init__(parent)
        self.user_selected_text = selected_text
        self.all_text = all_text
        self.action3 = QAction("加入单词本", self)
        self.action3.triggered.connect(self.handle_addDatabase)
        self.addAction(self.action3)

        self.action1 = QAction("解释(EN)", self)
        self.action1.triggered.connect(self.handle_transEN)
        self.addAction(self.action1)

        self.action2 = QAction("解释(CN)", self)
        self.action2.triggered.connect(self.handle_transCN)
        self.addAction(self.action2)

    @Slot()
    def handle_transEN(self):
        self.win = TranslateInfoWin(
            TranslationType.TARGET_LANGUAGE, self.user_selected_text, self.all_text
        )
        self.win.show()

    @Slot()
    def handle_transCN(self):
        self.win = TranslateInfoWin(
            TranslationType.MOTHER_TONGUE, self.user_selected_text, self.all_text
        )
        self.win.show()

    @Slot()
    def handle_addDatabase(self):
        pass
