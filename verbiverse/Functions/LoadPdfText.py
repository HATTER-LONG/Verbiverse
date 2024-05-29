from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document


class PdfReader:
    def __init__(self, pdf_path):
        self.loader = PyPDFLoader(pdf_path)
        self.pages = list[Document]()

    def getTextByPageNum(self, page_num: int) -> str:
        if page_num >= 0 and page_num < len(self.pages):
            return self.pages[page_num]
        return ""
