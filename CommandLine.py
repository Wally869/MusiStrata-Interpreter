from cmd import Cmd

from Globals import VERSION
# from this: https://code-maven.com/interactive-shell-with-cmd-in-python

from MusiStrata import *
import mido
import pygame

from dataclasses import dataclass

rtmidi = mido.Backend('mido.backends.rtmidi')


freq = 44100    # audio CD quality
bitsize = -16   # unsigned 16 bit
channels = 2    # 1 is mono, 2 is stereo
buffer = 1024    # number of samples
pygame.mixer.init(freq, bitsize, channels, buffer)


@dataclass
class SongData:
    Temp: int = 80

@dataclass
class TrackData:
    Name: str = "Unnamed"
    Volume: float = 0.8
    RhythmicModel: str = "Standard"
    MelodicModel: str = "Random"
    Instrument: str = "Grand Piano"

class StateMachine(object):
    def __init__(self):
        self.mCurrentTrackID = 0
        self.mSong = None
        #self.mSong.Tracks = [Track()]
        self.mTracksData = [TrackData()]
    def ClearSong(self):
        self.mSong = None
        #self.mSong.Tracks = [Track()]
        self.mTracksData = [TrackData()]
        self.mCurrentTrackID = 0
    def ClearTrackData(self, idTrack):
        self.mTracksData[idTrack] = TrackData()
    def ClearCurrentTrackData(self):
        self.ClearTrackData(self.mCurrentTrackID)
        self.mCurrentTrackID = 0
    def ClearAllTrackData(self):
        self.mTracksData = [TrackData()]
        self.mCurrentTrackID = 0
    def GenerateSong(self):
        s = Song()
        t = Track()
        b = Bar()
        b.SoundEvents = [SoundEvent(i, 1.0, Note("A", 5)) for i in range(4)]
        t.append(b)
        s.Tracks = [t]
        self.mSong = s
    def PlaySong(self):
        self.StopSong()
        if (self.mSong is not None):
            MidoConverter.ConvertSong(self.mSong, "temp.mid")
            pygame.mixer.music.load("temp.mid")
            pygame.mixer.music.play()
        else:
            print("No generated song found. Ensure you called generateSong before playSong")
    def StopSong(self):
        pygame.mixer.music.stop()
    def GetCurrentTrackData(self):
        return self.mTracksData[self.mCurrentTrackID]


state = StateMachine()

# input is pruned of command and following whitespace, except when defaulting
class MusiStrataCLI(Cmd):
    prompt = "musi>"
    intro = "Welcome to MusiStrata CLI V{}. Type help for a list of available commands.".format(VERSION)
    def do_clear(self, inp):
        commands = inp.split(" ")
        if commands[0] == "song":
            print("Clearing song")
            state.ClearSong()
        elif commands[0] == "track":
            if len(commands) == 1:
                print("Clearing current track")
                state.ClearCurrentTrackData()
            else:
                if commands[1] == "all":
                    print("Clearing all track data")
                    state.ClearAllTrackData()
                else:
                    print("Clearing track {}".format(commands[1]))
                    state.ClearTrackData(int(commands[1]))
        else: 
            print("Unknown command. Can clear song, track, or track [idtrack]")

    def do_play(self, inp):
        inp = inp.split(" ")
        if inp[0] == "song":
            print("Playing Song")
            state.PlaySong()
        elif inp[0] == "track":
            if len(inp) == 1:
                print("Playing Current Track")
            else:
                print("Playing track {}".format(inp[1]))

    def do_stop(self, inp):
        state.StopSong()

    def do_exit(self, inp):
        print("Exiting")
        return True
 
    def do_add(self, inp):
        inp = inp.split(" ")
        print("Adding '{}'".format(inp))

    def do_selectTrack(self, inp):
        print("switching to track {} - {}".format(inp, state.mTracksData[int(inp)].Name))
        state.mCurrentTrackID = int(inp)

    def do_setTrackModel(self, inp):
        print(inp)

    def do_setTrackName(self, inp):
        print(inp)

    def do_setTrackInstrument(self, inp):
        state.GetCurrentTrackData().Instrument = inp

    def do_getTrackMelodicModel(self, inp):
        print(state.GetCurrentTrackData().MelodicModel)

    def do_getTrackRhythmicModel(self, inp):
        print(state.GetCurrentTrackData().RhythmicModel)

    def do_setModelRhythm(self, inp):
        state.GetCurrentTrackData().RhythmicModel = inp

    def do_setModelMelodic(self, inp):
        state.GetCurrentTrackData().MelodicModel = inp

    def do_getListInstruments(self, inp):
        print("Allowed Instruments:")
        print(Instruments.InstrumentsLibrary.GetAllValuesFromField("Name"))

    def do_generateSong(self, inp):
        state.GenerateSong()

    def default(self, inp):
        print(inp)

