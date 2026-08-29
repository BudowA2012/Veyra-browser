from PySide6.QtCore import QEasingCurve, QPropertyAnimation, Signal
from PySide6.QtWidgets import QPushButton, QVBoxLayout, QWidget


class Sidebar(QWidget):

    home_requested = Signal()
    bookmarks_requested = Signal()
    history_requested = Signal()
    downloads_requested = Signal()
    settings_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.expanded = True
        self._animation = None

        self.setObjectName("Sidebar")

        self.setMinimumWidth(68)
        self.setMaximumWidth(220)

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            10,
            12,
            10,
            12,
        )

        layout.setSpacing(6)

        # ------------------------------------------
        # TOP
        # ------------------------------------------

        self.toggle_button = self._button("☰")

        layout.addWidget(
            self.toggle_button
        )

        layout.addSpacing(12)

        # ------------------------------------------
        # NAVIGATION
        # ------------------------------------------

        self.home_button = self._button(
            "Home"
        )

        self.bookmarks_button = self._button(
            "Bookmarks"
        )

        self.history_button = self._button(
            "History"
        )

        self.downloads_button = self._button(
            "Downloads"
        )

        layout.addWidget(
            self.home_button
        )

        layout.addWidget(
            self.bookmarks_button
        )

        layout.addWidget(
            self.history_button
        )

        layout.addWidget(
            self.downloads_button
        )

        layout.addStretch()

        # ------------------------------------------
        # SETTINGS
        # ------------------------------------------

        self.settings_button = self._button(
            "Settings"
        )

        layout.addWidget(
            self.settings_button
        )

        # ------------------------------------------
        # SIGNALS
        # ------------------------------------------

        self.toggle_button.clicked.connect(
            self.toggle
        )

        self.home_button.clicked.connect(
            self.home_requested.emit
        )

        self.bookmarks_button.clicked.connect(
            self.bookmarks_requested.emit
        )

        self.history_button.clicked.connect(
            self.history_requested.emit
        )

        self.downloads_button.clicked.connect(
            self.downloads_requested.emit
        )

        self.settings_button.clicked.connect(
            self.settings_requested.emit
        )

    def _button(self, text):

        button = QPushButton(text)

        button.setObjectName(
            "SidebarButton"
        )

        button.setMinimumHeight(42)

        return button

    def toggle(self):

        self.expanded = not self.expanded

        target_width = (
            220
            if self.expanded
            else 68
        )

        animation = QPropertyAnimation(
            self,
            b"maximumWidth",
        )

        animation.setDuration(220)

        animation.setStartValue(
            self.maximumWidth()
        )

        animation.setEndValue(
            target_width
        )

        animation.setEasingCurve(
            QEasingCurve.OutCubic
        )

        animation.start()

        self._animation = animation

        self._update_labels()

    def _update_labels(self):

        if self.expanded:

            self.home_button.setText(
                "Home"
            )

            self.bookmarks_button.setText(
                "Bookmarks"
            )

            self.history_button.setText(
                "History"
            )

            self.downloads_button.setText(
                "Downloads"
            )

            self.settings_button.setText(
                "Settings"
            )

        else:

            self.home_button.setText(
                "⌂"
            )

            self.bookmarks_button.setText(
                "☆"
            )

            self.history_button.setText(
                "◷"
            )

            self.downloads_button.setText(
                "↓"
            )

            self.settings_button.setText(
                "⚙"
            )