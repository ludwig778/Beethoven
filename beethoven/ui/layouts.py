from typing import List, Tuple, Type, Union, TypeVar

from pydantic import BaseModel
from PySide6.QtWidgets import QHBoxLayout, QStackedLayout, QVBoxLayout, QWidget


class Stretch(BaseModel):
    pass


class Spacing(BaseModel):
    size: int


LayoutItem = Union[QWidget, QHBoxLayout, QVBoxLayout, QStackedLayout, Stretch, Spacing]
StackedLayoutItem = Union[QWidget, QHBoxLayout, QVBoxLayout, QStackedLayout]
BoxLayout = TypeVar("BoxLayout", QHBoxLayout, QVBoxLayout)


def layout_widget_factory(
    layout_class: Type[BoxLayout],
    layout_items: List[LayoutItem],
    object_name: str = "",
    spacing: int = 0,
    margins: Tuple[int, int, int, int] = (0, 0, 0, 0),
) -> BoxLayout:
    layout = layout_class()
    layout.setSpacing(spacing)
    layout.setContentsMargins(*margins)

    for layout_item in layout_items:
        if isinstance(layout_item, QWidget):
            layout.addWidget(layout_item)
        elif isinstance(layout_item, (QHBoxLayout, QVBoxLayout)):
            layout.addLayout(layout_item)
        elif isinstance(layout_item, Stretch):
            layout.addStretch(stretch=1)
        elif isinstance(layout_item, Spacing):
            layout.addSpacing(layout_item.size)

    if object_name:
        widget = QWidget()
        widget.setLayout(layout)
        widget.setObjectName(object_name)

        container_layout = layout_class()
        container_layout.addWidget(widget)

        return container_layout

    return layout


def horizontal_layout(layout_items: List[LayoutItem], **kwargs) -> QHBoxLayout:
    return layout_widget_factory(QHBoxLayout, layout_items, **kwargs)


def vertical_layout(layout_items: List[LayoutItem], **kwargs) -> QVBoxLayout:
    return layout_widget_factory(QVBoxLayout, layout_items, **kwargs)


def stacked_layout(
    layout_items: List[StackedLayoutItem],
    spacing: int = 0,
    margins: Tuple[int, int, int, int] = (0, 0, 0, 0),
) -> QStackedLayout:
    layout = QStackedLayout()
    layout.setSpacing(spacing)
    layout.setContentsMargins(*margins)

    for layout_item in layout_items:
        layout.addWidget(layout_item)  # type: ignore

    return layout
