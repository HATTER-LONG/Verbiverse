import glob
import os
import traceback

import pysrt
from CustomWidgets import ExplainWindow
from CustomWidgets.ExplainFlyoutView import ExplainFlyoutView
from Functions.LanguageType import ExplainLanguage
from Functions.SignalBus import signalBus
from LLM.ExplainWorkerThread import ExplainWorkerThread
from ModuleLogger import logger
from PySide6.QtCore import QPoint, Qt, QThread, QUrl, Slot
from PySide6.QtGui import QAction, QCursor, QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QFileDialog,
    QListWidgetItem,
    QWidget,
)
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import (
    Flyout,
    FlyoutAnimationType,
    RoundMenu,
)
from VideoInterface_ui import Ui_VideoInterface


class VideoInterface(QWidget, Ui_VideoInterface):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.splitter.setStretchFactor(0, 2)
        self.splitter.setStretchFactor(1, 1)
        self.parse_button.setIcon(FIF.ROBOT)
        self.subtitel_browser.setContextMenuPolicy(Qt.CustomContextMenu)
        self.subtitel_browser.explain_signal.connect(self._onExplainSignal)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._onContextMenuRequested)
        self.file_path = None

        self.subtitle_path = None
        self.subtitle = None
        self.subtitle_map = {}
        self.last_timestamp = -1
        self.current_subtitle = None
        self.subtitle_index = -1
        self.subtitel_browser.hide()

        self.video_widget.playBar.setVolume(80)
        self.tab_widget.subtitle.itemDoubleClicked.connect(self.selectSubtitle)
        self.tab_widget.file_list.itemDoubleClicked.connect(self.selectVideoFile)
        self.video_widget.player.positionChanged.connect(self.updatePlayPos)
        space_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Space), self)
        space_shortcut.activated.connect(self.video_widget.togglePlayState)
        left_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Left), self)
        left_shortcut.activated.connect(
            lambda: self.video_widget.playBar.skipBack(5000)
        )
        right_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Right), self)
        right_shortcut.activated.connect(
            lambda: self.video_widget.playBar.skipForward(5000)
        )

        signalBus.open_video_signal.connect(self.open)

    def initSubTitleList(self):
        for index, item in enumerate(self.subtitle):
            if len(item.text) == 0:
                continue
            self.subtitle_map[item.text] = index
            widget = QListWidgetItem(f"[{item.start}] {item.text}")
            widget.setData(Qt.UserRole, index)
            self.tab_widget.subtitle.addItem(widget)

    def initVideoList(self):
        self.tab_widget.file_list.clear()
        file_dir = os.path.dirname(self.file_path)
        _, file_ext = os.path.splitext(self.file_path)
        logger.info(f"file dir: {file_dir} file ext: {file_ext}")
        search_pattern = os.path.join(file_dir, "*%s" % file_ext)
        files = sorted(glob.glob(search_pattern))
        index = 0
        for i, file in enumerate(files):
            if file == self.file_path:
                index = i
            name = os.path.basename(file)
            widget = QListWidgetItem(name)
            widget.setData(Qt.UserRole, file)
            self.tab_widget.file_list.addItem(widget)
        self.tab_widget.file_list.setCurrentRow(index)

    def selectSubtitle(self, item: QListWidgetItem):
        if not self.video_widget.player.isPlaying():
            self.video_widget.play()
        index = item.data(Qt.UserRole)
        time = self.subtitle[index].start.ordinal
        logger.info(f"select subtitle: {index} {time}")
        self.video_widget.player.setPosition(time)
        # self.updatePlayPos(time)

    def selectVideoFile(self, item: QListWidgetItem):
        file_path = item.data(Qt.UserRole)
        signalBus.open_video_signal.emit(QUrl.fromLocalFile(file_path))

    def updatePlayPos(self, time):
        if not self.subtitle or (
            time - self.last_timestamp > 0 and time - self.last_timestamp < 200
        ):
            return
        self.last_timestamp = time
        # + 1 avoid cannot search select subtitle item
        subtitle_item = self.subtitle.at(milliseconds=time + 1)
        if subtitle_item is None or self.current_subtitle == subtitle_item:
            return
        self.current_subtitle = subtitle_item

        if len(self.current_subtitle.text) > 0:
            text = self.current_subtitle.text
            logger.info(f"update subtitle: {text}")
            self.subtitel_browser.setText(text)
            self.subtitel_browser.show()
            self.subtitle_index = self.subtitle_map[text]
            self.tab_widget.subtitle.setCurrentRow(self.subtitle_index)
            self.tab_widget.subtitle.scrollTo(
                self.tab_widget.subtitle.currentIndex(),
                hint=QAbstractItemView.PositionAtCenter,
            )

    def clear(self):
        self.file_path = None
        self.clearSubTitle()
        self.clearVideoFileList()

    def clearSubTitle(self):
        self.subtitle_path = None
        self.subtitle = None
        self.subtitle_map = {}
        self.last_timestamp = -1
        self.subtitle_index = -1
        self.current_subtitle = None
        self.subtitel_browser.setText("")
        self.subtitel_browser.hide()
        self.tab_widget.subtitle.clear()

    def clearVideoFileList(self):
        self.tab_widget.file_list.clear()

    @Slot(QUrl)
    def open(self, file_path: QUrl):
        logger.info(f"open video file: [{file_path}]")
        if not file_path.isValid():
            return
        self.clear()
        self.file_path = file_path.toLocalFile()
        try:
            self.video_widget.stop()
            # FIX: WTF .... https://stackoverflow.com/questions/77219901/can-not-change-media-using-setsource-in-pyside6
            QThread.msleep(200)
            self.video_widget.setVideo(file_path)
            self.video_widget.play()
        except Exception as error:
            logger.error(f"open video error: [{error}]")
            traceback.print_exc()
        self.findSubtitle()
        self.initVideoList()

    def findSubtitle(self):
        file_dir = os.path.dirname(self.file_path)
        file_name = os.path.basename(self.file_path)
        srt_name = os.path.splitext(file_name)[0] + ".srt"
        srt_path = os.path.join(file_dir, srt_name)

        if os.path.exists(srt_path):
            logger.info(f"subtitle file: [{srt_path}]")
            self.subtitle = pysrt.open(srt_path)
            self.initSubTitleList()

    def _onAddSubtitle(self):
        self.clearSubTitle()
        diaglog = QFileDialog(self, "Choose a video subtitle file", self.file_path)
        diaglog.setFileMode(QFileDialog.FileMode.ExistingFile)
        diaglog.setAcceptMode(QFileDialog.AcceptOpen)

        diaglog.setNameFilter("SRT Files (*.srt)")
        if diaglog.exec() == QDialog.Accepted:
            self.subtitle_path = diaglog.selectedUrls()[0]
            logger.info(f"subtitle file: [{self.subtitle_path}]")
            self.subtitle = pysrt.open(self.subtitle_path.toLocalFile())
            self.initSubTitleList()

    @Slot(QPoint)
    def _onContextMenuRequested(self, event: QPoint) -> None:
        menu = RoundMenu(parent=self)

        menu.addAction(
            QAction(
                FIF.ADD_TO.icon(),
                self.tr("Add Subtitle"),
                self,
                triggered=self._onAddSubtitle,
            )
        )
        menu.exec(self.mapToGlobal(event))

    @Slot(str)
    def _onExplainSignal(self, word: str):
        if hasattr(self, "worker") and self.worker is not None:
            logger.warning("flyout explain thread is not done")
            return
        logger.info(f"explain signal: {word}")
        # 向上偏移避免超出屏幕
        cursor_pos = QCursor.pos()
        cursor_pos.setX(cursor_pos.x() + 10)
        cursor_pos.setY(cursor_pos.y() - 200)
        self.explain_flyout = Flyout.make(
            ExplainFlyoutView(word),
            cursor_pos,
            self,
            aniType=FlyoutAnimationType.SLIDE_RIGHT,
        )

        location = (
            self.file_path + " -> " + str(self.subtitle[self.subtitle_index].start)
        )
        logger.info(f"explanation location: {location}")
        self.explain_flyout.view.setTextResource(location)
        self.explain_flyout.closed.connect(self.explainClose)
        self.explain_flyout.view.pin_explain_signal.connect(self.pinFlyout)

        self.explain_window = None

        all_text = ""
        for i in range(self.subtitle_index - 10, self.subtitle_index + 5):
            all_text = all_text + self.subtitle[i].text
        self.worker = ExplainWorkerThread(
            selected_text=word,
            all_text=all_text,
            language_type=ExplainLanguage.MOTHER_TONGUE,
        )
        self.worker.messageCallBackSignal.connect(self.onExplainResultUpdate)
        self.worker.finished.connect(self.finishedExplain)
        self.worker.start()

    @Slot(str)
    def onExplainResultUpdate(self, explain: str):
        if self.explain_flyout is not None:
            self.explain_flyout.view.setContent(
                self.explain_flyout.view.getContent() + explain
            )
        elif self.explain_window is not None:
            self.explain_window.setContent(self.explain_window.getContent() + explain)

    @Slot()
    def explainClose(self):
        logger.debug("flyout close")
        self.explain_flyout = None
        if self.explain_window is None:
            self.stopWorker()

    @Slot()
    def finishedExplain(self):
        self.explain_flyout = None
        self.explain_window = None
        self.worker = None

    @Slot(str, str, bool)
    def pinFlyout(self, title: str, content: str, already_add: bool):
        logger.debug(f"pin flyout {title} \n content{content}")
        self.explain_window = ExplainWindow(
            title,
            content,
            self.file_path + " -> " + str(self.subtitle[self.subtitle_index].start),
            already_add,
        )
        self.explain_window.show()
        self.explain_window.close_signal.connect(self.pinWindowClose)

    @Slot()
    def pinWindowClose(self):
        logger.debug("webview window close")
        self.explain_window = None
        if self.explain_flyout is None:
            self.stopWorker()

    def stopWorker(self):
        if self.worker is not None:
            logger.debug("close video interface explain thread ... ")
            self.worker.stop()
            self.worker.wait()
            logger.debug("close video interface explain thread done !!! ")
