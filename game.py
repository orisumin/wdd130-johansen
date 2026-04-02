from pyscript import web, when, window # type: ignore   (pyscript imports when running the html, so no worries)
from datetime import datetime
import random #, csv
from map_data import *

CURRENT_ROOM = '0000'
PREVIOUS_ROOM = None
VISITED_ROOMS = []
HIGHSCORE = 0
START_TIME = None #datetime.now()       #Updated when game is started; once you enter the well. see game_start()
END_TIME = None
PLAYER_NAME = ''
PLAYER_WISH = ''
MAX_HP = 10 #TBD
HP = MAX_HP
INVENTORY = {'wish':False,
             'weapon':{'name':'fist','dmg':2},
             'hook':False,
             'potions':0,
             'lost wishes':[]}
GHOST_HP = {'BTLE':16, 'BTLW':16}
GHOST_ATK_PATTERN = {'BTLE':1, 'BTLW':1}
LOST_WISHES = {'LW_E':"I wish my little one would heal quickly...", 'LW_W':"I wish for the power to protect my homeland..."}

HEALTH_LABEL = web.page["health-label"]
WISH_ICON = web.page["wish"]
SWORD_ICON = web.page["sword"]
HOOK_ICON = web.page['hook']
POTIONS_ICON = web.page["potions"]
LOST_WISH_1_ICON = web.page["lost-wish-1"]
LOST_WISH_2_ICON = web.page["lost-wish-2"]
ROOM_IMG = web.page['room-img']
ROOM_TXT = web.page['room-txt']
TXT_INPUT = web.page['txt-input']
BTN1 = web.page['btn1']
BTN2 = web.page['btn2']
BTN3 = web.page['btn3']
BTN4 = web.page['btn4']

'''
def get_save_data():
    scoreboard = []
    with open('save_data.csv', 'rt') as save_file:
        reader = csv.reader(save_file)
        next(reader) #skips header line
        for row in reader:
            scoreboard.append(row)
    return scoreboard

def update_save_data(data):
    with open('save_data.csv', mode='w', newline='', encoding='utf-8') as savefile:
        writer = csv.writer(savefile)
        data.insert(0,['place','playername','playerwish','score','hmmmmm'])
        writer.writerows(data) #data is a list of lists

def update_scoreboard(scoreboard):
    count = 0
    found = False
    for row in scoreboard:
        if found:
            scoreboard[count][0] = count+1
        elif int(row[3]) < HIGHSCORE:
            found = True
            scoreboard.insert(count, [count+1, PLAYER_NAME, PLAYER_WISH, HIGHSCORE])
            scoreboard.pop()
        count += 1
    if found:
        update_save_data(scoreboard)
    return found, scoreboard
'''

def get_room_data():
    room = room_data[CURRENT_ROOM]
    cs = room['current_state']
    exits = room['exits']
    img = room['states'][cs]['img']
    txt = room['states'][cs]['txt']
    #state, exits, img, txt = get_room_data() <--- paste this at the top of each room function
    return room, cs, exits, img, txt

def get_move_options(exits):
    compass = {'N':'North', 'E':'East', 'S':'South', 'W':'West'}
    move_options = []
    for key in exits:
        if exits[key] == PREVIOUS_ROOM:
            move_options.append(f'Go Back ({compass[key]})')
        else:
            move_options.append(f'Go {compass[key]}')
    return move_options

def move(room_id):
    global PREVIOUS_ROOM, CURRENT_ROOM, VISITED_ROOMS
    PREVIOUS_ROOM = CURRENT_ROOM
    CURRENT_ROOM = room_id
    if not room_id in VISITED_ROOMS:
        VISITED_ROOMS.append(room_id)
    get_room_function(room_id, 0)

