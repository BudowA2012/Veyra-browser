from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QWidget,
)


class NavigationBar(QWidget):
    navigate_requested = Signal(str)
    new_tab_requested = Signal()

    back_requested = Signal()
    forward_requested = Signal()
    reload_requested = Signal()
    home_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("NavigationBar")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(6)

        self.back_button = QPushButton("‹")
        self.forward_button = QPushButton("›")
        self.reload_button = QPushButton("↻")
        self.home_button = QPushButton("⌂")

        self.address_bar = QLineEdit()
        self.address_bar.setPlaceholderText(
            "Search or enter address..."
        )

        self.new_tab_button = QPushButton("+")
        self.new_tab_button.setObjectName("NewTabButton")

        for button in (
            self.back_button,
            self.forward_button,
            self.reload_button,
            self.home_button,
            self.new_tab_button,
        ):
            button.setCursor(
                self.cursor().shape()
            )

        layout.addWidget(self.back_button)
        layout.addWidget(self.forward_button)
        layout.addWidget(self.reload_button)
        layout.addWidget(self.home_button)

        layout.addWidget(self.address_bar, 1)

        layout.addWidget(self.new_tab_button)

        self.address_bar.returnPressed.connect(
            self._address_submitted
        )

        self.new_tab_button.clicked.connect(
            self.new_tab_requested.emit
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

    def _address_submitted(self):
        text = self.address_bar.text().strip()

        if text:
            self.navigate_requested.emit(text)

    def set_url(self, url: str):
        self.address_bar.setText(url)
        self.address_bar.setCursorPosition(0)

    def focus_address_bar(self):
        self.address_bar.setFocus()
        self.address_bar.selectAll()