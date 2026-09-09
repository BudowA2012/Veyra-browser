from PySide6.QtCore import (
    QEvent,
    QSize,
    Qt,
    Signal,
)

from PySide6.QtWidgets import (
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QWidget,
)

from ui.components.address_suggestions import (
    AddressSuggestions,
)

from ui.components.icon_factory import (
    create_icon,
)


class NavigationBar(QWidget):

    navigate_requested = Signal(str)

    back_requested = Signal()
    forward_requested = Signal()
    reload_requested = Signal()
    home_requested = Signal()

    qr_requested = Signal()

    def __init__(
        self,
        parent=None,
    ):
        super().__init__(
            parent
        )

        self.setObjectName(
            "NavigationBar"
        )

        # ==================================================
        # LAYOUT
        # ==================================================

        layout = QHBoxLayout(
            self
        )

        layout.setContentsMargins(
            12,
            7,
            12,
            7,
        )

        layout.setSpacing(
            6
        )

        # ==================================================
        # BACK
        # ==================================================

        self.back_button = QPushButton()

        self._prepare_button(
            self.back_button,
            "back",
            "Back",
        )

        # ==================================================
        # FORWARD
        # ==================================================

        self.forward_button = QPushButton()

        self._prepare_button(
            self.forward_button,
            "forward",
            "Forward",
        )

        # ==================================================
        # RELOAD
        # ==================================================

        self.reload_button = QPushButton()

        self._prepare_button(
            self.reload_button,
            "reload",
            "Reload",
        )

        # ==================================================
        # HOME
        # ==================================================

        self.home_button = QPushButton()

        self._prepare_button(
            self.home_button,
            "home",
            "Home",
        )

        # ==================================================
        # ADDRESS BAR
        # ==================================================

        self.address_bar = QLineEdit()

        self.address_bar.setObjectName(
            "AddressBar"
        )

        self.address_bar.setPlaceholderText(
            "Search or enter address"
        )

        self.address_bar.setMinimumHeight(
            38
        )

        self.address_bar.setClearButtonEnabled(
            True
        )

        self.address_bar.installEventFilter(
            self
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
        # QR
        # ==================================================

        self.qr_button = QPushButton()

        self._prepare_button(
            self.qr_button,
            "qr",
            "Create QR code",
        )

        # ==================================================
        # ADD WIDGETS
        # ==================================================

        layout.addWidget(
            self.back_button
        )

        layout.addWidget(
            self.forward_button
        )

        layout.addWidget(
            self.reload_button
        )

        layout.addWidget(
            self.home_button
        )

        layout.addWidget(
            self.address_bar,
            1,
        )

        layout.addWidget(
            self.qr_button
        )

        # ==================================================
        # SIGNALS
        # ==================================================

        self.address_bar.textEdited.connect(
            self._address_text_edited
        )

        self.address_bar.returnPressed.connect(
            self._address_submitted
        )

        self.back_button.clicked.connect(
            self.back_requested.emit
        )

        self.forward_button.clicked.connect(
            self.forward_requested.emit
        )

        self.reload_button.clicked.connect(
            self.reload_requested.emit
        )

        self.home_button.clicked.connect(
            self.home_requested.emit
        )

        self.qr_button.clicked.connect(
            self.qr_requested.emit
        )

    # ======================================================
    # BUTTON
    # ======================================================

    def _prepare_button(
        self,
        button,
        icon_name,
        tooltip,
    ):

        button.setObjectName(
            "NavigationButton"
        )

        button.setFixedSize(
            36,
            36,
        )

        button.setIcon(
            create_icon(
                icon_name,
                20,
            )
        )

        button.setIconSize(
            QSize(
                20,
                20,
            )
        )

        button.setToolTip(
            tooltip
        )

        button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

    # ======================================================
    # TEXT EDITED
    # ======================================================

    def _address_text_edited(
        self,
        text,
    ):

        self.suggestions.query(
            text
        )

    # ======================================================
    # SHOW SUGGESTIONS
    # ======================================================

    def _show_suggestions(
        self,
    ):

        if not self.address_bar.hasFocus():
            return

        self.suggestions.show_below(
            self.address_bar
        )

    # ======================================================
    # SUBMIT
    # ======================================================

    def _address_submitted(
        self,
    ):

        if (
            self.suggestions.isVisible()
            and self.suggestions.activate_current()
        ):

            return

        text = (
            self.address_bar
            .text()
            .strip()
        )

        if not text:
            return

        self.suggestions.hide()

        self.navigate_requested.emit(
            text
        )

    # ======================================================
    # SUGGESTION SELECTED
    # ======================================================

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

        self.address_bar.setText(
            value
        )

        self.suggestions.hide()

        self.navigate_requested.emit(
            value
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
            is self.address_bar
            and event.type()
            == QEvent.Type.KeyPress
        ):

            key = (
                event.key()
            )

            # ==============================================
            # DOWN
            # ==============================================

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

            # ==============================================
            # UP
            # ==============================================

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

            # ==============================================
            # ESC
            # ==============================================

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
    # URL
    # ======================================================

    def set_url(
        self,
        url,
    ):

        self.suggestions.hide()

        self.address_bar.setText(
            url
        )

        self.address_bar.setCursorPosition(
            0
        )

    # ======================================================
    # FOCUS
    # ======================================================

    def focus_address_bar(
        self,
    ):

        self.address_bar.setFocus()

        self.address_bar.selectAll()

    # ======================================================
    # HIDE
    # ======================================================

    def hide_suggestions(
        self,
    ):

        self.suggestions.hide()