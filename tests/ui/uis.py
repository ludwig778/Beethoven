from typing import cast, Callable


def test_uis(qt_application, mock_midi_adapter, widget_partials):
    for widget_partial in widget_partials.values():
        assert cast(Callable, widget_partial)()
