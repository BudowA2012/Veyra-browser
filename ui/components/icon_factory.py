from PySide6.QtCore import (
    QPointF,
    QRectF,
    Qt,
)
from PySide6.QtGui import (
    QColor,
    QIcon,
    QPainter,
    QPen,
    QPixmap,
)


ICON_COLOR = QColor("#aeb3c1")


def create_icon(
    name: str,
    size: int = 20,
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

    pen = QPen(
        ICON_COLOR
    )

    pen.setWidthF(
        max(
            1.6,
            size * 0.09,
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

    if name == "back":
        _draw_back(
            painter,
            size,
        )

    elif name == "forward":
        _draw_forward(
            painter,
            size,
        )

    elif name == "reload":
        _draw_reload(
            painter,
            size,
        )

    elif name == "home":
        _draw_home(
            painter,
            size,
        )

    elif name == "qr":
        _draw_qr(
            painter,
            size,
        )

    elif name == "plus":
        _draw_plus(
            painter,
            size,
        )

    elif name == "close":
        _draw_close(
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

    left = size * 0.29
    center_y = size * 0.50
    right = size * 0.72

    painter.drawLine(
        QPointF(
            right,
            center_y,
        ),
        QPointF(
            left,
            center_y,
        ),
    )

    painter.drawLine(
        QPointF(
            left,
            center_y,
        ),
        QPointF(
            size * 0.47,
            size * 0.31,
        ),
    )

    painter.drawLine(
        QPointF(
            left,
            center_y,
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

    left = size * 0.28
    center_y = size * 0.50
    right = size * 0.71

    painter.drawLine(
        QPointF(
            left,
            center_y,
        ),
        QPointF(
            right,
            center_y,
        ),
    )

    painter.drawLine(
        QPointF(
            right,
            center_y,
        ),
        QPointF(
            size * 0.53,
            size * 0.31,
        ),
    )

    painter.drawLine(
        QPointF(
            right,
            center_y,
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
        30 * 16,
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
            size * 0.24,
            size * 0.48,
        ),
        QPointF(
            size * 0.50,
            size * 0.26,
        ),
    )

    painter.drawLine(
        QPointF(
            size * 0.50,
            size * 0.26,
        ),
        QPointF(
            size * 0.76,
            size * 0.48,
        ),
    )

    painter.drawLine(
        QPointF(
            size * 0.31,
            size * 0.44,
        ),
        QPointF(
            size * 0.31,
            size * 0.74,
        ),
    )

    painter.drawLine(
        QPointF(
            size * 0.69,
            size * 0.44,
        ),
        QPointF(
            size * 0.69,
            size * 0.74,
        ),
    )

    painter.drawLine(
        QPointF(
            size * 0.31,
            size * 0.74,
        ),
        QPointF(
            size * 0.69,
            size * 0.74,
        ),
    )


# =========================================================
# QR
# =========================================================


def _draw_qr(
    painter,
    size,
):

    small_pen = painter.pen()

    small_pen.setWidthF(
        max(
            1.4,
            size * 0.07,
        )
    )

    painter.setPen(
        small_pen
    )

    def box(x, y):

        painter.drawRect(
            QRectF(
                size * x,
                size * y,
                size * 0.23,
                size * 0.23,
            )
        )

        painter.drawRect(
            QRectF(
                size * (x + 0.07),
                size * (y + 0.07),
                size * 0.09,
                size * 0.09,
            )
        )

    box(
        0.17,
        0.17,
    )

    box(
        0.60,
        0.17,
    )

    box(
        0.17,
        0.60,
    )

    painter.drawLine(
        QPointF(
            size * 0.60,
            size * 0.60,
        ),
        QPointF(
            size * 0.60,
            size * 0.78,
        ),
    )

    painter.drawLine(
        QPointF(
            size * 0.60,
            size * 0.60,
        ),
        QPointF(
            size * 0.78,
            size * 0.60,
        ),
    )

    painter.drawLine(
        QPointF(
            size * 0.72,
            size * 0.68,
        ),
        QPointF(
            size * 0.79,
            size * 0.68,
        ),
    )

    painter.drawLine(
        QPointF(
            size * 0.72,
            size * 0.68,
        ),
        QPointF(
            size * 0.72,
            size * 0.79,
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