from PySide6.QtWebEngineWidgets import QWebEngineView


class QWebPdfView(QWebEngineView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # def contextMenuEvent(self, event):
    #     selected_text = self.selectedText()

    #     if len(selected_text) == 0:
    #         return
    #     all_text = ""

    #     self.menu = LabelMenu(self, selected_text, all_text)
    #     self.menu.popup(event.globalPos())

    # def gettext(self):
    #     print(self.page().selectedText())
    #     print(self.selectedText())
