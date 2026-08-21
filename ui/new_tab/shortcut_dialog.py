from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
)


class ShortcutDialog(QDialog):

    def __init__(self,parent=None,name="",url=""):
        super().__init__(parent)

        self.setWindowTitle("Shortcut")

        layout=QFormLayout(self)

        self.name=QLineEdit(name)
        self.url=QLineEdit(url)

        layout.addRow("Name",self.name)
        layout.addRow("URL",self.url)

        buttons=QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

    def values(self):

        return (
            self.name.text().strip(),
            self.url.text().strip()
        )