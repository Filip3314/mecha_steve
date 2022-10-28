import mecha_steve.utils as utils


def test_get_song():
    assert utils.get_song("youtube") == "searching for the word youtube"
    assert utils.get_song("spotify address") == "playing linked spotify song"
    assert utils.get_song("youtube link") == "playing linked youtube song"
    assert utils.get_song("bruh") == "searching for and playing bruh"
