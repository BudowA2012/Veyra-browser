from pathlib import Path
import re

from PySide6.QtCore import (
    QObject,
    QStandardPaths,
    Signal,
)
from PySide6.QtWebEngineCore import (
    QWebEngineDownloadRequest,
)


class DownloadManager(QObject):

    download_added = Signal(object)
    download_finished = Signal(object)

    def __init__(
        self,
        profile,
        parent=None,
    ):
        super().__init__(
            parent
        )

        self.profile = profile
        self.downloads = []

        # ==================================================
        # SYSTEM DOWNLOAD DIRECTORY
        # ==================================================

        downloads_location = (
            QStandardPaths.writableLocation(
                QStandardPaths.StandardLocation.DownloadLocation
            )
        )

        if downloads_location:

            self.download_folder = Path(
                downloads_location
            )

        else:

            self.download_folder = (
                Path.home()
                / "Downloads"
            )

        self.download_folder.mkdir(
            parents=True,
            exist_ok=True,
        )

        # Wszystkie downloady Veyry trafiają bezpośrednio
        # do systemowego folderu Downloads.
        self.profile.setDownloadPath(
            str(
                self.download_folder
            )
        )

        # ==================================================
        # DOWNLOAD SIGNAL
        # ==================================================

        self.profile.downloadRequested.connect(
            self._handle_download
        )

    # ======================================================
    # DOWNLOAD REQUEST
    # ======================================================

    def _handle_download(
        self,
        download: QWebEngineDownloadRequest,
    ):

        suggested_name = (
            download.suggestedFileName()
            or download.downloadFileName()
            or "download"
        )

        safe_name = (
            self._sanitize_filename(
                suggested_name
            )
        )

        final_name = (
            self._unique_filename(
                safe_name
            )
        )

        download.setDownloadDirectory(
            str(
                self.download_folder
            )
        )

        download.setDownloadFileName(
            final_name
        )

        self.downloads.append(
            download
        )

        download.stateChanged.connect(
            lambda state,
            item=download:
            self._state_changed(
                item,
                state,
            )
        )

        download.accept()

        self.download_added.emit(
            download
        )

    # ======================================================
    # STATE
    # ======================================================

    def _state_changed(
        self,
        download,
        state,
    ):

        finished_states = (
            QWebEngineDownloadRequest
            .DownloadState
            .DownloadCompleted,

            QWebEngineDownloadRequest
            .DownloadState
            .DownloadCancelled,

            QWebEngineDownloadRequest
            .DownloadState
            .DownloadInterrupted,
        )

        if state in finished_states:

            self.download_finished.emit(
                download
            )

    # ======================================================
    # SAFE FILENAME
    # ======================================================

    def _sanitize_filename(
        self,
        filename,
    ):

        filename = Path(
            filename
        ).name

        filename = re.sub(
            r'[<>:"/\\|?*]',
            "_",
            filename,
        )

        filename = filename.strip(
            " ."
        )

        if not filename:

            filename = "download"

        return filename

    # ======================================================
    # UNIQUE FILENAME
    # ======================================================

    def _unique_filename(
        self,
        filename,
    ):

        path = (
            self.download_folder
            / filename
        )

        active_names = {
            item.downloadFileName()
            for item in self.downloads
            if not item.isFinished()
        }

        if (
            not path.exists()
            and filename not in active_names
        ):

            return filename

        file_path = Path(
            filename
        )

        stem = file_path.stem
        suffix = file_path.suffix

        number = 1

        while True:

            candidate = (
                f"{stem} ({number}){suffix}"
            )

            candidate_path = (
                self.download_folder
                / candidate
            )

            if (
                not candidate_path.exists()
                and candidate not in active_names
            ):

                return candidate

            number += 1

    # ======================================================
    # GET DOWNLOADS
    # ======================================================

    def get_downloads(
        self,
    ):

        return list(
            self.downloads
        )