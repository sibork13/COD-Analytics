'''
Main script to scrape
'''

import functions as func

def url_builder(player_name,player_number):
    url = 'https://cod.tracker.gg/warzone/profile/battlenet/'
    url = url+str(player_name) + '%23' + str(player_number) + '/matches'
    return url

def match_info(website,url):
    match_page = func.MatchPage(website,url)
    buttons_list = match_page.extract_butons
    # stats = match_page.extract_players_stats
    for button in buttons_list:
        match_page.click_open_stats(button)
        stats = match_page.extract_players_stats
        for stat in stats:
            print(stat.text)
        match_page.click_open_stats(button)
    match_page.close_connection


if __name__== '__main__':
    nombre='sibork13'
    numero = '1199'
    website = 'CODTRACKER'

    url = url_builder(nombre,numero)
    # starting scraper
    page = func.HomePage(website,url)
    [page.click_next for i in range(0,2)]
    jugador_id = page.player_name
    print(jugador_id)
    print("\n")
    game_mode = page.get_game_mode
    place = page.get_place
    loby_kd = page.get_loby_kd
    kills_and_kd = page.get_kills
    every_match_link_list = page.get_main_match


    '''
    At this moment loby kd doesn exist if the game mode is blood money
    '''
    loby_kd_indx = 0
    # Reading allowed game modes
    with open('Game_Mode.txt',mode='r') as f:
        allowed_game_mode = list(f.read().split(",\n"))

    # creating a list of good indexes to scrape match per match after
    good_index_list = []

    # filtering matches, only allow game mode matches
    for index_list in range(0,len(place)):
        list = []
        if game_mode[index_list].text in allowed_game_mode:
            good_index_list.append(index_list)
            list.append(game_mode[index_list].text)
            list.append(place[index_list].text)
            list.append(loby_kd[loby_kd_indx].text)
            list.append(kills_and_kd[index_list*2].text)
            list.append(kills_and_kd[index_list*2+1].text)
            # print("Partida")
            # print(list)
            loby_kd_indx += 1
        else:
            pass
            # print("NO SUEM NADA")

    page.close_connection
    # print(good_index_list)
    # # starting scrape match per match
    for i in good_index_list[0:1]:
        print(i)
        print('*****************INFO DE LA PARTIDA *********************')
        match_info(website,every_match_link_list[i])

    print("FIN DE LA EJECUCION")
