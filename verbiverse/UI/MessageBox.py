from PySide6.QtWidgets import QFrame
from qfluentwidgets import FluentStyleSheet
from UI import Ui_MessageBox


class CMessageBox(QFrame, Ui_MessageBox):
    def __init__(self, image: str, name: str, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.user_image.setImage(image)
        self.user_image.scaledToHeight(30)
        self.user_image.setBorderRadius(8, 8, 8, 8)
        self.user_name.setText(name)
        FluentStyleSheet.MESSAGE_DIALOG.apply(self.user_message)

    def setMessageText(self, text: str):
        self.user_message.setText(text)

    def getMessageText(self) -> str:
        return self.user_message.text()
