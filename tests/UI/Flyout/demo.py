import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QWidget,
)
from qfluentwidgets import (
    BodyLabel,
    Flyout,
    FlyoutAnimationType,
    MessageBoxBase,
    PushButton,
    SubtitleLabel,
    Theme,
    setTheme,
)

import verbiverse  # noqa: F401
from verbiverse.CustomWidgets.ExplainFlyoutView import ExplainFlyoutView
from verbiverse.CustomWidgets.ExplainWindow import ExplainWindow
from verbiverse.resources import resources_rc  # noqa: F401


class CustomMessageBox(MessageBoxBase):
    """Custom message box"""

    def __init__(self, title, content, parent=None):
        super().__init__(parent)
        self.title = title
        self.titleLabel = SubtitleLabel(self.title)
        self.content = content
        self.body_content = BodyLabel(self.content)
        self.body_content.setWordWrap(True)

        # 将组件添加到布局中
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.body_content)

        # 设置对话框的最小宽度
        self.widget.setMinimumWidth(350)

    def getContent(self):
        return self.content

    def setContent(self, content):
        self.content = content
        self.body_content.setText(self.content)
        self.adjustSize()


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
        self.flyout.view.pin_explain_signal.connect(self.onPinClicked)

    def onPinClicked(self, title, content, already_add):
        print(title, content, already_add)
        msg = (
            content
            + """
1234567890 ab cd efg hijk lmn opq rstuvwx yzABC DEFGHI JKLMNO PQRSTUVWXYZ
1234567890 abcdefghijk lmn opq rstuvwx yzABCDE FGHI JKLMNOPQR STUV WXYZ
        """
        )
        self.w = ExplainWindow(title, content, "target resource", already_add)
        self.w.show()
        self.w.setContent(msg)


def main():
    setTheme(Theme.LIGHT)
    app = QApplication(sys.argv)
    window = Demo()
    window.show()

    app.exec()


if __name__ == "__main__":
    main()
