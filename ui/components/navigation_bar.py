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

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(5)

        self.back_button = QPushButton("←")
        self.forward_button = QPushButton("→")
        self.reload_button = QPushButton("↻")
        self.home_button = QPushButton("⌂")

        self.address_bar = QLineEdit()
        self.address_bar.setPlaceholderText(
            "Search or enter web address..."
        )

        self.new_tab_button = QPushButton("+")

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

    def _address_submitted(self):
        text = self.address_bar.text().strip()

        if text:
            self.navigate_requested.emit(text)

    def set_url(self, url: str):
        self.address_bar.setText(url)
        self.address_bar.setCursorPosition(0)