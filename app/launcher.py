import sys

from PySide6.QtWidgets import QApplication

from ui.main_window.main_window import MainWindow
from ui.styles.style_manager import load_style


def main():

    app = QApplication(sys.argv)

    app.setApplicationName("Veyra")
    app.setApplicationDisplayName(
        "Veyra Browser"
    )

    load_style(app)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()