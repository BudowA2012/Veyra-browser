from io import BytesIO
from pathlib import Path

import qrcode

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)


class QRDialog(QDialog):

    def __init__(
        self,
        url: str,
        parent=None,
    ):
        super().__init__(parent)

        self.url = url
        self.qr_pixmap = None

        self.setWindowTitle(
            "QR Code"
        )

        self.setMinimumWidth(
            430
        )

        self.setObjectName(
            "QRDialog"
        )

        self._build_ui()
        self._generate_qr()

    # ==================================================
    # BUILD
    # ==================================================

    def _build_ui(self):

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            24,
            24,
            24,
            24,
        )

        layout.setSpacing(
            16
        )

        # ==================================================
        # TITLE
        # ==================================================

        title = QLabel(
            "Share this page"
        )

        title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        title.setStyleSheet(
            """
            font-size: 22px;
            font-weight: 700;
            background: transparent;
            """
        )

        layout.addWidget(
            title
        )

        subtitle = QLabel(
            "Scan the QR code with your phone."
        )

        subtitle.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        subtitle.setStyleSheet(
            """
            color: #8b90a0;
            background: transparent;
            """
        )

        layout.addWidget(
            subtitle
        )

        # ==================================================
        # QR
        # ==================================================

        self.qr_label = QLabel()

        self.qr_label.setFixedSize(
            260,
            260,
        )

        self.qr_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.qr_label.setStyleSheet(
            """
            background: white;
            border-radius: 18px;
            padding: 12px;
            """
        )

        layout.addWidget(
            self.qr_label,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )

        # ==================================================
        # URL
        # ==================================================

        url_label = QLabel(
            self.url
        )

        url_label.setWordWrap(
            True
        )

        url_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        url_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        url_label.setStyleSheet(
            """
            color: #8b90a0;
            background: transparent;
            font-size: 12px;
            """
        )

        layout.addWidget(
            url_label
        )

        # ==================================================
        # BUTTONS
        # ==================================================

        buttons = QHBoxLayout()

        buttons.setSpacing(
            10
        )

        copy_link = QPushButton(
            "Copy link"
        )

        copy_image = QPushButton(
            "Copy QR"
        )

        save_button = QPushButton(
            "Save PNG"
        )

        close_button = QPushButton(
            "Close"
        )

        copy_link.clicked.connect(
            self._copy_link
        )

        copy_image.clicked.connect(
            self._copy_qr
        )

        save_button.clicked.connect(
            self._save_qr
        )

        close_button.clicked.connect(
            self.accept
        )

        buttons.addWidget(
            copy_link
        )

        buttons.addWidget(
            copy_image
        )

        buttons.addWidget(
            save_button
        )

        buttons.addWidget(
            close_button
        )

        layout.addLayout(
            buttons
        )

    # ==================================================
    # QR GENERATION
    # ==================================================

    def _generate_qr(self):

        qr = qrcode.QRCode(
            version=None,
            error_correction=(
                qrcode.constants.ERROR_CORRECT_M
            ),
            box_size=10,
            border=3,
        )

        qr.add_data(
            self.url
        )

        qr.make(
            fit=True
        )

        image = qr.make_image(
            fill_color="black",
            back_color="white",
        )

        buffer = BytesIO()

        image.save(
            buffer,
            format="PNG",
        )

        pixmap = QPixmap()

        pixmap.loadFromData(
            buffer.getvalue()
        )

        self.qr_pixmap = pixmap

        display_pixmap = pixmap.scaled(
            220,
            220,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        self.qr_label.setPixmap(
            display_pixmap
        )

    # ==================================================
    # COPY LINK
    # ==================================================

    def _copy_link(self):

        clipboard = (
            QApplication.clipboard()
        )

        clipboard.setText(
            self.url
        )

    # ==================================================
    # COPY QR
    # ==================================================

    def _copy_qr(self):

        if self.qr_pixmap is None:
            return

        clipboard = (
            QApplication.clipboard()
        )

        clipboard.setPixmap(
            self.qr_pixmap
        )

    # ==================================================
    # SAVE
    # ==================================================

    def _save_qr(self):

        if self.qr_pixmap is None:
            return

        default_path = (
            Path.home()
            / "Downloads"
            / "veyra_qr.png"
        )

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save QR Code",
            str(default_path),
            "PNG Image (*.png)",
        )

        if not filename:
            return

        if not filename.lower().endswith(
            ".png"
        ):
            filename += ".png"

        self.qr_pixmap.save(
            filename,
            "PNG",
        )