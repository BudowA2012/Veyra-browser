from pathlib import Path

from PySide6.QtCore import (
    QSettings,
    QStandardPaths,
    Qt,
    Signal,
)

from PySide6.QtWidgets import (
    QButtonGroup,
    QCheckBox,
    QComboBox,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSpinBox,
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

        self.theme_name = theme_name

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
    default_zoom_changed = Signal(int)
    download_location_changed = Signal(str)
    clear_browsing_data_requested = Signal()

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

    # ======================================================
    # BUILD
    # ======================================================

    def _build_ui(
        self,
    ):

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
            "Customize Veyra's theme and New Tab page.",
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

        self.theme_cards = {}

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

            self.theme_cards[
                theme_name
            ] = card

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

        appearance.layout.addWidget(
            self._separator()
        )

        # ==================================================
        # NEW TAB BACKGROUND
        # ==================================================

        background_row = QHBoxLayout()

        background_text = (
            self._label_box(
                "New Tab background",
                (
                    "Choose a built-in background "
                    "or use your own JPG, JPEG or PNG."
                ),
            )
        )

        self.background_combo = QComboBox()

        self.background_combo.setObjectName(
            "SettingsComboBox"
        )

        self.background_combo.addItems(
            [
                "Theme default",
                "Purple Glow",
                "Ocean Night",
                "Sunset",
                "Forest Night",
                "Custom image",
            ]
        )

        background_modes = {
            "theme": "Theme default",
            "purple": "Purple Glow",
            "ocean": "Ocean Night",
            "sunset": "Sunset",
            "forest": "Forest Night",
            "custom": "Custom image",
        }

        saved_background = (
            self.settings.value(
                "appearance/new_tab_background",
                "theme",
            )
        )

        self.background_combo.setCurrentText(
            background_modes.get(
                saved_background,
                "Theme default",
            )
        )

        self.background_combo.currentTextChanged.connect(
            self._background_changed
        )

        background_row.addLayout(
            background_text,
            1,
        )

        background_row.addWidget(
            self.background_combo
        )

        appearance.layout.addLayout(
            background_row
        )

        # ==================================================
        # CUSTOM IMAGE
        # ==================================================

        image_row = QHBoxLayout()

        image_box = QVBoxLayout()

        image_title = QLabel(
            "Custom background image"
        )

        image_title.setObjectName(
            "SettingsRowTitle"
        )

        self.background_path_label = QLabel()

        self.background_path_label.setObjectName(
            "SettingsRowDescription"
        )

        self.background_path_label.setWordWrap(
            True
        )

        image_box.addWidget(
            image_title
        )

        image_box.addWidget(
            self.background_path_label
        )

        choose_image = QPushButton(
            "Choose image"
        )

        choose_image.setObjectName(
            "HistoryClearButton"
        )

        choose_image.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        choose_image.clicked.connect(
            self._choose_background_image
        )

        image_row.addLayout(
            image_box,
            1,
        )

        image_row.addWidget(
            choose_image
        )

        appearance.layout.addLayout(
            image_row
        )

        self._update_background_path_label()

        appearance.layout.addWidget(
            self._separator()
        )

        # ==================================================
        # DEFAULT ZOOM
        # ==================================================

        zoom_row = QHBoxLayout()

        zoom_text = self._label_box(
            "Default zoom",
            "Zoom level used for newly opened pages.",
        )

        self.zoom_spin = QSpinBox()

        self.zoom_spin.setObjectName(
            "SettingsComboBox"
        )

        self.zoom_spin.setRange(
            80,
            150,
        )

        self.zoom_spin.setSingleStep(
            10
        )

        self.zoom_spin.setSuffix(
            "%"
        )

        self.zoom_spin.setValue(
            self.settings.value(
                "browser/default_zoom",
                100,
                type=int,
            )
        )

        self.zoom_spin.valueChanged.connect(
            self._set_zoom
        )

        zoom_row.addLayout(
            zoom_text,
            1,
        )

        zoom_row.addWidget(
            self.zoom_spin
        )

        appearance.layout.addLayout(
            zoom_row
        )

        layout.addWidget(
            appearance
        )

        # ==================================================
        # SEARCH
        # ==================================================

        search_section = SettingsSection(
            "Search",
            "Configure how Veyra searches the web.",
        )

        search_row = QHBoxLayout()

        search_text = self._label_box(
            "Search engine",
            "Default engine used when text is not a URL.",
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

        self.search_engine.setCurrentText(
            self.settings.value(
                "browser/search_engine",
                "Google",
            )
        )

        self.search_engine.currentTextChanged.connect(
            self._set_search_engine
        )

        search_row.addLayout(
            search_text,
            1,
        )

        search_row.addWidget(
            self.search_engine
        )

        search_section.layout.addLayout(
            search_row
        )

        layout.addWidget(
            search_section
        )

        # ==================================================
        # STARTUP
        # ==================================================

        startup = SettingsSection(
            "Startup",
            "Choose what happens when Veyra starts.",
        )

        startup_row = QHBoxLayout()

        startup_text = self._label_box(
            "On startup",
            "Open a fresh New Tab or restore your previous tabs.",
        )

        self.startup_mode = QComboBox()

        self.startup_mode.setObjectName(
            "SettingsComboBox"
        )

        self.startup_mode.addItems(
            [
                "New Tab",
                "Restore previous session",
            ]
        )

        restore_enabled = (
            self.settings.value(
                "browser/restore_session",
                True,
                type=bool,
            )
        )

        self.startup_mode.setCurrentText(
            (
                "Restore previous session"
                if restore_enabled
                else "New Tab"
            )
        )

        self.startup_mode.currentTextChanged.connect(
            self._set_startup_mode
        )

        startup_row.addLayout(
            startup_text,
            1,
        )

        startup_row.addWidget(
            self.startup_mode
        )

        startup.layout.addLayout(
            startup_row
        )

        layout.addWidget(
            startup
        )

        # ==================================================
        # DOWNLOADS
        # ==================================================

        downloads = SettingsSection(
            "Downloads",
            "Choose where downloaded files are saved.",
        )

        download_row = QHBoxLayout()

        download_text = QVBoxLayout()

        download_title = QLabel(
            "Download location"
        )

        download_title.setObjectName(
            "SettingsRowTitle"
        )

        self.download_path_label = QLabel()

        self.download_path_label.setObjectName(
            "SettingsRowDescription"
        )

        self.download_path_label.setWordWrap(
            True
        )

        download_text.addWidget(
            download_title
        )

        download_text.addWidget(
            self.download_path_label
        )

        choose_folder = QPushButton(
            "Choose folder"
        )

        choose_folder.setObjectName(
            "HistoryClearButton"
        )

        choose_folder.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        choose_folder.clicked.connect(
            self._choose_download_folder
        )

        download_row.addLayout(
            download_text,
            1,
        )

        download_row.addWidget(
            choose_folder
        )

        downloads.layout.addLayout(
            download_row
        )

        self._update_download_path_label()

        layout.addWidget(
            downloads
        )

        # ==================================================
        # PRIVACY
        # ==================================================

        privacy = SettingsSection(
            "Privacy",
            "Control locally stored browsing data.",
        )

        self.save_history_checkbox = (
            self._checkbox_row(
                privacy,
                "Save browsing history",
                "Store visited pages in Veyra history.",
                "privacy/save_history",
                True,
            )
        )

        privacy.layout.addWidget(
            self._separator()
        )

        self.cookies_checkbox = (
            self._checkbox_row(
                privacy,
                "Persistent cookies",
                "Keep website sign-ins between Veyra sessions.",
                "privacy/persistent_cookies",
                True,
            )
        )

        privacy.layout.addWidget(
            self._separator()
        )

        clear_row = QHBoxLayout()

        clear_text = self._label_box(
            "Clear browsing data",
            (
                "Delete browsing history, cookies "
                "and cached website files."
            ),
        )

        clear_button = QPushButton(
            "Clear data"
        )

        clear_button.setObjectName(
            "HistoryClearButton"
        )

        clear_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        clear_button.clicked.connect(
            self._clear_browsing_data
        )

        clear_row.addLayout(
            clear_text,
            1,
        )

        clear_row.addWidget(
            clear_button
        )

        privacy.layout.addLayout(
            clear_row
        )

        layout.addWidget(
            privacy
        )

        # ==================================================
        # RESET
        # ==================================================

        reset = SettingsSection(
            "Reset",
            "Restore Veyra settings to their default values.",
        )

        reset_row = QHBoxLayout()

        reset_text = self._label_box(
            "Reset settings",
            "This does not delete bookmarks or browsing history.",
        )

        reset_button = QPushButton(
            "Reset settings"
        )

        reset_button.setObjectName(
            "HistoryClearButton"
        )

        reset_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        reset_button.clicked.connect(
            self._reset_settings
        )

        reset_row.addLayout(
            reset_text,
            1,
        )

        reset_row.addWidget(
            reset_button
        )

        reset.layout.addLayout(
            reset_row
        )

        layout.addWidget(
            reset
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
            "Version 0.2 • Early development build\n"
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

    # ======================================================
    # BACKGROUND
    # ======================================================

    def _background_changed(
        self,
        text,
    ):

        mapping = {
            "Theme default": "theme",
            "Purple Glow": "purple",
            "Ocean Night": "ocean",
            "Sunset": "sunset",
            "Forest Night": "forest",
            "Custom image": "custom",
        }

        mode = mapping.get(
            text,
            "theme",
        )

        self.settings.setValue(
            "appearance/new_tab_background",
            mode,
        )

    def _choose_background_image(
        self,
    ):

        current = (
            self.settings.value(
                "appearance/new_tab_background_path",
                "",
            )
        )

        start_folder = ""

        if current:

            start_folder = str(
                Path(current).parent
            )

        filename, _filter = (
            QFileDialog.getOpenFileName(
                self,
                "Choose New Tab background",
                start_folder,
                (
                    "Images (*.jpg *.jpeg *.png);;"
                    "JPEG images (*.jpg *.jpeg);;"
                    "PNG images (*.png)"
                ),
            )
        )

        if not filename:
            return

        self.settings.setValue(
            "appearance/new_tab_background_path",
            filename,
        )

        self.settings.setValue(
            "appearance/new_tab_background",
            "custom",
        )

        self.background_combo.setCurrentText(
            "Custom image"
        )

        self._update_background_path_label()

    def _update_background_path_label(
        self,
    ):

        path = (
            self.settings.value(
                "appearance/new_tab_background_path",
                "",
            )
        )

        if path:

            self.background_path_label.setText(
                path
            )

        else:

            self.background_path_label.setText(
                "No custom image selected."
            )

    # ======================================================
    # HELPERS
    # ======================================================

    def _label_box(
        self,
        title,
        description,
    ):

        box = QVBoxLayout()

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

        description_label.setWordWrap(
            True
        )

        box.addWidget(
            title_label
        )

        box.addWidget(
            description_label
        )

        return box

    # ======================================================
    # THEME
    # ======================================================

    def _set_theme(
        self,
        theme_name,
    ):

        self.theme_changed.emit(
            theme_name
        )

    # ======================================================
    # SEARCH ENGINE
    # ======================================================

    def _set_search_engine(
        self,
        value,
    ):

        self.settings.setValue(
            "browser/search_engine",
            value,
        )

    # ======================================================
    # STARTUP
    # ======================================================

    def _set_startup_mode(
        self,
        value,
    ):

        restore = (
            value
            == "Restore previous session"
        )

        self.settings.setValue(
            "browser/restore_session",
            restore,
        )

    # ======================================================
    # ZOOM
    # ======================================================

    def _set_zoom(
        self,
        value,
    ):

        self.settings.setValue(
            "browser/default_zoom",
            value,
        )

        self.default_zoom_changed.emit(
            value
        )

    # ======================================================
    # DOWNLOADS
    # ======================================================

    def _default_download_folder(
        self,
    ):

        location = (
            QStandardPaths.writableLocation(
                QStandardPaths.StandardLocation.DownloadLocation
            )
        )

        if location:

            return location

        return str(
            Path.home()
            / "Downloads"
        )

    def _current_download_folder(
        self,
    ):

        return (
            self.settings.value(
                "downloads/location",
                self._default_download_folder(),
            )
        )

    def _update_download_path_label(
        self,
    ):

        self.download_path_label.setText(
            self._current_download_folder()
        )

    def _choose_download_folder(
        self,
    ):

        selected = (
            QFileDialog.getExistingDirectory(
                self,
                "Choose download folder",
                self._current_download_folder(),
            )
        )

        if not selected:
            return

        self.settings.setValue(
            "downloads/location",
            selected,
        )

        self._update_download_path_label()

        self.download_location_changed.emit(
            selected
        )

    # ======================================================
    # CLEAR DATA
    # ======================================================

    def _clear_browsing_data(
        self,
    ):

        answer = QMessageBox.question(
            self,
            "Clear browsing data",
            (
                "Delete browsing history, cookies "
                "and cached website data?"
            ),
            (
                QMessageBox.StandardButton.Yes
                | QMessageBox.StandardButton.No
            ),
            QMessageBox.StandardButton.No,
        )

        if (
            answer
            != QMessageBox.StandardButton.Yes
        ):

            return

        self.clear_browsing_data_requested.emit()

        QMessageBox.information(
            self,
            "Browsing data cleared",
            "Veyra browsing data has been cleared.",
        )

    # ======================================================
    # RESET
    # ======================================================

    def _reset_settings(
        self,
    ):

        answer = QMessageBox.question(
            self,
            "Reset settings",
            "Restore all Veyra settings to defaults?",
            (
                QMessageBox.StandardButton.Yes
                | QMessageBox.StandardButton.No
            ),
            QMessageBox.StandardButton.No,
        )

        if (
            answer
            != QMessageBox.StandardButton.Yes
        ):

            return

        default_download = (
            self._default_download_folder()
        )

        self.settings.setValue(
            "browser/search_engine",
            "Google",
        )

        self.settings.setValue(
            "browser/restore_session",
            True,
        )

        self.settings.setValue(
            "browser/default_zoom",
            100,
        )

        self.settings.setValue(
            "privacy/save_history",
            True,
        )

        self.settings.setValue(
            "privacy/persistent_cookies",
            True,
        )

        self.settings.setValue(
            "downloads/location",
            default_download,
        )

        self.settings.setValue(
            "appearance/new_tab_background",
            "theme",
        )

        self.search_engine.setCurrentText(
            "Google"
        )

        self.startup_mode.setCurrentText(
            "Restore previous session"
        )

        self.zoom_spin.setValue(
            100
        )

        self.save_history_checkbox.setChecked(
            True
        )

        self.cookies_checkbox.setChecked(
            True
        )

        self.background_combo.setCurrentText(
            "Theme default"
        )

        self._update_download_path_label()

        midnight = (
            self.theme_cards.get(
                "midnight"
            )
        )

        if midnight:

            midnight.setChecked(
                True
            )

        self.theme_changed.emit(
            "midnight"
        )

        self.default_zoom_changed.emit(
            100
        )

        self.download_location_changed.emit(
            default_download
        )

    # ======================================================
    # SEPARATOR
    # ======================================================

    def _separator(
        self,
    ):

        separator = QFrame()

        separator.setObjectName(
            "SettingsSeparator"
        )

        separator.setFrameShape(
            QFrame.Shape.HLine
        )

        return separator

    # ======================================================
    # CHECKBOX
    # ======================================================

    def _checkbox_row(
        self,
        section,
        title,
        description,
        settings_key,
        default_value,
    ):

        row = QHBoxLayout()

        text_box = self._label_box(
            title,
            description,
        )

        checkbox = QCheckBox()

        checkbox.setObjectName(
            "SettingsSwitch"
        )

        value = (
            self.settings.value(
                settings_key,
                default_value,
                type=bool,
            )
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

        section.layout.addLayout(
            row
        )

        return checkbox