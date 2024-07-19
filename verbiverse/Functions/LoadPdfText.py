from typing import List

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from pebble import concurrent


@concurrent.process()
def loadPdfFile(path: str) -> (PyPDFLoader, List[Document]):
    """
    A function that loads a PDF file from the specified path and returns a PyPDFLoader instance along with a list of Document objects.

    Parameters:
    - path (str): The path to the PDF file to be loaded.

    Returns:
    - Tuple[PyPDFLoader, List[Document]]: A tuple containing the PyPDFLoader instance and a list of Document objects.
    """
    ret = PyPDFLoader(path)

    return ret, ret.load()


class PdfReader:
    "Load PDF content using the feature and assign the loader and pages attributes."

    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.feature = loadPdfFile(pdf_path)

    def load(self):
        """
        Load the PDF content using the feature and assign the loader and pages attributes.
        """
        self.loader, self.pages = self.feature.result()

    def cancel(self):
        """
        Cancels the current operation by invoking the cancel method of the feature.
        """
        self.feature.cancel()

    def getTextByPageNum(self, page_num: int) -> str:
        """
        Get the text content of a specific page in the PDF document.

        Parameters:
            page_num (int): The index of the page to retrieve the text from.

        Returns:
            str: The text content of the specified page. If the page number is out of range, an None string is returned.
        """
        if page_num >= 0 and page_num < len(self.pages):
            return self.pages[page_num].page_content
        return None
