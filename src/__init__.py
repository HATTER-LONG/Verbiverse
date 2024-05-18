import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from .LoadPdfText import PdfReader  # noqa: F401
from .WebPdfView import QWebPdfView  # noqa: F401

__author__ = "Layton"
__version__ = "0.1.0"
