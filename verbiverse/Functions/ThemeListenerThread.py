import darkdetect
from PySide6.QtCore import QObject, QThread, Slot
from qfluentwidgets import (
    Theme,
    setTheme,
)


class ThemeThread(QThread):
    """
    This class is a QThread subclass that listens for changes in the system's theme and updates the application's theme accordingly.

    Attributes:
        parent: The parent QObject of this QThread.

    Methods:
        run(): Overrides the QThread's run method to listen for changes in the system's theme.
        callback(mode: str): A callback function that gets called when the system's theme changes. It updates the application's theme based on the mode.
    """

    def __init__(self, parent: QObject | None = None) -> None:
        """
        Initializes the ThemeThread object.

        Parameters:
            parent: The parent QObject of this QThread.
        """
        super().__init__(parent)

    @Slot()
    def run(self):
        """
        Overrides the QThread's run method to listen for changes in the system's theme.
        """
        darkdetect.listener(self.callback)

    def callback(self, mode: str):
        """
        A callback function that gets called when the system's theme changes. It updates the application's theme based on the mode.

        Parameters:
            mode: A string representing the current system's theme mode. It should be either "Light" or "Dark".
        """
        if mode == "Light":
            setTheme(Theme.LIGHT)
        else:
            setTheme(Theme.DARK)
