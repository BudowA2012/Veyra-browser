from PySide6.QtCore import QUrl
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QProgressBar,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from core.browser.browser_manager import BrowserManager
from core.downloads.download_manager import DownloadManager
from core.history.history_repository import HistoryRepository

from ui.components.navigation_bar import NavigationBar
from ui.downloads.download_page import DownloadPage
from ui.history.history_page import HistoryPage
from ui.new_tab.new_tab_page import NewTabPage
from ui.sidebar.sidebar import Sidebar
from ui.tabs.tab_bar import TabBar
from ui.tabs.tab_manager import TabManager


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # ==================================================
        # WINDOW
        # ==================================================

        self.setWindowTitle(
            "Veyra"
        )

        self.resize(
            1400,
            900,
        )

        self.setMinimumSize(
            1000,
            650,
        )

        # ==================================================
        # CORE
        # ==================================================

        self.browser_manager = BrowserManager(
            self
        )

        self.history_repository = (
            HistoryRepository()
        )

        self.download_manager = DownloadManager(
            self.browser_manager.profile
        )

        # ==================================================
        # UI
        # ==================================================

        self.sidebar = Sidebar()

        self.navigation_bar = NavigationBar()

        self.loading_bar = QProgressBar()

        self.loading_bar.setObjectName(
            "BrowserLoadingBar"
        )

        self.loading_bar.setRange(
            0,
            100,
        )

        self.loading_bar.setTextVisible(
            False
        )

        self.loading_bar.setFixedHeight(
            3
        )

        self.loading_bar.hide()

        # ==================================================
        # TABS
        # ==================================================

        self.tab_bar = TabBar()

        self.tabs = QTabWidget()

        self.tabs.setTabBar(
            self.tab_bar
        )

        self.tabs.setTabsClosable(
            True
        )

        self.tabs.setMovable(
            True
        )

        self.tabs.setDocumentMode(
            True
        )

        self.tab_manager = TabManager(
            self.tabs,
            self.browser_manager,
            self,
        )

        # ==================================================
        # BUILD
        # ==================================================

        self._build_layout()

        # ==================================================
        # SIGNALS
        # ==================================================

        self._connect_signals()

        # ==================================================
        # SHORTCUTS
        # ==================================================

        self._setup_shortcuts()

        # ==================================================
        # FIRST TAB
        # ==================================================

        self.new_tab()

    # ==================================================
    # LAYOUT
    # ==================================================

    def _build_layout(self):

        central = QWidget()

        root = QHBoxLayout(
            central
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

        # Sidebar
        root.addWidget(
            self.sidebar
        )

        # Main browser area
        content = QWidget()

        content_layout = QVBoxLayout(
            content
        )

        content_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        content_layout.setSpacing(
            0
        )

        content_layout.addWidget(
            self.navigation_bar
        )

        content_layout.addWidget(
            self.loading_bar
        )

        content_layout.addWidget(
            self.tabs,
            1,
        )

        root.addWidget(
            content,
            1,
        )

        self.setCentralWidget(
            central
        )

    # ==================================================
    # SIGNALS
    # ==================================================

    def _connect_signals(self):

        # Navigation
        self.navigation_bar.navigate_requested.connect(
            self.navigate
        )

        self.navigation_bar.back_requested.connect(
            self.go_back
        )

        self.navigation_bar.forward_requested.connect(
            self.go_forward
        )

        self.navigation_bar.reload_requested.connect(
            self.reload
        )

        self.navigation_bar.home_requested.connect(
            self.go_home
        )

        # Tabs
        self.tabs.currentChanged.connect(
            self._tab_changed
        )

        self.tabs.tabCloseRequested.connect(
            self.tab_manager.close_tab
        )

        self.tab_bar.new_tab_requested.connect(
            self.new_tab
        )

        # Browser
        self.browser_manager.url_changed.connect(
            self._url_changed
        )

        self.browser_manager.url_changed.connect(
            self._save_history
        )

        self.browser_manager.loading_changed.connect(
            self._loading_changed
        )

        self.browser_manager.load_progress.connect(
            self._load_progress
        )

        # Sidebar
        self.sidebar.home_requested.connect(
            self.new_tab
        )

        self.sidebar.history_requested.connect(
            self.show_history
        )

        self.sidebar.bookmarks_requested.connect(
            self._bookmarks_placeholder
        )

        self.sidebar.downloads_requested.connect(
            self.show_downloads
        )

        self.sidebar.settings_requested.connect(
            self._settings_placeholder
        )

    # ==================================================
    # SHORTCUTS
    # ==================================================

    def _setup_shortcuts(self):

        QShortcut(
            QKeySequence("Ctrl+L"),
            self,
            activated=(
                self.navigation_bar
                .focus_address_bar
            ),
        )

        QShortcut(
            QKeySequence("Ctrl+T"),
            self,
            activated=self.new_tab,
        )

        QShortcut(
            QKeySequence("Ctrl+W"),
            self,
            activated=self._close_current_tab,
        )

        QShortcut(
            QKeySequence("Ctrl+R"),
            self,
            activated=self.reload,
        )

        QShortcut(
            QKeySequence("Ctrl+B"),
            self,
            activated=self.sidebar.toggle,
        )

    # ==================================================
    # NAVIGATE
    # ==================================================

    def navigate(
        self,
        text: str,
    ):

        text = text.strip()

        if not text:
            return

        self.tab_manager.navigate_current(
            text
        )

    # ==================================================
    # NEW TAB
    # ==================================================

    def new_tab(self):

        index = (
            self.tab_manager
            .create_new_tab_page()
        )

        self.tabs.setCurrentIndex(
            index
        )

        self.navigation_bar.set_url(
            ""
        )

        self.loading_bar.hide()

        self.setWindowTitle(
            "New Tab — Veyra"
        )

    # ==================================================
    # CURRENT BROWSER
    # ==================================================

    def current_browser(self):

        return (
            self.tab_manager
            .current_browser()
        )

    # ==================================================
    # BROWSER CONTROLS
    # ==================================================

    def go_back(self):

        browser = self.current_browser()

        if browser and browser.history().canGoBack():

            browser.back()

    def go_forward(self):

        browser = self.current_browser()

        if browser and browser.history().canGoForward():

            browser.forward()

    def reload(self):

        browser = self.current_browser()

        if browser:

            browser.reload()

    def go_home(self):

        browser = self.current_browser()

        if browser:

            browser.setUrl(
                QUrl(
                    "https://www.google.com"
                )
            )

    # ==================================================
    # HISTORY
    # ==================================================

    def _save_history(
        self,
        url,
    ):

        browser = self.current_browser()

        if browser is None:
            return

        url_string = (
            url.toString()
        )

        if not url_string:
            return

        if url_string.startswith(
            "about:"
        ):
            return

        self.history_repository.add(
            browser.title(),
            url_string,
        )

    def show_history(self):

        page = HistoryPage()

        page.open_requested.connect(
            self.navigate
        )

        index = self.tabs.addTab(
            page,
            "History",
        )

        self.tabs.setCurrentIndex(
            index
        )

    # ==================================================
    # DOWNLOADS
    # ==================================================

    def show_downloads(self):

        page = DownloadPage(
            self.download_manager
        )

        index = self.tabs.addTab(
            page,
            "Downloads",
        )

        self.tabs.setCurrentIndex(
            index
        )

    # ==================================================
    # CLOSE TAB
    # ==================================================

    def _close_current_tab(self):

        index = (
            self.tabs.currentIndex()
        )

        if index >= 0:

            self.tab_manager.close_tab(
                index
            )

    # ==================================================
    # TAB CHANGE
    # ==================================================

    def _tab_changed(
        self,
        index,
    ):

        if index < 0:
            return

        widget = self.tabs.widget(
            index
        )

        self.loading_bar.hide()

        # New Tab
        if isinstance(
            widget,
            NewTabPage,
        ):

            self.navigation_bar.set_url(
                ""
            )

            self.setWindowTitle(
                "New Tab — Veyra"
            )

            return

        # History
        if isinstance(
            widget,
            HistoryPage,
        ):

            self.navigation_bar.set_url(
                ""
            )

            self.setWindowTitle(
                "History — Veyra"
            )

            return

        # Downloads
        if isinstance(
            widget,
            DownloadPage,
        ):

            self.navigation_bar.set_url(
                ""
            )

            self.setWindowTitle(
                "Downloads — Veyra"
            )

            return

        # Browser
        browser = self.current_browser()

        if browser is None:
            return

        self.navigation_bar.set_url(
            browser.url().toString()
        )

        title = browser.title()

        if title:

            self.setWindowTitle(
                f"{title} — Veyra"
            )

        else:

            self.setWindowTitle(
                "Veyra"
            )

    # ==================================================
    # URL CHANGED
    # ==================================================

    def _url_changed(
        self,
        url,
    ):

        # Tylko aktualna karta powinna
        # sterować paskiem adresu.
        browser = self.current_browser()

        if browser is None:
            return

        if browser.url() != url:
            return

        self.navigation_bar.set_url(
            url.toString()
        )

    # ==================================================
    # LOADING
    # ==================================================

    def _loading_changed(
        self,
        loading,
    ):

        if loading:

            self.loading_bar.setValue(
                0
            )

            self.loading_bar.show()

            return

        self.loading_bar.setValue(
            100
        )

        self.loading_bar.hide()

        browser = self.current_browser()

        if browser:

            title = browser.title()

            if title:

                self.setWindowTitle(
                    f"{title} — Veyra"
                )

    def _load_progress(
        self,
        progress,
    ):

        if not self.current_browser():
            return

        self.loading_bar.setValue(
            progress
        )

        if progress < 100:

            self.loading_bar.show()

        else:

            self.loading_bar.hide()

    # ==================================================
    # PLACEHOLDERS
    # ==================================================

    def _bookmarks_placeholder(self):

        print(
            "Bookmarks are not implemented yet."
        )

    def _settings_placeholder(self):

        print(
            "Settings are not implemented yet."
        )