def display_inventory():
    global HEALTH_LABEL, WISH_ICON, SWORD_ICON, HOOK_ICON, POTIONS_ICON, LOST_WISH_1_ICON, LOST_WISH_2_ICON, INVENTORY
    HEALTH_LABEL.innerText = HP
    if INVENTORY['wish'] == True:
        WISH_ICON.src = 'images/wishing-well-logo.png'
    if INVENTORY['weapon']['name'] == 'sword':
        SWORD_ICON.src = 'images/sword-icon.png'
    if INVENTORY['hook'] == True:
        HOOK_ICON.src = 'images/hook-icon.png'
    if INVENTORY['potions'] == 1:
        POTIONS_ICON.src = 'images/health-potion-icon.png'
    elif INVENTORY['potions'] > 0:
        POTIONS_ICON.src = f'images/health-potion-icon-x{INVENTORY["potions"]}.png'
    else:
        POTIONS_ICON.removeAttribute('src')
    if len(INVENTORY['lost wishes']) > 0:
        LOST_WISH_1_ICON.src = 'images/lost-wish-icon.png'
        if len(INVENTORY['lost wishes']) == 2:
            LOST_WISH_2_ICON.src = 'images/lost-wish-icon.png'
        else:
            LOST_WISH_2_ICON.removeAttribute('src')
    else:
        LOST_WISH_1_ICON.removeAttribute('src')

def display_room(img, txt, options):
    global ROOM_IMG, ROOM_TXT, BTN1, BTN2, BTN3, BTN4
    ROOM_IMG.src = img
    ROOM_TXT.innerText = txt
    count = 0
    for btn in (BTN1, BTN2, BTN3, BTN4):
        try:
            btn.innerText = options[count]
            btn.removeAttribute("style")
            count += 1
        except IndexError:
            btn.setAttribute("style", "display:none")
    display_inventory()



#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#       Room Functions:
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=    

def escape(option):
    global END_TIME, HIGHSCORE
    room, state, exits, img, txt = get_room_data()
    if state == 0:
        if option == 0:
            END_TIME = datetime.now()
            time = 600 - (((START_TIME.hour*3600)+(START_TIME.minute*60)+START_TIME.second) - ((END_TIME.hour*3600)+(END_TIME.minute*60)+END_TIME.second))
            if time < 0:
                time = 0
            HIGHSCORE += time
            HIGHSCORE += len(VISITED_ROOMS)
            if INVENTORY['wish']:
                HIGHSCORE += 4
            
            display_room(img,txt,['View Score'])
        elif option == 1:
            '''
            txt = f"Your Score: {HIGHSCORE}"
            x, y = update_scoreboard(get_save_data())
            if x:
                txt += "\nYou're on the leader board!"
                txt += f'\n\n{y}'
            display_room(img, txt, ['View High Scores'])
            '''
            room['current_state'] = 1
            escape(0)
    elif state == 1:
        if option == 0:
            display_room(img,f'{PLAYER_NAME}\n"{PLAYER_WISH}"\nSCORE: {HIGHSCORE} points',['Play Again'])
        elif option == 1:
            window.location.reload(True)
            

def entrance(option):
    room, state, exits, img, txt = get_room_data()

    if state == 0:
        if option == 0:
            display_room(img, txt, ['Go North', 'Go East', 'Go South', 'Go West'])
        elif option == 1:
            room['current_state'] = 1
            move(exits['N'])
        elif option == 2:
            room['current_state'] = 1
            move(exits['E'])
        elif option == 3:
            room['current_state'] = 1
            move(exits['S'])
        elif option == 4:
            room['current_state'] = 1
            move(exits['W'])

    elif state == 1:
        if option == 0:
            display_room(img, txt, get_move_options(exits))
        elif option == 1:
            move(exits['N'])
        elif option == 2:
            move(exits['E'])
        elif option == 3:
            move(exits['S'])
        elif option == 4:
            move(exits['W'])

    elif state == 2:
        #get_move_options(exits)
        if option == 0:
            display_room(img, txt, ['ESCAPE!!!', 'Keep exploring the dungeon'])
        elif option == 1:
            move('WIN!')
        elif option == 2:
           room['current_state'] = 3
           entrance(0)
    elif state == 3:
        if option == 0:
            display_room(img, txt, get_move_options(exits))
        elif option == 1:
            room['current_state'] = 2
            move(exits['N'])
        elif option == 2:
            room['current_state'] = 2
            move(exits['E'])
        elif option == 3:
            room['current_state'] = 2
            move(exits['S'])
        elif option == 4:
            room['current_state'] = 2
            move(exits['W'])

