from PySide6.QtCore import (
    QUrl,
)

from PySide6.QtGui import (
    QIcon,
)

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

        # ==================================================
        # TAB CONTEXT MENU
        # ==================================================

        self.tabs.tab_bar.duplicateRequested.connect(
            self.duplicate_tab
        )

        self.tabs.tab_bar.closeOthersRequested.connect(
            self.close_other_tabs
        )

        self.tabs.tab_bar.closeRightRequested.connect(
            self.close_tabs_to_right
        )

        self.tabs.tab_bar.pinToggleRequested.connect(
            self.toggle_pin
        )

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

        # New Tab nie ma favicony strony.
        self.tabs.setTabIcon(
            index,
            QIcon(),
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

        # Czyścimy ikonę, dopóki strona
        # nie dostarczy własnej favicony.
        self.tabs.setTabIcon(
            index,
            QIcon(),
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
    # NAVIGATE WIDGET
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

            index = (
                self.tabs.indexOf(
                    widget
                )
            )

            if index >= 0:

                # Nie pokazujemy favicony poprzedniej
                # strony podczas ładowania nowej.
                self.tabs.setTabIcon(
                    index,
                    QIcon(),
                )

            self.browser_manager.load_url(
                widget,
                text,
            )

            return

        # ==================================================
        # INTERNAL PAGE -> WEBSITE
        # ==================================================

        index = (
            self.tabs.indexOf(
                widget
            )
        )

        if index < 0:
            return

        was_current = (
            self.tabs.currentWidget()
            is widget
        )

        was_pinned = (
            self.tabs.tab_bar.is_pinned(
                index
            )
        )

        browser = (
            self.create_browser()
        )

        self.tabs.removeTab(
            index
        )

        self.tabs.insertTab(
            index,
            browser,
            "New Tab",
        )

        self.tabs.setTabIcon(
            index,
            QIcon(),
        )

        if was_pinned:

            self.tabs.tab_bar.set_pinned(
                index,
                True,
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

        # ==================================================
        # TITLE
        # ==================================================

        browser.titleChanged.connect(
            lambda title,
            browser=browser:
            self._update_title(
                browser,
                title,
            )
        )

        # ==================================================
        # FAVICON
        # ==================================================

        browser.iconChanged.connect(
            lambda icon,
            browser=browser:
            self._update_icon(
                browser,
                icon,
            )
        )

        # ==================================================
        # URL
        # ==================================================

        browser.urlChanged.connect(
            lambda url,
            browser=browser:
            self._browser_url_changed(
                browser,
                url,
            )
        )

        # ==================================================
        # LOAD FINISHED
        # ==================================================

        browser.loadFinished.connect(
            lambda success,
            browser=browser:
            self._load_finished(
                browser,
                success,
            )
        )

        # ==================================================
        # NEW WINDOWS / TABS
        # ==================================================

        browser.page().newWindowRequested.connect(
            self._handle_new_window_request
        )

    # ======================================================
    # URL CHANGED
    # ======================================================

    def _browser_url_changed(
        self,
        browser,
        url,
    ):

        index = (
            self.tabs.indexOf(
                browser
            )
        )

        if index < 0:
            return

        # Przy zmianie strony usuwamy starą faviconę.
        # Jeśli nowa strona ma ikonę, za chwilę
        # przyjdzie browser.iconChanged.
        self.tabs.setTabIcon(
            index,
            QIcon(),
        )

        # Jeśli tytułu jeszcze nie ma,
        # pokazujemy domenę zamiast "New Tab".
        if not browser.title():

            fallback_title = (
                self._title_from_url(
                    url
                )
            )

            if fallback_title:

                self.tabs.setTabText(
                    index,
                    fallback_title[:28],
                )

    # ======================================================
    # LOAD FINISHED
    # ======================================================

    def _load_finished(
        self,
        browser,
        success,
    ):

        index = (
            self.tabs.indexOf(
                browser
            )
        )

        if index < 0:
            return

        if not success:
            return

        # Czasami favicon jest już dostępna,
        # ale iconChanged nie odpalił ponownie.
        icon = (
            browser.icon()
        )

        if (
            icon is not None
            and not icon.isNull()
        ):

            self.tabs.setTabIcon(
                index,
                icon,
            )

        # To samo robimy z tytułem.
        title = (
            browser.title()
            .strip()
        )

        if title:

            self.tabs.setTabText(
                index,
                title[:28],
            )

    # ======================================================
    # FALLBACK TITLE
    # ======================================================

    def _title_from_url(
        self,
        url,
    ):

        if isinstance(
            url,
            QUrl,
        ):

            host = (
                url.host()
                .strip()
            )

        else:

            host = (
                QUrl(
                    str(url)
                )
                .host()
                .strip()
            )

        if not host:
            return "New Tab"

        if host.startswith(
            "www."
        ):

            host = host[4:]

        return host

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

        browser = (
            self.tabs.widget(
                new_index
            )
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
    # DUPLICATE TAB
    # ======================================================

    def duplicate_tab(
        self,
        index,
    ):

        if (
            index < 0
            or index >= self.tabs.count()
        ):

            return

        widget = (
            self.tabs.widget(
                index
            )
        )

        # ==================================================
        # WEB TAB
        # ==================================================

        if isinstance(
            widget,
            QWebEngineView,
        ):

            url = (
                widget.url()
                .toString()
                .strip()
            )

            if not url:
                return

            original_icon = (
                widget.icon()
            )

            new_index = (
                self.create_browser_tab(
                    url=url,
                    activate=True,
                )
            )

            # Pokaż faviconę od razu,
            # zanim duplikat skończy ładowanie.
            if (
                original_icon is not None
                and not original_icon.isNull()
            ):

                self.tabs.setTabIcon(
                    new_index,
                    original_icon,
                )

        # ==================================================
        # NEW TAB
        # ==================================================

        elif isinstance(
            widget,
            NewTabPage,
        ):

            new_index = (
                self.create_new_tab_page()
            )

        else:

            return

        # ==================================================
        # MOVE NEXT TO ORIGINAL
        # ==================================================

        target_index = min(
            index + 1,
            self.tabs.count() - 1,
        )

        if (
            new_index
            != target_index
        ):

            self.tabs.tab_bar.moveTab(
                new_index,
                target_index,
            )

        self.tabs.setCurrentIndex(
            target_index
        )

    # ======================================================
    # CLOSE TAB
    # ======================================================

    def close_tab(
        self,
        index,
    ):

        if (
            index < 0
            or index >= self.tabs.count()
        ):

            return

        widget = (
            self.tabs.widget(
                index
            )
        )

        self.tabs.removeTab(
            index
        )

        if widget:

            widget.deleteLater()

        if (
            self.tabs.count()
            == 0
        ):

            self.create_new_tab_page()

    # ======================================================
    # CLOSE OTHER TABS
    # ======================================================

    def close_other_tabs(
        self,
        index,
    ):

        if (
            index < 0
            or index >= self.tabs.count()
        ):

            return

        keep_widget = (
            self.tabs.widget(
                index
            )
        )

        for current_index in range(
            self.tabs.count() - 1,
            -1,
            -1,
        ):

            widget = (
                self.tabs.widget(
                    current_index
                )
            )

            if (
                widget
                is keep_widget
            ):

                continue

            self.close_tab(
                current_index
            )

        new_index = (
            self.tabs.indexOf(
                keep_widget
            )
        )

        if new_index >= 0:

            self.tabs.setCurrentIndex(
                new_index
            )

    # ======================================================
    # CLOSE RIGHT
    # ======================================================

    def close_tabs_to_right(
        self,
        index,
    ):

        if (
            index < 0
            or index >= self.tabs.count()
        ):

            return

        keep_widget = (
            self.tabs.widget(
                index
            )
        )

        for current_index in range(
            self.tabs.count() - 1,
            index,
            -1,
        ):

            self.close_tab(
                current_index
            )

        new_index = (
            self.tabs.indexOf(
                keep_widget
            )
        )

        if new_index >= 0:

            self.tabs.setCurrentIndex(
                new_index
            )

    # ======================================================
    # PIN / UNPIN
    # ======================================================

    def toggle_pin(
        self,
        index,
    ):

        if (
            index < 0
            or index >= self.tabs.count()
        ):

            return

        tab_bar = (
            self.tabs.tab_bar
        )

        widget = (
            self.tabs.widget(
                index
            )
        )

        pinned = (
            tab_bar.is_pinned(
                index
            )
        )

        # ==================================================
        # UNPIN
        # ==================================================

        if pinned:

            tab_bar.set_pinned(
                index,
                False,
            )

            return

        # ==================================================
        # PIN
        # ==================================================

        pinned_count = 0

        for current_index in range(
            self.tabs.count()
        ):

            if tab_bar.is_pinned(
                current_index
            ):

                pinned_count += 1

        if (
            index
            != pinned_count
        ):

            tab_bar.moveTab(
                index,
                pinned_count,
            )

        new_index = (
            self.tabs.indexOf(
                widget
            )
        )

        if new_index < 0:
            return

        tab_bar.set_pinned(
            new_index,
            True,
        )

        self.tabs.setCurrentIndex(
            new_index
        )

    # ======================================================
    # TITLE
    # ======================================================

    def _update_title(
        self,
        browser,
        title,
    ):

        index = (
            self.tabs.indexOf(
                browser
            )
        )

        if index < 0:
            return

        title = (
            str(title)
            .strip()
        )

        if not title:

            title = (
                self._title_from_url(
                    browser.url()
                )
            )

        self.tabs.setTabText(
            index,
            title[:28],
        )

    # ======================================================
    # FAVICON
    # ======================================================

    def _update_icon(
        self,
        browser,
        icon,
    ):

        index = (
            self.tabs.indexOf(
                browser
            )
        )

        if index < 0:
            return

        if (
            icon is None
            or icon.isNull()
        ):

            return

        self.tabs.setTabIcon(
            index,
            icon,
        )