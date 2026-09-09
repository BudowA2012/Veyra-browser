import json

from PySide6.QtCore import (
    QObject,
    QSettings,
    QTimer,
    Signal,
)

from PySide6.QtWebEngineWidgets import (
    QWebEngineView,
)

from ui.new_tab.new_tab_page import (
    NewTabPage,
)


class SessionManager(QObject):

    crash_detected = Signal()

    AUTOSAVE_INTERVAL = 5000

    def __init__(
        self,
        tabs,
        parent=None,
    ):
        super().__init__(
            parent
        )

        self.tabs = tabs

        self.settings = QSettings(
            "Veyra",
            "VeyraBrowser",
        )

        # ==================================================
        # CHECK PREVIOUS STATE
        # ==================================================

        self.previous_session_clean = (
            self.settings.value(
                "session/clean_shutdown",
                True,
                type=bool,
            )
        )

        # Od tej chwili aplikacja jest traktowana jako
        # uruchomiona i jeszcze niezamknięta poprawnie.
        self.settings.setValue(
            "session/clean_shutdown",
            False,
        )

        self.settings.sync()

        # ==================================================
        # AUTOSAVE
        # ==================================================

        self.autosave_timer = QTimer(
            self
        )

        self.autosave_timer.setInterval(
            self.AUTOSAVE_INTERVAL
        )

        self.autosave_timer.timeout.connect(
            self.save_session
        )

        self.autosave_timer.start()

    # ======================================================
    # CRASH
    # ======================================================

    def crashed_last_time(
        self,
    ):

        return (
            not self.previous_session_clean
        )

    # ======================================================
    # SAVE
    # ======================================================

    def save_session(
        self,
    ):

        tabs_data = []

        current_widget = (
            self.tabs.currentWidget()
        )

        active_saved_index = 0

        for index in range(
            self.tabs.count()
        ):

            widget = (
                self.tabs.widget(
                    index
                )
            )

            # ==============================================
            # NEW TAB
            # ==============================================

            if isinstance(
                widget,
                NewTabPage,
            ):

                if (
                    widget
                    is current_widget
                ):

                    active_saved_index = (
                        len(
                            tabs_data
                        )
                    )

                tabs_data.append(
                    {
                        "type": "new_tab",
                    }
                )

                continue

            # ==============================================
            # WEBSITE
            # ==============================================

            if isinstance(
                widget,
                QWebEngineView,
            ):

                url = (
                    widget.url()
                    .toString()
                    .strip()
                )

                if not url:
                    continue

                if (
                    widget
                    is current_widget
                ):

                    active_saved_index = (
                        len(
                            tabs_data
                        )
                    )

                tabs_data.append(
                    {
                        "type": "web",
                        "url": url,
                    }
                )

        data = {
            "tabs": tabs_data,
            "active_index": active_saved_index,
        }

        encoded = json.dumps(
            data
        )

        # Normal session restore
        self.settings.setValue(
            "session/tabs",
            encoded,
        )

        # Osobna kopia autosave pod crash recovery
        self.settings.setValue(
            "session/autosave",
            encoded,
        )

        self.settings.sync()

    # ======================================================
    # LOAD NORMAL SESSION
    # ======================================================

    def normal_session(
        self,
    ):

        raw = self.settings.value(
            "session/tabs",
            "",
        )

        return self._decode(
            raw
        )

    # ======================================================
    # LOAD CRASH AUTOSAVE
    # ======================================================

    def crash_session(
        self,
    ):

        raw = self.settings.value(
            "session/autosave",
            "",
        )

        return self._decode(
            raw
        )

    # ======================================================
    # DECODE
    # ======================================================

    @staticmethod
    def _decode(
        raw,
    ):

        if not raw:
            return None

        try:

            data = json.loads(
                raw
            )

        except (
            TypeError,
            json.JSONDecodeError,
        ):

            return None

        if not isinstance(
            data,
            dict,
        ):

            return None

        tabs = data.get(
            "tabs"
        )

        if not isinstance(
            tabs,
            list,
        ):

            return None

        return data

    # ======================================================
    # CLEAN SHUTDOWN
    # ======================================================

    def mark_clean_shutdown(
        self,
    ):

        self.save_session()

        self.settings.setValue(
            "session/clean_shutdown",
            True,
        )

        self.settings.sync()