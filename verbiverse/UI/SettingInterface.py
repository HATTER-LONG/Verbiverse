from CustomWidgets import StyleSheet
from Functions.Config import AUTHOR, FEEDBACK_URL, HELP_URL, VERSION, YEAR, cfg, isWin11
from Functions.SignalBus import signalBus
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QFileDialog, QWidget
from qfluentwidgets import (
    ComboBoxSettingCard,
    CustomColorSettingCard,
    ExpandLayout,
    HyperlinkCard,
    InfoBar,
    LargeTitleLabel,
    OptionsSettingCard,
    PrimaryPushSettingCard,
    PushSettingCard,
    ScrollArea,
    SettingCardGroup,
    SwitchSettingCard,
    setTheme,
    setThemeColor,
)
from qfluentwidgets import FluentIcon as FIF


class SettingInterface(ScrollArea):
    """Setting interface"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.scroll_widget = QWidget()
        self.expand_layout = ExpandLayout(self.scroll_widget)

        # setting label
        self.setting_label = LargeTitleLabel(self.tr("Settings"), self)

        # database folders
        self.function_info_group = SettingCardGroup(
            self.tr("Main function settings"), self.scroll_widget
        )
        self.provider_info = ComboBoxSettingCard(
            cfg.provider,
            FIF.ROBOT,
            self.tr("Provider"),
            self.tr("Set your preferred provider for LLM"),
            texts=["openai", "Tongyi"],
            parent=self.function_info_group,
        )
        self.datebase_save_path = PushSettingCard(
            self.tr("Choose folder"),
            FIF.CLOUD,
            self.tr("Database directory"),
            cfg.get(cfg.database_folder),
            self.function_info_group,
        )

        # personalization
        self.personal_group = SettingCardGroup(
            self.tr("Personalization"), self.scroll_widget
        )
        self.mica_card = SwitchSettingCard(
            FIF.TRANSPARENT,
            self.tr("Mica effect"),
            self.tr("Apply semi transparent to windows and surfaces"),
            cfg.mica_enabled,
            self.personal_group,
        )
        self.themeCard = OptionsSettingCard(
            cfg.themeMode,
            FIF.BRUSH,
            self.tr("Application theme"),
            self.tr("Change the appearance of your application"),
            texts=[self.tr("Light"), self.tr("Dark"), self.tr("Use system setting")],
            parent=self.personal_group,
        )
        self.themeColorCard = CustomColorSettingCard(
            cfg.themeColor,
            FIF.PALETTE,
            self.tr("Theme color"),
            self.tr("Change the theme color of you application"),
            self.personal_group,
        )
        self.zoomCard = OptionsSettingCard(
            cfg.dpiScale,
            FIF.ZOOM,
            self.tr("Interface zoom"),
            self.tr("Change the size of widgets and fonts"),
            texts=[
                "100%",
                "125%",
                "150%",
                "175%",
                "200%",
                self.tr("Use system setting"),
            ],
            parent=self.personal_group,
        )
        self.languageCard = ComboBoxSettingCard(
            cfg.language,
            FIF.LANGUAGE,
            self.tr("Language"),
            self.tr("Set your preferred language for UI"),
            texts=["简体中文", "繁體中文", "English", self.tr("Use system setting")],
            parent=self.personal_group,
        )

        # update software
        self.updateSoftwareGroup = SettingCardGroup(
            self.tr("Software update"), self.scroll_widget
        )
        self.updateOnStartUpCard = SwitchSettingCard(
            FIF.UPDATE,
            self.tr("Check for updates when the application starts"),
            self.tr("The new version will be more stable and have more features"),
            configItem=cfg.checkUpdateAtStartUp,
            parent=self.updateSoftwareGroup,
        )

        # application
        self.aboutGroup = SettingCardGroup(self.tr("About"), self.scroll_widget)
        self.helpCard = HyperlinkCard(
            HELP_URL,
            self.tr("Open help page"),
            FIF.HELP,
            self.tr("Help"),
            self.tr(
                "Discover new features and learn useful tips about PyQt-Fluent-Widgets"
            ),
            self.aboutGroup,
        )
        self.feedbackCard = PrimaryPushSettingCard(
            self.tr("Provide feedback"),
            FIF.FEEDBACK,
            self.tr("Provide feedback"),
            self.tr("Help us improve PyQt-Fluent-Widgets by providing feedback"),
            self.aboutGroup,
        )
        self.aboutCard = PrimaryPushSettingCard(
            self.tr("Check update"),
            FIF.INFO,
            self.tr("About"),
            "© "
            + self.tr("Copyright")
            + f" {YEAR}, {AUTHOR}. "
            + self.tr("Version")
            + " "
            + VERSION,
            self.aboutGroup,
        )

        self.__initWidget()

    def __initWidget(self):
        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 80, 0, 20)
        self.setWidget(self.scroll_widget)
        self.setWidgetResizable(True)
        self.setObjectName("settingInterface")

        # initialize style sheet
        self.scroll_widget.setObjectName("scrollWidget")
        self.setting_label.setObjectName("settingLabel")
        StyleSheet.SETTING_INTERFACE.apply(self)

        self.mica_card.setEnabled(isWin11())

        # initialize layout
        self.__initLayout()
        self.__connectSignalToSlot()

    def __initLayout(self):
        self.setting_label.move(36, 30)

        # add cards to group

        self.function_info_group.addSettingCard(self.provider_info)
        self.function_info_group.addSettingCard(self.datebase_save_path)

        self.personal_group.addSettingCard(self.mica_card)
        self.personal_group.addSettingCard(self.themeCard)
        self.personal_group.addSettingCard(self.themeColorCard)
        self.personal_group.addSettingCard(self.zoomCard)
        self.personal_group.addSettingCard(self.languageCard)

        self.updateSoftwareGroup.addSettingCard(self.updateOnStartUpCard)

        self.aboutGroup.addSettingCard(self.helpCard)
        self.aboutGroup.addSettingCard(self.feedbackCard)
        self.aboutGroup.addSettingCard(self.aboutCard)

        # add setting card group to layout
        self.expand_layout.setSpacing(28)
        self.expand_layout.setContentsMargins(36, 10, 36, 0)
        self.expand_layout.addWidget(self.function_info_group)
        self.expand_layout.addWidget(self.personal_group)
        self.expand_layout.addWidget(self.updateSoftwareGroup)
        self.expand_layout.addWidget(self.aboutGroup)

    def __showRestartTooltip(self):
        """show restart tooltip"""
        InfoBar.success(
            self.tr("Updated successfully"),
            self.tr("Configuration takes effect after restart"),
            duration=1500,
            parent=self,
        )

    def __onDatabaseSetFolderCardClicked(self):
        """download folder card clicked slot"""
        folder = QFileDialog.getExistingDirectory(self, self.tr("Choose folder"), "./")
        if not folder or cfg.get(cfg.database_folder) == folder:
            return

        cfg.set(cfg.database_folder, folder)
        self.datebase_save_path.setContent(folder)
        # TODO: 拷贝数据库

    def __connectSignalToSlot(self):
        """connect signal to slot"""
        cfg.appRestartSig.connect(self.__showRestartTooltip)

        # music in the pc
        self.datebase_save_path.clicked.connect(self.__onDatabaseSetFolderCardClicked)

        # personalization
        self.themeCard.optionChanged.connect(lambda ci: setTheme(cfg.get(ci)))
        self.themeColorCard.colorChanged.connect(lambda c: setThemeColor(c))
        self.mica_card.checkedChanged.connect(signalBus.mica_enable_change_signal)

        # about
        self.feedbackCard.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl(FEEDBACK_URL))
        )
