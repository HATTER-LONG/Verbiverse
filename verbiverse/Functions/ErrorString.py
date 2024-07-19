from PySide6.QtCore import QObject


class ErrorString(QObject):
    def __init__(self):
        self.NO_VALID_LLM = self.tr(
            "LLM config invalid. Please set it in the configuration interface:"
        )
        self.NO_VALID_LLM_NAME = self.tr(
            "No valid LLM model name. Please set it in the configuration interface."
        )
        self.NO_VALID_EMBED_LLM_NAME = self.tr(
            "No valid Embed LLM model name. Please set it in the configuration interface."
        )
        self.NO_VALID_LLM_API = self.tr(
            "No valid LLM API. Please set it in the configuration interface."
        )
        self.NO_VALID_LLM_URL = self.tr(
            "No valid LLM URL. Please set it in the configuration interface."
        )


error_string = ErrorString()
