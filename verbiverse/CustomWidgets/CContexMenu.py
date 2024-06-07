from enum import Enum

from ExplainFlyoutView import ExplainFlyoutView
from ModuleLogger import logger
from PySide6.QtCore import Signal, Slot
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QLabel
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import (
    Flyout,
    FlyoutAnimationType,
    MenuAnimationType,
    RoundMenu,
)


class ExplainLanguage(Enum):
    TARGET_LANGUAGE = 1
    MOTHER_TONGUE = 2

    def __eq__(self, other):
        if type(self).__qualname__ != type(other).__qualname__:
            return NotImplemented
        return self.name == other.name and self.value == other.value

    def __hash__(self):
        return hash((type(self).__qualname__, self.name))


class CContexMenu(RoundMenu):
    """Label context menu"""

    explain_signal = Signal(Flyout, str, ExplainLanguage)

    def __init__(self, parent):
        super().__init__("", parent)
        self.selected_text = parent.selectedText()
        self.explain = QAction(
            FIF.CHAT.icon(),
            self.tr("Explain"),
            self,
            triggered=self._onExplainTL,
        )

        self.explain_ml = QAction(
            FIF.CHAT.icon(),
            self.tr("Explain_ML"),
            self,
            triggered=self._onExplainML,
        )

        self.copyAct = QAction(
            FIF.COPY.icon(),
            self.tr("Copy"),
            self,
            shortcut="Ctrl+C",
            triggered=self._onCopy,
        )
        self.selectAllAct = QAction(
            self.tr("Select all"), self, shortcut="Ctrl+A", triggered=self._onSelectAll
        )

    @Slot()
    def _onCopy(self):
        QApplication.clipboard().setText(self.selected_text)

    @Slot()
    def _onSelectAll(self):
        self.label().setSelection(0, len(self.label().text()))

    @Slot()
    def _onExplainML(self):
        self._onExplain(ExplainLanguage.MOTHER_TONGUE)

    @Slot()
    def _onExplainTL(self):
        self._onExplain(ExplainLanguage.TARGET_LANGUAGE)

    def _onExplain(self, type: ExplainLanguage):
        self.flyout = Flyout.make(
            ExplainFlyoutView(self.selected_text),
            self.pos(),
            self,
            aniType=FlyoutAnimationType.NONE,
        )
        self.explain_signal.emit(self.flyout, self.selected_text, type)

    def label(self) -> QLabel:
        return self.parent()

    def exec(self, pos, ani=True, aniType=MenuAnimationType.DROP_DOWN):
        if self.label().hasSelectedText():
            self.addActions(
                [self.explain, self.explain_ml, self.copyAct, self.selectAllAct]
            )
        else:
            self.addAction(self.selectAllAct)

        return super().exec(pos, ani, aniType)
