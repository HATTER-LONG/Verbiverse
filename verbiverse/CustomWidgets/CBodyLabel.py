from CContexMenu import CContexMenu
from ModuleLogger import logger
from PySide6.QtCore import (
    QPoint,
    Qt,
    Slot,
)
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

    @Slot(Flyout)
    def explainSelectText(self, explain_flyout: Flyout):
        self.explain_flyout = explain_flyout
        self.explain_flyout.closed.connect(self.explainClose)
        # self.worker = ChatWorkThread()
        # self.worker.setChain(self.chain)
        # self.worker.setMessage(msg)
        # self.worker.messageCallBackSignal.connect(self.onTranslateResultUpdate)
        # self.worker.started.connect(self.workerStart)
        # self.worker.finished.connect(self.workerStop)
        # self.worker.start()

    def explainClose(self):
        logger.info("close bodylabel explain")
        self.explain_flyout = None
