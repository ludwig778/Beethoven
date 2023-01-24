def get_stylesheet() -> str:
    return """
    * {
        font-size: 12px;

        padding: 0px;
        margin: 0px;
    }
    MainWindow {
        max-width: 550px; min-width: 550px;
        max-height: 400px; min-height: 400px;
    }
    HarmonyGrid QListView {
        max-height: 80px; min-height: 80px;
    }
    ChordGrid QListView {
        max-height: 50px; min-height: 50px;
    }
    HarmonyGrid QPushButton {
        height: 40px;
        width: 72px;
    }
    ChordGrid QPushButton {
        height: 50px;
        width: 35px;
    }
    Button {
        font-size: 12px;
    }
    PushPullButton[pressed=true] {
        background-color: gray;
        color: white;
    }
    ScalePicker * {
        font-size: 12px;
        font: bold;
        height: 24px;
    }
    ScalePicker NoteComboBox {
        max-width: 34px; min-width: 34px;
    }
    ScalePicker ScaleComboBox {
        max-width: 100px; min-width: 100px;
    }
    ScalePicker OctaveSpinBox {
        height: 22px;
    }
    ChordPicker {
        max-width: 500px; min-width: 500px;
    }
    ChordPicker * {
        height: 50px;
    }
    ChordPicker QLabel {
        font-size: 13px;
        font: bold;
        margin: 5px auto 10px 10px;
    }
    ChordPicker QComboBox {
        font: bold;
    }
    ChordPicker DegreeAlterationComboBox {
        font-size: 26px;
        font: bold;
        max-width: 70px; min-width: 70px;
    }
    ChordPicker #duration_section QLabel {
        margin: 10px auto 15px 95px;
    }
    DurationSelector {
        height: 120px;
        max-width: 170px; min-width: 170px;
    }
    ChordPicker #duration_section DurationSelector {
    }
    QStackedLayout {
        max-width: 400px; min-width: 400px;
        max-height: 400px; min-height: 400px;
    }
    PlayerControl {
        max-width: 200px; min-width: 200px;
    }
    PlayerControl QPushButton {
        height: 23px;
        font-size: 13px;
        font: bold;
    }
    ComposeWidget #label_section {
        max-width: 120px; min-width: 120px;
    }
    MainWindow QLabel {
        font-size: 12px;
        font: bold;
    }
    MainWindow QSpinBox {
        height: 20px;
        font-size: 13px;
        font: bold;
        width: 26px;
    }
    MainWindow QComboBox {
        height: 22px;
        font-size: 13px;
        font: bold;
    }
    HarmonyTrainer #step_interval_section QPushButton {
        width: 50px;
    }
    QLineEdit {
        height: 38px;
        font-size: 20px;
        font: bold;
    }
    FramedText {
        background-color: white;
        border: 1px solid #ababab;
        border-radius: 3px;
        height: 40px;
    }
    FramedText #upper_text {
        margin-top: -4px;
        color: #888;
        font-size: 9px;
    }
    FramedText #lower_text {
        font-size: 20px;
        color: #555;
        font: bold;
    }
    TuningDialog {
        max-width: 200px; min-width: 200px;
        max-height: 350px; min-height: 350px;
    }
    TuningDialog * {
        font-size: 15px;
    }
    TuningDialog TuningComboBox {
        padding: 4px;
    }
    TuningDialog StringNumberSpinBox {
        max-width: 40px; min-width: 40px;
    }
    TuningDialog QPushButton {
        font-size: 17px;
        height: 30px;
    }
    StringSelectorRow QLabel {
        max-width: 62px;
    }
    StringSelectorRow NoteComboBox {
        max-width: 44px; min-width: 44px;
        padding: 2px 5px 2px 4px;
    }

    MidiDialog {
        max-width: 395px; min-width: 395px;
        max-height: 340x; min-height: 340px;
    }
    MidiDialog * {
        font-size: 15px;
    }
    MidiDialog MidiInputComboBox {
        padding: 4px;
        height: 23px;
        max-width: 255px; min-width: 255px;
    }
    MidiDialog MidiOutputSelector {
        font-size: 16px;
        max-height: 176px; min-height: 176px;
    }
    MidiDialog QPushButton {
        font-size: 17px;
        height: 30px;
    }

    PlayerDialog {
        max-width: 750px; min-width: 750px;
        max-height: 385x; min-height: 385px;
    }
    PlayerDialog * {
        font-size: 15px;
    }
    PlayerDialog MidiOutputComboBox {
        font-size: 15px;
        width: 20px;
    }
    PlayerDialog MidiInputComboBox {
        padding: 4px;
        height: 23px;
        max-width: 255px; min-width: 255px;
    }
    PlayerDialog MidiOutputSelector {
        font-size: 16px;
        max-height: 176px; min-height: 176px;
    }
    PlayerDialog Button {
        font-size: 17px;
        height: 30px;
    }
    PlayerDialog #button_box * {
        width: 230px;
    }
    PlayerDialog QLabel {
        font-size: 18px;
        font: bold;
        color: #444;
    }
    PlayerDialog #settings_label {
        font-size: 13px;
        padding-bottom: -1px;
        color: #808080;
    }

    PlayerRow QComboBox {
        font-size: 16px;
        height: 30px;
    }
    PlayerRow #instrument_name {
        max-width: 170px; min-width: 170px;
    }
    PlayerRow #instrument_style {
        max-width: 140px; min-width: 140px;
    }
    PlayerRow MidiOutputComboBox {
        max-width: 170px; min-width: 170px;
    }
    PlayerRow MidiChannelComboBox {
        max-width: 40px; min-width: 40px;
    }
    PlayerRow #enable_button {
        max-width: 120px; min-width: 120px;
    }
    PlayerRow #delete_button {
        background-color: #ff0000;
        max-width: 32px; min-width: 32px;
    }

    MidiAddDialog {
        max-width: 280px;
        min-width: 280px;
        max-height: 140px;
        min-height: 140px;
    }
    MidiAddDialog QLabel {
        font-size: 16px;
    }
    MidiAddDialog Button {
        font-size: 17px;
        height: 30px;
    }
    MidiAddDialog QLineEdit {
        font: normal;
    }

    TuningSaveDialog {
        max-width: 280px;
        min-width: 280px;
        max-height: 140px;
        min-height: 140px;
    }
    TuningSaveDialog QLabel {
        font-size: 16px;
    }
    TuningSaveDialog #error_label {
        font-size: 14px;
        color: red;
    }
    TuningSaveDialog Button {
        font-size: 17px;
        height: 30px;
    }
    TuningSaveDialog QLineEdit {
        font: normal;
    }
    """
