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
        print(players_name[player_name_index].text)
        print(players_stats[future_row:future_row+10])
        print("*********************")
        player_name_index += 1



if __name__== '__main__':
    # nombre='sibork13'
    # numero = '1199'
    nombre='opmarked'
    numero = '1818'
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



    page.close_connection
    for link in every_matrch_link_list[0:1]:
        # print(i)
        print('*****************INFO DE LA PARTIDA *********************')
        print(link)
        match_info(website,link)


    print("FIN DE LA EJECUCION")
