from PySide6.QtCore import QObject, QUrl, Signal


class SignalBus(QObject):
    """Signal bus"""

    switch_page_signal = Signal(str)
    open_localfile_signal = Signal(QUrl)


signalBus = SignalBus()
print(signalBus)
