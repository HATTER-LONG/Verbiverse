from PySide6.QtCore import QObject, Signal, Slot


class BridgeClass(QObject):
    """bridge with webview"""
    pageNumChangedSignal = Signal(int)
    pageOpenErrorSignal = Signal(str)

    @Slot(int)
    def pageChanged(self, page_num):
        self.pageNumChangedSignal.emit(page_num)

    @Slot(str)
    def openFailed(self, err: str):
        if "[ERROR]" in err:
            self.pageOpenErrorSignal.emit(err)
