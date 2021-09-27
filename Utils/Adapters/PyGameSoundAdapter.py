import pygame


class SoundManager:

    def __init__(self):

        self.s = pygame.mixer
        self.sounds = {}
        self.playing = False
        self.muted = False
        self.current_song = None
        self.volume = 0.0

    def init(self):
        self.s.init()
        self.volume = self.s.music.get_volume()

    def set_song(self, song_path):
        self.current_song = song_path
        self.s.music.load(song_path)

    def play_song(self):
        self.playing = True
        self.s.music.play(loops=-1)

    def stop(self):
        if self.playing:
            self.s.fadeout(500)
            self.s.music.stop()
            self.playing = False

    def quit(self):
        self.s.quit()

    def mute(self):
        if not self.muted:
            self.muted = True
            self.s.music.set_volume(0.0)
            for sound in self.sounds:
                self.sounds[sound].set_volume(0)
        else:
            self.muted = False
            self.s.music.set_volume(self.volume)
            for sound in self.sounds:
                self.sounds[sound].set_volume(1.0)

    def add_sound(self, name, sound_path):
        self.sounds[name] = self.s.Sound(sound_path)

    def play_sound(self, name):
        if not self.muted:
            self.sounds[name].play()
