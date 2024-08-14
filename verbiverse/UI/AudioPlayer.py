from UI import Ui_PlayerAudio
from PySide6.QtWidgets import QWidget
from qfluentwidgets import FluentIcon


class AudioPlayer(QWidget, Ui_PlayerAudio):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.player_title.setText("")
        self.clear_button.setText(self.tr("Clear All"))
        self.clear_button.setIcon(FluentIcon.DELETE)
        # self.player_bar.setMedia(self.player_title)
        # self.player_bar.setMedia(self.listWidget)
        # self.clear_button.clicked.connect(self.clear_button_clicked)
