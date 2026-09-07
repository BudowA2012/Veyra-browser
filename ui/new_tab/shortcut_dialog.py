from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QVBoxLayout,
)


class ShortcutDialog(QDialog):

    def __init__(
        self,
        parent=None,
        name="",
        url="",
    ):
        super().__init__(
            parent
        )

        self.setObjectName(
            "ShortcutDialog"
        )

        self.setWindowTitle(
            "Shortcut"
        )

        self.setMinimumWidth(
            420
        )

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            22,
            22,
            22,
            22,
        )

        layout.setSpacing(
            16
        )

        # ==================================================
        # TITLE
        # ==================================================

        title = QLabel(
            "Shortcut"
        )

        title.setObjectName(
            "ShortcutDialogTitle"
        )

        layout.addWidget(
            title
        )

        # ==================================================
        # FORM
        # ==================================================

        form = QFormLayout()

        form.setSpacing(
            12
        )

        self.name_input = QLineEdit(
            name
        )

        self.name_input.setObjectName(
            "ShortcutDialogInput"
        )

        self.name_input.setPlaceholderText(
            "Example: GitHub"
        )

        self.url_input = QLineEdit(
            url
        )

        self.url_input.setObjectName(
            "ShortcutDialogInput"
        )

        self.url_input.setPlaceholderText(
            "github.com"
        )

        form.addRow(
            "Name",
            self.name_input,
        )

        form.addRow(
            "URL",
            self.url_input,
        )

        layout.addLayout(
            form
        )

        # ==================================================
        # BUTTONS
        # ==================================================

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )

        buttons.accepted.connect(
            self.accept
        )

        buttons.rejected.connect(
            self.reject
        )

        layout.addWidget(
            buttons
        )

    # ==================================================
    # VALUES
    # ==================================================

    def values(self):

        name = (
            self.name_input
            .text()
            .strip()
        )

        url = (
            self.url_input
            .text()
            .strip()
        )

        if (
            url
            and "://" not in url
        ):

            url = (
                "https://"
                + url
            )

        return (
            name,
            url,
        )