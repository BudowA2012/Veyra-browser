from pathlib import Path

from PySide6.QtWidgets import QApplication


def load_style(app: QApplication):

    style_path = (
        Path(__file__).resolve().parent
        / "veyra.qss"
    )

    with open(
        style_path,
        "r",
        encoding="utf-8",
    ) as file:
        app.setStyleSheet(
            file.read()
        )