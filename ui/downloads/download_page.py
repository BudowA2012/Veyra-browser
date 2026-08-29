from PySide6.QtWidgets import (
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from ui.downloads.download_item import DownloadItem


class DownloadPage(QWidget):

    def __init__(
        self,
        manager,
        parent=None,
    ):
        super().__init__(parent)

        self.manager = manager

        layout = QVBoxLayout(self)

        title = QLabel("Downloads")

        title.setObjectName("DownloadsTitle")

        layout.addWidget(title)

        self.scroll = QScrollArea()

        self.scroll.setWidgetResizable(True)

        self.container = QWidget()

        self.items = QVBoxLayout(
            self.container
        )

        self.items.addStretch()

        self.scroll.setWidget(
            self.container
        )

        layout.addWidget(
            self.scroll
        )

        self.manager.download_added.connect(
            self._add_download
        )

    def _add_download(
        self,
        download,
    ):

        item = DownloadItem(download)

        self.items.insertWidget(
            self.items.count() - 1,
            item,
        )