from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QTabWidget, QWidget


class TabManager(QObject):
    """Handles browser tabs."""

    tab_created = Signal(int)
    tab_closed = Signal(int)

    def __init__(self, tabs: QTabWidget, browser_manager, parent=None):
        super().__init__(parent)

        self.tabs = tabs
        self.browser_manager = browser_manager

        self.tabs.tabCloseRequested.connect(self.close_tab)

    def create_tab(self, url: str = "https://www.google.com") -> int:
        browser = self.browser_manager.create_browser()

        browser.setUrl(url)

        index = self.tabs.addTab(browser, "New Tab")
        self.tabs.setCurrentIndex(index)

        browser.titleChanged.connect(
            lambda title, browser=browser:
            self._update_title(browser, title)
        )

        self.tab_created.emit(index)

        return index

    def close_tab(self, index: int):
        if self.tabs.count() <= 1:
            return

        widget = self.tabs.widget(index)

        self.tabs.removeTab(index)

        if widget:
            widget.deleteLater()

        self.tab_closed.emit(index)

    def current_browser(self):
        return self.tabs.currentWidget()

    def _update_title(self, browser, title: str):
        index = self.tabs.indexOf(browser)

        if index == -1:
            return

        if not title:
            title = "New Tab"

        self.tabs.setTabText(index, title[:30])