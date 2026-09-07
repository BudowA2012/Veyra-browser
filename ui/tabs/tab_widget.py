from PySide6.QtCore import (
    QSize,
    Signal,
)
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QHBoxLayout,
    QSizePolicy,
    QStackedWidget,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from ui.components.icon_factory import (
    create_icon,
)
from ui.tabs.tab_bar import TabBar


class VeyraTabWidget(QWidget):

    currentChanged = Signal(int)
    tabCloseRequested = Signal(int)
    newTabRequested = Signal()

    def __init__(
        self,
        parent=None,
    ):
        super().__init__(
            parent
        )

        self.setObjectName(
            "VeyraTabWidget"
        )

        self._build_ui()
        self._connect_signals()

    # ======================================================
    # BUILD
    # ======================================================

    def _build_ui(self):

        root = QVBoxLayout(
            self
        )

        root.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        root.setSpacing(
            0
        )

        # ==================================================
        # TAB STRIP
        # ==================================================

        self.tab_strip = QWidget()

        self.tab_strip.setObjectName(
            "VeyraTabStrip"
        )

        self.tab_strip.setFixedHeight(
            44
        )

        strip_layout = QHBoxLayout(
            self.tab_strip
        )

        strip_layout.setContentsMargins(
            6,
            0,
            8,
            0,
        )

        strip_layout.setSpacing(
            7
        )

        # ==================================================
        # TAB BAR
        # ==================================================

        self.tab_bar = TabBar()

        self.tab_bar.setSizePolicy(
            QSizePolicy.Policy.Maximum,
            QSizePolicy.Policy.Fixed,
        )

        strip_layout.addWidget(
            self.tab_bar
        )

        # ==================================================
        # NEW TAB BUTTON
        # ==================================================

        self.new_tab_button = QToolButton()

        self.new_tab_button.setObjectName(
            "TabNewButton"
        )

        self.new_tab_button.setIcon(
            create_icon(
                "plus",
                18,
            )
        )

        self.new_tab_button.setIconSize(
            QSize(
                17,
                17,
            )
        )

        self.new_tab_button.setToolTip(
            "New tab (Ctrl+T)"
        )

        self.new_tab_button.setFixedSize(
            32,
            32,
        )

        self.new_tab_button.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Fixed,
        )

        strip_layout.addWidget(
            self.new_tab_button
        )

        strip_layout.addStretch(
            1
        )

        root.addWidget(
            self.tab_strip
        )

        # ==================================================
        # STACK
        # ==================================================

        self.stack = QStackedWidget()

        self.stack.setObjectName(
            "VeyraTabStack"
        )

        root.addWidget(
            self.stack,
            1,
        )

    # ======================================================
    # SIGNALS
    # ======================================================

    def _connect_signals(
        self,
    ):

        self.tab_bar.currentChanged.connect(
            self._tab_bar_changed
        )

        self.tab_bar.tabCloseRequested.connect(
            self.tabCloseRequested.emit
        )

        self.tab_bar.tabMoved.connect(
            self._tab_moved
        )

        self.new_tab_button.clicked.connect(
            self.newTabRequested.emit
        )

    # ======================================================
    # CHANGE
    # ======================================================

    def _tab_bar_changed(
        self,
        index,
    ):

        if (
            index < 0
            or index >= self.stack.count()
        ):
            return

        self.stack.setCurrentIndex(
            index
        )

        self.currentChanged.emit(
            index
        )

    # ======================================================
    # MOVE
    # ======================================================

    def _tab_moved(
        self,
        from_index,
        to_index,
    ):

        if from_index == to_index:
            return

        widget = self.stack.widget(
            from_index
        )

        if widget is None:
            return

        was_current = (
            self.stack.currentWidget()
            is widget
        )

        self.stack.removeWidget(
            widget
        )

        self.stack.insertWidget(
            to_index,
            widget,
        )

        if was_current:

            self.stack.setCurrentWidget(
                widget
            )

    # ======================================================
    # ADD
    # ======================================================

    def addTab(
        self,
        widget,
        title,
    ):

        index = self.stack.addWidget(
            widget
        )

        self.tab_bar.addTab(
            title
        )

        if self.count() == 1:

            self.setCurrentIndex(
                0
            )

        return index

    # ======================================================
    # INSERT
    # ======================================================

    def insertTab(
        self,
        index,
        widget,
        title,
    ):

        index = max(
            0,
            min(
                index,
                self.count(),
            ),
        )

        self.stack.insertWidget(
            index,
            widget,
        )

        self.tab_bar.insertTab(
            index,
            title,
        )

        return index

    # ======================================================
    # REMOVE
    # ======================================================

    def removeTab(
        self,
        index,
    ):

        if (
            index < 0
            or index >= self.count()
        ):
            return

        widget = self.stack.widget(
            index
        )

        self.tab_bar.removeTab(
            index
        )

        if widget is not None:

            self.stack.removeWidget(
                widget
            )

        if self.count() > 0:

            new_index = min(
                index,
                self.count() - 1,
            )

            self.setCurrentIndex(
                new_index
            )

    # ======================================================
    # API
    # ======================================================

    def count(self):

        return self.stack.count()

    def widget(
        self,
        index,
    ):

        return self.stack.widget(
            index
        )

    def indexOf(
        self,
        widget,
    ):

        return self.stack.indexOf(
            widget
        )

    def currentIndex(self):

        return self.stack.currentIndex()

    def currentWidget(self):

        return self.stack.currentWidget()

    def setCurrentIndex(
        self,
        index,
    ):

        if (
            index < 0
            or index >= self.count()
        ):
            return

        self.stack.setCurrentIndex(
            index
        )

        if (
            self.tab_bar.currentIndex()
            != index
        ):

            self.tab_bar.setCurrentIndex(
                index
            )

        self.currentChanged.emit(
            index
        )

    def setTabText(
        self,
        index,
        text,
    ):

        self.tab_bar.setTabText(
            index,
            text,
        )

    def tabText(
        self,
        index,
    ):

        return self.tab_bar.tabText(
            index
        )

    def setTabIcon(
        self,
        index,
        icon: QIcon,
    ):

        self.tab_bar.setTabIcon(
            index,
            icon,
        )

    def setTabsClosable(
        self,
        enabled,
    ):

        pass

    def setMovable(
        self,
        enabled,
    ):

        self.tab_bar.setMovable(
            enabled
        )

    def setDocumentMode(
        self,
        enabled,
    ):

        self.tab_bar.setDocumentMode(
            enabled
        )