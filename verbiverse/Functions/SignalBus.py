from PySide6.QtCore import QObject, QUrl, Signal


class SignalBus(QObject):
    """Signal bus"""

    switch_page_signal = Signal(str)

    open_localfile_signal = Signal(QUrl)
    load_localfile_signal = Signal(int)

    info_signal = Signal(str)
    warning_signal = Signal(str)
    error_signal = Signal(str)


signalBus = SignalBus()
print(signalBus)
