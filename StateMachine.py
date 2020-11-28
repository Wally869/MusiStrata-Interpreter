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
