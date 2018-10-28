import mido
from mido import Message


class Data2Midi:
    _port = None
    _notes_on = []
    _control_channel = None

    def __init__(self, control_channel=1, virtual=True):
        #  @ToDo: how can i set MIDI-port?
        self._port = mido.open_output('video2midi', virtual=virtual)
        self.set_control_channel(control_channel)

    def __del__(self):
        self.stop_all()
        if self._port:
            self._port.close()

    def set_control_channel(self, value):
        if value < 0 or value > 127:
            raise ValueError('Whong channel number. Must be between 1 and 127')
        else:
            self._control_channel = value

    @staticmethod
    def float_to_127(float_val):
        data = round(float_val * 127)
        if data > 127:
            return 127
        elif data < 0:
            return 0
        else:
            return int(data)

    @staticmethod
    def int_to_127(int_value):
        if int_value > 127:
            return 127
        elif int_value < 0:
            return 0
        else:
            return round(int_value)

    def send_midi_note(self, note, value):
        note = self.int_to_127(note)
        value = self.int_to_127(value)
        if note not in self._notes_on:
            self._notes_on.append(note)
            msg = Message('note_on', note=note, velocity=value)
            self._port.send(msg)

    def send_midi_cc(self, value):
        value = self.int_to_127(value)
        print(f'cc={value}')
        msg = Message('control_change', control=self._control_channel,
                      value=value)
        self._port.send(msg)

    def notes_off_all(self):
        self._port.send(Message('control_change', control=123, value=0))
