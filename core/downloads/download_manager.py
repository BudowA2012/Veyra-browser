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
        super().__init__(parent)

        self.profile = profile
        self.downloads = []

        # ==================================================
        # DOWNLOAD DIRECTORY
        # ==================================================

        downloads_location = (
            QStandardPaths.writableLocation(
                QStandardPaths.StandardLocation.DownloadLocation
            )
        )

        if downloads_location:

            self.download_folder = (
                Path(downloads_location)
                / "Veyra"
            )

        else:

            self.download_folder = (
                Path.home()
                / "Downloads"
                / "Veyra"
            )

        self.download_folder.mkdir(
            parents=True,
            exist_ok=True,
        )

        # Default dla całego profilu.
        self.profile.setDownloadPath(
            str(self.download_folder)
        )

        # ==================================================
        # WEBENGINE DOWNLOAD SIGNAL
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

        safe_name = self._sanitize_filename(
            suggested_name
        )

        final_name = self._unique_filename(
            safe_name
        )

        # WAŻNE:
        # directory i filename MUSZĄ być ustawione
        # przed accept().
        download.setDownloadDirectory(
            str(self.download_folder)
        )

        download.setDownloadFileName(
            final_name
        )

        # Trzymamy obiekt przy życiu / mamy historię
        # obecnej sesji.
        self.downloads.append(
            download
        )

        # Stan końcowy
        download.stateChanged.connect(
            lambda state,
            item=download:
            self._state_changed(
                item,
                state,
            )
        )

        # Start właściwego pobierania
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
            QWebEngineDownloadRequest.DownloadState.DownloadCompleted,
            QWebEngineDownloadRequest.DownloadState.DownloadCancelled,
            QWebEngineDownloadRequest.DownloadState.DownloadInterrupted,
        )

        if state in finished_states:

            self.download_finished.emit(
                download
            )

    # ======================================================
    # FILE NAME
    # ======================================================

    def _sanitize_filename(
        self,
        filename,
    ):

        # Brak ścieżki z serwera typu:
        # ../../file.exe
        filename = Path(
            filename
        ).name

        # Znaki niedozwolone m.in. w Windows
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

    def _unique_filename(
        self,
        filename,
    ):

        path = (
            self.download_folder
            / filename
        )

        # Sprawdzamy też aktywne downloady,
        # nie tylko pliki już istniejące.
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
    # GETTERS
    # ======================================================

    def get_downloads(self):

        return list(
            self.downloads
        )