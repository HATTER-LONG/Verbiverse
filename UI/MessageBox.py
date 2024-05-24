from PySide6.QtWidgets import QFrame
from qfluentwidgets import FluentStyleSheet, RoundMenu

from UI import Ui_MessageBox
from PySide6.QtCore import QPoint, Qt, Slot

from CustomWidgets import CMenu


class MessageBox(QFrame, Ui_MessageBox):
    def __init__(self, image: str, name: str, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.user_image.setImage(image)
        self.user_image.scaledToHeight(30)
        self.user_image.setBorderRadius(8, 8, 8, 8)
        self.user_name.setText(name)
        FluentStyleSheet.MESSAGE_DIALOG.apply(self.user_message)

        # self.user_message.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.user_message.customContextMenuRequested.disconnect(
        #     self.user_message._onContextMenuRequested
        # )

        # self.user_message.customContextMenuRequested.connect(self.contextMenuEvent)

    def setMessageText(self, text: str):
        self.user_message.setText(text)

    @Slot(QPoint)
    def contextMenuEvent(self, event: QPoint) -> None:
        """
        Show a context menu with options based on selected text in the user_message.

        Args:
        - event (QPoint): The position of the mouse click.
        """
        # get selected text
        # selected_text = self.user_message.selectedText()

        # if len(selected_text) == 0:
        #     return

        # all_text = self.user_message.text()

        # menu = CMenu(self, selected_text, all_text)
        # menu.exec_(self.mapToGlobal(event))

        menu2 = RoundMenu("test", parent=self)
        menu2.exec(self.mapToGlobal(event))
