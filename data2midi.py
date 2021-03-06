import mido
from mido import Message


class Data2Midi:
    MIN = 0
    MAX = 127
    CHANNEL_NOTE_OFF = 123
    _port = None
    _notes_on = []
    _control_channel = None

    def __init__(self, control_channel=1, midi_out_name=False):
        if midi_out_name is False:
            self._port = mido.open_output('video2midi', virtual=True)
        else:
            self._port = mido.open_output(midi_out_name)
        self.set_control_channel(control_channel)

    def __del__(self):
        self.notes_off_all()
        if self._port:
            self._port.close()

    def set_control_channel(self, value):
        if value < self.MIN or value > self.MAX:
            raise ValueError('Whong channel number. Must be between 1 and 127')
        else:
            self._control_channel = value

    @staticmethod
    def get_midi_out_list():
        return mido.get_output_names()

    @staticmethod
    def float_to_midi(float_val):
        data = round(float_val * Data2Midi.MAX)
        return Data2Midi.int_to_midi(data)

    @staticmethod
    def int_to_midi(int_value):
        if int_value > Data2Midi.MAX:
            return Data2Midi.MAX
        elif int_value < Data2Midi.MIN:
            return Data2Midi.MIN
        else:
            return round(int_value)

    def send_midi_note(self, note, value):
        note = self.float_to_midi(note)
        value = self.int_to_midi(value)
        self.notes_off_all()
        msg = Message('note_on', note=note, velocity=value)
        self._port.send(msg)

    def send_midi_cc(self, value):
        value = self.float_to_midi(value)
        msg = Message('control_change', control=self._control_channel,
                      value=value)
        self._port.send(msg)

    def notes_off_all(self):
        if self._port:
            self._port.send(
                Message('control_change', control=self.CHANNEL_NOTE_OFF,
                        value=0))
