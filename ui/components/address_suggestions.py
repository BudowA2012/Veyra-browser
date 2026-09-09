import json

from PySide6.QtCore import (
    QTimer,
    QUrl,
    Qt,
    Signal,
)

from PySide6.QtNetwork import (
    QNetworkAccessManager,
    QNetworkReply,
    QNetworkRequest,
)

from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from ui.styles.style_manager import (
    get_current_theme,
)


class SuggestionRow(QFrame):

    clicked = Signal(str)

    def __init__(
        self,
        text,
        parent=None,
    ):
        super().__init__(
            parent
        )

        self.value = text

        self.setObjectName(
            "SearchSuggestionRow"
        )

        self.setProperty(
            "selected",
            False,
        )

        self.setFixedHeight(
            44
        )

        self.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        layout = QHBoxLayout(
            self
        )

        layout.setContentsMargins(
            14,
            4,
            14,
            4,
        )

        layout.setSpacing(
            10
        )

        # ==================================================
        # SEARCH ICON
        # ==================================================

        self.icon = QLabel(
            "⌕"
        )

        self.icon.setObjectName(
            "SearchSuggestionIcon"
        )

        self.icon.setFixedWidth(
            22
        )

        self.icon.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(
            self.icon
        )

        # ==================================================
        # TEXT
        # ==================================================

        self.label = QLabel(
            text
        )

        self.label.setObjectName(
            "SearchSuggestionText"
        )

        self.label.setTextInteractionFlags(
            Qt.TextInteractionFlag.NoTextInteraction
        )

        layout.addWidget(
            self.label,
            1,
        )

    # ======================================================
    # SELECTED
    # ======================================================

    def set_selected(
        self,
        selected,
    ):

        self.setProperty(
            "selected",
            selected,
        )

        self.style().unpolish(
            self
        )

        self.style().polish(
            self
        )

        self.update()

    # ======================================================
    # CLICK
    # ======================================================

    def mousePressEvent(
        self,
        event,
    ):

        if (
            event.button()
            == Qt.MouseButton.LeftButton
        ):

            self.clicked.emit(
                self.value
            )

        super().mousePressEvent(
            event
        )


