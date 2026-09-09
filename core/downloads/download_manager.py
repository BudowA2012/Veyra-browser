from pathlib import Path
import re

from PySide6.QtCore import (
    QObject,
    QSettings,
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

        self.settings = QSettings(
            "Veyra",
            "VeyraBrowser",
        )

        self.download_folder = (
            self._load_download_folder()
        )

        self.download_folder.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.profile.setDownloadPath(
            str(
                self.download_folder
            )
        )

        self.profile.downloadRequested.connect(
            self._handle_download
        )

    # ======================================================
    # DEFAULT FOLDER
    # ======================================================

    def _default_download_folder(
        self,
    ):

        downloads_location = (
            QStandardPaths.writableLocation(
                QStandardPaths.StandardLocation.DownloadLocation
            )
        )

        if downloads_location:

            return Path(
                downloads_location
            )

        return (
            Path.home()
            / "Downloads"
        )

    # ======================================================
    # LOAD FOLDER
    # ======================================================

    def _load_download_folder(
        self,
    ):

        saved = self.settings.value(
            "downloads/location",
            "",
        )

        if saved:

            return Path(
                saved
            )

        return (
            self._default_download_folder()
        )

    # ======================================================
    # SET FOLDER
    # ======================================================

    def set_download_folder(
        self,
        folder,
    ):

        if not folder:
            return

        path = Path(
            folder
        )

        try:

            path.mkdir(
                parents=True,
                exist_ok=True,
            )

        except OSError:

            return

        self.download_folder = path

        self.settings.setValue(
            "downloads/location",
            str(path),
        )

        self.profile.setDownloadPath(
            str(path)
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
            and filename
            not in active_names
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
                and candidate
                not in active_names
            ):

                return candidate

            number += 1

    # ======================================================
    # DOWNLOADS
    # ======================================================

    def get_downloads(
        self,
    ):

        return list(
            self.downloads
        )