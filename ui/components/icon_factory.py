from PySide6.QtCore import (
    QPointF,
    QRectF,
    Qt,
)
from PySide6.QtGui import (
    QColor,
    QIcon,
    QPainter,
    QPainterPath,
    QPen,
    QPixmap,
)


ICON_COLOR = QColor(
    "#aeb3c1"
)


def create_icon(
    name: str,
    size: int = 20,
    color=None,
) -> QIcon:

    pixmap = QPixmap(
        size,
        size,
    )

    pixmap.fill(
        Qt.GlobalColor.transparent
    )

    painter = QPainter(
        pixmap
    )

    painter.setRenderHint(
        QPainter.RenderHint.Antialiasing,
        True,
    )

    icon_color = (
        QColor(color)
        if color
        else ICON_COLOR
    )

    pen = QPen(
        icon_color
    )

    pen.setWidthF(
        max(
            1.5,
            size * 0.085,
        )
    )

    pen.setCapStyle(
        Qt.PenCapStyle.RoundCap
    )

    pen.setJoinStyle(
        Qt.PenJoinStyle.RoundJoin
    )

    painter.setPen(
        pen
    )

    painter.setBrush(
        Qt.BrushStyle.NoBrush
    )

    drawers = {
        "back": _draw_back,
        "forward": _draw_forward,
        "reload": _draw_reload,
        "home": _draw_home,
        "qr": _draw_qr,
        "plus": _draw_plus,
        "close": _draw_close,
        "download": _draw_download,
        "menu": _draw_menu,
        "bookmark": _draw_bookmark,
        "history": _draw_history,
        "settings": _draw_settings,
    }

    drawer = drawers.get(
        name
    )

    if drawer:

        drawer(
            painter,
            size,
        )

    painter.end()

    return QIcon(
        pixmap
    )


# =========================================================
# BACK
# =========================================================


def _draw_back(
    painter,
    size,
):

    painter.drawLine(
        QPointF(
            size * 0.72,
            size * 0.50,
        ),
        QPointF(
            size * 0.29,
            size * 0.50,
        ),
    )

    painter.drawLine(
        QPointF(
            size * 0.29,
            size * 0.50,
        ),
        QPointF(
            size * 0.47,
            size * 0.31,
        ),
    )

    painter.drawLine(
        QPointF(
            size * 0.29,
            size * 0.50,
        ),
        QPointF(
            size * 0.47,
            size * 0.69,
        ),
    )


# =========================================================
# FORWARD
# =========================================================


def _draw_forward(
    painter,
    size,
):

    painter.drawLine(
        QPointF(
            size * 0.28,
            size * 0.50,
        ),
        QPointF(
            size * 0.71,
            size * 0.50,
        ),
    )

    painter.drawLine(
        QPointF(
            size * 0.71,
            size * 0.50,
        ),
        QPointF(
            size * 0.53,
            size * 0.31,
        ),
    )

    painter.drawLine(
        QPointF(
            size * 0.71,
            size * 0.50,
        ),
        QPointF(
            size * 0.53,
            size * 0.69,
        ),
    )


# =========================================================
# RELOAD
# =========================================================


def _draw_reload(
    painter,
    size,
):

    rect = QRectF(
        size * 0.23,
        size * 0.23,
        size * 0.54,
        size * 0.54,
    )

    painter.drawArc(
        rect,
        35 * 16,
        285 * 16,
    )

    painter.drawLine(
        QPointF(
            size * 0.70,
            size * 0.23,
        ),
        QPointF(
            size * 0.76,
            size * 0.37,
        ),
    )

    painter.drawLine(
        QPointF(
            size * 0.70,
            size * 0.23,
        ),
        QPointF(
            size * 0.55,
            size * 0.27,
        ),
    )


# =========================================================
# HOME
# =========================================================


def _draw_home(
    painter,
    size,
):

    painter.drawLine(
        QPointF(
            size * 0.22,
            size * 0.49,
        ),
        QPointF(
            size * 0.50,
            size * 0.25,
        ),
    )

    painter.drawLine(
        QPointF(
            size * 0.50,
            size * 0.25,
        ),
        QPointF(
            size * 0.78,
            size * 0.49,
        ),
    )

    painter.drawLine(
        QPointF(
            size * 0.30,
            size * 0.43,
        ),
        QPointF(
            size * 0.30,
            size * 0.76,
        ),
    )

    painter.drawLine(
        QPointF(
            size * 0.70,
            size * 0.43,
        ),
        QPointF(
            size * 0.70,
            size * 0.76,
        ),
    )

    painter.drawLine(
        QPointF(
            size * 0.30,
            size * 0.76,
        ),
        QPointF(
            size * 0.70,
            size * 0.76,
        ),
    )

    painter.drawLine(
        QPointF(
            size * 0.44,
            size * 0.76,
        ),
        QPointF(
            size * 0.44,
            size * 0.59,
        ),
    )

    painter.drawLine(
        QPointF(
            size * 0.44,
            size * 0.59,
        ),
        QPointF(
            size * 0.56,
            size * 0.59,
        ),
    )

    painter.drawLine(
        QPointF(
            size * 0.56,
            size * 0.59,
        ),
        QPointF(
            size * 0.56,
            size * 0.76,
        ),
    )


# =========================================================
# MENU
# =========================================================


