from PySide6.QtCore import QObject, Signal, Slot


class BridgeClass(QObject):
    pageNumChangedSignal = Signal(int)

    @Slot(int)
    def pageChanged(self, page_num):
        self.pageNumChangedSignal.emit(page_num)