def generic_room(option):
    room, state, exits, img, txt = get_room_data()
    exit_list = []
    for key in exits:
        exit_list.append(key)
    if len(room['states']) > 1:
        if state == 0:
            if CURRENT_ROOM == 'LMSE' and 'RickRoll' in VISITED_ROOMS:
                txt = 'You come across a room with music notes painted on the walls. Reminds you of that otherworldly melody...\n\nExits to the East and West'
                room['current_state'] = 2
            elif 'BTL' not in CURRENT_ROOM:
                room['current_state'] = 1
    if option == 0:
        display_room(img,txt,get_move_options(exits))
    elif option == 1:
        move(exits[exit_list[0]])
    elif option == 2:
        move(exits[exit_list[1]])
    elif option == 3:
        move(exits[exit_list[2]])
    elif option == 4:
        move(exits[exit_list[3]])

def collectable(option):
    global INVENTORY, HIGHSCORE
    room, state, exits, img, txt = get_room_data()
    if state == 0:
        if option == 0:
            display_room(img, txt, ['Take it', 'Go back'])
        elif option == 1:
            explain_potion = ''
            HIGHSCORE += 1
            room['current_state'] = 1
            if CURRENT_ROOM == 'SWRD':
                INVENTORY['weapon']['name'] = 'sword'
                INVENTORY['weapon']['dmg'] = 4
                room_data['LMNW']['current_state'] = 3
            elif 'HP' in CURRENT_ROOM:
                explain_potion = '(Click on the potion icon in your inventory to drink it!)'
                INVENTORY['potions'] += 1
            elif 'LW' in CURRENT_ROOM:
                INVENTORY['lost wishes'].append(CURRENT_ROOM)
            elif CURRENT_ROOM == 'WISH':
                INVENTORY['wish'] = True
            elif CURRENT_ROOM == 'EXIT':
                INVENTORY['hook'] = True
                room_data['ENTR']['current_state'] = 2
            
            display_room('images/empty-pedestal.png', f'You added it to your inventory.\n{explain_potion}', get_move_options(exits))
                
        elif option == 2:
            if PREVIOUS_ROOM == 'LMNW' and INVENTORY['weapon']['name'] != 'sword':
                room_data['LMNW']['current_state'] = 2
            move(PREVIOUS_ROOM)
    elif state == 1:
        generic_room(option)

def spike_trap(option):
    global HP
    room, state, exits, img, txt = get_room_data()
    if state == 0:
        if option == 0:
            room_data['LMNE']['current_state'] = 2
            display_room(img, txt, ['Attempt to avoid the spikes (0 to 4 damage)','Accept your fate (2 damage)'])
        else:
            if option == 1:
                dmg = random.randint(0,4)
            elif option == 2:
                dmg = 2
            
            HP -= dmg
            if HP > 0:
                room['current_state'] = 1
            else:
                room['current_state'] = 2
            display_room(img, f'You twist as you fall in, taking {dmg} damage.',['ouch'])
    elif state == 1:
        generic_room(option)
        room['current_state'] = 0
    elif state == 2:
        move('DEAD')

