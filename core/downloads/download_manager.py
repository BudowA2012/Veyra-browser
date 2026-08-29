from pathlib import Path

from PySide6.QtCore import QObject, Signal
from PySide6.QtWebEngineCore import QWebEngineDownloadRequest


class DownloadManager(QObject):

    download_added = Signal(object)

    def __init__(self, profile):
        super().__init__()

        self.profile = profile
        self.downloads = []

        self.profile.downloadRequested.connect(
            self._handle_download
        )

    def _handle_download(
        self,
        download: QWebEngineDownloadRequest,
    ):

        downloads_folder = (
            Path.home()
            / "Downloads"
            / "Veyra"
        )

        downloads_folder.mkdir(
            parents=True,
            exist_ok=True,
        )

        path = (
            downloads_folder
            / download.downloadFileName()
        )

        download.setDownloadDirectory(
            str(downloads_folder)
        )

        download.setDownloadFileName(
            path.name
        )

        download.accept()

        self.downloads.append(download)

        self.download_added.emit(download)