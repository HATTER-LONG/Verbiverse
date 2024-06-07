from ExplainFlyoutView import ExplainFlyoutView
from PySide6.QtCore import Signal
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QLabel
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import (
    Flyout,
    FlyoutAnimationType,
    MenuAnimationType,
    RoundMenu,
)


class CContexMenu(RoundMenu):
    """Label context menu"""

    explain_signal = Signal(Flyout)

    def __init__(self, parent):
        super().__init__("", parent)
        print("select context")
        self.selectedText = parent.selectedText()
        self.explain = QAction(
            FIF.CHAT.icon(),
            self.tr("Explain"),
            self,
            triggered=self._onExplain,
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

    def _onCopy(self):
        QApplication.clipboard().setText(self.selectedText)

    def _onSelectAll(self):
        self.label().setSelection(0, len(self.label().text()))

    def _onExplain(self):
        self.flyout = Flyout.make(
            ExplainFlyoutView("test"),
            self.pos(),
            self,
            aniType=FlyoutAnimationType.NONE,
        )
        self.flyout.closed.connect(self._explainFlyoutClosed)
        self.explain_signal.emit(self.flyout)

    def _explainFlyoutClosed(self):
        print("already closed")

    def label(self) -> QLabel:
        return self.parent()

    def exec(self, pos, ani=True, aniType=MenuAnimationType.DROP_DOWN):
        if self.label().hasSelectedText():
            self.addActions([self.explain, self.copyAct, self.selectAllAct])
        else:
            self.addAction(self.selectAllAct)

        return super().exec(pos, ani, aniType)
