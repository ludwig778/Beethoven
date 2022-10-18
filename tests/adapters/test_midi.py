from pytest import fixture

from beethoven.adapters.midi import MidiMessage, MidiMetaMessage


@fixture(scope="function", autouse=True)
def mock_midi_adapter(mock_midi_adapter):
    pass


def test_midi_adapter_open_output(adapters):
    adapters.midi.open_output("PIANO_CHANNEL")
    adapters.midi.open_output("DRUM_CHANNEL")

    assert len(adapters.midi.outputs) == 2


def test_midi_adapter_close_output(adapters):
    adapters.midi.open_output("PIANO_CHANNEL")
    adapters.midi.open_output("DRUM_CHANNEL")

    adapters.midi.close_output("DRUM_CHANNEL")

    assert len(adapters.midi.outputs) == 1


def test_midi_adapter_close_all_outputs(adapters):
    adapters.midi.open_output("PIANO_CHANNEL")
    adapters.midi.open_output("DRUM_CHANNEL")

    adapters.midi.close_all_outputs()

    assert len(adapters.midi.outputs) == 0


def test_midi_adapter_shutdown(adapters, mocker):
    mocked_panic = mocker.patch("beethoven.adapters.midi.Output.panic")

    adapters.midi.open_output("PIANO_CHANNEL")
    adapters.midi.open_output("DRUM_CHANNEL")

    adapters.midi.shutdown()

    assert mocked_panic.call_count == 2


def test_midi_adapter_send_midi_message(adapters, mocker):
    mocked_midi_send = mocker.patch("beethoven.adapters.midi.Output.send")

    output = adapters.midi.open_output("PIANO_CHANNEL")

    message = MidiMessage(
        note=64, output=output, velocity=127, channel=0, type="note_on"
    )
    adapters.midi.send_message(message)

    assert mocked_midi_send.call_count == 1


def test_midi_adapter_send_midi_meta_message(adapters, mocker):
    mocked_midi_send = mocker.patch("beethoven.adapters.midi.Output._send")

    output = adapters.midi.open_output("PIANO_CHANNEL")

    message = MidiMetaMessage(
        output=output,
        type="text",
        text="start",
    )
    adapters.midi.send_message(message)

    assert mocked_midi_send.call_count == 1
