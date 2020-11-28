from cmd import Cmd

from StateMachine import StateMachine
from Globals import VERSION
# from this: https://code-maven.com/interactive-shell-with-cmd-in-python

from MusiStrata.Instruments import InstrumentsLibrary

state = StateMachine()

# input is pruned of command and following whitespace, except when defaulting
class MusiStrataCLI(Cmd):
    prompt = "musi>"
    intro = "\nWelcome to MusiStrata CLI V{}. Type help for a list of available commands.".format(VERSION)
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

    def do_addTrack(self, inp):
        state.AddTrack()
    
    def do_delTrack(self, inp):
        print("Deleting Track.")
        state.DelTrack()
        print("Current: Track ID {} - {}".format(state.mCurrentTrackID, state.GetCurrentTrackData()))

    def do_play(self, inp):
        inp = inp.split(" ")
        if inp[0] == "song":
            print("Playing Song")
            state.PlaySong()
        else:  # inp[0] == "track":
            print("Playing Current Track")
            state.PlayCurrentTrack()

    def do_stop(self, inp):
        state.StopSong()

    def do_exit(self, inp):
        print("Exiting")
        return True
 
    def do_getListTracks(self, inp):
        print(state.mTracksData)

    def do_selectTrack(self, inp):
        print("switching to track {} - {}".format(inp, state.mTracksData[int(inp)].Name))
        state.mCurrentTrackID = int(inp)    

    def do_setName(self, inp):
        state.GetCurrentTrackData().Name
    
    def do_getName(self, inp):
        print(state.GetCurrentTrackData().Name)

    def do_setInstrument(self, inp):
        state.GetCurrentTrackData().Instrument = inp
    
    def do_getInstrument(self, inp):
        print(state.GetCurrentTrackData().Instrument)    

    def do_setMelodicModel(self, inp):
        state.GetCurrentTrackData().MelodicModel = inp

    def do_getMelodicModel(self, inp):
        print(state.GetCurrentTrackData().MelodicModel)

    def do_setRhythmicModel(self, inp):
        state.GetCurrentTrackData().RhythmicModel = inp

    def do_getRhythmicModel(self, inp):
        print(state.GetCurrentTrackData().RhythmicModel)

    def do_getListInstruments(self, inp):
        print("Allowed Instruments:")
        print(InstrumentsLibrary.GetAllValuesFromField("Name"))

    def do_generateSong(self, inp):
        state.GenerateSong()

    def default(self, inp):
        print("Unknown Command: {}".format(inp))

