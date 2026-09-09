from PySide6.QtCore import (
    QSize,
    Qt,
    Signal,
)

from PySide6.QtWidgets import (
    QMenu,
    QTabBar,
    QToolButton,
)

from ui.components.icon_factory import (
    create_icon,
)


class TabBar(QTabBar):

    duplicateRequested = Signal(int)
    closeOthersRequested = Signal(int)
    closeRightRequested = Signal(int)
    pinToggleRequested = Signal(int)

    TAB_MIN_WIDTH = 125
    TAB_MAX_WIDTH = 220
    PINNED_TAB_WIDTH = 105

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

        # Własne X zamiast standardowego Qt.
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

        # ==================================================
        # CONTEXT MENU
        # ==================================================

        self.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu
        )

        self.customContextMenuRequested.connect(
            self._show_context_menu
        )

    # ======================================================
    # TAB SIZE
    # ======================================================

    def tabSizeHint(
        self,
        index,
    ):

        if self.is_pinned(
            index
        ):

            return QSize(
                self.PINNED_TAB_WIDTH,
                36,
            )

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

        if self.is_pinned(
            index
        ):

            return QSize(
                self.PINNED_TAB_WIDTH,
                36,
            )

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

        # Domyślnie karta nie jest przypięta.
        self.setTabData(
            index,
            False,
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
    # CLOSE FROM BUTTON
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

            if (
                current_button
                is button
            ):

                self.tabCloseRequested.emit(
                    index
                )

                return

    # ======================================================
    # PIN STATE
    # ======================================================

    def is_pinned(
        self,
        index,
    ):

        if (
            index < 0
            or index >= self.count()
        ):

            return False

        return bool(
            self.tabData(
                index
            )
        )

    def set_pinned(
        self,
        index,
        pinned,
    ):

        if (
            index < 0
            or index >= self.count()
        ):

            return

        self.setTabData(
            index,
            bool(
                pinned
            ),
        )

        close_button = (
            self.tabButton(
                index,
                QTabBar.ButtonPosition.RightSide,
            )
        )

        if close_button:

            close_button.setVisible(
                not pinned
            )

        self.updateGeometry()
        self.update()

    # ======================================================
    # CONTEXT MENU
    # ======================================================

    def _show_context_menu(
        self,
        position,
    ):

        index = self.tabAt(
            position
        )

        if index < 0:
            return

        # Prawy klik ustawia kartę jako aktywną.
        self.setCurrentIndex(
            index
        )

        menu = QMenu(
            self
        )

        # ==================================================
        # DUPLICATE
        # ==================================================

        duplicate_action = (
            menu.addAction(
                "Duplicate tab"
            )
        )

        duplicate_action.triggered.connect(
            lambda:
            self.duplicateRequested.emit(
                index
            )
        )

        # ==================================================
        # PIN
        # ==================================================

        if self.is_pinned(
            index
        ):

            pin_text = (
                "Unpin tab"
            )

        else:

            pin_text = (
                "Pin tab"
            )

        pin_action = (
            menu.addAction(
                pin_text
            )
        )

        pin_action.triggered.connect(
            lambda:
            self.pinToggleRequested.emit(
                index
            )
        )

        menu.addSeparator()

        # ==================================================
        # CLOSE
        # ==================================================

        close_action = (
            menu.addAction(
                "Close tab"
            )
        )

        close_action.triggered.connect(
            lambda:
            self.tabCloseRequested.emit(
                index
            )
        )

        # ==================================================
        # CLOSE OTHERS
        # ==================================================

        close_others_action = (
            menu.addAction(
                "Close other tabs"
            )
        )

        close_others_action.setEnabled(
            self.count() > 1
        )

        close_others_action.triggered.connect(
            lambda:
            self.closeOthersRequested.emit(
                index
            )
        )

        # ==================================================
        # CLOSE RIGHT
        # ==================================================

        close_right_action = (
            menu.addAction(
                "Close tabs to the right"
            )
        )

        close_right_action.setEnabled(
            index
            < self.count() - 1
        )

        close_right_action.triggered.connect(
            lambda:
            self.closeRightRequested.emit(
                index
            )
        )

        # ==================================================
        # SHOW
        # ==================================================

        menu.exec(
            self.mapToGlobal(
                position
            )
        )