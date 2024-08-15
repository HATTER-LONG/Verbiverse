# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget)

import PySide6.QtAsyncio as QtAsyncio

import asyncio
import sys


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        widget = QWidget()
        self.setCentralWidget(widget)

        layout = QVBoxLayout(widget)

        self.text = QLabel("The answer is 42.")
        layout.addWidget(self.text, alignment=Qt.AlignmentFlag.AlignCenter)

        async_trigger = QPushButton(text="What is the question?")
        async_trigger.clicked.connect(lambda: asyncio.ensure_future(self.set_text()))
        layout.addWidget(async_trigger, alignment=Qt.AlignmentFlag.AlignCenter)

    async def set_text(self):
        await asyncio.sleep(10)
        self.text.setText("What do you get if you multiply six by nine?")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()

    QtAsyncio.run()