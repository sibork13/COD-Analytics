'''
Main script to scrape
'''

import functions as func

def url_builder(player_name,player_number):
    url = 'https://cod.tracker.gg/warzone/profile/battlenet/'
    url = url+str(player_name) + '%23' + str(player_number) + '/matches'
    return url


if __name__== '__main__':
    nombre='sibork13'
    numero = '1199'
    website = 'CODTRACKER'

    url = url_builder(nombre,numero)
    # starting scraper
    page = func.HomePage(website,url)
    [page.click_next for i in range(0,10)]
    jugador_id = page.player_name
    print(jugador_id)
    print("\n")
    game_mode = page.get_game_mode
    place = page.get_place
    loby_kd = page.get_loby_kd
    kills_and_kd = page.get_kills


    '''
    At this moment loby kd doesn exist if the game mode is blood money
    '''
    loby_kd_indx = 0
    allowed_game_mode = ['BR Solos','BR Duos','BR Trios','BR Quads',
                        'BR Buyback Solos','BR Buyback Duos','BR Buyback Trios','BR Buyback Quads']
    for index_list in range(0,len(place)):
        list = []
        if game_mode[index_list].text in allowed_game_mode:
            list.append(game_mode[index_list].text)
            list.append(place[index_list].text)
            list.append(loby_kd[loby_kd_indx].text)
            list.append(kills_and_kd[index_list*2].text)
            list.append(kills_and_kd[index_list*2+1].text)
            print("Partida")
            print(list)
            loby_kd_indx += 1
        else:
            print("NO SUEM NADA")

    page.close_connection
    print("FIN DE LA EJECUCION")
