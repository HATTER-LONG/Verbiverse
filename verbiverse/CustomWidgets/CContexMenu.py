from ExplainFlyoutView import ExplainFlyoutView
from Functions.LanguageType import ExplainLanguage
from Functions.SignalBus import signalBus
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
        self.play_audio = QAction(
            FIF.VOLUME.icon(),
            self.tr("Play Audio"),
            self,
            triggered=self._onPlayAudio,
        )

        self.explain_ml = QAction(
            FIF.CHAT.icon(),
            self.tr("Explain"),
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
    def _onPlayAudio(self):
        signalBus.play_audio_signal.emit(self.selected_text)

    @Slot()
    def _onExplainTL(self):
        self._onExplain(ExplainLanguage.TARGET_LANGUAGE)

    def _onExplain(self, type: ExplainLanguage):
        # screen = QApplication.primaryScreen()
        # screen_geometry = screen.geometry()
        # window = self.mapToGlobal(self.pos())
        pos = self.pos()
        pos.setX(pos.x() - 200)
        self.flyout = Flyout.make(
            ExplainFlyoutView(self.selected_text),
            pos,
            self,
            aniType=FlyoutAnimationType.DROP_DOWN,
        )
        self.explain_signal.emit(self.flyout, self.selected_text, type)

    def label(self) -> QLabel:
        return self.parent()

    def exec(self, pos, ani=True, aniType=MenuAnimationType.DROP_DOWN):
        if self.label().hasSelectedText():
            self.addActions(
                [self.explain_ml, self.play_audio, self.copyAct, self.selectAllAct]
            )
        else:
            self.addAction(self.selectAllAct)

        return super().exec(pos, ani, aniType)
