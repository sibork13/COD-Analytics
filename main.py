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
    for button in buttons_list:
        match_page.click_open_stats(button)
    players_stats,players_name = match_page.test_get_player_block
    match_page.close_connection
    player_name_index = 0
    for future_row in range(0,len(players_stats),10):
        print(players_name[player_name_index])
        print(players_stats[future_row:future_row+10])
        print("*********************")
        player_name_index += 1



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
    # game_mode = page.get_game_mode
    # place = page.get_place
    # loby_kd = page.get_loby_kd
    # kills_and_kd = page.get_kills
    # every_match_link_list = page.get_main_match


    '''
    At this moment loby kd doesn exist if the game mode is blood money
    '''
    loby_kd_indx = 0
    # Reading allowed game modes
    with open('Game_Mode.txt',mode='r') as f:
        allowed_game_mode = list(f.read().split(",\n"))

    all_matches_list,every_matrch_link_list = page.matches_list(allowed_game_mode)



    # for i in range(0,len(all_matches_list),4):
    #     print(all_matches_list[i:i+4])

    # # creating a list of good indexes to scrape match per match after
    # good_index_list = []
    # # filtering matches, only allow game mode matches
    # for index_list in range(0,len(place)):
    #     list = []
    #     if game_mode[index_list].text in allowed_game_mode:
    #         good_index_list.append(index_list)
    #         list.append(game_mode[index_list].text)
    #         list.append(place[index_list].text)
    #         list.append(loby_kd[loby_kd_indx].text)
    #         list.append(kills_and_kd[index_list*2].text)
    #         list.append(kills_and_kd[index_list*2+1].text)
    #         print("Partida")
    #         print(list)
    #         loby_kd_indx += 1
    #     else:
    #         pass
    #

    page.close_connection
    for link in every_matrch_link_list[0:5]:
        # print(i)
        print('*****************INFO DE LA PARTIDA *********************')
        print(link)
        # match_info(website,link)


    print("FIN DE LA EJECUCION")
