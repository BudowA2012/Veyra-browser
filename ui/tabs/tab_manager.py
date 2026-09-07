from PySide6.QtWebEngineCore import (
    QWebEngineNewWindowRequest,
)
from PySide6.QtWebEngineWidgets import (
    QWebEngineView,
)

from ui.new_tab.new_tab_page import (
    NewTabPage,
)


class TabManager:

    def __init__(
        self,
        tabs,
        browser_manager,
        parent=None,
    ):
        self.tabs = tabs

        self.browser_manager = (
            browser_manager
        )

        self.parent = parent

    # ======================================================
    # NEW TAB PAGE
    # ======================================================

    def create_new_tab_page(
        self,
    ):

        page = NewTabPage(
            parent=self.tabs
        )

        page.search_requested.connect(
            lambda text,
            page=page:
            self.navigate_widget(
                page,
                text,
            )
        )

        page.shortcut_requested.connect(
            lambda text,
            page=page:
            self.navigate_widget(
                page,
                text,
            )
        )

        index = self.tabs.addTab(
            page,
            "New Tab",
        )

        self.tabs.setCurrentIndex(
            index
        )

        return index

    # ======================================================
    # CREATE BROWSER
    # ======================================================

    def create_browser(
        self,
    ):

        browser = (
            self.browser_manager
            .create_browser()
        )

        self._connect_browser(
            browser
        )

        return browser

    # ======================================================
    # CREATE WEB TAB
    # ======================================================

    def create_browser_tab(
        self,
        url=None,
        activate=True,
    ):

        browser = (
            self.create_browser()
        )

        index = self.tabs.addTab(
            browser,
            "New Tab",
        )

        if activate:

            self.tabs.setCurrentIndex(
                index
            )

        if url:

            self.browser_manager.load_url(
                browser,
                url,
            )

        return index

    # ======================================================
    # NAVIGATE CURRENT
    # ======================================================

    def navigate_current(
        self,
        text,
    ):

        widget = (
            self.tabs.currentWidget()
        )

        if widget is None:
            return

        self.navigate_widget(
            widget,
            text,
        )

    # ======================================================
    # NAVIGATE
    # ======================================================

    def navigate_widget(
        self,
        widget,
        text,
    ):

        text = str(
            text
        ).strip()

        if not text:
            return

        # ==================================================
        # NORMAL WEBSITE
        # ==================================================

        if isinstance(
            widget,
            QWebEngineView,
        ):

            self.browser_manager.load_url(
                widget,
                text,
            )

            return

        # ==================================================
        # INTERNAL PAGE -> WEBSITE
        # ==================================================

        index = self.tabs.indexOf(
            widget
        )

        if index < 0:
            return

        was_current = (
            self.tabs.currentWidget()
            is widget
        )

        browser = (
            self.create_browser()
        )

        # ----------------------------------------------
        # Keep same tab position
        # ----------------------------------------------

        self.tabs.removeTab(
            index
        )

        self.tabs.insertTab(
            index,
            browser,
            "New Tab",
        )

        if was_current:

            self.tabs.setCurrentIndex(
                index
            )

        widget.deleteLater()

        self.browser_manager.load_url(
            browser,
            text,
        )

    # ======================================================
    # BROWSER SIGNALS
    # ======================================================

    def _connect_browser(
        self,
        browser,
    ):

        browser.titleChanged.connect(
            lambda title,
            browser=browser:
            self._update_title(
                browser,
                title,
            )
        )

        browser.iconChanged.connect(
            lambda icon,
            browser=browser:
            self._update_icon(
                browser,
                icon,
            )
        )

        browser.page().newWindowRequested.connect(
            self._handle_new_window_request
        )

    # ======================================================
    # NEW WINDOW
    # ======================================================

    def _handle_new_window_request(
        self,
        request,
    ):

        destination = (
            request.destination()
        )

        background = (
            destination
            == QWebEngineNewWindowRequest
            .DestinationType
            .InNewBackgroundTab
        )

        previous_index = (
            self.tabs.currentIndex()
        )

        new_index = (
            self.create_browser_tab(
                activate=not background
            )
        )

        browser = self.tabs.widget(
            new_index
        )

        request.openIn(
            browser.page()
        )

        if background:

            self.tabs.setCurrentIndex(
                previous_index
            )

    # ======================================================
    # CURRENT BROWSER
    # ======================================================

    def current_browser(
        self,
    ):

        widget = (
            self.tabs.currentWidget()
        )

        if isinstance(
            widget,
            QWebEngineView,
        ):

            return widget

        return None

    # ======================================================
    # CLOSE
    # ======================================================

    def close_tab(
        self,
        index,
    ):

        if index < 0:
            return

        widget = self.tabs.widget(
            index
        )

        self.tabs.removeTab(
            index
        )

        if widget:

            widget.deleteLater()

        if self.tabs.count() == 0:

            self.create_new_tab_page()

    # ======================================================
    # TITLE
    # ======================================================

    def _update_title(
        self,
        browser,
        title,
    ):

        index = self.tabs.indexOf(
            browser
        )

        if index < 0:
            return

        if not title:

            title = "New Tab"

        self.tabs.setTabText(
            index,
            title[:28],
        )

    # ======================================================
    # ICON
    # ======================================================

    def _update_icon(
        self,
        browser,
        icon,
    ):

        index = self.tabs.indexOf(
            browser
        )

        if index < 0:
            return

        if icon.isNull():
            return

        self.tabs.setTabIcon(
            index,
            icon,
        )