import sys

from PySide6.QtWidgets import QApplication

from ui.main_window.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    app.setApplicationName("Veyra")
    app.setApplicationDisplayName("Veyra Browser")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()