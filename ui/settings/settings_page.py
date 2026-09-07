from PySide6.QtCore import (
    QSettings,
    Qt,
    Signal,
)
from PySide6.QtWidgets import (
    QButtonGroup,
    QCheckBox,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from ui.styles.style_manager import (
    get_current_theme,
)


class ThemeCard(QPushButton):

    def __init__(
        self,
        title,
        subtitle,
        theme_name,
        parent=None,
    ):
        super().__init__(
            parent
        )

        self.theme_name = (
            theme_name
        )

        self.setObjectName(
            "ThemeCard"
        )

        self.setCheckable(
            True
        )

        self.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.setMinimumHeight(
            105
        )

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            18,
            16,
            18,
            16,
        )

        layout.setSpacing(
            6
        )

        title_label = QLabel(
            title
        )

        title_label.setObjectName(
            "ThemeCardTitle"
        )

        subtitle_label = QLabel(
            subtitle
        )

        subtitle_label.setObjectName(
            "ThemeCardSubtitle"
        )

        subtitle_label.setWordWrap(
            True
        )

        layout.addWidget(
            title_label
        )

        layout.addWidget(
            subtitle_label
        )

        layout.addStretch()


class SettingsSection(QFrame):

    def __init__(
        self,
        title,
        description="",
        parent=None,
    ):
        super().__init__(
            parent
        )

        self.setObjectName(
            "SettingsSection"
        )

        self.layout = QVBoxLayout(
            self
        )

        self.layout.setContentsMargins(
            22,
            20,
            22,
            22,
        )

        self.layout.setSpacing(
            14
        )

        title_label = QLabel(
            title
        )

        title_label.setObjectName(
            "SettingsSectionTitle"
        )

        self.layout.addWidget(
            title_label
        )

        if description:

            description_label = QLabel(
                description
            )

            description_label.setObjectName(
                "SettingsSectionDescription"
            )

            description_label.setWordWrap(
                True
            )

            self.layout.addWidget(
                description_label
            )