def _draw_menu(
    painter,
    size,
):

    for y in (
        0.32,
        0.50,
        0.68,
    ):

        painter.drawLine(
            QPointF(
                size * 0.28,
                size * y,
            ),
            QPointF(
                size * 0.72,
                size * y,
            ),
        )


# =========================================================
# BOOKMARK
# =========================================================


def _draw_bookmark(
    painter,
    size,
):

    path = QPainterPath()

    path.moveTo(
        size * 0.34,
        size * 0.22,
    )

    path.lineTo(
        size * 0.66,
        size * 0.22,
    )

    path.lineTo(
        size * 0.66,
        size * 0.78,
    )

    path.lineTo(
        size * 0.50,
        size * 0.66,
    )

    path.lineTo(
        size * 0.34,
        size * 0.78,
    )

    path.closeSubpath()

    painter.drawPath(
        path
    )


# =========================================================
# HISTORY
# =========================================================


def _draw_history(
    painter,
    size,
):

    rect = QRectF(
        size * 0.23,
        size * 0.23,
        size * 0.54,
        size * 0.54,
    )

    painter.drawEllipse(
        rect
    )

    painter.drawLine(
        QPointF(
            size * 0.50,
            size * 0.34,
        ),
        QPointF(
            size * 0.50,
            size * 0.52,
        ),
    )

    painter.drawLine(
        QPointF(
            size * 0.50,
            size * 0.52,
        ),
        QPointF(
            size * 0.63,
            size * 0.59,
        ),
    )


# =========================================================
# DOWNLOAD
# =========================================================


def _draw_download(
    painter,
    size,
):

    painter.drawLine(
        QPointF(
            size * 0.50,
            size * 0.19,
        ),
        QPointF(
            size * 0.50,
            size * 0.62,
        ),
    )

    painter.drawLine(
        QPointF(
            size * 0.34,
            size * 0.47,
        ),
        QPointF(
            size * 0.50,
            size * 0.62,
        ),
    )

    painter.drawLine(
        QPointF(
            size * 0.66,
            size * 0.47,
        ),
        QPointF(
            size * 0.50,
            size * 0.62,
        ),
    )

    painter.drawLine(
        QPointF(
            size * 0.27,
            size * 0.77,
        ),
        QPointF(
            size * 0.73,
            size * 0.77,
        ),
    )


# =========================================================
# SETTINGS
# =========================================================


def _draw_settings(
    painter,
    size,
):

    center = QPointF(
        size * 0.50,
        size * 0.50,
    )

    painter.drawEllipse(
        center,
        size * 0.13,
        size * 0.13,
    )

    outer = QRectF(
        size * 0.27,
        size * 0.27,
        size * 0.46,
        size * 0.46,
    )

    painter.drawEllipse(
        outer
    )

    for x1, y1, x2, y2 in (
        (0.50, 0.16, 0.50, 0.27),
        (0.50, 0.73, 0.50, 0.84),
        (0.16, 0.50, 0.27, 0.50),
        (0.73, 0.50, 0.84, 0.50),
        (0.26, 0.26, 0.34, 0.34),
        (0.66, 0.66, 0.74, 0.74),
        (0.74, 0.26, 0.66, 0.34),
        (0.34, 0.66, 0.26, 0.74),
    ):

        painter.drawLine(
            QPointF(
                size * x1,
                size * y1,
            ),
            QPointF(
                size * x2,
                size * y2,
            ),
        )


# =========================================================
# QR
# =========================================================


def _draw_qr(
    painter,
    size,
):

    def box(
        x,
        y,
    ):

        painter.drawRect(
            QRectF(
                size * x,
                size * y,
                size * 0.22,
                size * 0.22,
            )
        )

        painter.drawRect(
            QRectF(
                size * (x + 0.065),
                size * (y + 0.065),
                size * 0.09,
                size * 0.09,
            )
        )

    box(
        0.17,
        0.17,
    )

    box(
        0.61,
        0.17,
    )

    box(
        0.17,
        0.61,
    )

    painter.drawLine(
        QPointF(
            size * 0.61,
            size * 0.61,
        ),
        QPointF(
            size * 0.61,
            size * 0.80,
        ),
    )

    painter.drawLine(
        QPointF(
            size * 0.61,
            size * 0.61,
        ),
        QPointF(
            size * 0.80,
            size * 0.61,
        ),
    )

    painter.drawLine(
        QPointF(
            size * 0.73,
            size * 0.70,
        ),
        QPointF(
            size * 0.80,
            size * 0.70,
        ),
    )


# =========================================================
# PLUS
# =========================================================


def _draw_plus(
    painter,
    size,
):

    painter.drawLine(
        QPointF(
            size * 0.28,
            size * 0.50,
        ),
        QPointF(
            size * 0.72,
            size * 0.50,
        ),
    )

    painter.drawLine(
        QPointF(
            size * 0.50,
            size * 0.28,
        ),
        QPointF(
            size * 0.50,
            size * 0.72,
        ),
    )


# =========================================================
# CLOSE
# =========================================================


def _draw_close(
    painter,
    size,
):

    painter.drawLine(
        QPointF(
            size * 0.31,
            size * 0.31,
        ),
        QPointF(
            size * 0.69,
            size * 0.69,
        ),
    )

    painter.drawLine(
        QPointF(
            size * 0.69,
            size * 0.31,
        ),
        QPointF(
            size * 0.31,
            size * 0.69,
        ),
    )