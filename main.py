'''
Main script to scrape
'''

import functions as func

def url_builder(player_name,player_number):
    # url = 'https://cod.tracker.gg/warzone/profile/battlenet/'
    url = 'https://cod.tracker.gg/warzone/profile/atvi/'
    url = url+str(player_name) + '%23' + str(player_number) + '/matches'
    return url

def match_info(website,url):
    match_page = func.MatchPage(website,url)
    buttons_list = match_page.extract_butons
    for button in buttons_list:
        match_page.click_open_stats(button)
    players_stats = match_page.test_get_player_block
    for row in players_stats:
        print(row)
    # for future_row in range(0,len(players_stats),12):
        # print(players_stats[future_row:future_row+12])
        # print("*********************")
    match_page.close_connection



if __name__== '__main__':
    # nombre='sibork13'
    # numero = '1199'
    nombre='manny'
    numero = '4039159'
    website = 'CODTRACKER'

    url = url_builder(nombre,numero)
    # starting scraper
    page = func.HomePage(website,url)
    [page.click_next for i in range(0,2)]
    jugador_id = page.player_name

    print(jugador_id)
    print("\n")

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

    page.close_connection
    for link in every_matrch_link_list[0:1]:
        print('*****************INFO DE LA PARTIDA *********************')
        print(link)
        match_info(website,link)


    print("FIN DE LA EJECUCION")
