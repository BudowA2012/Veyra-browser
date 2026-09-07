from PySide6.QtCore import (
    Qt,
    Signal,
)
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QWidget,
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
        # NAV BUTTONS
        # ==================================================

        self.back_button = QPushButton(
            "‹"
        )

        self.forward_button = QPushButton(
            "›"
        )

        self.reload_button = QPushButton(
            "↻"
        )

        self.home_button = QPushButton(
            "⌂"
        )

        for button in (
            self.back_button,
            self.forward_button,
            self.reload_button,
            self.home_button,
        ):

            button.setObjectName(
                "NavigationButton"
            )

            button.setFixedSize(
                36,
                36,
            )

            button.setCursor(
                Qt.CursorShape.PointingHandCursor
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

        # ==================================================
        # QR BUTTON
        # ==================================================

        self.qr_button = QPushButton(
            "QR"
        )

        self.qr_button.setObjectName(
            "NavigationButton"
        )

        self.qr_button.setFixedSize(
            36,
            36,
        )

        self.qr_button.setToolTip(
            "Create QR code for this page"
        )

        self.qr_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        # ==================================================
        # LAYOUT
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

    # ==================================================
    # ADDRESS
    # ==================================================

    def _address_submitted(
        self,
    ):

        text = (
            self.address_bar
            .text()
            .strip()
        )

        if text:

            self.navigate_requested.emit(
                text
            )

    def set_url(
        self,
        url: str,
    ):

        self.address_bar.setText(
            url
        )

        self.address_bar.setCursorPosition(
            0
        )

    def focus_address_bar(
        self,
    ):

        self.address_bar.setFocus()

        self.address_bar.selectAll()