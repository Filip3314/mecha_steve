"""Functions to offload work to. Helps enable testing of the app"""


def get_song(arg):
    """Figures out the song to play based on the argument passed in"""
    if 'youtube' in arg:
        return 'A youtube link!'
    if 'spotify' in arg:
        return 'A spotify link!'
    return 'Gotta search for this!'
