def test_live_ui(qt_application, widget_partials, adapters):
    check_list = [
        "main_window",
    ]

    for widget_name in check_list:
        window = widget_partials[widget_name]()
        window.setWindowTitle("Beethoven")
        window.show()

        qt_application.exec()
