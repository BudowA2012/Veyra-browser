from PySide6.QtCore import QUrl
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QMainWindow,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from core.browser.browser_manager import BrowserManager
from ui.components.navigation_bar import NavigationBar
from ui.new_tab.new_tab_page import NewTabPage
from ui.tabs.tab_manager import TabManager


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Veyra")
        self.setMinimumSize(900, 600)
        self.resize(1400, 900)

        # ==========================================
        # Core
        # ==========================================

        self.browser_manager = BrowserManager(self)

        # ==========================================
        # UI
        # ==========================================

        self.navigation_bar = NavigationBar()

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.setDocumentMode(True)

        self.tab_manager = TabManager(
            self.tabs,
            self.browser_manager,
            self,
        )

        # ==========================================
        # Central Widget
        # ==========================================

        central = QWidget()

        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(self.navigation_bar)
        layout.addWidget(self.tabs)

        self.setCentralWidget(central)

        self._connect_signals()
        self._setup_shortcuts()

        # pierwsza karta
        self.tab_manager.create_new_tab_page()

    # ==========================================
    # Signals
    # ==========================================

    def _connect_signals(self):

        self.navigation_bar.navigate_requested.connect(
            self.navigate
        )

        self.navigation_bar.new_tab_requested.connect(
            self.new_tab
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

        self.tabs.currentChanged.connect(
            self._current_tab_changed
        )

        self.browser_manager.url_changed.connect(
            self._url_changed
        )

        self.browser_manager.loading_changed.connect(
            self._loading_changed
        )

    # ==========================================
    # Shortcuts
    # ==========================================

    def _setup_shortcuts(self):

        QShortcut(
            QKeySequence("Ctrl+L"),
            self,
            activated=self.navigation_bar.focus_address_bar,
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

    # ==========================================
    # Browser
    # ==========================================

    def current_browser(self):
        return self.tab_manager.current_browser()

    def navigate(self, text: str):

        text = text.strip()

        if not text:
            return

        browser = self.current_browser()

        # jeśli jesteśmy na NewTabPage,
        # zamieniamy ją na normalną kartę
        if browser is None:

            index = self.tabs.currentIndex()

            self.tabs.removeTab(index)

            self.tab_manager.create_tab(text)

            return

        if "://" in text:
            url = text

        elif "." in text and " " not in text:
            url = "https://" + text

        else:
            query = text.replace(" ", "+")
            url = (
                "https://www.google.com/search?q="
                + query
            )

        browser.setUrl(QUrl(url))

    def new_tab(self):

        index = self.tab_manager.create_new_tab_page()

        self.tabs.setCurrentIndex(index)

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
                QUrl("https://www.google.com")
            )

    # ==========================================
    # Tabs
    # ==========================================

    def _close_current_tab(self):

        index = self.tabs.currentIndex()

        if index >= 0:
            self.tab_manager.close_tab(index)

    def _current_tab_changed(self, index):

        if index < 0:
            return

        widget = self.tabs.widget(index)

        if isinstance(widget, NewTabPage):

            self.navigation_bar.set_url("")

            try:
                widget.search_requested.disconnect(
                    self.navigate
                )
            except Exception:
                pass

            try:
                widget.shortcut_requested.disconnect(
                    self.navigate
                )
            except Exception:
                pass

            widget.search_requested.connect(
                self.navigate
            )

            widget.shortcut_requested.connect(
                self.navigate
            )

            self.setWindowTitle("New Tab — Veyra")

            return

        browser = self.current_browser()

        if browser:

            self.navigation_bar.set_url(
                browser.url().toString()
            )

            title = browser.title()

            if title:
                self.setWindowTitle(
                    f"{title} — Veyra"
                )

    # ==========================================
    # URL
    # ==========================================

    def _url_changed(self, url):

        browser = self.current_browser()

        if browser is None:
            return

        if browser.url() == url:

            self.navigation_bar.set_url(
                url.toString()
            )

    # ==========================================
    # Loading
    # ==========================================

    def _loading_changed(self, loading: bool):

        browser = self.current_browser()

        if loading:

            self.setWindowTitle(
                "Loading... — Veyra"
            )

            return

        if browser:

            title = browser.title()

            if title:
                self.setWindowTitle(
                    f"{title} — Veyra"
                )

            else:
                self.setWindowTitle(
                    "Veyra"
                )

        else:

            self.setWindowTitle(
                "Veyra"
            )