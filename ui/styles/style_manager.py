from pathlib import Path

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QApplication


AVAILABLE_THEMES = {
    "midnight",
    "graphite",
    "aurora",
    "light",
}

DEFAULT_THEME = "midnight"


def get_current_theme():
    settings = QSettings(
        "Veyra",
        "VeyraBrowser",
    )

    theme = settings.value(
        "appearance/theme",
        DEFAULT_THEME,
    )

    if theme not in AVAILABLE_THEMES:
        return DEFAULT_THEME

    return theme


def apply_theme(
    app: QApplication,
    theme_name: str,
):
    if theme_name not in AVAILABLE_THEMES:
        theme_name = DEFAULT_THEME

    project_root = Path(
        __file__
    ).resolve().parents[2]

    themes_folder = (
        project_root
        / "resources"
        / "themes"
    )

    base_path = (
        themes_folder
        / "veyra.qss"
    )

    theme_path = (
        themes_folder
        / f"{theme_name}.qss"
    )

    if not base_path.exists():
        print(
            f"Base stylesheet not found: {base_path}"
        )
        return

    if not theme_path.exists():
        print(
            f"Theme stylesheet not found: {theme_path}"
        )
        return

    base_stylesheet = base_path.read_text(
        encoding="utf-8"
    )

    theme_stylesheet = theme_path.read_text(
        encoding="utf-8"
    )

    stylesheet = (
        base_stylesheet
        + "\n\n"
        + theme_stylesheet
    )

    app.setStyleSheet(
        stylesheet
    )

    settings = QSettings(
        "Veyra",
        "VeyraBrowser",
    )

    settings.setValue(
        "appearance/theme",
        theme_name,
    )


def load_style(
    app: QApplication,
):
    apply_theme(
        app,
        get_current_theme(),
    )