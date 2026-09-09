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

    # ======================================================
    # SEARCH ENGINES
    # ======================================================

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

        # ==================================================
        # SETTINGS
        # ==================================================

        self.settings = QSettings(
            "Veyra",
            "VeyraBrowser",
        )

        # ==================================================
        # WEB ENGINE PROFILE
        # ==================================================

        self.profile = QWebEngineProfile(
            "Veyra",
            self,
        )

        self.profile.setPersistentCookiesPolicy(
            QWebEngineProfile
            .PersistentCookiesPolicy
            .ForcePersistentCookies
        )

        self.profile.setHttpCacheType(
            QWebEngineProfile
            .HttpCacheType
            .DiskHttpCache
        )

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
        # URL
        # ==================================================

        browser.urlChanged.connect(
            self.url_changed.emit
        )

        # ==================================================
        # TITLE
        # ==================================================

        browser.titleChanged.connect(
            self.title_changed.emit
        )

        # ==================================================
        # LOAD START
        # ==================================================

        browser.loadStarted.connect(
            lambda:
            self.loading_changed.emit(
                True
            )
        )

        # ==================================================
        # LOAD PROGRESS
        # ==================================================

        browser.loadProgress.connect(
            self.load_progress.emit
        )

        # ==================================================
        # LOAD END
        # ==================================================

        browser.loadFinished.connect(
            lambda _success:
            self.loading_changed.emit(
                False
            )
        )

        return browser

    # ======================================================
    # LOAD URL / SEARCH
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

        # ==================================================
        # ALREADY HAS SCHEME
        # ==================================================

        if self._has_scheme(
            text
        ):

            final_url = text

        # ==================================================
        # LOOKS LIKE WEBSITE
        # ==================================================

        elif self._looks_like_url(
            text
        ):

            final_url = (
                "https://"
                + text
            )

        # ==================================================
        # SEARCH QUERY
        # ==================================================

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
    # BUILD SEARCH URL
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

        if engine not in self.SEARCH_ENGINES:

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

        # Tekst ze spacjami traktujemy jako wyszukiwanie.
        if " " in text:

            return False

        # localhost
        if text.startswith(
            "localhost"
        ):

            return True

        # IP / port
        if ":" in text:

            return True

        # Normalna domena
        if "." in text:

            return True

        return False