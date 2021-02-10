from collections import defaultdict
import mido

from beethoven.sequencer.grid import Grid
from beethoven.sequencer.players.base import Players
from beethoven.sequencer.harmony import Harmony
from beethoven.sequencer.scale import Scale
from beethoven.sequencer.chord import Chord
from beethoven.sequencer.note import Note
from beethoven.sequencer.tempo import default_tempo_factory, Tempo
from beethoven.sequencer.time_signature import default_time_signature_factory, TimeSignature
from beethoven.sequencer.note_duration import *


class PlayRoom:
    def __init__(self, **kwargs):
        self.grid = Grid(**kwargs)
        self.players = Players(**kwargs)

    def play(self):
        pass

    def _parse_grid(self, string, repeat=False):
        output = mido.open_output("LMAO", virtual=True)
        from time import sleep
        sleep(1.9)
        midi_file = mido.MidiFile(type=1)
        track = mido.MidiTrack()
        midi_file.tracks.append(track)



        splitted = string.split()

        print(splitted)
        #note = Note(splitted[0])
        note = splitted[0]
        scale = Scale(note, splitted[1])
        chord = Chord(note, splitted[2])
        harmony = Harmony(scale)
        harmony_list = splitted[3].replace("_", " ")

        time_signature = default_time_signature_factory()
        time_signature = TimeSignature(3, 4)
        tempo = default_tempo_factory()
        tempo = Tempo(60)
        bar_duration = None #Whole

        print("NOTE", note)
        print("SCALE", scale)
        print("CHORD", chord)
        print("HARMONY", harmony)
        print("HARMONY_LIST", harmony_list)
        print("PLAYERS", self.players.all())

        global_time = 0
        timeline = defaultdict(list)

        for item in harmony_list.split(","):
            chord = harmony.get(item)
            print("- CHORD", chord)

            if bar_duration:
                limit_time = global_time + bar_duration.duration(tempo)
            else:
                limit_time = global_time + time_signature.get_duration(tempo)
            print("LIM", limit_time)
            for channel, player in self.players.items():
                player.prepare(
                    duration=bar_duration,
                    time_signature=time_signature,
                    tempo=tempo,
                    scale=scale,
                    chord=chord
                )

                #
                # AVOID TIME SIGNATURE STUFF ADDING
                # AND TRY FIX IT WITH LIM STUFF limit_time
                #

                for note in player.play_measure():
                    part = note.pop("part")

                    offset_time = part.start_offset(time_signature, tempo)

                    part_time = global_time + offset_time

                    duration = note["duration"].duration(tempo)

                    print("PPPP", duration, part.max_time, part_time)
                    #if duration > part.max_time - part_time:
                    #    duration = part.max_time# - part_time

                    note["channel"] = channel
                    note["duration"] = duration

                    if part_time < limit_time:
                        timeline[part_time].append(note)

            global_time = limit_time

        return
        from pprint import pprint as pp
        print("TIME LINE " * 33)
        pp(timeline)

        messages = defaultdict(list)
        for start_time, players_notes in sorted(timeline.items(), key=lambda x: x[0]):
            for player_notes in players_notes:
                velocity = player_notes['velocity']
                channel = player_notes['channel']
                duration = player_notes['duration']

                for note in player_notes['notes']:

                    #print("SSSSSS", start_time, duration)
                    messages[start_time].append([
                        'note_on', note.index, velocity, channel
                    ])
                    messages[start_time + duration].append([
                        'note_off', note.index, 127, channel
                    ])

        print("MESSAGES " * 33)
        pp(messages)

        current_time = 0

        sorted_timestamps = sorted(messages.keys())
        for start_time, events in sorted(messages.items(), key=lambda x: x[0]):

            num_events = len(events)

            for i, event in enumerate(events, start=1):
                #print(start_time, i, event)
                instruction = event[0]
                note = event[1]
                velocity = event[2]
                channel = event[3]

                current_time_index = sorted_timestamps.index(start_time)
                #print()
                #print(i, current_time_index, start_time)
                if i == 1 and current_time_index != 0: # and current_time_index < (len(sorted_timestamps) - 1):
                    previous_time = sorted_timestamps[current_time_index - 1]
                    time = (start_time - previous_time) * 1000
                else:
                    time = 0
                #time = 0
                #if instruction == "note_off":
                #    time = 200 * start_time

                #print(instruction, note, velocity, channel, time)

                msg = mido.Message(
                    instruction,
                    note=note,
                    velocity=velocity,
                    channel=channel,
                    time=time
                )
                
                print(msg)
                track.append(msg)

        """
        track.append(mido.Message('note_on', note=64, velocity=64, time=0))
        track.append(mido.Message('note_off', note=64, velocity=127, time=320))
        track.append(mido.Message('note_on', note=64, velocity=64, time=0))
        track.append(mido.Message('note_off', note=64, velocity=127, time=320))
        track.append(mido.Message('note_on', note=64, velocity=64, time=0))
        track.append(mido.Message('note_off', note=64, velocity=127, time=320))
        """

        try:
            #print(sorted_timestamps)
            #sleep(3.5)
            #print("TRACK  :", track)
            if repeat:
                while 1:
                    for msg in midi_file.play():
                        #print("MESSAGE:", msg)
                        output.send(msg)
            else:
                for msg in midi_file.play():
                    #print("MESSAGE:", msg)
                    output.send(msg)
        except:
            pass
        finally:
            output.panic()