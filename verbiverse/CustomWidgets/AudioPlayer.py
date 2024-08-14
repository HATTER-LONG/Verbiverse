from AudioPlayer_ui import Ui_PlayerAudio
from Functions.EdgeTTS import EdgeTTS
from Functions.SignalBus import signalBus
from ModuleLogger import logger
from PySide6.QtCore import QThread
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtWidgets import QListWidgetItem, QWidget
from qfluentwidgets import FluentIcon
import asyncio


class AudioPlayer(QWidget, Ui_PlayerAudio):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.player_title.setText("")
        self.clear_button.setText(self.tr("Clear All"))
        self.clear_button.setIcon(FluentIcon.DELETE)
        self.clear_button.clicked.connect(self.clearAudio)
        self.listWidget.itemDoubleClicked.connect(
            lambda item: asyncio.ensure_future(self.selectionItem(item))
        )
        self.player_bar.player.setVolume(100)
        self.edge_tts = EdgeTTS()
        self.audio_path = None
        self.loadAudioList(self.edge_tts.getAudioList())
        signalBus.play_audio_signal.connect(
            lambda text: asyncio.ensure_future(self.playAudio(text))
        )

    def loadAudioList(self, audio_list: list):
        for audio in audio_list:
            self.listWidget.addItem(audio)

    def clearAudio(self):
        self.player_title.setText("")
        self.listWidget.clear()
        self.player_bar.player.stop()
        self.edge_tts.clearAudioList()

    def __playAudio(self, audio_path: str):
        logger.debug("start to stop and play")
        self.player_bar.player.stop()
        count = 0
        while (
            self.player_bar.player.playbackState()
            != QMediaPlayer.PlaybackState.StoppedState
        ):
            if count > 10:
                raise Exception("can not stop player")

            logger.debug("wait stop")
            count += 1
            QThread.msleep(200)
        self.player_bar.player.setSource(audio_path)
        self.player_bar.player.play()

    async def playAudio(self, text):
        signalBus.status_signal.emit("Convert text to speech", "Please wait...")
        self.player_title.setText(text)
        try:
            self.audio_path = await self.edge_tts.getAudio(text)
        except Exception as e:
            self.player_title.setText("")
            logger.error(f"Error: {e}")
            signalBus.status_signal.emit("Convert text to speech Failed", f"Error: {e}")
            return
        if self.audio_path is not None:
            self.listWidget.addItem(text)
            self.listWidget.setCurrentRow(self.listWidget.count() - 1)
            self.__playAudio(self.audio_path)
        signalBus.status_signal.emit("Convert text to speech Finish", "Finish")

    async def selectionItem(self, item: QListWidgetItem):
        self.player_title.setText(item.text())
        self.audio_path = await self.edge_tts.getAudio(item.text())
        logger.debug(f"audio_path: {self.audio_path}")
        self.__playAudio(self.audio_path)
