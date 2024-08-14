from verbiverse.UI import AudioPlayer
from PySide6.QtWidgets import QApplication
import sys


def main():
    app = QApplication(sys.argv)
    window = AudioPlayer()
    window.player_title.setText(
        "1234567890 1234567890 1234567890 1234567890 1234567890 1234567890 1234567890 "
    )
    window.show()

    app.exec()


if __name__ == "__main__":
    main()
