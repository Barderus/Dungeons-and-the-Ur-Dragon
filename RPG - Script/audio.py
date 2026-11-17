import random
import time
from pygame import mixer


def play_sound():
    # List of songs
    songs = [
        "../Music/AudioCoffee Band - Cinematic Galactic.mp3",
        "../Music/ArcSound - Dark Horror Nightmare.mp3",
        "../Music/BlackTrendMusic - Epic.mp3",
        "../Music/Lowtone Music - Cinematic Soundtrack.mp3",
        "../Music/Lowtone Music - Dark Trailer.mp3",
        "../Music/Lowtone Music - Epic Action.mp3",
        "../Music/Lowtone Music - Fantasy Teaser.mp3",
        "../Music/Lowtone Music - Get Up & Fight.mp3",
        "../Music/Lowtone Music - This is War - Cinematic Epic.mp3",
        "../Music/UNIVERSFIELD - Gloomy Depths.mp3"
    ]

    mixer.init()
    mixer.music.set_volume(0.8)

    def queue_songs(song_list):
        # Shuffle and queue all songs
        random.shuffle(song_list)
        first_song = song_list.pop(0)
        mixer.music.load(first_song)
        for song in song_list:
            mixer.music.queue(song)
        mixer.music.play()

    queue_songs(songs.copy())  # Queue initial songs

    # Loop to check if queue is empty
    while True:
        if not mixer.music.get_busy():
            #print("Queue empty, reloading songs...")
            queue_songs(songs.copy())  # Reload the songs
        time.sleep(5)
