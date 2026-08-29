from pathlib import Path

from PySide6.QtWidgets import QApplication


def load_style(app: QApplication):

    project_root = Path(__file__).resolve().parents[2]

    style_path = (
        project_root
        / "resources"
        / "themes"
        / "veyra.qss"
    )

    if not style_path.exists():
        print(
            f"Veyra style not found: {style_path}"
        )
        return

    with open(
        style_path,
        "r",
        encoding="utf-8",
    ) as file:

        stylesheet = file.read()

    app.setStyleSheet(stylesheet)