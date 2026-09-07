from PySide6.QtCore import (
    QSize,
    Qt,
)
from PySide6.QtWidgets import (
    QTabBar,
    QToolButton,
)

from ui.components.icon_factory import (
    create_icon,
)


class TabBar(QTabBar):

    TAB_MIN_WIDTH = 125
    TAB_MAX_WIDTH = 220

    def __init__(
        self,
        parent=None,
    ):
        super().__init__(
            parent
        )

        self.setObjectName(
            "VeyraTabBar"
        )

        # ==================================================
        # BEHAVIOUR
        # ==================================================

        self.setExpanding(
            False
        )

        self.setMovable(
            True
        )

        self.setDocumentMode(
            True
        )

        self.setDrawBase(
            False
        )

        self.setUsesScrollButtons(
            True
        )

        self.setElideMode(
            Qt.TextElideMode.ElideRight
        )

        # Wyłączamy standardowe X od Qt.
        self.setTabsClosable(
            False
        )

        self.setFixedHeight(
            44
        )

        self.setIconSize(
            QSize(
                16,
                16,
            )
        )

    # ======================================================
    # TAB SIZE
    # ======================================================

    def tabSizeHint(
        self,
        index,
    ):

        base = super().tabSizeHint(
            index
        )

        width = max(
            base.width() + 28,
            170,
        )

        width = min(
            width,
            self.TAB_MAX_WIDTH,
        )

        return QSize(
            width,
            36,
        )

    # ======================================================
    # MINIMUM SIZE
    # ======================================================

    def minimumTabSizeHint(
        self,
        index,
    ):

        return QSize(
            self.TAB_MIN_WIDTH,
            36,
        )

    # ======================================================
    # INSERT
    # ======================================================

    def tabInserted(
        self,
        index,
    ):

        super().tabInserted(
            index
        )

        self._install_close_button(
            index
        )

    # ======================================================
    # CLOSE BUTTON
    # ======================================================

    def _install_close_button(
        self,
        index,
    ):

        button = QToolButton(
            self
        )

        button.setObjectName(
            "TabCloseButton"
        )

        button.setIcon(
            create_icon(
                "close",
                16,
            )
        )

        button.setIconSize(
            QSize(
                15,
                15,
            )
        )

        button.setFixedSize(
            24,
            24,
        )

        button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        button.setToolTip(
            "Close tab"
        )

        button.clicked.connect(
            lambda:
            self._close_from_button(
                button
            )
        )

        self.setTabButton(
            index,
            QTabBar.ButtonPosition.RightSide,
            button,
        )

    # ======================================================
    # CLOSE
    # ======================================================

    def _close_from_button(
        self,
        button,
    ):

        for index in range(
            self.count()
        ):

            current_button = (
                self.tabButton(
                    index,
                    QTabBar.ButtonPosition.RightSide,
                )
            )

            if current_button is button:

                self.tabCloseRequested.emit(
                    index
                )

                return