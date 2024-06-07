from typing import List

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from pebble import concurrent


@concurrent.process()
def loadPdfFile(path: str) -> (PyPDFLoader, List[Document]):
    ret = PyPDFLoader(path)
    return ret, ret.load()


class PdfReader:
    def __init__(self, pdf_path):
        self.feature = loadPdfFile(pdf_path)

    def load(self):
        self.loader, self.pages = self.feature.result()

    def cancel(self):
        self.feature.cancel()

    def getTextByPageNum(self, page_num: int) -> str:
        if page_num >= 0 and page_num < len(self.pages):
            return self.pages[page_num].page_content
        return ""
