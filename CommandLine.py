from cmd import Cmd

from StateMachine import StateMachine
from Globals import VERSION
# from this: https://code-maven.com/interactive-shell-with-cmd-in-python

from MusiStrata.Instruments import InstrumentsLibrary

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
        print(InstrumentsLibrary.GetAllValuesFromField("Name"))

    def do_generateSong(self, inp):
        state.GenerateSong()

    def default(self, inp):
        print(inp)

