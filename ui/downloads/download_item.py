from pathlib import Path

from PySide6.QtCore import (
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QDesktopServices,
)
from PySide6.QtWebEngineCore import (
    QWebEngineDownloadRequest,
)
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
)


class DownloadItem(QFrame):

    def __init__(
        self,
        download,
        parent=None,
    ):
        super().__init__(
            parent
        )

        self.download = download

        self.setObjectName(
            "DownloadItem"
        )

        self._build_ui()
        self._connect_signals()

        self._update_all()

    # ======================================================
    # BUILD
    # ======================================================

    def _build_ui(self):

        root = QVBoxLayout(
            self
        )

        root.setContentsMargins(
            18,
            16,
            18,
            16,
        )

        root.setSpacing(
            10
        )

        # ==================================================
        # TOP
        # ==================================================

        top = QHBoxLayout()

        top.setSpacing(
            12
        )

        info = QVBoxLayout()

        info.setSpacing(
            3
        )

        self.name_label = QLabel()

        self.name_label.setObjectName(
            "DownloadFileName"
        )

        self.name_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        self.status_label = QLabel()

        self.status_label.setObjectName(
            "DownloadStatus"
        )

        info.addWidget(
            self.name_label
        )

        info.addWidget(
            self.status_label
        )

        top.addLayout(
            info,
            1,
        )

        # ==================================================
        # ACTIONS
        # ==================================================

        self.pause_button = QPushButton(
            "Pause"
        )

        self.pause_button.setObjectName(
            "DownloadActionButton"
        )

        self.cancel_button = QPushButton(
            "Cancel"
        )

        self.cancel_button.setObjectName(
            "DownloadActionButton"
        )

        self.open_button = QPushButton(
            "Open"
        )

        self.open_button.setObjectName(
            "DownloadPrimaryButton"
        )

        self.folder_button = QPushButton(
            "Folder"
        )

        self.folder_button.setObjectName(
            "DownloadActionButton"
        )

        self.pause_button.clicked.connect(
            self._toggle_pause
        )

        self.cancel_button.clicked.connect(
            self.download.cancel
        )

        self.open_button.clicked.connect(
            self._open_file
        )

        self.folder_button.clicked.connect(
            self._open_folder
        )

        top.addWidget(
            self.pause_button
        )

        top.addWidget(
            self.cancel_button
        )

        top.addWidget(
            self.open_button
        )

        top.addWidget(
            self.folder_button
        )

        root.addLayout(
            top
        )

        # ==================================================
        # PROGRESS
        # ==================================================

        self.progress = QProgressBar()

        self.progress.setObjectName(
            "DownloadProgress"
        )

        self.progress.setTextVisible(
            False
        )

        self.progress.setFixedHeight(
            5
        )

        root.addWidget(
            self.progress
        )

    # ======================================================
    # SIGNALS
    # ======================================================

    def _connect_signals(self):

        self.download.receivedBytesChanged.connect(
            self._update_progress
        )

        self.download.totalBytesChanged.connect(
            self._update_progress
        )

        self.download.stateChanged.connect(
            self._state_changed
        )

        self.download.isPausedChanged.connect(
            self._paused_changed
        )

        self.download.interruptReasonChanged.connect(
            self._update_status
        )

    # ======================================================
    # UPDATE ALL
    # ======================================================

    def _update_all(self):

        self.name_label.setText(
            self.download.downloadFileName()
        )

        self._update_progress()
        self._update_status()
        self._update_buttons()

    # ======================================================
    # PROGRESS
    # ======================================================

    def _update_progress(self):

        received = max(
            0,
            self.download.receivedBytes(),
        )

        total = self.download.totalBytes()

        if total <= 0:

            # Nie znamy całkowitego rozmiaru.
            self.progress.setRange(
                0,
                0,
            )

        else:

            self.progress.setRange(
                0,
                100,
            )

            percentage = int(
                received
                / total
                * 100
            )

            self.progress.setValue(
                min(
                    percentage,
                    100,
                )
            )

        self._update_status()

    # ======================================================
    # STATUS
    # ======================================================

    def _update_status(self):

        state = self.download.state()

        received = self._format_bytes(
            max(
                0,
                self.download.receivedBytes(),
            )
        )

        total_bytes = (
            self.download.totalBytes()
        )

        total = (
            self._format_bytes(total_bytes)
            if total_bytes > 0
            else "Unknown size"
        )

        if (
            state
            == QWebEngineDownloadRequest.DownloadState.DownloadRequested
        ):

            text = "Preparing download..."

        elif (
            state
            == QWebEngineDownloadRequest.DownloadState.DownloadInProgress
        ):

            if self.download.isPaused():

                text = (
                    f"Paused • {received} / {total}"
                )

            else:

                text = (
                    f"Downloading • {received} / {total}"
                )

        elif (
            state
            == QWebEngineDownloadRequest.DownloadState.DownloadCompleted
        ):

            text = (
                f"Completed • {received}"
            )

        elif (
            state
            == QWebEngineDownloadRequest.DownloadState.DownloadCancelled
        ):

            text = "Cancelled"

        elif (
            state
            == QWebEngineDownloadRequest.DownloadState.DownloadInterrupted
        ):

            reason = (
                self.download.interruptReasonString()
            )

            if reason:

                text = (
                    f"Failed • {reason}"
                )

            else:

                text = "Download failed"

        else:

            text = "Download"

        self.status_label.setText(
            text
        )

    # ======================================================
    # STATE
    # ======================================================

    def _state_changed(
        self,
        _state,
    ):

        self._update_progress()
        self._update_status()
        self._update_buttons()

    def _paused_changed(self):

        self._update_status()
        self._update_buttons()

    # ======================================================
    # BUTTONS
    # ======================================================

    def _update_buttons(self):

        state = self.download.state()

        in_progress = (
            state
            == QWebEngineDownloadRequest.DownloadState.DownloadInProgress
        )

        completed = (
            state
            == QWebEngineDownloadRequest.DownloadState.DownloadCompleted
        )

        self.pause_button.setVisible(
            in_progress
        )

        self.cancel_button.setVisible(
            in_progress
        )

        self.open_button.setVisible(
            completed
        )

        # Folder zawsze może być użyteczny.
        self.folder_button.setVisible(
            True
        )

        if self.download.isPaused():

            self.pause_button.setText(
                "Resume"
            )

        else:

            self.pause_button.setText(
                "Pause"
            )

    def _toggle_pause(self):

        if self.download.isPaused():

            self.download.resume()

        else:

            self.download.pause()

    # ======================================================
    # OPEN
    # ======================================================

    def _file_path(self):

        return (
            Path(
                self.download.downloadDirectory()
            )
            / self.download.downloadFileName()
        )

    def _open_file(self):

        path = self._file_path()

        if not path.exists():
            return

        QDesktopServices.openUrl(
            QUrl.fromLocalFile(
                str(path)
            )
        )

    def _open_folder(self):

        directory = Path(
            self.download.downloadDirectory()
        )

        directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        QDesktopServices.openUrl(
            QUrl.fromLocalFile(
                str(directory)
            )
        )

    # ======================================================
    # SIZE
    # ======================================================

    def _format_bytes(
        self,
        size,
    ):

        size = float(
            size
        )

        units = (
            "B",
            "KB",
            "MB",
            "GB",
            "TB",
        )

        for unit in units:

            if size < 1024:

                if unit == "B":

                    return (
                        f"{int(size)} {unit}"
                    )

                return (
                    f"{size:.1f} {unit}"
                )

            size /= 1024

        return (
            f"{size:.1f} PB"
        )