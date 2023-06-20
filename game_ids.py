def get_game_id(game_name):
    url = "https://www.boardgamegeek.com/xmlapi/search"
    params = {
        "search": game_name,
        "exact": 1
    }
    response = requests.get(url, params=params)
    # parse the response text as XML
    root = ElementTree.fromstring(response.text)
    # find the first 'boardgame' element and get its 'objectid' attribute
    boardgame = root.find('boardgame')
    if boardgame is not None:
        return boardgame.get('objectid')
    else:
        return None

game_ids = {}

for game in top_games:
    game_id = get_game_id(game)
    if game_id:
        game_ids[game] = game_id
    # sleep for a while to avoid rate limiting
    time.sleep(2)
        