class SettingsPage(QWidget):

    theme_changed = Signal(str)

    def __init__(
        self,
        parent=None,
    ):
        super().__init__(
            parent
        )

        self.setObjectName(
            "SettingsPage"
        )

        self.settings = QSettings(
            "Veyra",
            "VeyraBrowser",
        )

        self._build_ui()

    # ==================================================
    # BUILD
    # ==================================================

    def _build_ui(self):

        root = QVBoxLayout(
            self
        )

        root.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        scroll = QScrollArea()

        scroll.setWidgetResizable(
            True
        )

        scroll.setFrameShape(
            QFrame.Shape.NoFrame
        )

        container = QWidget()

        container.setObjectName(
            "SettingsContainer"
        )

        layout = QVBoxLayout(
            container
        )

        layout.setContentsMargins(
            70,
            48,
            70,
            70,
        )

        layout.setSpacing(
            24
        )

        # ==================================================
        # HEADER
        # ==================================================

        title = QLabel(
            "Settings"
        )

        title.setObjectName(
            "SettingsTitle"
        )

        subtitle = QLabel(
            "Customize how Veyra looks and behaves."
        )

        subtitle.setObjectName(
            "SettingsSubtitle"
        )

        layout.addWidget(
            title
        )

        layout.addWidget(
            subtitle
        )

        # ==================================================
        # APPEARANCE
        # ==================================================

        appearance = SettingsSection(
            "Appearance",
            "Choose the visual style of Veyra.",
        )

        theme_grid = QHBoxLayout()

        theme_grid.setSpacing(
            12
        )

        self.theme_group = QButtonGroup(
            self
        )

        self.theme_group.setExclusive(
            True
        )

        themes = [
            (
                "Midnight",
                "Deep dark Veyra with the signature purple accent.",
                "midnight",
            ),
            (
                "Graphite",
                "Neutral dark theme with a clean professional look.",
                "graphite",
            ),
            (
                "Aurora",
                "Dark futuristic theme with a stronger violet accent.",
                "aurora",
            ),
            (
                "Light",
                "Bright and minimal for daytime use.",
                "light",
            ),
        ]

        current_theme = (
            get_current_theme()
        )

        for (
            title_text,
            subtitle_text,
            theme_name,
        ) in themes:

            card = ThemeCard(
                title_text,
                subtitle_text,
                theme_name,
            )

            self.theme_group.addButton(
                card
            )

            card.setChecked(
                current_theme
                == theme_name
            )

            card.clicked.connect(
                lambda checked,
                name=theme_name:
                self._set_theme(
                    name
                )
            )

            theme_grid.addWidget(
                card
            )

        appearance.layout.addLayout(
            theme_grid
        )

        layout.addWidget(
            appearance
        )

        # ==================================================
        # BROWSER
        # ==================================================

        browser_section = SettingsSection(
            "Browser",
            "Basic browsing preferences.",
        )

        search_row = QHBoxLayout()

        search_label_box = QVBoxLayout()

        search_title = QLabel(
            "Search engine"
        )

        search_title.setObjectName(
            "SettingsRowTitle"
        )

        search_description = QLabel(
            "Default engine used when text is not a URL."
        )

        search_description.setObjectName(
            "SettingsRowDescription"
        )

        search_label_box.addWidget(
            search_title
        )

        search_label_box.addWidget(
            search_description
        )

        self.search_engine = QComboBox()

        self.search_engine.setObjectName(
            "SettingsComboBox"
        )

        self.search_engine.addItems(
            [
                "Google",
                "DuckDuckGo",
                "Bing",
            ]
        )

        saved_engine = self.settings.value(
            "browser/search_engine",
            "Google",
        )

        self.search_engine.setCurrentText(
            saved_engine
        )

        self.search_engine.currentTextChanged.connect(
            lambda value:
            self.settings.setValue(
                "browser/search_engine",
                value,
            )
        )

        search_row.addLayout(
            search_label_box,
            1,
        )

        search_row.addWidget(
            self.search_engine
        )

        browser_section.layout.addLayout(
            search_row
        )

        browser_section.layout.addWidget(
            self._separator()
        )

        restore_row = self._checkbox_row(
            "Restore previous session",
            "Reopen your previous tabs when Veyra starts.",
            "browser/restore_session",
            True,
        )

        browser_section.layout.addLayout(
            restore_row
        )

        layout.addWidget(
            browser_section
        )

        # ==================================================
        # PRIVACY
        # ==================================================

        privacy = SettingsSection(
            "Privacy",
            "Control local browsing behaviour.",
        )

        privacy.layout.addLayout(
            self._checkbox_row(
                "Save browsing history",
                "Store visited pages in Veyra history.",
                "privacy/save_history",
                True,
            )
        )

        privacy.layout.addWidget(
            self._separator()
        )

        privacy.layout.addLayout(
            self._checkbox_row(
                "Persistent cookies",
                "Keep website sign-ins between sessions.",
                "privacy/persistent_cookies",
                True,
            )
        )

        layout.addWidget(
            privacy
        )

        # ==================================================
        # DOWNLOADS
        # ==================================================

        downloads = SettingsSection(
            "Downloads",
            "Configure how downloaded files are handled.",
        )

        downloads.layout.addLayout(
            self._checkbox_row(
                "Show downloads automatically",
                "Open the downloads view after a new download starts.",
                "downloads/show_automatically",
                False,
            )
        )

        layout.addWidget(
            downloads
        )

        # ==================================================
        # ABOUT
        # ==================================================

        about = SettingsSection(
            "About Veyra"
        )

        about_title = QLabel(
            "Veyra Browser"
        )

        about_title.setObjectName(
            "AboutTitle"
        )

        about_text = QLabel(
            "Version 0.1 • Early development build\n"
            "Built with Python, PySide6 and Qt WebEngine."
        )

        about_text.setObjectName(
            "AboutText"
        )

        about.layout.addWidget(
            about_title
        )

        about.layout.addWidget(
            about_text
        )

        layout.addWidget(
            about
        )

        layout.addStretch()

        scroll.setWidget(
            container
        )

        root.addWidget(
            scroll
        )

    # ==================================================
    # HELPERS
    # ==================================================

    def _set_theme(
        self,
        theme_name,
    ):

        self.theme_changed.emit(
            theme_name
        )

    def _separator(self):

        separator = QFrame()

        separator.setObjectName(
            "SettingsSeparator"
        )

        separator.setFrameShape(
            QFrame.Shape.HLine
        )

        return separator

    def _checkbox_row(
        self,
        title,
        description,
        settings_key,
        default_value,
    ):

        row = QHBoxLayout()

        text_box = QVBoxLayout()

        title_label = QLabel(
            title
        )

        title_label.setObjectName(
            "SettingsRowTitle"
        )

        description_label = QLabel(
            description
        )

        description_label.setObjectName(
            "SettingsRowDescription"
        )

        text_box.addWidget(
            title_label
        )

        text_box.addWidget(
            description_label
        )

        checkbox = QCheckBox()

        checkbox.setObjectName(
            "SettingsSwitch"
        )

        value = self.settings.value(
            settings_key,
            default_value,
            type=bool,
        )

        checkbox.setChecked(
            value
        )

        checkbox.toggled.connect(
            lambda checked:
            self.settings.setValue(
                settings_key,
                checked,
            )
        )

        row.addLayout(
            text_box,
            1,
        )

        row.addWidget(
            checkbox
        )

        return row