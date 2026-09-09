from PySide6.QtCore import (
    QObject,
    QSettings,
    QUrl,
    Signal,
)

from PySide6.QtWebEngineCore import (
    QWebEnginePage,
    QWebEngineProfile,
)

from PySide6.QtWebEngineWidgets import (
    QWebEngineView,
)


class BrowserManager(QObject):

    url_changed = Signal(QUrl)
    title_changed = Signal(str)
    loading_changed = Signal(bool)
    load_progress = Signal(int)

    SEARCH_ENGINES = {
        "Google": (
            "https://www.google.com/search?q={query}"
        ),
        "DuckDuckGo": (
            "https://duckduckgo.com/?q={query}"
        ),
        "Bing": (
            "https://www.bing.com/search?q={query}"
        ),
    }

    DEFAULT_SEARCH_ENGINE = "Google"

    def __init__(
        self,
        parent=None,
    ):
        super().__init__(
            parent
        )

        self.settings = QSettings(
            "Veyra",
            "VeyraBrowser",
        )

        # ==================================================
        # PROFILE
        # ==================================================

        self.profile = QWebEngineProfile(
            "Veyra",
            self,
        )

        self._apply_cookie_policy()

        self.profile.setHttpCacheType(
            QWebEngineProfile
            .HttpCacheType
            .DiskHttpCache
        )

    # ======================================================
    # COOKIE POLICY
    # ======================================================

    def _apply_cookie_policy(
        self,
    ):

        persistent = self.settings.value(
            "privacy/persistent_cookies",
            True,
            type=bool,
        )

        if persistent:

            policy = (
                QWebEngineProfile
                .PersistentCookiesPolicy
                .ForcePersistentCookies
            )

        else:

            policy = (
                QWebEngineProfile
                .PersistentCookiesPolicy
                .NoPersistentCookies
            )

        self.profile.setPersistentCookiesPolicy(
            policy
        )

    def refresh_cookie_policy(
        self,
    ):

        self._apply_cookie_policy()

    # ======================================================
    # CREATE BROWSER
    # ======================================================

    def create_browser(
        self,
    ):

        page = QWebEnginePage(
            self.profile,
            self,
        )

        browser = QWebEngineView()

        browser.setPage(
            page
        )

        # ==================================================
        # DEFAULT ZOOM
        # ==================================================

        zoom = self.settings.value(
            "browser/default_zoom",
            100,
            type=int,
        )

        zoom = max(
            50,
            min(
                zoom,
                300,
            ),
        )

        browser.setZoomFactor(
            zoom / 100.0
        )

        browser.urlChanged.connect(
            self.url_changed.emit
        )

        browser.titleChanged.connect(
            self.title_changed.emit
        )

        browser.loadStarted.connect(
            lambda:
            self.loading_changed.emit(
                True
            )
        )

        browser.loadProgress.connect(
            self.load_progress.emit
        )

        browser.loadFinished.connect(
            lambda _success:
            self.loading_changed.emit(
                False
            )
        )

        return browser

    # ======================================================
    # CLEAR DATA
    # ======================================================

    def clear_browsing_data(
        self,
    ):

        self.profile.cookieStore().deleteAllCookies()

        self.profile.clearHttpCache()

    # ======================================================
    # LOAD URL
    # ======================================================

    def load_url(
        self,
        browser,
        text: str,
    ):

        if not text:
            return

        text = text.strip()

        if not text:
            return

        if self._has_scheme(
            text
        ):

            final_url = text

        elif self._looks_like_url(
            text
        ):

            final_url = (
                "https://"
                + text
            )

        else:

            final_url = (
                self.build_search_url(
                    text
                )
            )

        browser.setUrl(
            QUrl(
                final_url
            )
        )

    # ======================================================
    # SEARCH URL
    # ======================================================

    def build_search_url(
        self,
        query: str,
    ):

        engine = (
            self.get_search_engine()
        )

        template = (
            self.SEARCH_ENGINES.get(
                engine,
                self.SEARCH_ENGINES[
                    self.DEFAULT_SEARCH_ENGINE
                ],
            )
        )

        encoded_query = (
            QUrl
            .toPercentEncoding(
                query
            )
            .data()
            .decode(
                "utf-8"
            )
        )

        return template.format(
            query=encoded_query
        )

    # ======================================================
    # SEARCH ENGINE
    # ======================================================

    def get_search_engine(
        self,
    ):

        engine = self.settings.value(
            "browser/search_engine",
            self.DEFAULT_SEARCH_ENGINE,
        )

        if (
            engine
            not in self.SEARCH_ENGINES
        ):

            return (
                self.DEFAULT_SEARCH_ENGINE
            )

        return engine

    # ======================================================
    # URL DETECTION
    # ======================================================

    def _has_scheme(
        self,
        text: str,
    ):

        lower = text.lower()

        known_schemes = (
            "http://",
            "https://",
            "file://",
            "ftp://",
            "about:",
            "data:",
            "mailto:",
        )

        return lower.startswith(
            known_schemes
        )

    def _looks_like_url(
        self,
        text: str,
    ):

        if " " in text:

            return False

        if text.startswith(
            "localhost"
        ):

            return True

        if ":" in text:

            return True

        if "." in text:

            return True

        return False