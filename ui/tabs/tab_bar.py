from PySide6.QtCore import QSize, Qt, QTimer, Signal
from PySide6.QtWidgets import QTabBar, QToolButton


class TabBar(QTabBar):

    new_tab_requested = Signal()

    TAB_MIN_WIDTH = 120
    TAB_MAX_WIDTH = 210

    PLUS_SIZE = 32
    PLUS_GAP = 8

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("VeyraTabBar")

        # ==================================================
        # TAB BAR
        # ==================================================

        self.setExpanding(False)
        self.setMovable(True)
        self.setDocumentMode(True)
        self.setDrawBase(False)

        self.setElideMode(
            Qt.TextElideMode.ElideRight
        )

        self.setUsesScrollButtons(True)

        self.setFixedHeight(44)

        # ==================================================
        # PLUS BUTTON
        # ==================================================

        self.new_tab_button = QToolButton(
            self
        )

        self.new_tab_button.setObjectName(
            "TabNewButton"
        )

        self.new_tab_button.setText("+")

        self.new_tab_button.setToolTip(
            "New tab (Ctrl+T)"
        )

        self.new_tab_button.setFixedSize(
            self.PLUS_SIZE,
            self.PLUS_SIZE,
        )

        self.new_tab_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.new_tab_button.clicked.connect(
            self.new_tab_requested.emit
        )

        # ==================================================
        # SIGNALS
        # ==================================================

        self.tabMoved.connect(
            lambda *_:
            self._schedule_layout_update()
        )

        self.currentChanged.connect(
            lambda *_:
            self._schedule_layout_update()
        )

        self._schedule_layout_update()

    # ======================================================
    # TAB SIZE
    # ======================================================

    def tabSizeHint(self, index):

        base = super().tabSizeHint(index)

        count = max(
            self.count(),
            1,
        )

        # 1-2 karty: stały, normalny rozmiar
        if count <= 2:

            width = max(
                base.width(),
                160,
            )

            width = min(
                width,
                self.TAB_MAX_WIDTH,
            )

        else:

            # Więcej kart -> dynamiczne zwężanie
            available = (
                self.width()
                - self.PLUS_SIZE
                - self.PLUS_GAP
                - 20
            )

            width = available // count

            width = max(
                self.TAB_MIN_WIDTH,
                min(
                    width,
                    self.TAB_MAX_WIDTH,
                ),
            )

        return QSize(
            width,
            36,
        )

    # ======================================================
    # IMPORTANT:
    # RESERVE SPACE FOR +
    # ======================================================

    def sizeHint(self):

        size = super().sizeHint()

        tabs_width = 0

        for index in range(
            self.count()
        ):
            tabs_width += (
                self.tabSizeHint(index).width()
            )

        required_width = (
            tabs_width
            + self.PLUS_GAP
            + self.PLUS_SIZE
            + 12
        )

        size.setWidth(
            max(
                size.width(),
                required_width,
            )
        )

        size.setHeight(44)

        return size

    def minimumSizeHint(self):

        size = super().minimumSizeHint()

        size.setHeight(44)

        return size

    # ======================================================
    # UPDATE
    # ======================================================

    def _schedule_layout_update(self):

        QTimer.singleShot(
            0,
            self._update_layout,
        )

        QTimer.singleShot(
            30,
            self._update_layout,
        )

        QTimer.singleShot(
            80,
            self._update_layout,
        )

    def _update_layout(self):

        self.updateGeometry()

        self._update_plus_position()

    # ======================================================
    # PLUS POSITION
    # ======================================================

    def _update_plus_position(self):

        if self.count() == 0:

            x = 8

        else:

            last_rect = self.tabRect(
                self.count() - 1
            )

            # DOKŁADNIE za ostatnią kartą
            x = (
                last_rect.right()
                + 1
                + self.PLUS_GAP
            )

        # środek wysokości + delikatna korekta optyczna
        y = (
            self.height()
            - self.PLUS_SIZE
        ) // 2 - 2

        self.new_tab_button.move(
            x,
            y,
        )

        self.new_tab_button.raise_()
        self.new_tab_button.show()

    # ======================================================
    # QT EVENTS
    # ======================================================

    def resizeEvent(self, event):

        super().resizeEvent(event)

        self._schedule_layout_update()

    def tabInserted(self, index):

        super().tabInserted(index)

        self._schedule_layout_update()

    def tabRemoved(self, index):

        super().tabRemoved(index)

        self._schedule_layout_update()

    def showEvent(self, event):

        super().showEvent(event)

        self._schedule_layout_update()