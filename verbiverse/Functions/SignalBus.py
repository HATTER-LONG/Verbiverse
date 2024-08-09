from ModuleLogger import logger
from PySide6.QtCore import QObject, QUrl, Signal


class SignalBus(QObject):
    """Signal bus"""

    # localfile ctrl signal
    open_localfile_signal = Signal(QUrl, int)
    open_video_signal = Signal(QUrl, int)
    load_localfile_signal = Signal(int)
    switch_page_signal = Signal(str)
    update_file_schedule_signal = Signal(str, int)

    # message signal
    info_signal = Signal(str)
    warning_signal = Signal(str)
    error_signal = Signal(str)
    status_signal = Signal(str, str)

    # setting signal
    mica_enable_change_signal = Signal(bool)
    llm_config_change_signal = Signal()


signalBus = SignalBus()
logger.debug(signalBus)
