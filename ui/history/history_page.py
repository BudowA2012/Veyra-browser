from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from core.history.history_repository import HistoryRepository
from ui.history.history_item import HistoryItem


class HistoryPage(QWidget):

    open_requested = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.repository = HistoryRepository()

        self.setObjectName("HistoryPage")

        self._build_ui()
        self.reload()

    # ==================================================
    # UI
    # ==================================================

    def _build_ui(self):

        main = QVBoxLayout(self)

        main.setContentsMargins(
            50,
            40,
            50,
            40,
        )

        main.setSpacing(20)

        # ------------------------------------------
        # HEADER
        # ------------------------------------------

        header = QHBoxLayout()

        title = QLabel("History")

        title.setObjectName("HistoryPageTitle")

        header.addWidget(title)

        header.addStretch()

        clear_button = QPushButton(
            "Clear history"
        )

        clear_button.setObjectName(
            "HistoryClearButton"
        )

        clear_button.clicked.connect(
            self._clear_history
        )

        header.addWidget(clear_button)

        main.addLayout(header)

        # ------------------------------------------
        # SEARCH
        # ------------------------------------------

        self.search = QLineEdit()

        self.search.setPlaceholderText(
            "Search history..."
        )

        self.search.setObjectName(
            "HistorySearch"
        )

        self.search.textChanged.connect(
            self.reload
        )

        main.addWidget(self.search)

        # ------------------------------------------
        # SCROLL AREA
        # ------------------------------------------

        self.scroll = QScrollArea()

        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(
            QScrollArea.Shape.NoFrame
        )

        self.container = QWidget()

        self.items_layout = QVBoxLayout(
            self.container
        )

        self.items_layout.setSpacing(10)
        self.items_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        self.items_layout.addStretch()

        self.scroll.setWidget(
            self.container
        )

        main.addWidget(
            self.scroll,
            1,
        )

    # ==================================================
    # LOAD
    # ==================================================

    def reload(self):

        # Remove old widgets

        while self.items_layout.count():

            item = self.items_layout.takeAt(0)

            if item.widget():
                item.widget().deleteLater()

        query = self.search.text().lower().strip()

        entries = self.repository.get_all()

        found = 0

        for history_id, title, url, visited_at in entries:

            if query:

                searchable = (
                    f"{title} {url}"
                ).lower()

                if query not in searchable:
                    continue

            item = HistoryItem(
                history_id,
                title,
                url,
                visited_at,
            )

            item.open_requested.connect(
                self.open_requested.emit
            )

            item.delete_requested.connect(
                self._delete_entry
            )

            # Insert before stretch
            self.items_layout.insertWidget(
                self.items_layout.count() - 1,
                item,
            )

            found += 1

        if found == 0:

            empty = QLabel(
                "No history yet."
            )

            empty.setAlignment(
                Qt.AlignmentFlag.AlignCenter
            )

            empty.setObjectName(
                "HistoryEmpty"
            )

            self.items_layout.insertWidget(
                0,
                empty,
            )

    # ==================================================
    # ACTIONS
    # ==================================================

    def _delete_entry(self, history_id):

        self.repository.delete(
            history_id
        )

        self.reload()

    def _clear_history(self):

        self.repository.clear()

        self.reload()
