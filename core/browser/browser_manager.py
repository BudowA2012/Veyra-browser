from PySide6.QtCore import QObject, QUrl, Signal
from PySide6.QtWebEngineCore import (
    QWebEnginePage,
    QWebEngineProfile,
)
from PySide6.QtWebEngineWidgets import QWebEngineView


class BrowserManager(QObject):

    url_changed = Signal(QUrl)
    title_changed = Signal(str)

    loading_changed = Signal(bool)
    load_progress = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Jeden profil dla całej Veyry
        self.profile = QWebEngineProfile(
            "Veyra",
            self,
        )

        self.profile.setPersistentCookiesPolicy(
            QWebEngineProfile.ForcePersistentCookies
        )

        self.profile.setHttpCacheType(
            QWebEngineProfile.DiskHttpCache
        )

    # ==================================================
    # CREATE BROWSER
    # ==================================================

    def create_browser(self):

        page = QWebEnginePage(
            self.profile,
            self,
        )

        browser = QWebEngineView()

        browser.setPage(page)

        # URL
        browser.urlChanged.connect(
            self.url_changed.emit
        )

        # TITLE
        browser.titleChanged.connect(
            self.title_changed.emit
        )

        # LOAD START
        browser.loadStarted.connect(
            lambda:
            self.loading_changed.emit(True)
        )

        # LOAD PROGRESS
        browser.loadProgress.connect(
            self.load_progress.emit
        )

        # LOAD END
        browser.loadFinished.connect(
            lambda _success:
            self.loading_changed.emit(False)
        )

        return browser

    # ==================================================
    # LOAD URL / SEARCH
    # ==================================================

    def load_url(
        self,
        browser,
        url: str,
    ):

        if not url:
            return

        url = url.strip()

        if "://" not in url:

            # wygląda jak domena
            if "." in url and " " not in url:

                url = (
                    "https://"
                    + url
                )

            # wyszukiwanie Google
            else:

                encoded = (
                    QUrl
                    .toPercentEncoding(url)
                    .data()
                    .decode()
                )

                url = (
                    "https://www.google.com/search?q="
                    + encoded
                )

        browser.setUrl(
            QUrl(url)
        )