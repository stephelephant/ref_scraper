import functions

def test_get_game_log_url():
    ret = functions.get_game_log_url("/players/c/collijo01.html")
    assert type(ret) == list

