from urllib.parse import urlparse

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PySide6.QtWidgets import QMenu, QPushButton


class ShortcutCard(QPushButton):

    clicked_url = Signal(str)
    edit_requested = Signal(int)
    delete_requested = Signal(int)

    network = QNetworkAccessManager()

    def __init__(self, shortcut_id, name, url, parent=None):
        super().__init__(name, parent)

        self.shortcut_id = shortcut_id
        self.url = url

        self.setObjectName("ShortcutButton")
        self.setCursor(Qt.PointingHandCursor)

        self.clicked.connect(
            lambda: self.clicked_url.emit(self.url)
        )

        self._load_favicon()

    def _load_favicon(self):

        domain = urlparse(self.url).netloc

        if not domain:
            return

        icon_url = (
            f"https://www.google.com/s2/favicons"
            f"?sz=64&domain={domain}"
        )

        request = QNetworkRequest(icon_url)

        reply = self.network.get(request)

        reply.finished.connect(
            lambda: self._icon_ready(reply)
        )

    def _icon_ready(self, reply):

        pixmap = QPixmap()

        pixmap.loadFromData(reply.readAll())

        if not pixmap.isNull():
            self.setIcon(QIcon(pixmap))
            self.setIconSize(pixmap.size())

        reply.deleteLater()

    def contextMenuEvent(self, event):

        menu = QMenu(self)

        edit = menu.addAction("✏ Edit")
        delete = menu.addAction("🗑 Delete")

        action = menu.exec(event.globalPos())

        if action == edit:
            self.edit_requested.emit(self.shortcut_id)

        elif action == delete:
            self.delete_requested.emit(self.shortcut_id)