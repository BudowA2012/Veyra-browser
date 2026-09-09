from PySide6.QtCore import (
    Qt,
    Signal,
)

from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from core.bookmarks.bookmark_repository import (
    BookmarkRepository,
)

from ui.components.icon_factory import (
    create_icon,
)

from ui.styles.style_manager import (
    get_current_theme,
)


class BookmarkItem(QFrame):

    open_requested = Signal(str)
    delete_requested = Signal(int)

    COLORS = {
        "midnight": {
            "background": "#171b24",
            "border": "#292f3d",
            "hover": "#1e2430",
            "title": "#f1f2f6",
            "url": "#9097a7",
            "button": "#aeb3c1",
        },

        "graphite": {
            "background": "#222326",
            "border": "#37393f",
            "hover": "#2b2d31",
            "title": "#f2f2f2",
            "url": "#96999f",
            "button": "#c1c3c8",
        },

        "aurora": {
            "background": "#191520",
            "border": "#3a2e4d",
            "hover": "#231c2d",
            "title": "#f6f2ff",
            "url": "#9d92ae",
            "button": "#bb91ff",
        },

        "light": {
            "background": "#ffffff",
            "border": "#dfe1e8",
            "hover": "#f5f6f8",
            "title": "#24262b",
            "url": "#777c87",
            "button": "#666b76",
        },
    }

    def __init__(
        self,
        bookmark_id,
        title,
        url,
        parent=None,
    ):
        super().__init__(
            parent
        )

        self.bookmark_id = bookmark_id
        self.url = url

        self.setObjectName(
            "BookmarkItem"
        )

        self.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.setMinimumHeight(
            74
        )

        self._build_ui(
            title,
            url,
        )

        self._apply_theme()

    # ======================================================
    # UI
    # ======================================================

    def _build_ui(
        self,
        title,
        url,
    ):

        layout = QHBoxLayout(
            self
        )

        layout.setContentsMargins(
            18,
            10,
            12,
            10,
        )

        layout.setSpacing(
            12
        )

        # ==================================================
        # ICON
        # ==================================================

        icon = QLabel()

        icon.setPixmap(
            create_icon(
                "bookmark",
                22,
            ).pixmap(
                22,
                22,
            )
        )

        icon.setFixedWidth(
            28
        )

        layout.addWidget(
            icon
        )

        # ==================================================
        # TEXT
        # ==================================================

        text_layout = QVBoxLayout()

        text_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        text_layout.setSpacing(
            3
        )

        self.title_label = QLabel(
            title
        )

        self.title_label.setObjectName(
            "BookmarkItemTitle"
        )

        self.url_label = QLabel(
            url
        )

        self.url_label.setObjectName(
            "BookmarkItemUrl"
        )

        text_layout.addWidget(
            self.title_label
        )

        text_layout.addWidget(
            self.url_label
        )

        layout.addLayout(
            text_layout,
            1,
        )

        # ==================================================
        # OPEN
        # ==================================================

        self.open_button = QPushButton(
            "Open"
        )

        self.open_button.setObjectName(
            "BookmarkOpenButton"
        )

        self.open_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.open_button.clicked.connect(
            lambda:
            self.open_requested.emit(
                self.url
            )
        )

        layout.addWidget(
            self.open_button
        )

        # ==================================================
        # DELETE
        # ==================================================

        self.delete_button = QPushButton(
            "Remove"
        )

        self.delete_button.setObjectName(
            "BookmarkDeleteButton"
        )

        self.delete_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.delete_button.clicked.connect(
            lambda:
            self.delete_requested.emit(
                self.bookmark_id
            )
        )

        layout.addWidget(
            self.delete_button
        )

    # ======================================================
    # THEME
    # ======================================================

    def _apply_theme(
        self,
    ):

        theme = (
            get_current_theme()
        )

        colors = (
            self.COLORS.get(
                theme,
                self.COLORS["midnight"],
            )
        )

        self.setStyleSheet(
            f"""
            QFrame#BookmarkItem {{
                background: {colors["background"]};
                border: 1px solid {colors["border"]};
                border-radius: 12px;
            }}

            QFrame#BookmarkItem:hover {{
                background: {colors["hover"]};
            }}

            QLabel#BookmarkItemTitle {{
                background: transparent;
                border: none;
                color: {colors["title"]};
                font-size: 14px;
                font-weight: 600;
            }}

            QLabel#BookmarkItemUrl {{
                background: transparent;
                border: none;
                color: {colors["url"]};
                font-size: 11px;
            }}

            QPushButton#BookmarkOpenButton,
            QPushButton#BookmarkDeleteButton {{
                min-height: 30px;
                padding: 0 12px;

                background: transparent;
                color: {colors["button"]};

                border: 1px solid {colors["border"]};
                border-radius: 7px;
            }}

            QPushButton#BookmarkOpenButton:hover,
            QPushButton#BookmarkDeleteButton:hover {{
                background: {colors["hover"]};
            }}
            """
        )

    # ======================================================
    # CLICK
    # ======================================================

    def mouseDoubleClickEvent(
        self,
        event,
    ):

        if (
            event.button()
            == Qt.MouseButton.LeftButton
        ):

            self.open_requested.emit(
                self.url
            )

        super().mouseDoubleClickEvent(
            event
        )


