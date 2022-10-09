from typing import List

from PySide6.QtWidgets import QSizePolicy, QWidget

VerticalExplandPolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)


def set_size_policies(widgets: List[QWidget], policy: QSizePolicy) -> None:
    for widget in widgets:
        widget.setSizePolicy(policy)
