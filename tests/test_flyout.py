import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QWidget,
)
from qfluentwidgets import (
    Flyout,
    FlyoutAnimationType,
    PushButton,
)

import verbiverse  # noqa: F401
from verbiverse.CustomWidgets.ExplainFlyoutView import ExplainFlyoutView
from verbiverse.resources import resources_rc  # noqa: F401


class Demo(QWidget):
    def __init__(self):
        super().__init__()
        self.button = PushButton("Click Me", self)
        self.button.clicked.connect(self.showFlyout)

        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.addWidget(self.button, 0, Qt.AlignCenter)
        self.resize(600, 500)

    def showFlyout(self):
        pos = self.mapToGlobal(self.button.pos())
        pos.setX(pos.x() - 150)
        self.flyout = Flyout.make(
            ExplainFlyoutView("mytesttitle"),
            pos,
            self,
            aniType=FlyoutAnimationType.NONE,
        )
        msg = """
1234567890 ab cd efg hijk lmn opq rstuvwx yzABC DEFGHI JKLMNO PQRSTUVWXYZ
1234567890 abcdefghijk lmn opq rstuvwx yzABCDE FGHI JKLMNOPQR STUV WXYZ
        """
        self.flyout.view.setContent(msg)


def main():
    app = QApplication(sys.argv)
    window = Demo()
    window.show()

    app.exec()


if __name__ == "__main__":
    main()
