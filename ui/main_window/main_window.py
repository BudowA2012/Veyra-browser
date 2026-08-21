from PySide6.QtCore import QUrl
from PySide6.QtWidgets import (
    QMainWindow,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from core.browser.browser_manager import BrowserManager
from ui.components.navigation_bar import NavigationBar
from ui.tabs.tab_manager import TabManager


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Veyra")
        self.resize(1400, 900)

        self.browser_manager = BrowserManager(self)

        self.navigation_bar = NavigationBar()

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.setDocumentMode(True)

        self.tab_manager = TabManager(
            self.tabs,
            self.browser_manager,
            self,
        )

        central = QWidget()

        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(self.navigation_bar)
        layout.addWidget(self.tabs)

        self.setCentralWidget(central)

        self._connect_signals()

        self.tab_manager.create_tab(
            "https://www.google.com"
        )

    def _connect_signals(self):

        self.navigation_bar.navigate_requested.connect(
            self.navigate
        )

        self.navigation_bar.new_tab_requested.connect(
            self.new_tab
        )

        self.tabs.currentChanged.connect(
            self._current_tab_changed
        )

        self.browser_manager.url_changed.connect(
            self._url_changed
        )

        self.navigation_bar.back_button.clicked.connect(
            self.go_back
        )

        self.navigation_bar.forward_button.clicked.connect(
            self.go_forward
        )

        self.navigation_bar.reload_button.clicked.connect(
            self.reload
        )

        self.navigation_bar.home_button.clicked.connect(
            self.go_home
        )

    def current_browser(self):
        return self.tab_manager.current_browser()

    def navigate(self, text: str):

        browser = self.current_browser()

        if browser is None:
            return

        if "://" not in text:
            if " " in text:
                text = (
                    "https://www.google.com/search?q="
                    + text.replace(" ", "+")
                )
            else:
                text = "https://" + text

        browser.setUrl(QUrl(text))

    def new_tab(self):
        self.tab_manager.create_tab(
            "https://www.google.com"
        )

    def go_back(self):
        browser = self.current_browser()

        if browser:
            browser.back()

    def go_forward(self):
        browser = self.current_browser()

        if browser:
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

    def _current_tab_changed(self, index):
        browser = self.current_browser()

        if browser:
            self.navigation_bar.set_url(
                browser.url().toString()
            )

    def _url_changed(self, url):
        browser = self.current_browser()

        if browser is None:
            return

        if browser.url() == url:
            self.navigation_bar.set_url(
                url.toString()
            )