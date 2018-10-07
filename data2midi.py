from time import sleep


import mido
from mido import Message


class Data2Midi:
    _port = None
    _notes_on = []

    def __init__(self):
        #  @ToDo: how can i set MIDI-port?
        self._port = mido.open_output()

    def __del__(self):
        self.stop_all()
        if self._port:
            self._port.close()

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

    #  @ToDo: How can i send MIDI CC?
    def send_midi_note(self, note, value):
        note = self.int_to_127(note)
        value = self.int_to_127(value)
        if note not in self._notes_on:
            self._notes_on.append(note)
            msg = Message('note_on', note=note, velocity=value)
            self._port.send(msg)

    def stop_all(self):
        if self._port:
            for i in range(128):
                self._port.send(Message('note_off', note=i))
