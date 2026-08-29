from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFrame, QLabel, QPushButton, QHBoxLayout, QVBoxLayout


class HistoryItem(QFrame):

    open_requested = Signal(str)
    delete_requested = Signal(int)

    def __init__(self, history_id, title, url, visited_at, parent=None):
        super().__init__(parent)

        self.history_id = history_id
        self.url = url

        self.setObjectName("HistoryItem")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(14)

        # ------------------------------------------
        # TEXT
        # ------------------------------------------

        text_layout = QVBoxLayout()
        text_layout.setSpacing(4)

        self.title_label = QLabel(title or url)
        self.title_label.setObjectName("HistoryTitle")

        self.url_label = QLabel(url)
        self.url_label.setObjectName("HistoryUrl")

        self.time_label = QLabel(
            self._format_time(visited_at)
        )
        self.time_label.setObjectName("HistoryTime")

        text_layout.addWidget(self.title_label)
        text_layout.addWidget(self.url_label)
        text_layout.addWidget(self.time_label)

        layout.addLayout(text_layout, 1)

        # ------------------------------------------
        # OPEN
        # ------------------------------------------

        open_button = QPushButton("Open")
        open_button.setObjectName("HistoryOpenButton")

        open_button.clicked.connect(
            lambda: self.open_requested.emit(self.url)
        )

        layout.addWidget(open_button)

        # ------------------------------------------
        # DELETE
        # ------------------------------------------

        delete_button = QPushButton("×")
        delete_button.setObjectName("HistoryDeleteButton")

        delete_button.clicked.connect(
            lambda: self.delete_requested.emit(
                self.history_id
            )
        )

        layout.addWidget(delete_button)

    def _format_time(self, value):

        try:
            from datetime import datetime

            date = datetime.fromisoformat(value)

            return date.strftime(
                "%d.%m.%Y  %H:%M"
            )

        except Exception:
            return value