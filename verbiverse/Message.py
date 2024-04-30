from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)


class Message(QWidget):
    def __init__(self, image_path, user_name):
        super().__init__()

        self.verticalLayout = QVBoxLayout(self)

        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.user_image = QLabel(self)
        self.user_image.setText(image_path)
        self.user_image.setFrameStyle(
            QLabel.StyledPanel | QLabel.Sunken
        )  # 设置带阴影的样式，这样看起来更像有边框

        self.user_image.setSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Fixed
        )  # 高度固定
        self.user_image.setObjectName("user_image")

        self.horizontalLayout.addWidget(self.user_image)

        self.user_name = QLabel(self)

        self.user_name.setFrameStyle(QLabel.StyledPanel | QLabel.Sunken)
        self.user_name.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.user_name.setText(user_name)
        self.user_name.setObjectName("user_name")

        self.horizontalLayout.addWidget(self.user_name)

        self.horizontalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalSpacer_2 = QSpacerItem(
            40, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum
        )

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.user_message = QLabel(self)

        self.user_message.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.user_message.setFrameStyle(QLabel.StyledPanel | QLabel.Sunken)
        self.user_message.setObjectName("user_message")
        self.user_message.setWordWrap(True)

        self.horizontalLayout_3.addWidget(self.user_message)

        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.setLayout(self.verticalLayout)

    def setMessageText(self, text) -> None:
        self.user_message.setText(text)

    def getMessageText(self) -> str:
        return self.user_message.text()
