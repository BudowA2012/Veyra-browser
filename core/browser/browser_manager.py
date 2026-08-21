from PySide6.QtCore import QObject, QUrl, Signal
from PySide6.QtWebEngineWidgets import QWebEngineView


class BrowserManager(QObject):
    """Creates and manages browser views."""

    page_title_changed = Signal(str)
    url_changed = Signal(QUrl)
    loading_changed = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)

    def create_browser(self, parent=None) -> QWebEngineView:
        browser = QWebEngineView(parent)

        browser.titleChanged.connect(self.page_title_changed.emit)
        browser.urlChanged.connect(self.url_changed.emit)

        browser.loadStarted.connect(
            lambda: self.loading_changed.emit(True)
        )

        browser.loadFinished.connect(
            lambda _: self.loading_changed.emit(False)
        )

        return browser