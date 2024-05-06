from CustomLabelMenu import LabelMenu
from PySide6.QtCore import QPoint, Qt, Slot
from PySide6.QtWidgets import QFrame
from UI import Ui_MessageBox


class MessageBox(QFrame, Ui_MessageBox):
    """
    A custom QMessageBox subclass with a user image, name, and context menu for selecting text.

    Attributes:
    - user_image (QLabel): Displays the user's image.
    - user_name ( QLabel): Shows the user's name.
    - user_message (QTextEdit): The main message area with custom context menu support.
    """

    def __init__(self, image_path: str, user_name: str):
        """
        Initialize the MessageBox with an image path and a user's name.

        Args:
        - image_path (str): Path to the user's image file.
        - user_name (str): The user's name to display in the message box.
        """
        super().__init__()
        self.setupUi(self)
        self.user_image.setText(image_path)
        self.user_name.setText(user_name)
        self.user_message.setContextMenuPolicy(Qt.CustomContextMenu)
        self.user_message.customContextMenuRequested.connect(self.handleContextMenu)

    def getMessageText(self) -> str:
        """
        Return the text content of the user_message.

        Returns:
        - str: The current message text.
        """
        return self.user_message.text()

    def setMessageText(self, text: str) -> None:
        """
        Set the text content of the user_message.

        Args:
        - text (str): The new message text to display.
        """
        self.user_message.setText(text)

    # Handle context menu when right-clicking on the user_message
    @Slot(QPoint)
    def handleContextMenu(self, event: QPoint) -> None:
        """
        Show a context menu with options based on selected text in the user_message.

        Args:
        - event (QPoint): The position of the mouse click.
        """
        selected_text = self.user_message.text()

        if len(selected_text) == 0:
            return

        all_text = self.user_message.text()

        menu = LabelMenu(self, selected_text, all_text)
        menu.exec_(self.mapToGlobal(event))
