from PySide6.QtCore import Qt, Signal
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

from core.storage.shortcut_repository import ShortcutRepository
from ui.new_tab.shortcut_card import ShortcutCard
from ui.new_tab.shortcut_dialog import ShortcutDialog


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

        self.setObjectName(
            "NewTabPage"
        )

        self._build_ui()
        self._load_shortcuts()

    # ==================================================
    # UI
    # ==================================================

    def _build_ui(self):

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

        center = QWidget()

        center.setObjectName(
            "NewTabCenter"
        )

        center.setMaximumWidth(
            760
        )

        center_layout = QVBoxLayout(
            center
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

        logo = QLabel(
            "Veyra"
        )

        logo.setObjectName(
            "VeyraLogo"
        )

        logo.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        center_layout.addWidget(
            logo
        )

        subtitle = QLabel(
            "Fast. Private. Yours."
        )

        subtitle.setObjectName(
            "VeyraSubtitle"
        )

        subtitle.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        center_layout.addWidget(
            subtitle
        )

        # ==================================================
        # SEARCH
        # ==================================================

        search_frame = QFrame()

        search_frame.setObjectName(
            "NewTabSearchContainer"
        )

        search_layout = QHBoxLayout(
            search_frame
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
            search_frame
        )

        self.search_bar.returnPressed.connect(
            self._submit_search
        )

        self.search_button.clicked.connect(
            self._submit_search
        )

        # ==================================================
        # SHORTCUTS TITLE
        # ==================================================

        shortcuts_header = QHBoxLayout()

        shortcuts_header.setContentsMargins(
            4,
            8,
            4,
            0,
        )

        shortcuts_title = QLabel(
            "Shortcuts"
        )

        shortcuts_title.setObjectName(
            "ShortcutsTitle"
        )

        shortcuts_header.addWidget(
            shortcuts_title
        )

        shortcuts_header.addStretch()

        center_layout.addLayout(
            shortcuts_header
        )

        # ==================================================
        # SHORTCUT GRID
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
            center,
            alignment=Qt.AlignmentFlag.AlignHCenter,
        )

        main.addStretch(
            3
        )

    # ==================================================
    # SEARCH
    # ==================================================

    def _submit_search(self):

        text = (
            self.search_bar
            .text()
            .strip()
        )

        if text:

            self.search_requested.emit(
                text
            )

    # ==================================================
    # SHORTCUTS
    # ==================================================

    def _clear_shortcuts(self):

        while self.grid.count():

            item = self.grid.takeAt(
                0
            )

            widget = item.widget()

            if widget:

                widget.deleteLater()

    def _load_shortcuts(self):

        self._clear_shortcuts()

        shortcuts = (
            self.repository.get_all()
        )

        # Pierwsze uruchomienie
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

            for name, url in defaults:

                self.repository.add(
                    name,
                    url,
                )

            shortcuts = (
                self.repository.get_all()
            )

        # ==================================================
        # NORMAL CARDS
        # ==================================================

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
        # ADD SHORTCUT CARD
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

    # ==================================================
    # ADD
    # ==================================================

    def _add_shortcut(self):

        dialog = ShortcutDialog(
            self
        )

        if not dialog.exec():
            return

        name, url = (
            dialog.values()
        )

        if not name or not url:
            return

        self.repository.add(
            name,
            url,
        )

        self._load_shortcuts()

    # ==================================================
    # EDIT
    # ==================================================

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

    # ==================================================
    # DELETE
    # ==================================================

    def _delete_shortcut(
        self,
        shortcut_id,
    ):

        self.repository.delete(
            shortcut_id
        )

        self._load_shortcuts()

    # ==================================================
    # FOCUS
    # ==================================================

    def focus_search(self):

        self.search_bar.setFocus()

        self.search_bar.selectAll()