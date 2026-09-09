from pathlib import Path

from PySide6.QtCore import (
    QEvent,
    QSettings,
    Qt,
    Signal,
)

from PySide6.QtGui import (
    QColor,
    QLinearGradient,
    QPainter,
    QPixmap,
)

from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from core.storage.shortcut_repository import (
    ShortcutRepository,
)

from ui.components.address_suggestions import (
    AddressSuggestions,
)

from ui.new_tab.shortcut_card import (
    ShortcutCard,
)

from ui.new_tab.shortcut_dialog import (
    ShortcutDialog,
)


class NewTabPage(QWidget):

    search_requested = Signal(str)
    shortcut_requested = Signal(str)

    MAX_COLUMNS = 4

    def __init__(
        self,
        parent=None,
    ):
        super().__init__(
            parent
        )

        self.repository = (
            ShortcutRepository()
        )

        self.settings = QSettings(
            "Veyra",
            "VeyraBrowser",
        )

        self.background_mode = "theme"
        self.background_path = ""

        self.background_pixmap = None

        self.setObjectName(
            "NewTabPage"
        )

        self._load_background()

        self._build_ui()

        self._load_shortcuts()

    # ======================================================
    # BACKGROUND SETTINGS
    # ======================================================

    def _load_background(
        self,
    ):

        self.background_mode = (
            self.settings.value(
                "appearance/new_tab_background",
                "theme",
            )
        )

        self.background_path = (
            self.settings.value(
                "appearance/new_tab_background_path",
                "",
            )
        )

        self.background_pixmap = None

        if (
            self.background_mode
            == "custom"
            and self.background_path
        ):

            path = Path(
                self.background_path
            )

            if path.exists():

                pixmap = QPixmap(
                    str(path)
                )

                if not pixmap.isNull():

                    self.background_pixmap = (
                        pixmap
                    )

    # ======================================================
    # SHOW
    # ======================================================

    def showEvent(
        self,
        event,
    ):

        super().showEvent(
            event
        )

        self._load_background()

        self.update()

    # ======================================================
    # BACKGROUND
    # ======================================================

    def paintEvent(
        self,
        event,
    ):

        super().paintEvent(
            event
        )

        if (
            self.background_mode
            == "theme"
        ):

            return

        painter = QPainter(
            self
        )

        painter.setRenderHint(
            QPainter.RenderHint.SmoothPixmapTransform,
            True,
        )

        rect = self.rect()

        # ==================================================
        # CUSTOM IMAGE
        # ==================================================

        if (
            self.background_mode
            == "custom"
            and self.background_pixmap
            is not None
        ):

            scaled = (
                self.background_pixmap
                .scaled(
                    self.size(),
                    Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )

            source_x = max(
                0,
                (
                    scaled.width()
                    - self.width()
                ) // 2,
            )

            source_y = max(
                0,
                (
                    scaled.height()
                    - self.height()
                ) // 2,
            )

            source_width = min(
                self.width(),
                scaled.width(),
            )

            source_height = min(
                self.height(),
                scaled.height(),
            )

            painter.drawPixmap(
                0,
                0,
                self.width(),
                self.height(),
                scaled,
                source_x,
                source_y,
                source_width,
                source_height,
            )

            # Lekko przyciemniamy całą tapetę,
            # ale NIE robimy żadnego czarnego panelu
            # pod centralnym UI.
            painter.fillRect(
                rect,
                QColor(
                    0,
                    0,
                    0,
                    55,
                ),
            )

            painter.end()

            return

        # ==================================================
        # PURPLE
        # ==================================================

        if (
            self.background_mode
            == "purple"
        ):

            gradient = QLinearGradient(
                0,
                0,
                self.width(),
                self.height(),
            )

            gradient.setColorAt(
                0.0,
                QColor(
                    "#161225"
                ),
            )

            gradient.setColorAt(
                0.45,
                QColor(
                    "#281848"
                ),
            )

            gradient.setColorAt(
                1.0,
                QColor(
                    "#10131d"
                ),
            )

            painter.fillRect(
                rect,
                gradient,
            )

        # ==================================================
        # OCEAN
        # ==================================================

        elif (
            self.background_mode
            == "ocean"
        ):

            gradient = QLinearGradient(
                0,
                0,
                self.width(),
                self.height(),
            )

            gradient.setColorAt(
                0.0,
                QColor(
                    "#071a2b"
                ),
            )

            gradient.setColorAt(
                0.5,
                QColor(
                    "#0c3145"
                ),
            )

            gradient.setColorAt(
                1.0,
                QColor(
                    "#12152b"
                ),
            )

            painter.fillRect(
                rect,
                gradient,
            )

        # ==================================================
        # SUNSET
        # ==================================================

        elif (
            self.background_mode
            == "sunset"
        ):

            gradient = QLinearGradient(
                0,
                0,
                self.width(),
                self.height(),
            )

            gradient.setColorAt(
                0.0,
                QColor(
                    "#35152f"
                ),
            )

            gradient.setColorAt(
                0.50,
                QColor(
                    "#6a2a3e"
                ),
            )

            gradient.setColorAt(
                1.0,
                QColor(
                    "#191728"
                ),
            )

            painter.fillRect(
                rect,
                gradient,
            )

        # ==================================================
        # FOREST
        # ==================================================

        elif (
            self.background_mode
            == "forest"
        ):

            gradient = QLinearGradient(
                0,
                0,
                self.width(),
                self.height(),
            )

            gradient.setColorAt(
                0.0,
                QColor(
                    "#0b1e19"
                ),
            )

            gradient.setColorAt(
                0.48,
                QColor(
                    "#173b31"
                ),
            )

            gradient.setColorAt(
                1.0,
                QColor(
                    "#10191c"
                ),
            )

            painter.fillRect(
                rect,
                gradient,
            )

        painter.end()

    # ======================================================
    # UI
    # ======================================================

    def _build_ui(
        self,
    ):

        main = QVBoxLayout(
            self
        )

        main.setContentsMargins(
            40,
            40,
            40,
            40,
        )

        main.setSpacing(
            0
        )

        main.addStretch(
            2
        )

        # ==================================================
        # CENTER
        # ==================================================

        self.center = QWidget()

        self.center.setObjectName(
            "NewTabCenter"
        )

        # WAŻNE:
        # cały centralny kontener jest przezroczysty
        self.center.setAttribute(
            Qt.WidgetAttribute.WA_StyledBackground,
            True,
        )

        self.center.setStyleSheet(
            """
            QWidget#NewTabCenter {
                background: transparent;
                border: none;
            }
            """
        )

        self.center.setMaximumWidth(
            760
        )

        center_layout = QVBoxLayout(
            self.center
        )

        center_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        center_layout.setSpacing(
            22
        )

        # ==================================================
        # LOGO
        # ==================================================

        self.logo = QLabel(
            "Veyra"
        )

        self.logo.setObjectName(
            "VeyraLogo"
        )

        self.logo.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.logo.setStyleSheet(
            """
            background: transparent;
            border: none;
            """
        )

        center_layout.addWidget(
            self.logo
        )

        # ==================================================
        # SUBTITLE
        # ==================================================

        self.subtitle = QLabel(
            "Fast. Private. Yours."
        )

        self.subtitle.setObjectName(
            "VeyraSubtitle"
        )

        self.subtitle.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.subtitle.setStyleSheet(
            """
            background: transparent;
            border: none;
            """
        )

        center_layout.addWidget(
            self.subtitle
        )

        # ==================================================
        # SEARCH FRAME
        # ==================================================

        self.search_frame = QFrame()

        self.search_frame.setObjectName(
            "NewTabSearchContainer"
        )

        search_layout = QHBoxLayout(
            self.search_frame
        )

        search_layout.setContentsMargins(
            18,
            5,
            6,
            5,
        )

        search_layout.setSpacing(
            6
        )

        # ==================================================
        # SEARCH BAR
        # ==================================================

        self.search_bar = QLineEdit()

        self.search_bar.setObjectName(
            "NewTabSearch"
        )

        self.search_bar.setPlaceholderText(
            "Search the web or enter an address"
        )

        self.search_bar.setMinimumHeight(
            42
        )

        self.search_bar.installEventFilter(
            self
        )

        # ==================================================
        # SEARCH BUTTON
        # ==================================================

        self.search_button = QPushButton(
            "→"
        )

        self.search_button.setObjectName(
            "NewTabSearchButton"
        )

        self.search_button.setFixedSize(
            42,
            42,
        )

        self.search_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        search_layout.addWidget(
            self.search_bar,
            1,
        )

        search_layout.addWidget(
            self.search_button
        )

        center_layout.addWidget(
            self.search_frame
        )

        # ==================================================
        # SUGGESTIONS
        # ==================================================

        self.suggestions = (
            AddressSuggestions()
        )

        self.suggestions.selected.connect(
            self._suggestion_selected
        )

        self.suggestions.results_ready.connect(
            self._show_suggestions
        )

        # ==================================================
        # SEARCH SIGNALS
        # ==================================================

        self.search_bar.textEdited.connect(
            self._search_text_edited
        )

        self.search_bar.returnPressed.connect(
            self._submit_search
        )

        self.search_button.clicked.connect(
            self._submit_search
        )

        # ==================================================
        # SHORTCUT HEADER
        # ==================================================

        shortcuts_header = QHBoxLayout()

        shortcuts_header.setContentsMargins(
            4,
            8,
            4,
            0,
        )

        self.shortcuts_title = QLabel(
            "Shortcuts"
        )

        self.shortcuts_title.setObjectName(
            "ShortcutsTitle"
        )

        self.shortcuts_title.setStyleSheet(
            """
            background: transparent;
            border: none;
            """
        )

        shortcuts_header.addWidget(
            self.shortcuts_title
        )

        shortcuts_header.addStretch()

        center_layout.addLayout(
            shortcuts_header
        )

        # ==================================================
        # SHORTCUTS
        # ==================================================

        self.grid = QGridLayout()

        self.grid.setHorizontalSpacing(
            14
        )

        self.grid.setVerticalSpacing(
            14
        )

        self.grid.setAlignment(
            Qt.AlignmentFlag.AlignHCenter
            | Qt.AlignmentFlag.AlignTop
        )

        center_layout.addLayout(
            self.grid
        )

        # ==================================================
        # PAGE
        # ==================================================

        main.addWidget(
            self.center,
            alignment=(
                Qt.AlignmentFlag.AlignHCenter
            ),
        )

        main.addStretch(
            3
        )

    # ======================================================
    # SEARCH
    # ======================================================

    def _search_text_edited(
        self,
        text,
    ):

        self.suggestions.query(
            text
        )

    def _show_suggestions(
        self,
    ):

        if not self.search_bar.hasFocus():
            return

        self.suggestions.show_below(
            self.search_frame
        )

    def _suggestion_selected(
        self,
        value,
    ):

        value = (
            str(value)
            .strip()
        )

        if not value:
            return

        self.search_bar.setText(
            value
        )

        self.suggestions.hide()

        self.search_requested.emit(
            value
        )

    def _submit_search(
        self,
    ):

        if (
            self.suggestions.isVisible()
            and self.suggestions.activate_current()
        ):

            return

        text = (
            self.search_bar
            .text()
            .strip()
        )

        if not text:
            return

        self.suggestions.hide()

        self.search_requested.emit(
            text
        )

    # ======================================================
    # KEYBOARD
    # ======================================================

    def eventFilter(
        self,
        watched,
        event,
    ):

        if (
            watched
            is self.search_bar
            and event.type()
            == QEvent.Type.KeyPress
        ):

            key = (
                event.key()
            )

            if (
                key
                == Qt.Key.Key_Down
            ):

                if (
                    self.suggestions
                    .isVisible()
                ):

                    self.suggestions.move_selection(
                        1
                    )

                    return True

            if (
                key
                == Qt.Key.Key_Up
            ):

                if (
                    self.suggestions
                    .isVisible()
                ):

                    self.suggestions.move_selection(
                        -1
                    )

                    return True

            if (
                key
                == Qt.Key.Key_Escape
            ):

                self.suggestions.hide()

                return True

        return super().eventFilter(
            watched,
            event,
        )

    # ======================================================
    # SHORTCUTS
    # ======================================================

    def _clear_shortcuts(
        self,
    ):

        while self.grid.count():

            item = (
                self.grid.takeAt(
                    0
                )
            )

            widget = (
                item.widget()
            )

            if widget:

                widget.deleteLater()

    def _load_shortcuts(
        self,
    ):

        self._clear_shortcuts()

        shortcuts = (
            self.repository.get_all()
        )

        if not shortcuts:

            defaults = [
                (
                    "Google",
                    "https://google.com",
                ),
                (
                    "YouTube",
                    "https://youtube.com",
                ),
                (
                    "GitHub",
                    "https://github.com",
                ),
            ]

            for (
                name,
                url,
            ) in defaults:

                self.repository.add(
                    name,
                    url,
                )

            shortcuts = (
                self.repository.get_all()
            )

        position = 0

        for (
            shortcut_id,
            name,
            url,
        ) in shortcuts:

            row = (
                position
                // self.MAX_COLUMNS
            )

            column = (
                position
                % self.MAX_COLUMNS
            )

            card = ShortcutCard(
                shortcut_id,
                name,
                url,
            )

            card.clicked_url.connect(
                self.shortcut_requested.emit
            )

            card.edit_requested.connect(
                self._edit_shortcut
            )

            card.delete_requested.connect(
                self._delete_shortcut
            )

            self.grid.addWidget(
                card,
                row,
                column,
            )

            position += 1

        # ==================================================
        # ADD SHORTCUT
        # ==================================================

        row = (
            position
            // self.MAX_COLUMNS
        )

        column = (
            position
            % self.MAX_COLUMNS
        )

        add_button = QPushButton()

        add_button.setObjectName(
            "AddShortcutCard"
        )

        add_button.setText(
            "+\nAdd shortcut"
        )

        add_button.setFixedSize(
            150,
            125,
        )

        add_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        add_button.clicked.connect(
            self._add_shortcut
        )

        self.grid.addWidget(
            add_button,
            row,
            column,
        )

    # ======================================================
    # ADD
    # ======================================================

    def _add_shortcut(
        self,
    ):

        dialog = ShortcutDialog(
            self
        )

        if not dialog.exec():
            return

        name, url = (
            dialog.values()
        )

        if (
            not name
            or not url
        ):

            return

        self.repository.add(
            name,
            url,
        )

        self._load_shortcuts()

    # ======================================================
    # EDIT
    # ======================================================

    def _edit_shortcut(
        self,
        shortcut_id,
    ):

        shortcuts = (
            self.repository.get_all()
        )

        for (
            current_id,
            name,
            url,
        ) in shortcuts:

            if (
                current_id
                != shortcut_id
            ):

                continue

            dialog = ShortcutDialog(
                self,
                name,
                url,
            )

            if not dialog.exec():
                return

            new_name, new_url = (
                dialog.values()
            )

            if (
                not new_name
                or not new_url
            ):

                return

            self.repository.update(
                shortcut_id,
                new_name,
                new_url,
            )

            self._load_shortcuts()

            return

    # ======================================================
    # DELETE
    # ======================================================

    def _delete_shortcut(
        self,
        shortcut_id,
    ):

        self.repository.delete(
            shortcut_id
        )

        self._load_shortcuts()

    # ======================================================
    # FOCUS
    # ======================================================

    def focus_search(
        self,
    ):

        self.search_bar.setFocus()

        self.search_bar.selectAll()