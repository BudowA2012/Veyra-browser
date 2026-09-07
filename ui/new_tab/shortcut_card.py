from urllib.parse import urlparse

from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtNetwork import (
    QNetworkAccessManager,
    QNetworkRequest,
)
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMenu,
    QPushButton,
    QToolButton,
    QVBoxLayout,
    QWidget,
)


class ShortcutCard(QWidget):

    clicked_url = Signal(str)
    edit_requested = Signal(int)
    delete_requested = Signal(int)

    def __init__(
        self,
        shortcut_id,
        name,
        url,
        parent=None,
    ):
        super().__init__(parent)

        self.shortcut_id = shortcut_id
        self.shortcut_name = name
        self.url = url

        self.setObjectName("ShortcutCard")

        self.setFixedSize(
            150,
            125,
        )

        self.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        # Każdy kafelek ma manager powiązany
        # ze swoim cyklem życia.
        self.network = QNetworkAccessManager(
            self
        )

        self._build_ui()
        self._load_favicon()

    # ==================================================
    # UI
    # ==================================================

    def _build_ui(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            12,
            8,
            10,
            12,
        )

        layout.setSpacing(
            4
        )

        # ----------------------------------------------
        # TOP
        # ----------------------------------------------

        top = QHBoxLayout()

        top.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        top.addStretch()

        self.menu_button = QToolButton()

        self.menu_button.setObjectName(
            "ShortcutMenuButton"
        )

        self.menu_button.setText(
            "⋯"
        )

        self.menu_button.setFixedSize(
            26,
            26,
        )

        self.menu_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.menu_button.clicked.connect(
            self._show_menu
        )

        top.addWidget(
            self.menu_button
        )

        layout.addLayout(
            top
        )

        # ----------------------------------------------
        # ICON
        # ----------------------------------------------

        self.icon_label = QLabel()

        self.icon_label.setObjectName(
            "ShortcutIcon"
        )

        self.icon_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.icon_label.setFixedSize(
            44,
            44,
        )

        # Fallback zanim favicon się pobierze
        self.icon_label.setText(
            self.shortcut_name[:1].upper()
        )

        layout.addWidget(
            self.icon_label,
            alignment=Qt.AlignmentFlag.AlignHCenter,
        )

        # ----------------------------------------------
        # NAME
        # ----------------------------------------------

        self.name_label = QLabel(
            self.shortcut_name
        )

        self.name_label.setObjectName(
            "ShortcutName"
        )

        self.name_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(
            self.name_label
        )

        layout.addStretch()

    # ==================================================
    # FAVICON
    # ==================================================

    def _load_favicon(self):

        parsed = urlparse(
            self.url
        )

        domain = parsed.netloc

        if not domain:
            return

        favicon_url = (
            "https://www.google.com/s2/favicons"
            f"?domain={domain}&sz=128"
        )

        request = QNetworkRequest(
            favicon_url
        )

        reply = self.network.get(
            request
        )

        reply.finished.connect(
            lambda:
            self._favicon_ready(reply)
        )

    def _favicon_ready(
        self,
        reply,
    ):

        data = reply.readAll()

        pixmap = QPixmap()

        pixmap.loadFromData(
            data
        )

        if not pixmap.isNull():

            pixmap = pixmap.scaled(
                36,
                36,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )

            self.icon_label.setText(
                ""
            )

            self.icon_label.setPixmap(
                pixmap
            )

        reply.deleteLater()

    # ==================================================
    # MENU
    # ==================================================

    def _show_menu(self):

        menu = QMenu(
            self
        )

        menu.setObjectName(
            "ShortcutContextMenu"
        )

        edit_action = menu.addAction(
            "Edit shortcut"
        )

        delete_action = menu.addAction(
            "Delete shortcut"
        )

        action = menu.exec(
            self.menu_button.mapToGlobal(
                self.menu_button.rect().bottomLeft()
            )
        )

        if action == edit_action:

            self.edit_requested.emit(
                self.shortcut_id
            )

        elif action == delete_action:

            self.delete_requested.emit(
                self.shortcut_id
            )

    # ==================================================
    # CLICK
    # ==================================================

    def mouseReleaseEvent(
        self,
        event,
    ):

        # Kliknięcie menu nie powinno otwierać strony.
        if self.menu_button.geometry().contains(
            event.position().toPoint()
        ):
            super().mouseReleaseEvent(
                event
            )
            return

        if (
            event.button()
            == Qt.MouseButton.LeftButton
        ):

            self.clicked_url.emit(
                self.url
            )

        super().mouseReleaseEvent(
            event
        )

    # ==================================================
    # CONTEXT MENU
    # ==================================================

    def contextMenuEvent(
        self,
        event,
    ):

        self._show_menu()