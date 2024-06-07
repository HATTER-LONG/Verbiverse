from CContexMenu import CContexMenu
from Functions.LanguageType import ExplainLanguage
from LLM.ExplainWorkerThread import ExplainWorkerThread
from ModuleLogger import logger
from PySide6.QtCore import QPoint, Qt, Slot
from qfluentwidgets import BodyLabel, Flyout


class CBodyLabel(BodyLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContextMenuPolicy(Qt.CustomContextMenu)

    @Slot(QPoint)
    def _onContextMenuRequested(self, event: QPoint) -> None:
        menu = CContexMenu(parent=self)
        menu.explain_signal.connect(self.explainSelectText)
        menu.exec(self.mapToGlobal(event))

    @Slot(Flyout, str, ExplainLanguage)
    def explainSelectText(
        self, explain_flyout: Flyout, selected_text: str, language_type: ExplainLanguage
    ):
        self.explain_flyout = explain_flyout
        self.explain_flyout.closed.connect(self.explainClose)

        logger.debug(language_type == ExplainLanguage.TARGET_LANGUAGE)
        self.worker = ExplainWorkerThread(
            selected_text=selected_text,
            all_text=self.text(),
            language_type=language_type,
        )
        self.worker.messageCallBackSignal.connect(self.onExplainResultUpdate)
        self.worker.start()

    @Slot(str)
    def onExplainResultUpdate(self, explain: str):
        if self.explain_flyout is None:
            return
        self.explain_flyout.view.setContent(
            self.explain_flyout.view.getContent() + explain
        )

    def explainClose(self):
        logger.debug("close bodylabel explain thread ... ")
        self.explain_flyout = None
        self.worker.stop()
        self.worker.wait()
        logger.debug("close bodylabel explain thread done !!! ")
