import sys
import asyncio
from PySide6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget
import edge_tts
from qasync import QEventLoop, QApplication


from qfluentwidgets import StateToolTip

OUTPUT_FILE = "sample_output.mp3"
VOICE = "en-US-AvaNeural"


async def convert_text_to_speech(text):
    """Convert text to speech using edge-tts.
    Args:
        text (str): The text to convert to speech.
    """
    print("start communicate")
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(OUTPUT_FILE)
    print("finish communicate")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Async PySide6 Example")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.button = QPushButton("Convert Text to Speech")
        self.button.clicked.connect(
            lambda: asyncio.ensure_future(self.on_button_click())
        )
        layout.addWidget(self.button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    async def on_button_click(self):
        text = "hello world, My good day to meet you"
        await asyncio.sleep(1)
        stateTooltip = StateToolTip("Start TTS", f"Content: {text}", self)
        stateTooltip.show()
        print("start convert")
        communicate = edge_tts.Communicate(text, VOICE)
        print("start save")
        await communicate.save(OUTPUT_FILE)
        print("finish convert")
        stateTooltip.setContent("TTS Done")
        stateTooltip.setState(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    event_loop = QEventLoop(app)
    asyncio.set_event_loop(event_loop)
    app_close_event = asyncio.Event()
    app.aboutToQuit.connect(app_close_event.set)
    window = MainWindow()
    window.show()
    with event_loop:
        event_loop.run_until_complete(app_close_event.wait())
