from CContexMenu import CContexMenu
from ExplainWindow import ExplainWindow
from Functions.LanguageType import ExplainLanguage
from LLM.ExplainWorkerThread import ExplainWorkerThread
from ModuleLogger import logger
from PySide6.QtCore import QPoint, Qt, Slot
from qfluentwidgets import BodyLabel, Flyout


class CBodyLabel(BodyLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.explain_window = None
        self.explain_flyout = None
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
        # TODO: 考虑优化为可以多线程更新, 需要确认下是否有必要？
        if hasattr(self, "worker") and self.worker is not None:
            logger.warning("flyout explain thread is not done")
            return
        self.explain_flyout = explain_flyout
        self.explain_flyout.closed.connect(self.explainClose)
        self.explain_flyout.view.pin_explain_signal.connect(self.pinFlyout)

        self.worker = ExplainWorkerThread(
            selected_text=selected_text,
            all_text=self.text(),
            language_type=language_type,
        )
        self.worker.messageCallBackSignal.connect(self.onExplainResultUpdate)
        self.worker.finished.connect(self.finishedExplain)
        self.worker.start()

    @Slot()
    def finishedExplain(self):
        self.explain_flyout = None
        self.explain_window = None
        self.worker = None

    @Slot(str)
    def onExplainResultUpdate(self, explain: str):
        if self.explain_flyout is not None:
            self.explain_flyout.view.setContent(
                self.explain_flyout.view.getContent() + explain
            )
        elif self.explain_window is not None:
            self.explain_window.setContent(self.explain_window.getContent() + explain)

    @Slot()
    def explainClose(self):
        logger.debug("flyout close")
        self.explain_flyout = None
        if self.explain_window is None:
            self.stopWorker()

    @Slot(str, str)
    def pinFlyout(self, title: str, content: str):
        logger.debug(f"pin flyout {title}")
        self.explain_window = ExplainWindow(title, content)
        self.explain_window.show()
        self.explain_window.close_signal.connect(self.pinWindowClose)

    @Slot()
    def pinWindowClose(self):
        logger.debug("bodylabel window close")
        self.explain_window = None
        if self.explain_flyout is None:
            self.stopWorker()

    def stopWorker(self):
        if self.worker is not None:
            logger.debug("close bodylabel explain thread ... ")
            self.worker.stop()
            self.worker.wait()
            logger.debug("close bodylabel explain thread done !!! ")