def fourth_wall_trap(option):
    global VISITED_ROOMS
    room, state, exits, img, txt = get_room_data()
    if state == 0:
        if option == 0:
            display_room(img, txt, ['Go Back', 'Break the wall'])
        if option == 1:
            move(PREVIOUS_ROOM)
        elif option == 2:
            window.open('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
            VISITED_ROOMS.append('RickRoll')
            room['current_state'] = 1
            room_data['LMSE']['current_state'] = 2
            display_room('images/dead-end.png', 'You manage to crawl back through the fourth wall before your brain melts.\nThe break in reality seals behind you.', ['Leave'])
    elif state == 1:
        generic_room(option)
            
def stair_trap(option):
    room, state, exits, img, txt = get_room_data()
    if state == 0:
        if option == 0:
            display_room(img, txt, ['Climb the stairs', 'Go back'])
        elif option == 1:
            room['current_state'] = 1
            stair_trap(0)
        elif option == 2:
            move(PREVIOUS_ROOM)
    elif state == 1:
        if option == 0:
            display_room(img, txt, ['Continue climbing', 'Go back down'])
        elif option == 1:
            room['current_state'] = 2
            stair_trap(0)
        elif option == 2:
            room['current_state'] = 4
            stair_trap(0)
    elif state == 2:
        if option == 0:
            display_room(img, txt, ['Continue climbing', 'Go back down'])
        elif option == 1:
            room['current_state'] = 3
            stair_trap(0)
        elif option == 2:
            room['current_state'] = 4
            stair_trap(0)
    elif state == 3:
        if option == 0:
            display_room(img, txt, ['Continue climbing', 'Go back down'])
        elif option == 2:
            room['current_state'] = 4
            stair_trap(0)
    elif state == 4:
        if option == 0:
            display_room(img, txt, ['Stubbornly go back up', 'Leave'])
        elif option == 1:
            room['current_state'] = 1
            stair_trap(0)
        elif option == 2:
            room['current_state'] = 5
            room_data['LM_S']['current_state'] = 2
            move(PREVIOUS_ROOM)
    elif state == 5:
        if option == 0:
            display_room(img, txt, ['Stubbornly climb the stairs', 'Go back'])
        elif option == 1:
            room['current_state'] = 1
            stair_trap(0)
        elif option == 2:
            room['current_state'] = 5
            move(PREVIOUS_ROOM)

def flee(opportunity):
    if opportunity == 'block':
        return True
    elif opportunity == 'attack':
        if GHOST_HP[CURRENT_ROOM] >= 8:
            if random.randint(0,2) == 2:
                return True
            else:
                return False
        else:
            if random.randint(0,9) == 9:
                return True
            else:
                return False
            
def attack(target):
    global GHOST_HP, HP, HIGHSCORE
    if target == 'ghost':
        GHOST_HP[CURRENT_ROOM] -= INVENTORY['weapon']['dmg']
        if GHOST_HP[CURRENT_ROOM] <= 0:
            HIGHSCORE += 1
            return 'defeated'
        else:
            return None
    elif target == 'player':
        damage = random.randint(0,2)
        if damage == 0:
            damage = 1
        HP -= damage
        if HP <= 0:
            move('DEAD')
        else:
            return str(damage)

def battle(option):
    global GHOST_ATK_PATTERN, INVENTORY, HP, HIGHSCORE
    room, state, exits, img, txt = get_room_data()
    if state == 0:
        if option == 0: #enter room
            GHOST_ATK_PATTERN[CURRENT_ROOM] = 1
            display_room(img, txt, ['Confront the Ghost','Attempt to flee'])
        elif option == 1:
            room['current_state'] = 1
            battle(0)
        elif option == 2:
            if flee('attack'):
                room['current_state'] = 2
                battle(0)
            else:
                room['current_state'] = 5
                display_room(img, "You couldn't escape!", ['Continue'])
    elif state == 1: #scream
        if option == 0:
            options = ['Attack', 'Flee']
            if len(INVENTORY['lost wishes']) > 0:
                options.append('Offer lost wish')
            display_room(img, txt, options)
        elif option == 1:
            GHOST_ATK_PATTERN[CURRENT_ROOM] = 3
            room['current_state'] = 5
            if attack('ghost') == 'defeated':
                display_room('images/four-exits.png',f'Your attack connects, dealing {INVENTORY['weapon']['dmg']} damage and vanquishing the Ghost!',['Continue'])
            else:
                display_room(img,f'Your attack connects, dealing {INVENTORY['weapon']['dmg']} damage',['Continue'])
        elif option == 2:
            if flee('attack'):
                room['current_state'] = 2
                battle(0)
            else:
                GHOST_ATK_PATTERN[CURRENT_ROOM] = 3
                room['current_state'] = 5
                display_room(img, "You couldn't escape!", ['Continue'])
        elif option == 3:
            room['current_state'] = 9 #done too much now to care about changing the order :(
            HIGHSCORE += 2
            battle(0)
    elif state == 2: #flee
        if option != 0:
            room['current_state'] = 0
        generic_room(option)
    elif state == 3: #Attack
        if option == 0:
            options = ['Attack','Block','flee']
            if len(INVENTORY['lost wishes']) > 0:
                options.append('Offer lost wish')
            display_room(img, txt, options)
        elif option == 1:
            GHOST_ATK_PATTERN[CURRENT_ROOM] = 4
            room['current_state'] = 5
            if attack('ghost') == 'defeated':
                display_room('images/four-exits.png',f'Your attack connects, dealing {INVENTORY['weapon']['dmg']} damage and vanquishing the Ghost!',['Continue'])
            else:
                display_room(img,f'Your attack connects, dealing {INVENTORY['weapon']['dmg']} damage, but the ghost also hits you, dealing {attack('player')} damage!',['Continue'])
        elif option == 2:
            GHOST_ATK_PATTERN[CURRENT_ROOM] = 4
            room['current_state'] = 5
            if INVENTORY['weapon']['name'] == 'sword':
                blocking_txt = "deflecting the ghost's attack with the blade of your sword!"
            else:
                blocking_txt = "dodging the ghost's attack!"
            clash = int(attack('player')) - 1
            HP += 1
            if clash > 0:
                dmg_txt = f'only take {clash}'
            else:
                dmg_txt = 'avoid all of the'
            display_room(img,f'You step into a defensive stance, {blocking_txt}\n You {dmg_txt} damage.',['Continue'])
        elif option == 3:
            if flee('attack'):
                room['current_state'] = 2
                battle(0)
            else:
                GHOST_ATK_PATTERN[CURRENT_ROOM] = 4
                room['current_state'] = 5
                display_room(img, f"You couldn't escape! The ghost hits you dealing {attack('player')} damage.", ['Continue'])
        elif option == 4:
            room['current_state'] = 9
            HIGHSCORE += 2
            battle(0)
    elif state == 4: #Block
        GHOST_ATK_PATTERN[CURRENT_ROOM] = 1
        if option == 0:
            options = ['Attack','Block','Flee']
            if len(INVENTORY['lost wishes']) > 0:
                options.append('Offer lost wish')
            display_room(img, txt, options)
        elif option == 1:
            room['current_state'] = 5
            if attack('ghost') == 'defeated':
                display_room('images/four-exits.png',f'Your attack connects, but the ghost defends itself. It takes only {int((INVENTORY['weapon']['dmg'])/2)} damage, yet you manage to defeat it!',['Continue'])
            else:
                display_room(img,f'Your attack connects, but the ghost defends itself. It takes only {int((INVENTORY['weapon']['dmg'])/2)} damage.',['Continue'])
        elif option == 2:
            room['current_state'] = 5
            display_room(img,f"You match the ghost's defensive posture, wary",['Continue'])
        elif option == 3:
            if flee('block'):
                room['current_state'] = 2
                battle(0)
            else:
                room['current_state'] = 5
                display_room(img, "You couldn't escape!", ['Continue'])
        elif option == 4:
            room['current_state'] = 9
            HIGHSCORE += 2
            battle(0)
    elif state == 5: #attack results
        '''
        if GHOST_ATK_PATTERN[CURRENT_ROOM] == 1:
            GHOST_ATK_PATTERN[CURRENT_ROOM] = 3
        elif GHOST_ATK_PATTERN[CURRENT_ROOM] == 3:
            GHOST_ATK_PATTERN[CURRENT_ROOM] = 4
        elif GHOST_ATK_PATTERN[CURRENT_ROOM] == 4:
            GHOST_ATK_PATTERN[CURRENT_ROOM] = 1
        '''
        if GHOST_HP[CURRENT_ROOM] > 0:
            room['current_state'] = GHOST_ATK_PATTERN[CURRENT_ROOM]
        else:
            room['current_state'] = 8
        battle(0)
    elif state == 6:
        generic_room(option)
        room['current_state'] = 6
    elif state == 7:
        if option == 0:
            if CURRENT_ROOM == 'BTLE':
                ghost_txt = '"I only ever wanted my little girl to be ok. Thank you, for bringing peace to my soul."'
            elif CURRENT_ROOM == 'BTLW':
                ghost_txt = '"I wanted to be able to protect those I love. Thank you for bringing peace to my soul."'
            display_room(img, f"The ghost accepts it's wish.\n{ghost_txt}", ['Continue'])
        if option == 1:
            room['current_state'] = 6
            battle(0)
    elif state == 8:
        generic_room(option)
    elif state == 9:
        if option == 0:
            if len(INVENTORY['lost wishes']) > 1:
                display_room(img, 'Give which wish?', [LOST_WISHES[INVENTORY['lost wishes'][0]], LOST_WISHES[INVENTORY['lost wishes'][1]]])
            else:
                display_room(img, 'Give wish?', [LOST_WISHES[INVENTORY['lost wishes'][0]]])
        elif option in (1,2):
            if INVENTORY['lost wishes'][option - 1][-1] == CURRENT_ROOM[-1]: #checks if the last letter in each string are the same
                INVENTORY['lost wishes'].pop(option-1)
                room['current_state'] = 7
                battle(0)
            else:
                room['current_state'] = 5
                display_room(img, "The ghost rejects it!", ['Continue'])

def game_over(option):
    room, state, exits, img, txt = get_room_data()
    if option == 0:
        display_room(img,txt,['Play Again'])
    if option == 1:
        window.location.reload(True)

def game_start(option):
    global TXT_INPUT, PLAYER_NAME, PLAYER_WISH, START_TIME
    room, state, exits, img, txt = get_room_data()
    if state == 0:
        if option == 0:
            display_room(img, txt, ['Submit'])
        if option == 1:
            PLAYER_NAME = TXT_INPUT.value
            TXT_INPUT.value = ''
            TXT_INPUT.setAttribute('placeholder', 'Enter wish')
            room['current_state'] = 1
            game_start(0)
    elif state == 1:
        if option == 0:
            display_room(img, txt, ['Submit'])
        elif option == 1:
            PLAYER_WISH = TXT_INPUT.value
            TXT_INPUT.value = ''
            TXT_INPUT.setAttribute("style", "display:none")
            room['current_state'] = 2
            game_start(0)
    elif state == 2:
        if option == 0:
            display_room(img, txt, [f'AAAaaAaahhhh!!!'])
        elif option == 1:
            START_TIME = datetime.now()
            move('ENTR')

def get_room_function(room_id, option):
    if room_id == 'ENTR':
        entrance(option)
    elif room_id in ('SWRD', 'HP#1', 'HP#2', 'HP#3', 'LW_E', 'LW_W', 'WISH', 'EXIT'):
        collectable(option)
    elif room_id == '^TRP':
        spike_trap(option)
    elif room_id == '4TRP':
        fourth_wall_trap(option)
    elif room_id == '$TRP':
        stair_trap(option)
    elif 'BTL' in room_id:
        battle(option)
    elif room_id == '0000':
        game_start(option)
    elif room_id == 'DEAD':
        game_over(option)
    elif room_id == 'WIN!':
        escape(option)
    else:
        generic_room(option)


@when("click", "#btn1")
def click_option_1(event):
    get_room_function(CURRENT_ROOM, 1)

@when("click", "#btn2")
def click_option_2(event):
    get_room_function(CURRENT_ROOM, 2)
        
@when('click', '#btn3')
def click_option_3(event):
    get_room_function(CURRENT_ROOM, 3)

@when('click', '#btn4')
def click_option_4(event):
    get_room_function(CURRENT_ROOM, 4)

@when('click', '#potions')
def click_heal(event):
    global INVENTORY, HP, ROOM_TXT

    if HP < MAX_HP:
        INVENTORY['potions'] -= 1
        HP += 3
        if HP > MAX_HP:
            HP = MAX_HP
        ROOM_TXT.innerText += '\nYou drank a health potion. Refreshing!'
        display_inventory()
    else:
        if "You're at full health, no need to drink one yet." in ROOM_TXT.innerText:
            max_hp_text = ''
        else:
            max_hp_text = "\nYou're at full health, no need to drink one yet."
        ROOM_TXT.innerText += max_hp_text
        
if __name__ == '__main__':
    game_start(0)