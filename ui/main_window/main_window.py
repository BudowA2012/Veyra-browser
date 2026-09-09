from PySide6.QtCore import (
    QSettings,
    QUrl,
)

from PySide6.QtGui import (
    QKeySequence,
    QShortcut,
)

from PySide6.QtWebEngineWidgets import (
    QWebEngineView,
)

from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QProgressBar,
    QVBoxLayout,
    QWidget,
)

from core.bookmarks.bookmark_repository import (
    BookmarkRepository,
)

from core.browser.browser_manager import (
    BrowserManager,
)

from core.downloads.download_manager import (
    DownloadManager,
)

from core.history.history_repository import (
    HistoryRepository,
)

from core.session.session_manager import (
    SessionManager,
)

from ui.bookmarks.bookmarks_page import (
    BookmarksPage,
)

from ui.components.navigation_bar import (
    NavigationBar,
)

from ui.components.qr_dialog import (
    QRDialog,
)

from ui.downloads.download_page import (
    DownloadPage,
)

from ui.downloads.download_popup import (
    DownloadPopup,
)

from ui.history.history_page import (
    HistoryPage,
)

from ui.new_tab.new_tab_page import (
    NewTabPage,
)

from ui.settings.settings_page import (
    SettingsPage,
)

from ui.sidebar.sidebar import (
    Sidebar,
)

from ui.styles.style_manager import (
    apply_theme,
)

from ui.tabs.tab_manager import (
    TabManager,
)

from ui.tabs.tab_widget import (
    VeyraTabWidget,
)


