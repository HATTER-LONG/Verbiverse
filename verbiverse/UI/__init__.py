import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from .MainWindow import Ui_MainWindow  # noqa: F401,E402
from .MessageBox import Ui_MessageBox  # noqa: F401,E402
from .Translate import Ui_TranslateInfoWin  # noqa: F401,E402
