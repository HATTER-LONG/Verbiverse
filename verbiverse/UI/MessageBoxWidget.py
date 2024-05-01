from PySide6.QtWidgets import QFrame, QLabel
from UI.MessageBox import Ui_MessageBox


class MessageBox(QFrame, Ui_MessageBox):
    def __init__(self, image_path, user_name):
        super().__init__()
        self.setupUi(self)
        # self.user_name.setFrameStyle(QLabel.StyledPanel | QLabel.Sunken)
        # self.user_image.setFrameStyle(QLabel.StyledPanel | QLabel.Sunken)
        # self.user_message.setFrameStyle(QLabel.StyledPanel | QLabel.Sunken)
        self.user_image.setText(image_path)
        self.user_name.setText(user_name)
        # self.setStyleSheet("border: 1px solid #000000; border-radius: 5px; padding: 5px;")

    def getMessageText(self)->str:
        return self.user_message.text()

    def setMessageText(self, text: str)->None:
        self.user_message.setText(text)

