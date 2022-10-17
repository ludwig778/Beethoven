from typing import Sequence, Union

from pydantic import BaseModel
from PySide6.QtWidgets import QHBoxLayout, QLayout, QVBoxLayout, QWidget, QStackedLayout


class Stretch(BaseModel):
    pass


class Spacing(BaseModel):
    size: int


LayoutItem = Union[QWidget, QLayout, Stretch, Spacing]


def layout_widget_factory(
    layout: QLayout, layout_items: Sequence[LayoutItem], object_name: str = ""
):
    layout.setSpacing(0)

    for layout_item in layout_items:
        if isinstance(layout_item, QWidget):
            layout.addWidget(layout_item)
        elif isinstance(layout_item, QLayout):
            layout.addLayout(layout_item)
        elif isinstance(layout_item, Stretch):
            layout.addStretch(stretch=1)
        elif isinstance(layout_item, Spacing):
            layout.addSpacing(layout_item.size)

    if object_name:
        widget = QWidget()
        widget.setLayout(layout)
        widget.setObjectName(object_name)

        return widget

    return layout


def horizontal_layout(layout_items: Sequence[LayoutItem], **kwargs):
    return layout_widget_factory(
        QHBoxLayout(),
        layout_items,
        **kwargs,
    )


def vertical_layout(layout_items: Sequence[LayoutItem], **kwargs):
    return layout_widget_factory(
        QVBoxLayout(),
        layout_items,
        **kwargs,
    )


def stacked_layout(layout_items: Sequence[QWidget], **kwargs):
    return layout_widget_factory(
        QStackedLayout(),
        layout_items,
        **kwargs,
    )