class MainWindow(QMainWindow):

    DOWNLOAD_POPUP_MARGIN = 18

    def __init__(
        self,
    ):
        super().__init__()

        # ==================================================
        # SETTINGS
        # ==================================================

        self.settings = QSettings(
            "Veyra",
            "VeyraBrowser",
        )

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

        self.browser_manager = (
            BrowserManager(
                self
            )
        )

        self.history_repository = (
            HistoryRepository()
        )

        self.bookmark_repository = (
            BookmarkRepository()
        )

        self.download_manager = (
            DownloadManager(
                self.browser_manager.profile,
                self,
            )
        )

        # ==================================================
        # UI
        # ==================================================

        self.sidebar = Sidebar()

        self.navigation_bar = (
            NavigationBar()
        )

        # ==================================================
        # LOADING BAR
        # ==================================================

        self.loading_bar = (
            QProgressBar()
        )

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

        self.tabs = (
            VeyraTabWidget()
        )

        self.tab_bar = (
            self.tabs.tab_bar
        )

        self.tab_manager = (
            TabManager(
                self.tabs,
                self.browser_manager,
                self,
            )
        )

        # ==================================================
        # SESSION
        # ==================================================

        self.session_manager = (
            SessionManager(
                self.tabs,
                self,
            )
        )

        # ==================================================
        # BUILD
        # ==================================================

        self._build_layout()

        # ==================================================
        # DOWNLOAD POPUP
        # ==================================================

        self.download_popup = (
            DownloadPopup(
                self
            )
        )

        self.download_popup.show_all_requested.connect(
            self._show_all_downloads_from_popup
        )

        # ==================================================
        # SIGNALS
        # ==================================================

        self._connect_signals()

        self._setup_shortcuts()

        # ==================================================
        # STARTUP
        # ==================================================

        self._restore_session_or_new_tab()

    # ======================================================
    # LAYOUT
    # ======================================================

    def _build_layout(
        self,
    ):

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

        root.addWidget(
            self.sidebar
        )

        self.content = QWidget()

        content_layout = QVBoxLayout(
            self.content
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
            self.content,
            1,
        )

        self.setCentralWidget(
            central
        )

    # ======================================================
    # SIGNALS
    # ======================================================

    def _connect_signals(
        self,
    ):

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

        self.navigation_bar.bookmark_requested.connect(
            self.toggle_bookmark
        )

        self.navigation_bar.qr_requested.connect(
            self.show_qr_code
        )

        self.tabs.currentChanged.connect(
            self._tab_changed
        )

        self.tabs.tabCloseRequested.connect(
            self.tab_manager.close_tab
        )

        self.tabs.newTabRequested.connect(
            self.new_tab
        )

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

        self.download_manager.download_added.connect(
            self._download_started
        )

        self.sidebar.home_requested.connect(
            self.new_tab
        )

        self.sidebar.history_requested.connect(
            self.show_history
        )

        self.sidebar.bookmarks_requested.connect(
            self.show_bookmarks
        )

        self.sidebar.downloads_requested.connect(
            self.show_downloads
        )

        self.sidebar.settings_requested.connect(
            self.show_settings
        )

    # ======================================================
    # SHORTCUTS
    # ======================================================

    def _setup_shortcuts(
        self,
    ):

        QShortcut(
            QKeySequence(
                "Ctrl+L"
            ),
            self,
            activated=(
                self.navigation_bar
                .focus_address_bar
            ),
        )

        QShortcut(
            QKeySequence(
                "Ctrl+T"
            ),
            self,
            activated=self.new_tab,
        )

        QShortcut(
            QKeySequence(
                "Ctrl+W"
            ),
            self,
            activated=(
                self._close_current_tab
            ),
        )

        QShortcut(
            QKeySequence(
                "Ctrl+R"
            ),
            self,
            activated=self.reload,
        )

        QShortcut(
            QKeySequence(
                "Ctrl+B"
            ),
            self,
            activated=(
                self.sidebar.toggle
            ),
        )

        QShortcut(
            QKeySequence(
                "Ctrl+D"
            ),
            self,
            activated=self.toggle_bookmark,
        )

        QShortcut(
            QKeySequence(
                "Ctrl+Shift+Q"
            ),
            self,
            activated=self.show_qr_code,
        )

    # ======================================================
    # NAVIGATE
    # ======================================================

    def navigate(
        self,
        text: str,
    ):

        text = text.strip()

        if not text:
            return

        self.navigation_bar.hide_suggestions()

        self.tab_manager.navigate_current(
            text
        )

    # ======================================================
    # NEW TAB
    # ======================================================

    def new_tab(
        self,
    ):

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

        self.navigation_bar.set_bookmarked(
            False
        )

        self.loading_bar.hide()

        self.setWindowTitle(
            "New Tab — Veyra"
        )

    # ======================================================
    # CURRENT BROWSER
    # ======================================================

    def current_browser(
        self,
    ):

        return (
            self.tab_manager
            .current_browser()
        )

    # ======================================================
    # BOOKMARKS
    # ======================================================

    def toggle_bookmark(
        self,
    ):

        browser = (
            self.current_browser()
        )

        if browser is None:
            return

        url = (
            browser.url()
            .toString()
            .strip()
        )

        if not url:
            return

        if url.startswith(
            "about:"
        ):

            return

        if (
            self.bookmark_repository
            .is_bookmarked(
                url
            )
        ):

            self.bookmark_repository.remove_url(
                url
            )

            self.navigation_bar.set_bookmarked(
                False
            )

        else:

            title = (
                browser.title()
                .strip()
            )

            if not title:

                title = url

            self.bookmark_repository.add(
                title,
                url,
            )

            self.navigation_bar.set_bookmarked(
                True
            )

        for index in range(
            self.tabs.count()
        ):

            widget = (
                self.tabs.widget(
                    index
                )
            )

            if isinstance(
                widget,
                BookmarksPage,
            ):

                widget.reload()

    def _update_bookmark_state(
        self,
    ):

        browser = (
            self.current_browser()
        )

        if browser is None:

            self.navigation_bar.set_bookmarked(
                False
            )

            return

        url = (
            browser.url()
            .toString()
            .strip()
        )

        bookmarked = (
            self.bookmark_repository
            .is_bookmarked(
                url
            )
        )

        self.navigation_bar.set_bookmarked(
            bookmarked
        )

    def show_bookmarks(
        self,
    ):

        self.navigation_bar.hide_suggestions()

        for index in range(
            self.tabs.count()
        ):

            widget = (
                self.tabs.widget(
                    index
                )
            )

            if isinstance(
                widget,
                BookmarksPage,
            ):

                widget.reload()

                self.tabs.setCurrentIndex(
                    index
                )

                return

        page = BookmarksPage(
            self.bookmark_repository
        )

        page.open_requested.connect(
            self.navigate
        )

        index = (
            self.tabs.addTab(
                page,
                "Bookmarks",
            )
        )

        self.tabs.setCurrentIndex(
            index
        )

    # ======================================================
    # SESSION RESTORE
    # ======================================================

    def _restore_session_or_new_tab(
        self,
    ):

        restore_enabled = (
            self.settings.value(
                "browser/restore_session",
                True,
                type=bool,
            )
        )

        session = None

        if (
            self.session_manager
            .crashed_last_time()
        ):

            session = (
                self.session_manager
                .crash_session()
            )

        elif restore_enabled:

            session = (
                self.session_manager
                .normal_session()
            )

        if not session:

            self.new_tab()
            return

        tabs_data = session.get(
            "tabs",
            [],
        )

        active_index = session.get(
            "active_index",
            0,
        )

        if not tabs_data:

            self.new_tab()
            return

        restored = 0

        for tab_data in tabs_data:

            if not isinstance(
                tab_data,
                dict,
            ):

                continue

            tab_type = tab_data.get(
                "type"
            )

            if (
                tab_type
                == "new_tab"
            ):

                self.tab_manager.create_new_tab_page()

                restored += 1

                continue

            if (
                tab_type
                == "web"
            ):

                url = tab_data.get(
                    "url",
                    "",
                )

                if not url:
                    continue

                self.tab_manager.create_browser_tab(
                    url=url,
                    activate=False,
                )

                restored += 1

        if restored == 0:

            self.new_tab()
            return

        active_index = max(
            0,
            min(
                active_index,
                self.tabs.count() - 1,
            ),
        )

        self.tabs.setCurrentIndex(
            active_index
        )

    # ======================================================
    # QR
    # ======================================================

    def show_qr_code(
        self,
    ):

        browser = (
            self.current_browser()
        )

        if browser is None:
            return

        url = (
            browser.url()
            .toString()
            .strip()
        )

        if not url:
            return

        dialog = QRDialog(
            url,
            self,
        )

        dialog.exec()

    # ======================================================
    # BROWSER CONTROLS
    # ======================================================

    def go_back(
        self,
    ):

        browser = (
            self.current_browser()
        )

        if (
            browser
            and browser.history().canGoBack()
        ):

            browser.back()

    def go_forward(
        self,
    ):

        browser = (
            self.current_browser()
        )

        if (
            browser
            and browser.history().canGoForward()
        ):

            browser.forward()

    def reload(
        self,
    ):

        browser = (
            self.current_browser()
        )

        if browser:

            browser.reload()

    def go_home(
        self,
    ):

        browser = (
            self.current_browser()
        )

        if browser:

            browser.setUrl(
                QUrl(
                    "https://www.google.com"
                )
            )

        else:

            self.new_tab()

    # ======================================================
    # HISTORY
    # ======================================================

    def _save_history(
        self,
        url,
    ):

        save_history = (
            self.settings.value(
                "privacy/save_history",
                True,
                type=bool,
            )
        )

        if not save_history:
            return

        browser = (
            self.current_browser()
        )

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

    def show_history(
        self,
    ):

        self.navigation_bar.hide_suggestions()

        for index in range(
            self.tabs.count()
        ):

            widget = (
                self.tabs.widget(
                    index
                )
            )

            if isinstance(
                widget,
                HistoryPage,
            ):

                widget.reload()

                self.tabs.setCurrentIndex(
                    index
                )

                return

        page = HistoryPage()

        page.open_requested.connect(
            self.navigate
        )

        index = (
            self.tabs.addTab(
                page,
                "History",
            )
        )

        self.tabs.setCurrentIndex(
            index
        )

    # ======================================================
    # SETTINGS
    # ======================================================

    def show_settings(
        self,
    ):

        self.navigation_bar.hide_suggestions()

        for index in range(
            self.tabs.count()
        ):

            widget = (
                self.tabs.widget(
                    index
                )
            )

            if isinstance(
                widget,
                SettingsPage,
            ):

                self.tabs.setCurrentIndex(
                    index
                )

                return

        page = SettingsPage()

        page.theme_changed.connect(
            self._change_theme
        )

        page.default_zoom_changed.connect(
            self._set_default_zoom
        )

        page.download_location_changed.connect(
            self.download_manager
            .set_download_folder
        )

        page.clear_browsing_data_requested.connect(
            self._clear_browsing_data
        )

        index = (
            self.tabs.addTab(
                page,
                "Settings",
            )
        )

        self.tabs.setCurrentIndex(
            index
        )

    # ======================================================
    # DEFAULT ZOOM
    # ======================================================

    def _set_default_zoom(
        self,
        zoom,
    ):

        factor = (
            zoom
            / 100.0
        )

        for index in range(
            self.tabs.count()
        ):

            widget = (
                self.tabs.widget(
                    index
                )
            )

            if isinstance(
                widget,
                QWebEngineView,
            ):

                widget.setZoomFactor(
                    factor
                )

    # ======================================================
    # CLEAR BROWSING DATA
    # ======================================================

    def _clear_browsing_data(
        self,
    ):

        self.history_repository.clear()

        self.browser_manager.clear_browsing_data()

        for index in range(
            self.tabs.count()
        ):

            widget = (
                self.tabs.widget(
                    index
                )
            )

            if isinstance(
                widget,
                HistoryPage,
            ):

                widget.reload()

    # ======================================================
    # DOWNLOAD POPUP
    # ======================================================

    def _download_started(
        self,
        download,
    ):

        self.download_popup.show_download(
            download
        )

        self._position_download_popup()

    def _position_download_popup(
        self,
    ):

        if (
            not self.download_popup
            .isVisible()
        ):

            return

        self.download_popup.adjustSize()

        x = (
            self.width()
            - self.download_popup.width()
            - self.DOWNLOAD_POPUP_MARGIN
        )

        y = (
            self.navigation_bar.height()
            + 10
        )

        self.download_popup.move(
            max(
                x,
                0,
            ),
            max(
                y,
                0,
            ),
        )

        self.download_popup.raise_()

    def _show_all_downloads_from_popup(
        self,
    ):

        self.download_popup.hide_popup()

        self.show_downloads()

    # ======================================================
    # DOWNLOADS
    # ======================================================

    def show_downloads(
        self,
    ):

        self.navigation_bar.hide_suggestions()

        for index in range(
            self.tabs.count()
        ):

            widget = (
                self.tabs.widget(
                    index
                )
            )

            if isinstance(
                widget,
                DownloadPage,
            ):

                self.tabs.setCurrentIndex(
                    index
                )

                return

        page = DownloadPage(
            self.download_manager
        )

        index = (
            self.tabs.addTab(
                page,
                "Downloads",
            )
        )

        self.tabs.setCurrentIndex(
            index
        )

    # ======================================================
    # THEME
    # ======================================================

    def _change_theme(
        self,
        theme_name,
    ):

        app = (
            QApplication.instance()
        )

        if app:

            apply_theme(
                app,
                theme_name,
            )

        self.download_popup._apply_theme()

        self.navigation_bar.suggestions._apply_theme()

        for index in range(
            self.tabs.count()
        ):

            widget = (
                self.tabs.widget(
                    index
                )
            )

            if isinstance(
                widget,
                NewTabPage,
            ):

                widget.suggestions._apply_theme()

            if isinstance(
                widget,
                BookmarksPage,
            ):

                widget.reload()

    # ======================================================
    # CLOSE TAB
    # ======================================================

    def _close_current_tab(
        self,
    ):

        index = (
            self.tabs.currentIndex()
        )

        if index >= 0:

            self.tab_manager.close_tab(
                index
            )

    # ======================================================
    # TAB CHANGED
    # ======================================================

    def _tab_changed(
        self,
        index,
    ):

        self.navigation_bar.hide_suggestions()

        if index < 0:
            return

        widget = (
            self.tabs.widget(
                index
            )
        )

        self.loading_bar.hide()

        if isinstance(
            widget,
            NewTabPage,
        ):

            self.navigation_bar.set_url(
                ""
            )

            self.navigation_bar.set_bookmarked(
                False
            )

            self.setWindowTitle(
                "New Tab — Veyra"
            )

            return

        if isinstance(
            widget,
            HistoryPage,
        ):

            self.navigation_bar.set_url(
                ""
            )

            self.navigation_bar.set_bookmarked(
                False
            )

            self.setWindowTitle(
                "History — Veyra"
            )

            return

        if isinstance(
            widget,
            BookmarksPage,
        ):

            self.navigation_bar.set_url(
                ""
            )

            self.navigation_bar.set_bookmarked(
                False
            )

            self.setWindowTitle(
                "Bookmarks — Veyra"
            )

            return

        if isinstance(
            widget,
            DownloadPage,
        ):

            self.navigation_bar.set_url(
                ""
            )

            self.navigation_bar.set_bookmarked(
                False
            )

            self.setWindowTitle(
                "Downloads — Veyra"
            )

            return

        if isinstance(
            widget,
            SettingsPage,
        ):

            self.navigation_bar.set_url(
                ""
            )

            self.navigation_bar.set_bookmarked(
                False
            )

            self.setWindowTitle(
                "Settings — Veyra"
            )

            return

        browser = (
            self.current_browser()
        )

        if browser is None:
            return

        self.navigation_bar.set_url(
            browser.url()
            .toString()
        )

        self._update_bookmark_state()

        title = browser.title()

        if title:

            self.setWindowTitle(
                f"{title} — Veyra"
            )

        else:

            self.setWindowTitle(
                "Veyra"
            )

    # ======================================================
    # URL
    # ======================================================

    def _url_changed(
        self,
        url,
    ):

        browser = (
            self.current_browser()
        )

        if browser is None:
            return

        if (
            browser.url()
            != url
        ):

            return

        self.navigation_bar.set_url(
            url.toString()
        )

        self._update_bookmark_state()

    # ======================================================
    # LOADING
    # ======================================================

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

    # ======================================================
    # RESIZE
    # ======================================================

    def resizeEvent(
        self,
        event,
    ):

        super().resizeEvent(
            event
        )

        self._position_download_popup()

        self.navigation_bar.hide_suggestions()

    # ======================================================
    # CLOSE
    # ======================================================

    def closeEvent(
        self,
        event,
    ):

        self.navigation_bar.hide_suggestions()

        self.session_manager.mark_clean_shutdown()

        super().closeEvent(
            event
        )