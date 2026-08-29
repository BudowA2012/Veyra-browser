from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QProgressBar,
)


class DownloadItem(QFrame):

    def __init__(self, download, parent=None):
        super().__init__(parent)

        self.download = download

        self.setObjectName("DownloadItem")

        layout = QHBoxLayout(self)

        text = QVBoxLayout()

        self.name = QLabel(
            download.downloadFileName()
        )

        self.status = QLabel(
            "Downloading..."
        )

        text.addWidget(self.name)
        text.addWidget(self.status)

        self.progress = QProgressBar()

        self.cancel = QPushButton("Cancel")

        self.cancel.clicked.connect(
            self._cancel
        )

        right = QVBoxLayout()

        right.addWidget(self.progress)
        right.addWidget(self.cancel)

        layout.addLayout(text, 1)
        layout.addLayout(right)

        download.receivedBytesChanged.connect(
            self._update
        )

        download.stateChanged.connect(
            self._state_changed
        )

    def _update(self):

        total = self.download.totalBytes()

        if total > 0:

            value = int(
                self.download.receivedBytes()
                / total
                * 100
            )

            self.progress.setValue(value)

    def _state_changed(self):

        state = self.download.state()

        if state == self.download.DownloadCompleted:
            self.status.setText("Completed")
            self.cancel.setEnabled(False)

        elif state == self.download.DownloadCancelled:
            self.status.setText("Cancelled")

        elif state == self.download.DownloadInterrupted:
            self.status.setText("Interrupted")

    def _cancel(self):

        self.download.cancel()