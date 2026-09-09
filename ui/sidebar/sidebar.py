from PySide6.QtCore import (
    QEasingCurve,
    QPropertyAnimation,
    QSize,
    Qt,
    Signal,
)
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from ui.components.icon_factory import (
    create_icon,
)


class Sidebar(QWidget):

    home_requested = Signal()
    bookmarks_requested = Signal()
    history_requested = Signal()
    downloads_requested = Signal()
    settings_requested = Signal()

    EXPANDED_WIDTH = 210
    COLLAPSED_WIDTH = 64

    def __init__(
        self,
        parent=None,
    ):
        super().__init__(
            parent
        )

        self.expanded = True
        self._animation = None

        self.setObjectName(
            "Sidebar"
        )

        self.setMinimumWidth(
            self.COLLAPSED_WIDTH
        )

        self.setMaximumWidth(
            self.EXPANDED_WIDTH
        )

        self._build_ui()
        self._connect_signals()

    # ======================================================
    # BUILD
    # ======================================================

    def _build_ui(
        self,
    ):

        root = QVBoxLayout(
            self
        )

        root.setContentsMargins(
            9,
            10,
            9,
            10,
        )

        root.setSpacing(
            3
        )

        # ==================================================
        # BRAND HEADER
        # ==================================================

        self.header = QFrame()

        self.header.setObjectName(
            "SidebarHeader"
        )

        header_layout = QHBoxLayout(
            self.header
        )

        header_layout.setContentsMargins(
            5,
            3,
            3,
            8,
        )

        header_layout.setSpacing(
            9
        )

        self.logo = QLabel(
            "V"
        )

        self.logo.setObjectName(
            "SidebarLogo"
        )

        self.logo.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.logo.setFixedSize(
            34,
            34,
        )

        self.brand = QLabel(
            "Veyra"
        )

        self.brand.setObjectName(
            "SidebarBrand"
        )

        self.toggle_button = QToolButton()

        self.toggle_button.setObjectName(
            "SidebarToggleButton"
        )

        self.toggle_button.setIcon(
            create_icon(
                "menu",
                19,
            )
        )

        self.toggle_button.setIconSize(
            QSize(
                18,
                18,
            )
        )

        self.toggle_button.setFixedSize(
            32,
            32,
        )

        self.toggle_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.toggle_button.setToolTip(
            "Collapse sidebar (Ctrl+B)"
        )

        header_layout.addWidget(
            self.logo
        )

        header_layout.addWidget(
            self.brand
        )

        header_layout.addStretch(
            1
        )

        header_layout.addWidget(
            self.toggle_button
        )

        root.addWidget(
            self.header
        )

        # ==================================================
        # SECTION
        # ==================================================

        self.navigation_label = QLabel(
            "NAVIGATION"
        )

        self.navigation_label.setObjectName(
            "SidebarSectionLabel"
        )

        root.addSpacing(
            5
        )

        root.addWidget(
            self.navigation_label
        )

        root.addSpacing(
            3
        )

        # ==================================================
        # BUTTONS
        # ==================================================

        self.home_button = (
            self._create_button(
                "home",
                "Home",
            )
        )

        self.bookmarks_button = (
            self._create_button(
                "bookmark",
                "Bookmarks",
            )
        )

        self.history_button = (
            self._create_button(
                "history",
                "History",
            )
        )

        self.downloads_button = (
            self._create_button(
                "download",
                "Downloads",
            )
        )

        root.addWidget(
            self.home_button
        )

        root.addWidget(
            self.bookmarks_button
        )

        root.addWidget(
            self.history_button
        )

        root.addWidget(
            self.downloads_button
        )

        root.addStretch(
            1
        )

        # ==================================================
        # BOTTOM DIVIDER
        # ==================================================

        self.bottom_divider = QFrame()

        self.bottom_divider.setObjectName(
            "SidebarDivider"
        )

        self.bottom_divider.setFixedHeight(
            1
        )

        root.addWidget(
            self.bottom_divider
        )

        root.addSpacing(
            4
        )

        # ==================================================
        # SETTINGS
        # ==================================================

        self.settings_button = (
            self._create_button(
                "settings",
                "Settings",
            )
        )

        root.addWidget(
            self.settings_button
        )

    # ======================================================
    # CREATE BUTTON
    # ======================================================

    def _create_button(
        self,
        icon_name,
        text,
    ):

        button = QPushButton(
            text
        )

        button.setObjectName(
            "SidebarButton"
        )

        button.setProperty(
            "sidebarText",
            text,
        )

        button.setProperty(
            "sidebarIcon",
            icon_name,
        )

        button.setIcon(
            create_icon(
                icon_name,
                20,
            )
        )

        button.setIconSize(
            QSize(
                19,
                19,
            )
        )

        button.setMinimumHeight(
            42
        )

        button.setMaximumHeight(
            42
        )

        button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        button.setToolTip(
            text
        )

        return button

    # ======================================================
    # SIGNALS
    # ======================================================

    def _connect_signals(
        self,
    ):

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

    # ======================================================
    # TOGGLE
    # ======================================================

    def toggle(
        self,
    ):

        self.expanded = (
            not self.expanded
        )

        target_width = (
            self.EXPANDED_WIDTH
            if self.expanded
            else self.COLLAPSED_WIDTH
        )

        animation = QPropertyAnimation(
            self,
            b"maximumWidth",
            self,
        )

        animation.setDuration(
            180
        )

        animation.setStartValue(
            self.maximumWidth()
        )

        animation.setEndValue(
            target_width
        )

        animation.setEasingCurve(
            QEasingCurve.Type.OutCubic
        )

        animation.start()

        self._animation = animation

        self._update_mode()

    # ======================================================
    # UPDATE MODE
    # ======================================================

    def _update_mode(
        self,
    ):

        buttons = [
            self.home_button,
            self.bookmarks_button,
            self.history_button,
            self.downloads_button,
            self.settings_button,
        ]

        if self.expanded:

            self.brand.show()

            self.navigation_label.show()

            self.logo.show()

            self.toggle_button.setToolTip(
                "Collapse sidebar (Ctrl+B)"
            )

            for button in buttons:

                text = button.property(
                    "sidebarText"
                )

                button.setText(
                    text
                )

                button.setStyleSheet(
                    ""
                )

        else:

            self.brand.hide()

            self.navigation_label.hide()

            self.logo.hide()

            self.toggle_button.setToolTip(
                "Expand sidebar (Ctrl+B)"
            )

            for button in buttons:

                button.setText(
                    ""
                )

                button.setStyleSheet(
                    """
                    QPushButton {
                        padding-left: 0px;
                        padding-right: 0px;
                        text-align: center;
                    }
                    """
                )