class AddressSuggestions(QFrame):

    selected = Signal(str)
    results_ready = Signal()

    MAX_RESULTS = 8

    COLORS = {
        "midnight": {
            "background": "#151922",
            "border": "#2b3140",
            "hover": "#1e2431",
            "selected": "#282f40",
            "text": "#f4f5f8",
            "muted": "#949bab",
        },

        "graphite": {
            "background": "#202124",
            "border": "#37393f",
            "hover": "#292b30",
            "selected": "#33353b",
            "text": "#f2f2f3",
            "muted": "#92959d",
        },

        "aurora": {
            "background": "#181420",
            "border": "#392d4d",
            "hover": "#231b2e",
            "selected": "#2d2340",
            "text": "#f7f3ff",
            "muted": "#a093b5",
        },

        "light": {
            "background": "#ffffff",
            "border": "#d9dce4",
            "hover": "#f3f4f7",
            "selected": "#e9ecf4",
            "text": "#24262b",
            "muted": "#777c87",
        },
    }

    def __init__(
        self,
        parent=None,
    ):
        super().__init__(
            None,
            (
                Qt.WindowType.ToolTip
                | Qt.WindowType.FramelessWindowHint
            ),
        )

        self.setObjectName(
            "AddressSuggestions"
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_ShowWithoutActivating,
            True,
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_StyledBackground,
            True,
        )

        # ==================================================
        # NETWORK
        # ==================================================

        self.network = (
            QNetworkAccessManager(
                self
            )
        )

        self.current_reply = None
        self.current_query = ""

        # ==================================================
        # DEBOUNCE
        # ==================================================

        self.timer = QTimer(
            self
        )

        self.timer.setSingleShot(
            True
        )

        self.timer.setInterval(
            130
        )

        self.timer.timeout.connect(
            self._request_suggestions
        )

        # ==================================================
        # STATE
        # ==================================================

        self.rows = []
        self.current_index = -1

        # ==================================================
        # UI
        # ==================================================

        self._build_ui()
        self._apply_theme()

        self.hide()

    # ======================================================
    # BUILD UI
    # ======================================================

    def _build_ui(
        self,
    ):

        root = QVBoxLayout(
            self
        )

        root.setContentsMargins(
            5,
            5,
            5,
            5,
        )

        root.setSpacing(
            2
        )

        self.container = QWidget()

        self.container.setObjectName(
            "SearchSuggestionContainer"
        )

        self.rows_layout = QVBoxLayout(
            self.container
        )

        self.rows_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        self.rows_layout.setSpacing(
            1
        )

        root.addWidget(
            self.container
        )

    # ======================================================
    # THEME
    # ======================================================

    def _apply_theme(
        self,
    ):

        theme = get_current_theme()

        colors = self.COLORS.get(
            theme,
            self.COLORS["midnight"],
        )

        self.setStyleSheet(
            f"""
            QFrame#AddressSuggestions {{
                background: {colors["background"]};
                border: 1px solid {colors["border"]};
                border-radius: 12px;
            }}

            QWidget#SearchSuggestionContainer {{
                background: transparent;
                border: none;
            }}

            QFrame#SearchSuggestionRow {{
                background: transparent;
                border: none;
                border-radius: 8px;
            }}

            QFrame#SearchSuggestionRow:hover {{
                background: {colors["hover"]};
            }}

            QFrame#SearchSuggestionRow[selected="true"] {{
                background: {colors["selected"]};
            }}

            QLabel#SearchSuggestionIcon {{
                background: transparent;
                color: {colors["muted"]};

                border: none;

                font-size: 18px;
            }}

            QLabel#SearchSuggestionText {{
                background: transparent;
                color: {colors["text"]};

                border: none;

                font-size: 13px;
                font-weight: 500;
            }}
            """
        )

    # ======================================================
    # QUERY
    # ======================================================

    def query(
        self,
        text,
    ):

        text = (
            text
            .strip()
        )

        self.current_query = text

        if not text:

            self.timer.stop()

            self._abort_current_reply()

            self.hide()

            self.clear()

            return

        self.timer.start()

    # ======================================================
    # REQUEST
    # ======================================================

    def _request_suggestions(
        self,
    ):

        query = (
            self.current_query
        )

        if not query:
            return

        # ==================================================
        # ABORT OLD
        # ==================================================

        self._abort_current_reply()

        # ==================================================
        # GOOGLE SUGGEST ENDPOINT
        # ==================================================

        encoded = (
            QUrl.toPercentEncoding(
                query
            )
            .data()
            .decode(
                "utf-8"
            )
        )

        url = QUrl(
            "https://suggestqueries.google.com/"
            "complete/search"
            "?client=firefox"
            f"&q={encoded}"
        )

        request = QNetworkRequest(
            url
        )

        request.setRawHeader(
            b"User-Agent",
            b"Mozilla/5.0 VeyraBrowser",
        )

        request.setRawHeader(
            b"Accept",
            b"application/json,text/plain,*/*",
        )

        reply = (
            self.network.get(
                request
            )
        )

        self.current_reply = reply

        reply.finished.connect(
            lambda:
            self._reply_finished(
                reply,
                query,
            )
        )

    # ======================================================
    # ABORT OLD REPLY
    # ======================================================

    def _abort_current_reply(
        self,
    ):

        if (
            self.current_reply
            is None
        ):

            return

        if (
            self.current_reply.isRunning()
        ):

            self.current_reply.abort()

        self.current_reply = None

    # ======================================================
    # RESPONSE
    # ======================================================

    def _reply_finished(
        self,
        reply,
        requested_query,
    ):

        if (
            reply
            is self.current_reply
        ):

            self.current_reply = None

        # ==================================================
        # ERROR
        # ==================================================

        if (
            reply.error()
            != QNetworkReply.NetworkError.NoError
        ):

            reply.deleteLater()

            return

        # ==================================================
        # STALE RESULT
        # ==================================================

        if (
            requested_query
            != self.current_query
        ):

            reply.deleteLater()

            return

        raw = bytes(
            reply.readAll()
        )

        reply.deleteLater()

        # ==================================================
        # JSON
        # ==================================================

        try:

            decoded = raw.decode(
                "utf-8"
            )

            data = json.loads(
                decoded
            )

        except (
            UnicodeDecodeError,
            json.JSONDecodeError,
        ):

            self.hide()

            return

        # Format:
        #
        # [
        #   "rubi",
        #   [
        #       "rubik's cube",
        #       "rubik's cube solver",
        #       ...
        #   ]
        # ]

        if (
            not isinstance(
                data,
                list,
            )
            or len(data) < 2
        ):

            self.hide()

            return

        suggestions = (
            data[1]
        )

        if not isinstance(
            suggestions,
            list,
        ):

            self.hide()

            return

        cleaned = []

        seen = set()

        for item in suggestions:

            text = (
                str(item)
                .strip()
            )

            if not text:
                continue

            key = (
                text.lower()
            )

            if key in seen:
                continue

            seen.add(
                key
            )

            cleaned.append(
                text
            )

            if (
                len(cleaned)
                >= self.MAX_RESULTS
            ):

                break

        self.set_results(
            cleaned
        )

    # ======================================================
    # SET RESULTS
    # ======================================================

    def set_results(
        self,
        suggestions,
    ):

        self.clear()

        self._apply_theme()

        if not suggestions:

            self.hide()

            return

        for suggestion in suggestions:

            row = SuggestionRow(
                suggestion,
                self.container,
            )

            row.clicked.connect(
                self._row_clicked
            )

            self.rows_layout.addWidget(
                row
            )

            self.rows.append(
                row
            )

        # ==================================================
        # HEIGHT
        # ==================================================

        row_count = len(
            self.rows
        )

        height = (
            10
            + row_count * 45
        )

        self.setFixedHeight(
            height
        )

        # Nie ustawiamy tutaj pozycji,
        # bo górny address bar i New Tab
        # mają inne miejsce na ekranie.

        self.results_ready.emit()

    # ======================================================
    # CLEAR
    # ======================================================

    def clear(
        self,
    ):

        while (
            self.rows_layout.count()
        ):

            item = (
                self.rows_layout
                .takeAt(
                    0
                )
            )

            widget = (
                item.widget()
            )

            if widget:

                widget.deleteLater()

        self.rows = []

        self.current_index = -1

    # ======================================================
    # SHOW BELOW
    # ======================================================

    def show_below(
        self,
        widget,
    ):

        if not self.rows:

            self.hide()

            return

        position = (
            widget.mapToGlobal(
                widget.rect()
                .bottomLeft()
            )
        )

        self.setFixedWidth(
            widget.width()
        )

        self.move(
            position.x(),
            position.y() + 5,
        )

        self.show()

        self.raise_()

    # ======================================================
    # KEYBOARD SELECTION
    # ======================================================

    def move_selection(
        self,
        direction,
    ):

        if not self.rows:
            return

        if (
            self.current_index
            >= 0
        ):

            self.rows[
                self.current_index
            ].set_selected(
                False
            )

        # Pierwsze naciśnięcie.
        if (
            self.current_index
            == -1
        ):

            if direction > 0:

                self.current_index = 0

            else:

                self.current_index = (
                    len(self.rows)
                    - 1
                )

        else:

            self.current_index = (
                self.current_index
                + direction
            ) % len(
                self.rows
            )

        self.rows[
            self.current_index
        ].set_selected(
            True
        )

    # ======================================================
    # CURRENT VALUE
    # ======================================================

    def current_value(
        self,
    ):

        if (
            self.current_index < 0
            or self.current_index
            >= len(self.rows)
        ):

            return None

        return (
            self.rows[
                self.current_index
            ].value
        )

    # ======================================================
    # ACTIVATE CURRENT
    # ======================================================

    def activate_current(
        self,
    ):

        value = (
            self.current_value()
        )

        if not value:

            return False

        self._row_clicked(
            value
        )

        return True

    # ======================================================
    # CLICK
    # ======================================================

    def _row_clicked(
        self,
        value,
    ):

        self.hide()

        self.selected.emit(
            value
        )