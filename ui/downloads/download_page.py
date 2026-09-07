from PySide6.QtCore import (
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QDesktopServices,
)
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from ui.downloads.download_item import (
    DownloadItem,
)


class DownloadPage(QWidget):

    def __init__(
        self,
        manager,
        parent=None,
    ):
        super().__init__(
            parent
        )

        self.manager = manager

        self.setObjectName(
            "DownloadPage"
        )

        self.download_widgets = []

        self._build_ui()

        # Ważne:
        # gdy otwieramy Downloads później,
        # pokazujemy też wcześniejsze downloady.
        self._load_existing_downloads()

        self.manager.download_added.connect(
            self._add_download
        )

    # ======================================================
    # BUILD
    # ======================================================

    def _build_ui(self):

        root = QVBoxLayout(
            self
        )

        root.setContentsMargins(
            48,
            38,
            48,
            38,
        )

        root.setSpacing(
            20
        )

        # ==================================================
        # HEADER
        # ==================================================

        header = QHBoxLayout()

        header_text = QVBoxLayout()

        header_text.setSpacing(
            3
        )

        title = QLabel(
            "Downloads"
        )

        title.setObjectName(
            "DownloadsTitle"
        )

        subtitle = QLabel(
            "Files downloaded with Veyra"
        )

        subtitle.setObjectName(
            "DownloadsSubtitle"
        )

        header_text.addWidget(
            title
        )

        header_text.addWidget(
            subtitle
        )

        header.addLayout(
            header_text
        )

        header.addStretch()

        folder_button = QPushButton(
            "Open downloads folder"
        )

        folder_button.setObjectName(
            "DownloadsFolderButton"
        )

        folder_button.clicked.connect(
            self._open_download_folder
        )

        header.addWidget(
            folder_button
        )

        root.addLayout(
            header
        )

        # ==================================================
        # SCROLL
        # ==================================================

        self.scroll = QScrollArea()

        self.scroll.setWidgetResizable(
            True
        )

        self.scroll.setFrameShape(
            QFrame.Shape.NoFrame
        )

        self.container = QWidget()

        self.container.setObjectName(
            "DownloadsContainer"
        )

        self.items_layout = QVBoxLayout(
            self.container
        )

        self.items_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        self.items_layout.setSpacing(
            10
        )

        self.empty_label = QLabel(
            "No downloads yet."
        )

        self.empty_label.setObjectName(
            "DownloadsEmpty"
        )

        self.empty_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.items_layout.addWidget(
            self.empty_label
        )

        self.items_layout.addStretch()

        self.scroll.setWidget(
            self.container
        )

        root.addWidget(
            self.scroll,
            1,
        )

    # ======================================================
    # EXISTING
    # ======================================================

    def _load_existing_downloads(self):

        for download in (
            self.manager.get_downloads()
        ):

            self._add_download(
                download
            )

    # ======================================================
    # ADD
    # ======================================================

    def _add_download(
        self,
        download,
    ):

        # Ta sama instancja nie może być dwa razy.
        for item in self.download_widgets:

            if (
                item.download
                is download
            ):
                return

        self.empty_label.hide()

        item = DownloadItem(
            download
        )

        self.download_widgets.append(
            item
        )

        # Najnowszy download u góry.
        self.items_layout.insertWidget(
            0,
            item,
        )

    # ======================================================
    # OPEN FOLDER
    # ======================================================

    def _open_download_folder(self):

        QDesktopServices.openUrl(
            QUrl.fromLocalFile(
                str(
                    self.manager.download_folder
                )
            )
        )