def bgg_stats():

    count = 0

    for id in game_ids:
        url = f"https://boardgamegeek.com/xmlapi2/thing?id={id}&type=boardgame&stats=1"
        response = requests.get(url, timeout=15)
        soup =  BeautifulSoup(response.content, "xml")
        name = soup.find('name')
        if name != None:
            name = name.attrs['value']
            if bgg_stats['Name'].isin([name]).any().item():
                game_ids.remove(id)
            else:
                bgg_stats.loc[count, 'Name'] = name
                min_players = int(soup.find('minplayers').attrs['value'])
                bgg_stats.loc[count, 'Min_players'] = min_players
                max_players = int(soup.find('maxplayers').attrs['value'])
                bgg_stats.loc[count, 'Max_players'] = max_players
                min_playtime = int(soup.find('minplaytime').attrs['value'])
                bgg_stats.loc[count, 'Min_playtime'] = min_playtime
                max_playtime = int(soup.find('maxplaytime').attrs['value'])
                bgg_stats.loc[count, 'Max_playtime'] = max_playtime
                weight = float(soup.find('averageweight').attrs['value'])
                bgg_stats.loc[count, 'Weight'] = weight
                designers = [designer.attrs['value'] for designer in soup.find_all(type='boardgamedesigner')]
                designers = ','.join(designers)
                bgg_stats.loc[count, 'Designers'] = designers
                categories = [category.attrs['value'] for category in soup.find_all(type='boardgamecategory')]
                categories = ','.join(categories)
                bgg_stats.loc[count, 'Categories'] = categories
                mechanics = [mechanic.attrs['value'] for mechanic in soup.find_all(type='boardgamemechanic')]
                mechanics = ','.join(mechanics)
                bgg_stats.loc[count, 'Mechanics'] = mechanics
                rating = float(soup.find('average').attrs['value'])
                bgg_stats.loc[count, 'Rating'] = rating

                game_ids.remove(id)

                clear_output(wait=True)
                display(f'Completed line {count}.', display_id=True)
                count += 1
                
    return bgg_stats