from CustomLabelMenu import LabelMenu
from PySide6.QtCore import QPoint, Qt, Slot
from PySide6.QtWidgets import QFrame
from UI import Ui_MessageBox


class MessageBox(QFrame, Ui_MessageBox):
    def __init__(self, image_path, user_name):
        super().__init__()
        self.setupUi(self)
        self.user_image.setText(image_path)
        self.user_name.setText(user_name)
        self.user_message.setContextMenuPolicy(Qt.CustomContextMenu)
        self.user_message.customContextMenuRequested.connect(self.handleContextMenu)
        # self.setStyleSheet("border: 1px solid #000000; border-radius: 5px; padding: 5px;")

    def getMessageText(self) -> str:
        return self.user_message.text()

    def setMessageText(self, text: str) -> None:
        self.user_message.setText(text)

    @Slot(QPoint)
    def handleContextMenu(self, event: QPoint):
        selected_text = self.user_message.selectedText()
        print("Selected text:", selected_text)
        if len(selected_text) == 0:
            return
        all_text = self.user_message.text()
        print("All text:", all_text)
        menu = LabelMenu(self, selected_text, all_text)
        menu.exec(self.mapToGlobal(event))
