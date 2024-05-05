import re

from PySide6.QtCore import Slot
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu
from TranslateInfoWindow import TranslateInfoWin, TranslationType
from WordsBookDatabase import WordsBookDatabase


# TODO: 多语言兼容
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
        self.db = WordsBookDatabase()

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

    """
    使用 python 实现如下功能
    类成员有 selected_text 为选中的单词或短语，all_text 则是选中单词的原始句子或者文章段落
    需要从原始句子中截取第一次出现选中的单词短语的完整句子作为例句

    """

    @Slot()
    def handle_addDatabase(self):
        sentences = re.split(r"[.!?]\s+", self.all_text)
        example = ""
        for sentence in sentences:
            if self.user_selected_text in sentence:
                example = sentence.strip()
        self.db.add_word(self.user_selected_text, example)
