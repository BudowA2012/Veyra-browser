from pathlib import Path

from PySide6.QtCore import (
    QEasingCurve,
    QPropertyAnimation,
    QTimer,
    Qt,
    Signal,
)
from PySide6.QtGui import (
    QDesktopServices,
)
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QToolButton,
    QVBoxLayout,
)

from ui.components.icon_factory import (
    create_icon,
)
from ui.styles.style_manager import (
    get_current_theme,
)


class DownloadPopup(QFrame):

    show_all_requested = Signal()

    WIDTH = 340

    THEME_COLORS = {
        "midnight": {
            "background": "#151922",
            "border": "#2a3040",
            "title": "#f4f5f8",
            "text": "#aeb3c1",
            "muted": "#7f8594",
            "hover": "#232938",
            "accent": "#7c5cff",
        },
        "graphite": {
            "background": "#202124",
            "border": "#34363b",
            "title": "#f1f1f1",
            "text": "#b8bbc2",
            "muted": "#858990",
            "hover": "#2c2e33",
            "accent": "#8c8f98",
        },
        "aurora": {
            "background": "#181421",
            "border": "#332944",
            "title": "#f5f0ff",
            "text": "#bbb1cc",
            "muted": "#887d99",
            "hover": "#282034",
            "accent": "#9c6cff",
        },
        "light": {
            "background": "#ffffff",
            "border": "#d9dbe2",
            "title": "#202124",
            "text": "#555962",
            "muted": "#858993",
            "hover": "#f0f1f5",
            "accent": "#7057e8",
        },
    }

    def __init__(
        self,
        parent=None,
    ):
        super().__init__(
            parent
        )

        self.download = None

        self.setObjectName(
            "DownloadPopup"
        )

        self.setFixedWidth(
            self.WIDTH
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_StyledBackground,
            True,
        )

        self._build_ui()
        self._apply_theme()

        self.hide()

        self.hide_timer = QTimer(
            self
        )

        self.hide_timer.setSingleShot(
            True
        )

        self.hide_timer.timeout.connect(
            self.hide_popup
        )

        self.opacity_animation = (
            QPropertyAnimation(
                self,
                b"windowOpacity",
                self,
            )
        )

        self.opacity_animation.setDuration(
            160
        )

        self.opacity_animation.setEasingCurve(
            QEasingCurve.Type.OutCubic
        )

    # ======================================================
    # BUILD UI
    # ======================================================

    def _build_ui(
        self,
    ):

        root = QVBoxLayout(
            self
        )

        root.setContentsMargins(
            16,
            14,
            16,
            14,
        )

        root.setSpacing(
            9
        )

        # ==================================================
        # HEADER
        # ==================================================

        header = QHBoxLayout()

        header.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        header.setSpacing(
            8
        )

        self.icon_label = QLabel()

        self.icon_label.setFixedSize(
            22,
            22,
        )

        self.icon_label.setPixmap(
            create_icon(
                "download",
                18,
            ).pixmap(
                18,
                18,
            )
        )

        self.title_label = QLabel(
            "Downloading"
        )

        self.title_label.setObjectName(
            "DownloadPopupTitle"
        )

        self.title_label.setStyleSheet(
            "font-size: 14px; font-weight: 600;"
        )

        header.addWidget(
            self.icon_label
        )

        header.addWidget(
            self.title_label
        )

        header.addStretch(
            1
        )

        self.close_button = QToolButton()

        self.close_button.setIcon(
            create_icon(
                "close",
                15,
            )
        )

        self.close_button.setFixedSize(
            26,
            26,
        )

        self.close_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.close_button.clicked.connect(
            self.hide_popup
        )

        header.addWidget(
            self.close_button
        )

        root.addLayout(
            header
        )

        # ==================================================
        # FILE NAME
        # ==================================================

        self.file_label = QLabel(
            "File"
        )

        self.file_label.setObjectName(
            "DownloadPopupFile"
        )

        self.file_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        root.addWidget(
            self.file_label
        )

        # ==================================================
        # PROGRESS
        # ==================================================

        self.progress = QProgressBar()

        self.progress.setRange(
            0,
            100
        )

        self.progress.setValue(
            0
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

        # ==================================================
        # STATUS
        # ==================================================

        status_row = QHBoxLayout()

        status_row.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        self.status_label = QLabel(
            "Starting..."
        )

        self.status_label.setObjectName(
            "DownloadPopupStatus"
        )

        self.percent_label = QLabel(
            "0%"
        )

        self.percent_label.setObjectName(
            "DownloadPopupPercent"
        )

        status_row.addWidget(
            self.status_label
        )

        status_row.addStretch(
            1
        )

        status_row.addWidget(
            self.percent_label
        )

        root.addLayout(
            status_row
        )

        # ==================================================
        # ACTIONS
        # ==================================================

        action_row = QHBoxLayout()

        action_row.setContentsMargins(
            0,
            2,
            0,
            0,
        )

        action_row.setSpacing(
            7
        )

        self.open_button = QPushButton(
            "Open"
        )

        self.open_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.open_button.hide()

        self.open_button.clicked.connect(
            self._open_file
        )

        self.show_all_button = QPushButton(
            "View all downloads"
        )

        self.show_all_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.show_all_button.clicked.connect(
            self.show_all_requested.emit
        )

        action_row.addStretch(
            1
        )

        action_row.addWidget(
            self.open_button
        )

        action_row.addWidget(
            self.show_all_button
        )

        root.addLayout(
            action_row
        )

    # ======================================================
    # THEME
    # ======================================================

    def _apply_theme(
        self,
    ):

        theme = get_current_theme()

        colors = self.THEME_COLORS.get(
            theme,
            self.THEME_COLORS["midnight"],
        )

        self.setStyleSheet(
            f"""
            QFrame#DownloadPopup {{
                background: {colors["background"]};
                border: 1px solid {colors["border"]};
                border-radius: 14px;
            }}

            QLabel {{
                background: transparent;
                border: none;
            }}

            QLabel#DownloadPopupTitle {{
                color: {colors["title"]};
            }}

            QLabel#DownloadPopupFile {{
                color: {colors["title"]};
                font-size: 13px;
                font-weight: 500;
            }}

            QLabel#DownloadPopupStatus,
            QLabel#DownloadPopupPercent {{
                color: {colors["muted"]};
                font-size: 12px;
            }}

            QProgressBar {{
                background: {colors["hover"]};
                border: none;
                border-radius: 2px;
            }}

            QProgressBar::chunk {{
                background: {colors["accent"]};
                border: none;
                border-radius: 2px;
            }}

            QToolButton {{
                background: transparent;
                border: none;
                border-radius: 7px;
            }}

            QToolButton:hover {{
                background: {colors["hover"]};
            }}

            QPushButton {{
                background: transparent;
                color: {colors["text"]};

                border: none;
                border-radius: 8px;

                padding: 6px 9px;

                font-size: 12px;
            }}

            QPushButton:hover {{
                background: {colors["hover"]};
                color: {colors["title"]};
            }}
            """
        )

    # ======================================================
    # SHOW DOWNLOAD
    # ======================================================

    def show_download(
        self,
        download,
    ):

        self.download = download

        self.hide_timer.stop()

        self._apply_theme()

        file_name = (
            download.downloadFileName()
        )

        if not file_name:

            file_name = "Download"

        self.file_label.setText(
            file_name
        )

        self.file_label.setToolTip(
            file_name
        )

        self.title_label.setText(
            "Downloading"
        )

        self.status_label.setText(
            "Starting..."
        )

        self.percent_label.setText(
            "0%"
        )

        self.progress.setValue(
            0
        )

        self.open_button.hide()

        download.receivedBytesChanged.connect(
            self._update_progress
        )

        download.totalBytesChanged.connect(
            self._update_progress
        )

        download.stateChanged.connect(
            self._state_changed
        )

        self._update_progress()

        self.adjustSize()

        self.show()
        self.raise_()

        self.setWindowOpacity(
            0.0
        )

        self.opacity_animation.stop()

        self.opacity_animation.setStartValue(
            0.0
        )

        self.opacity_animation.setEndValue(
            1.0
        )

        self.opacity_animation.start()

    # ======================================================
    # PROGRESS
    # ======================================================

    def _update_progress(
        self,
        *_,
    ):

        if self.download is None:
            return

        received = (
            self.download.receivedBytes()
        )

        total = (
            self.download.totalBytes()
        )

        if total > 0:

            percent = int(
                received
                / total
                * 100
            )

            percent = max(
                0,
                min(
                    percent,
                    100,
                ),
            )

            self.progress.setRange(
                0,
                100
            )

            self.progress.setValue(
                percent
            )

            self.percent_label.setText(
                f"{percent}%"
            )

            self.status_label.setText(
                (
                    f"{self._format_size(received)}"
                    f" / "
                    f"{self._format_size(total)}"
                )
            )

        else:

            self.progress.setRange(
                0,
                0
            )

            self.percent_label.setText(
                ""
            )

            self.status_label.setText(
                self._format_size(
                    received
                )
            )

    # ======================================================
    # STATE
    # ======================================================

    def _state_changed(
        self,
        *_,
    ):

        if self.download is None:
            return

        state = (
            self.download.state()
        )

        state_name = (
            str(state)
            .lower()
        )

        if "completed" in state_name:

            self.progress.setRange(
                0,
                100
            )

            self.progress.setValue(
                100
            )

            self.percent_label.setText(
                "100%"
            )

            self.title_label.setText(
                "Download complete"
            )

            self.status_label.setText(
                "Saved to Downloads"
            )

            self.open_button.show()

            self.adjustSize()

            self.hide_timer.start(
                5000
            )

        elif "cancelled" in state_name:

            self.title_label.setText(
                "Download cancelled"
            )

            self.status_label.setText(
                "Download was cancelled"
            )

            self.percent_label.setText(
                ""
            )

            self.hide_timer.start(
                3500
            )

        elif "interrupted" in state_name:

            self.title_label.setText(
                "Download failed"
            )

            reason = (
                self.download
                .interruptReasonString()
            )

            if not reason:

                reason = (
                    "Download interrupted"
                )

            self.status_label.setText(
                reason
            )

            self.percent_label.setText(
                ""
            )

    # ======================================================
    # OPEN
    # ======================================================

    def _open_file(
        self,
    ):

        if self.download is None:
            return

        directory = (
            self.download
            .downloadDirectory()
        )

        file_name = (
            self.download
            .downloadFileName()
        )

        path = Path(
            directory
        ) / file_name

        if not path.exists():
            return

        QDesktopServices.openUrl(
            path.as_uri()
        )

    # ======================================================
    # HIDE
    # ======================================================

    def hide_popup(
        self,
    ):

        self.hide_timer.stop()

        self.hide()

    # ======================================================
    # SIZE
    # ======================================================

    @staticmethod
    def _format_size(
        number,
    ):

        number = float(
            number
        )

        units = [
            "B",
            "KB",
            "MB",
            "GB",
        ]

        for unit in units:

            if (
                number < 1024
                or unit == "GB"
            ):

                if unit == "B":

                    return (
                        f"{int(number)} {unit}"
                    )

                return (
                    f"{number:.1f} {unit}"
                )

            number /= 1024

        return (
            f"{number:.1f} GB"
        )