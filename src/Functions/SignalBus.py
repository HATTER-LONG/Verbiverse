from PySide6.QtCore import QObject, Signal


class SignalBus(QObject):
    """Signal bus"""

    switch_page_signal = Signal(str)
    open_url_signal = Signal(str)


signalBus = SignalBus()
print("header")
print(signalBus)