class BookmarksPage(QWidget):

    open_requested = Signal(str)

    def __init__(
        self,
        repository=None,
        parent=None,
    ):
        super().__init__(
            parent
        )

        self.setObjectName(
            "BookmarksPage"
        )

        self.repository = (
            repository
            or BookmarkRepository()
        )

        self._build_ui()

        self.reload()

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
            50,
            40,
            50,
            40,
        )

        main.setSpacing(
            20
        )

        # ==================================================
        # HEADER
        # ==================================================

        header = QHBoxLayout()

        title = QLabel(
            "Bookmarks"
        )

        title.setObjectName(
            "HistoryPageTitle"
        )

        header.addWidget(
            title
        )

        header.addStretch()

        self.clear_button = QPushButton(
            "Clear bookmarks"
        )

        self.clear_button.setObjectName(
            "HistoryClearButton"
        )

        self.clear_button.clicked.connect(
            self._clear_bookmarks
        )

        header.addWidget(
            self.clear_button
        )

        main.addLayout(
            header
        )

        # ==================================================
        # SEARCH
        # ==================================================

        self.search = QLineEdit()

        self.search.setObjectName(
            "HistorySearch"
        )

        self.search.setPlaceholderText(
            "Search bookmarks..."
        )

        self.search.textChanged.connect(
            self.reload
        )

        main.addWidget(
            self.search
        )

        # ==================================================
        # SCROLL
        # ==================================================

        self.scroll = QScrollArea()

        self.scroll.setWidgetResizable(
            True
        )

        self.scroll.setFrameShape(
            QScrollArea.Shape.NoFrame
        )

        self.container = QWidget()

        self.items_layout = QVBoxLayout(
            self.container
        )

        self.items_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        self.items_layout.setSpacing(
            10
        )

        self.items_layout.addStretch()

        self.scroll.setWidget(
            self.container
        )

        main.addWidget(
            self.scroll,
            1,
        )

    # ======================================================
    # RELOAD
    # ======================================================

    def reload(
        self,
    ):

        while (
            self.items_layout.count()
        ):

            item = (
                self.items_layout
                .takeAt(
                    0
                )
            )

            widget = (
                item.widget()
            )

            if widget:

                widget.deleteLater()

        query = (
            self.search
            .text()
            .strip()
        )

        entries = (
            self.repository.search(
                query
            )
        )

        if not entries:

            empty = QLabel(
                "No bookmarks yet."
            )

            empty.setAlignment(
                Qt.AlignmentFlag.AlignCenter
            )

            empty.setObjectName(
                "HistoryEmpty"
            )

            self.items_layout.addWidget(
                empty
            )

            self.items_layout.addStretch()

            return

        for (
            bookmark_id,
            title,
            url,
            _created_at,
        ) in entries:

            item = BookmarkItem(
                bookmark_id,
                title,
                url,
            )

            item.open_requested.connect(
                self.open_requested.emit
            )

            item.delete_requested.connect(
                self._delete_bookmark
            )

            self.items_layout.addWidget(
                item
            )

        self.items_layout.addStretch()

    # ======================================================
    # DELETE
    # ======================================================

    def _delete_bookmark(
        self,
        bookmark_id,
    ):

        self.repository.delete(
            bookmark_id
        )

        self.reload()

    # ======================================================
    # CLEAR
    # ======================================================

    def _clear_bookmarks(
        self,
    ):

        self.repository.clear()

        self.reload()