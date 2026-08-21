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

    def __init__(self, parent=None):
        super().__init__(parent)

        self.repository = ShortcutRepository()

        self.setObjectName("NewTabPage")

        self._build_ui()
        self._load_shortcuts()

    def _build_ui(self):

        main = QVBoxLayout(self)

        main.setContentsMargins(40,40,40,40)

        main.addStretch()

        center = QWidget()
        center.setMaximumWidth(760)

        center_layout = QVBoxLayout(center)
        center_layout.setSpacing(18)

        logo = QLabel("Veyra")
        logo.setObjectName("VeyraLogo")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("Fast. Private. Yours.")
        subtitle.setObjectName("VeyraSubtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        center_layout.addWidget(logo)
        center_layout.addWidget(subtitle)

        search_frame = QFrame()
        search_frame.setObjectName("NewTabSearchContainer")

        search_layout = QHBoxLayout(search_frame)

        self.search_bar = QLineEdit()
        self.search_bar.setObjectName("NewTabSearch")
        self.search_bar.setPlaceholderText(
            "Search the web or enter an address..."
        )

        button = QPushButton("→")
        button.setObjectName("NewTabSearchButton")

        search_layout.addWidget(self.search_bar)
        search_layout.addWidget(button)

        center_layout.addWidget(search_frame)

        self.search_bar.returnPressed.connect(
            self._submit_search
        )

        button.clicked.connect(
            self._submit_search
        )

        self.grid = QGridLayout()
        self.grid.setSpacing(12)

        center_layout.addLayout(self.grid)

        self.add_button = QPushButton("＋ Add Shortcut")
        self.add_button.clicked.connect(
            self._add_shortcut
        )

        center_layout.addWidget(
            self.add_button,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )

        main.addWidget(
            center,
            alignment=Qt.AlignmentFlag.AlignHCenter,
        )

        main.addStretch()

    def _submit_search(self):

        text = self.search_bar.text().strip()

        if text:
            self.search_requested.emit(text)

    def _load_shortcuts(self):

        while self.grid.count():

            item = self.grid.takeAt(0)

            if item.widget():
                item.widget().deleteLater()

        shortcuts = self.repository.get_all()

        if not shortcuts:

            defaults = [
                ("Google","https://google.com"),
                ("GitHub","https://github.com"),
                ("YouTube","https://youtube.com"),
            ]

            for name,url in defaults:
                self.repository.add(name,url)

            shortcuts = self.repository.get_all()

        row = 0
        col = 0

        for sid,name,url in shortcuts:

            card = ShortcutCard(
                sid,
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

            self.grid.addWidget(card,row,col)

            col += 1

            if col == 3:
                col = 0
                row += 1

    def _add_shortcut(self):

        dialog = ShortcutDialog(self)

        if dialog.exec():

            name,url = dialog.values()

            if name and url:
                self.repository.add(name,url)
                self._load_shortcuts()

    def _edit_shortcut(self, sid):

        for current_id,name,url in self.repository.get_all():

            if current_id == sid:

                dialog = ShortcutDialog(
                    self,
                    name,
                    url,
                )

                if dialog.exec():

                    new_name,new_url = dialog.values()

                    self.repository.update(
                        sid,
                        new_name,
                        new_url,
                    )

                    self._load_shortcuts()

                break

    def _delete_shortcut(self,sid):

        self.repository.delete(sid)

        self._load_shortcuts()

    def focus_search(self):
        self.search_bar.setFocus()