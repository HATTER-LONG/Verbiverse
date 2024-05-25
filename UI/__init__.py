import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


from .ChatWidget import ChatWidget  # noqa: F401,E402,I001
from .ReadAndChatWidget import ReadAndChatWidget  # noqa: F401
from .ChatWidget_ui import Ui_ChatWidget  # noqa: F401,E402,I001
from .MessageBox_ui import Ui_MessageBox  # noqa: F401,E402
from .MessageBox import CMessageBox  # noqa: F401,E402
from .SettingInterface import SettingInterface  # noqa: F401,E402

# from .MainWindow import Ui_MainWindow  # noqa: F401,E402

# from .Translate import Ui_TranslateInfoWin  # noqa: F401,E402
