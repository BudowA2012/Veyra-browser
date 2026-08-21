from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QTabWidget

from ui.new_tab.new_tab_page import NewTabPage


class TabManager:
    """Creates, manages and closes browser tabs."""

    def __init__(
        self,
        tabs: QTabWidget,
        browser_manager,
        parent=None,
    ):
        self.tabs = tabs
        self.browser_manager = browser_manager
        self.parent = parent

        self.tabs.tabCloseRequested.connect(
            self.close_tab
        )

    def create_tab(
        self,
        url: str = "https://www.google.com",
    ) -> int:

        browser = self.browser_manager.create_browser()

        index = self.tabs.addTab(
            browser,
            "New Tab",
        )

        self.tabs.setCurrentIndex(index)

        browser.setUrl(QUrl(url))

        browser.titleChanged.connect(
            lambda title, browser=browser:
            self._update_title(browser, title)
        )

        browser.iconChanged.connect(
            lambda icon, browser=browser:
            self._update_icon(browser, icon)
        )

        return index

    def create_new_tab_page(self) -> int:

        page = NewTabPage()

        index = self.tabs.addTab(
            page,
            "New Tab",
        )

        self.tabs.setCurrentIndex(index)

        return index

    def close_tab(self, index: int):

        if index < 0 or index >= self.tabs.count():
            return

        widget = self.tabs.widget(index)

        self.tabs.removeTab(index)

        if widget:
            widget.deleteLater()

        if self.tabs.count() == 0:
            self.create_new_tab_page()

    def current_browser(self):

        widget = self.tabs.currentWidget()

        if isinstance(widget, NewTabPage):
            return None

        return widget

    def current_widget(self):

        return self.tabs.currentWidget()

    def _update_title(
        self,
        browser,
        title: str,
    ):

        index = self.tabs.indexOf(browser)

        if index == -1:
            return

        if not title:
            title = "New Tab"

        self.tabs.setTabText(
            index,
            title[:24],
        )

    def _update_icon(
        self,
        browser,
        icon,
    ):

        index = self.tabs.indexOf(browser)

        if index == -1:
            return

        if not icon.isNull():

            self.tabs.setTabIcon(
                index,
                icon,
            )