import pygame, random, sys,time,copy
from pygame.locals import *
from classes import *
from creatures import *

WINDOWWIDTH = 896
WINDOWHEIGHT = 504
TEXTCOLOR = (255,255,255)
BACKGROUNDCOLOR = (0,0,0)
FPS_COM = 50
FPS = 80
PLAYERMOVERATE = 5
room = False

def mouse_test():
    pygame.event.set_grab(True)
    pygame.mouse.set_visible(True)
    pos = pygame.mouse.get_pos()
    return pos

def plus_sign():
    plusImage = pygame.image.load('plus.png')
    plusRect= plusImage.get_rect()
    data = [plusImage,plusRect]
    return data

def level_up(player):
    font = pygame.font.SysFont('centaur', 20)
    plus = []
    stats = 10
    for i in range(5):
        plus.append(plus_sign())
        plus[i][1].topleft = (350,150+(i*17))
        windowSurface.blit(plus[i][0],plus[i][1])
    pygame.display.update()
    while stats != 0:
         for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()
         windowSurface.fill((0,0,0))
         i = 0
         while i != 5:
            windowSurface.blit(plus[i][0],plus[i][1])
            i += 1
         drawText('You are now lvl '+str(player[2].lvl)+'.  Please place 10 stats wherever you like.',font,windowSurface,200,125,TEXTCOLOR)
         drawText('Stamina: '+str(player[2].stamina),font,windowSurface,375,150,TEXTCOLOR)
         drawText('Wisdom: '+str(player[2].wisdom),font,windowSurface,375,167,TEXTCOLOR)
         drawText('Intellect: '+str(player[2].intellect),font,windowSurface,375,184,TEXTCOLOR)
         drawText('Dexterity: '+str(player[2].dexterity),font,windowSurface,375,201,TEXTCOLOR)
         drawText('Strength: '+str(player[2].strength),font,windowSurface,375,218,TEXTCOLOR)
         pygame.display.update()
         pressed = pygame.mouse.get_pressed()
         if pressed[0] == True:
             time.sleep(0.1)
             pos = mouse_test()
             if plus[0][1].collidepoint(pos):
                 stats -= 1
                 player[2].stamina += 1
             if plus[1][1].collidepoint(pos):
                 stats -= 1
                 player[2].wisdom += 1
             if plus[2][1].collidepoint(pos):
                 stats -= 1
                 player[2].intellect += 1
             if plus[3][1].collidepoint(pos):
                 stats -= 1
                 player[2].dexterity += 1
             if plus[4][1].collidepoint(pos):
                 stats -= 1
                 player[2].strength += 1
             windowSurface.fill((0,0,0))
             j = 0
             while j != 5:
                windowSurface.blit(plus[j][0],plus[j][1])
                j += 1
             drawText('You are now lvl '+str(player[2].lvl)+'.  Please place 10 stats wherever you like.',font,windowSurface,200,125,TEXTCOLOR)
             drawText('Stamina: '+str(player[2].stamina),font,windowSurface,375,150,TEXTCOLOR)
             drawText('Wisdom: '+str(player[2].wisdom),font,windowSurface,375,167,TEXTCOLOR)
             drawText('Intellect: '+str(player[2].intellect),font,windowSurface,375,184,TEXTCOLOR)
             drawText('Dexterity: '+str(player[2].dexterity),font,windowSurface,375,201,TEXTCOLOR)
             drawText('Strength: '+str(player[2].strength),font,windowSurface,375,218,TEXTCOLOR)
             pygame.display.update()
             player[2].health = player[2].stamina*10
             player[2].f_level()
         pygame.event.set_grab(False)
         
def damage(enemy,player,alive):
    enemy.health -= player.damage
    if(player.shield):
        if(player.shield < enemy.damage):
            enemy.damage -= player.shield
            player.shield = 0
        else:
            player.shield -= enemy.damage
            enemy.damage = 0
    if player.cls == 'warrior':
        if player.block == True:
            fnt = pygame.font.SysFont('centaur', 22)
            drawText('You BLOCKED the enemies attack and take '+str(player.lvl+25)+' less damage.',fnt,windowSurface,0,90,TEXTCOLOR)
            pygame.display.update()
            if (enemy.damage - player.lvl+25) >=0:
                player.health -= (enemy.damage - (player.lvl+25))
        else:
            player.health -= enemy.damage
    if player.cls == 'swashbuckler':
        if player.dodge == True:
            fnt = pygame.font.SysFont('centaur', 22)
            drawText('You DODGED the enemies attack.',fnt,windowSurface,0,90,TEXTCOLOR)
            pygame.display.update()
        else:
            player.health -= enemy.damage
    if player.cls == 'mage' or player.cls == 'warlock' or player.cls == 'cleric':
        player.health -= enemy.damage
    if enemy.health <= 0 and player.health > 0:
         LowHPSound.stop()
         enemy.f_death()
         player.health = player.health + enemy.stamina*2
         if player.health > (player.stamina*10):
             player.health = player.stamina*10
         player_alive = True
         enemy_alive = False
         combat = False
    elif player.health <= 0:
        player_alive = False
        enemy_alive = True
        combat = False
    else:
        player_alive = True
        enemy_alive = True
        combat = True
    alive =  [player_alive,enemy_alive,combat]
    return alive

def player_health(health,player,shield):
    playerhealth = str(health)
    healthlocation = player[1].topleft
    drawText(playerhealth,font,windowSurface,healthlocation[0]+25,healthlocation[1]-25,(255,0,0))
    if shield > 0:
        playershield = str(shield)
        drawText(playershield,font,windowSurface,healthlocation[0]+25,healthlocation[1]-50,(0,255,255))

def enemy_health(health,enemy):
    enemyhealth = str(health)
    healthlocation = enemy[1].topleft
    drawText(enemyhealth,font,windowSurface,healthlocation[0]+25,healthlocation[1]-25,(255,0,0))
        
def gameover():
    gameoverImage = pygame.image.load('gameover_.png')
    gameoverRect = gameoverImage.get_rect()
    data = [gameoverImage, gameoverRect]
    return data

def coin():
    coinImg = pygame.image.load('coin.png')
    coinRect = coinImg.get_rect()
    data = [coinImg,coinRect]
    return data

def exit_sign():
    img = pygame.image.load('exit.png')
    rct = img.get_rect()
    data = [img,rct]
    return data

def shop_pic():
    img = pygame.image.load('shop.png')
    rct = img.get_rect()
    data = [img,rct]
    return data
    
def cleric_empowerment():
    empImage = pygame.image.load('cleric_empowerment_dragonia.png')
    empRect = empImage.get_rect()
    data = [empImage,empRect]
    return data

def cleric_holyblow():
    hbImage = pygame.image.load('cleric_holyblow_dragonia.png')
    hbRect= hbImage.get_rect()
    data = [hbImage,hbRect]
    return data

def warlock_shield():
    shieldImage = pygame.image.load('warlock_bloodshield_dragonia.png')
    shieldRect = shieldImage.get_rect()
    data = [shieldImage,shieldRect]
    return data

def warlock_entropic():
    entImage = pygame.image.load('warlock_entropicassault_dragonia.png')
    entRect = entImage.get_rect()
    data = [entImage,entRect]
    return data

def warrior_tactics():
    tactImage = pygame.image.load('warrior_tactics_dragonia.png')
    tactRect = tactImage.get_rect()
    data = [tactImage,tactRect]
    return data

def mage_shield():
    shieldImage = pygame.image.load('mage_shield_dragonia.png')
    shieldRect = shieldImage.get_rect()
    data = [shieldImage,shieldRect]
    return data

def mage_fireball():
    fireballImage = pygame.image.load('mage_fireball_dragonia.png')
    fireballRect = fireballImage.get_rect()
    data = [fireballImage,fireballRect]
    return data

def mage_minion():
    minImage = pygame.image.load('mage_minion_dragonia.png')
    minRect = minImage.get_rect()
    data = [minImage,minRect]
    return data

def dragonia():
    dragImage = pygame.image.load('dragonia.png')
    dragRect = dragImage.get_rect()
    data = [dragImage,dragRect]
    return data

def alt_mage():
    altImage = pygame.image.load('mage_minion(alt)_dragonia.png')
    altRect = altImage.get_rect()
    data = [altImage,altRect]
    return data

def mage_with_minion(fireball,place,enemy_place,plyr,enemy,player,en_attack,min_attack):
    enemy = enemy_place
    minion = mage_minion()
    min_attack = True
    for i in range(16):
        mage_battle(place,enemy_place,plyr,enemy,player,en_attack,min_attack)
        minion[1].topleft = (220+(i*17),290)
        windowSurface.blit(minion[0], minion[1])
        pygame.display.update()
    mainClock.tick(FPS_COM)
    min_attack = False
    if fireball != []:
        for i in range(16):
            fireball[1].topleft = (220+(i*17),290)
            mage_battle(place,enemy_place,plyr,enemy,player,en_attack,min_attack)
            windowSurface.blit(fireball[0], fireball[1])
            pygame.display.update()
        mainClock.tick(FPS_COM)
    
def abilityone(ability1,place,enemy_place,plyr,enemy,player,en_attack,min_attack):
    enemy = enemy_place
    for i in range(16):
        if player[2].cls == 'mage':
            mage_battle(place,enemy_place,plyr,enemy,player,en_attack,min_attack)
            ability1[1].topleft = (220+(i*17),290)
            windowSurface.blit(ability1[0], ability1[1])
        elif player[2].cls == 'cleric':
            cleric_battle(place,enemy_place,plyr,enemy,player,en_attack)
            ability1[1].topleft = (220+(i*17),400)
            windowSurface.blit(ability1[0], ability1[1])
        elif player[2].cls == 'warlock':
            warlock_battle(place,enemy_place,plyr,enemy,player,en_attack)
            ability1[1].topleft = (220+(i*17),400)
            windowSurface.blit(ability1[0], ability1[1])
        pygame.display.update()
    #time.sleep(0.5)
    mainClock.tick(FPS_COM)
  
def default_attack(place,enemy_place,plyr,player,en_attack,min_attack):
    enemy = enemy_place
    for i in range(16):
        plyr[1].topleft = (200+(i*17),400)
        if player[2].cls == 'mage':
            mage_battle(place,enemy_place,plyr,enemy,player,en_attack,min_attack)
        elif player[2].cls == 'warrior':
            warrior_battle(place,enemy_place,plyr,enemy,player,en_attack)
        elif player[2].cls == 'cleric':
            cleric_battle(place,enemy_place,plyr,enemy,player,en_attack)
        elif player[2].cls == 'warlock':
            warlock_battle(place,enemy_place,plyr,enemy,player,en_attack)
        elif player[2].cls == 'swashbuckler':
            swashbuckler_battle(place,enemy_place,plyr,enemy,player,en_attack)
        pygame.display.update()
    mainClock.tick(FPS_COM)
    #time.sleep(0.5)
    plyr[1].topleft = (200,400)
    
def enemy_attack(place,enemy_place,plyr,player,en_attack,min_attack):
    enemy = enemy_place
    en_attack = True
    min_attack = False
    enemy[2].f_attack()
    for i in range(16):
        enemy[1].topleft = (500-(i*17),200)
        if player[2].cls == 'mage':
            mage_battle(place,enemy_place,plyr,enemy,player,en_attack,min_attack)  
        elif player[2].cls == 'warrior':
            warrior_battle(place,enemy_place,plyr,enemy,player,en_attack)
        elif player[2].cls == 'cleric':
            cleric_battle(place,enemy_place,plyr,enemy,player,en_attack)
        elif player[2].cls == 'warlock':
            warlock_battle(place,enemy_place,plyr,enemy,player,en_attack)
        elif player[2].cls == 'swashbuckler':
            swashbuckler_battle(place,enemy_place,plyr,enemy,player,en_attack)
        #enemy[1].topleft = (500-(i*5),200)
        #windowSurface.blit(enemy[0],enemy[1])    
        pygame.display.update()
    mainClock.tick(FPS_COM)
    enemy[1].topleft = (500,200)
    #time.sleep(0.5)
    en_attack = False
    
def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey(thing):
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # pressing escape quits
                    terminate()
                elif event.key == K_RETURN:
                    return False
                if thing == True:
                    if event.key == ord('r'):
                        return True

def playerHasHitEnemy(playerRect, the_enemies):
    i = 0
    while i != len(the_enemies):
        if playerRect.colliderect(the_enemies[i][1]):
            return i
        i += 1
    return -1

def drawText(text, font, surface, x, y, color):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def mage_battle(place,enemy_place,plyr,enemy,player,en_attack,min_attack):
    windowSurface.blit(place[0],place[1])
    windowSurface.blit(enemy_place[0],enemy_place[1])
    if player[2].minion > 0:
        plyralt = alt_mage()
        plyralt[1].topleft = (150,350)
        windowSurface.blit(plyralt[0],plyralt[1])
    else:
        windowSurface.blit(plyr[0],plyr[1])
    if player[2].shield != 0:
        shield = mage_shield()
        current_loc = plyr[1].topleft
        shield[1].topleft =  (current_loc[0]-50,current_loc[1]-50)
        windowSurface.blit(shield[0],shield[1])
    enemy_health(enemy[2].health,enemy_place)
    player_health(player[2].health,plyr,player[2].shield)
    pygame.display.update()
    
def warrior_battle(place,enemy_place,plyr,enemy,player,en_attack):
    windowSurface.blit(place[0],place[1])
    windowSurface.blit(enemy_place[0],enemy_place[1])
    windowSurface.blit(plyr[0],plyr[1])
    if player[2].tactics > 0:
        tact = warrior_tactics()
        current_loc = plyr[1].topleft
        tact[1].topleft = (current_loc[0]-50,current_loc[1]-50)
        windowSurface.blit(tact[0],tact[1])
    enemy_health(enemy[2].health,enemy_place)
    player_health(player[2].health,plyr,player[2].shield)
    pygame.display.update()
    
def cleric_battle(place,enemy_place,plyr,enemy,player,en_attack):
    windowSurface.blit(place[0],place[1])
    windowSurface.blit(enemy_place[0],enemy_place[1])
    windowSurface.blit(plyr[0],plyr[1])
    if player[2].empowered == 1:
        emp = cleric_empowerment()
        current_loc = plyr[1].topleft
        emp[1].topleft = (current_loc[0]-50,current_loc[1]-50)
        windowSurface.blit(emp[0],emp[1])
    enemy_health(enemy[2].health,enemy_place)
    player_health(player[2].health,plyr,player[2].shield)
    pygame.display.update()

def warlock_battle(place,enemy_place,plyr,enemy,player,en_attack):
    windowSurface.blit(place[0],place[1])
    windowSurface.blit(enemy_place[0],enemy_place[1])
    windowSurface.blit(plyr[0],plyr[1])
    if player[2].shield != 0:
        shield = warlock_shield()
        current_loc = plyr[1].topleft
        shield[1].topleft =  (current_loc[0]-50,current_loc[1]-50)
        windowSurface.blit(shield[0],shield[1])
    enemy_health(enemy[2].health,enemy_place)
    player_health(player[2].health,plyr,player[2].shield)
    pygame.display.update()

def swashbuckler_battle(place,enemy_place,plyr,enemy,player,en_attack):
    windowSurface.blit(place[0],place[1])
    windowSurface.blit(enemy_place[0],enemy_place[1])
    windowSurface.blit(plyr[0],plyr[1])
    enemy_health(enemy[2].health,enemy_place)
    player_health(player[2].health,plyr,player[2].shield)
    pygame.display.update()

def potions():
    potions = []
    pots = ['health_pot.png','strength_pot.png','dex_pot.png','int_pot.png','stam_pot.png']
    for x in range(5):
        img = pygame.image.load(pots[x])
        rect = img.get_rect()
        data = [img,rect]
        potions.append(data)
    return potions

def shop(player):
    exit_sn = exit_sign()
    exit_sn[1].topleft = (0,430)
    player[1].topleft = (0,30)
    windowSurface.fill(BACKGROUNDCOLOR)
    windowSurface.blit(player[0],player[1])
    player_health(player[2].health,player,player[2].shield)
    windowSurface.blit(exit_sn[0],exit_sn[1])
    pots = potions()
    for i in range(5):
        pots[i][1].topleft = (200+(i*100),150)
        windowSurface.blit(pots[i][0],pots[i][1])
    pygame.display.update()
    while True:
        windowSurface.fill(BACKGROUNDCOLOR)
        windowSurface.blit(player[0],player[1])
        player_health(player[2].health,player,player[2].shield)
        windowSurface.blit(exit_sn[0],exit_sn[1])
        for i in range(5):
            pots[i][1].topleft = (200+(i*100),150)
            windowSurface.blit(pots[i][0],pots[i][1])
        for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()
                if event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        terminate()
        pressed = pygame.mouse.get_pressed()
        pos = mouse_test()
        if pots[0][1].collidepoint(pos):
            fnt = pygame.font.SysFont('centaur', 22)
            drawText('Heals your character 50%.',fnt,windowSurface,pos[0]-50,pos[1],TEXTCOLOR)
        elif pots[1][1].collidepoint(pos):
            fnt = pygame.font.SysFont('centaur', 22)
            drawText('Gives your character 30 strength for 3 battles.',fnt,windowSurface,pos[0]-50,pos[1],TEXTCOLOR)
        elif pots[2][1].collidepoint(pos):
            fnt = pygame.font.SysFont('centaur', 22)
            drawText('Gives your character 30 dexterity for 3 battles.',fnt,windowSurface,pos[0]-50,pos[1],TEXTCOLOR)
        elif pots[3][1].collidepoint(pos):
            fnt = pygame.font.SysFont('centaur', 22)
            drawText('Gives your character 30 intellect for 3 battles.',fnt,windowSurface,pos[0]-50,pos[1],TEXTCOLOR)
        elif pots[4][1].collidepoint(pos):
            fnt = pygame.font.SysFont('centaur', 22)
            drawText('Gives your character 30 stamina for 3 battles.',fnt,windowSurface,pos[0]-50,pos[1],TEXTCOLOR)
        if pressed[0] == True:
            pos = mouse_test()
            if exit_sn[1].collidepoint(pos):
                break
        pygame.display.update()
    pygame.event.set_grab(False)
    #time.sleep(5)
    
def battle(place,player,enemy):
    alive = [True,True,True]
    if player[2].cls == 'mage':
        img = pygame.image.load('mage_dragonia.png')
        rect = img.get_rect()
        plyr = [img,rect]
    elif player[2].cls == 'warrior':
        img = pygame.image.load('warrior_dragonia.png')
        rect = img.get_rect()
        plyr = [img,rect]
        player[2].tactics = 0
    elif player[2].cls == 'cleric':
        img = pygame.image.load('cleric_dragonia.png')
        rect = img.get_rect()
        plyr = [img,rect]
    elif player[2].cls == 'warlock':
        img = pygame.image.load('warlock_dragonia.png')
        rect = img.get_rect()
        plyr = [img,rect]
    elif player[2].cls == 'swashbuckler':
        img = pygame.image.load('swashbuckler_dragonia.png')
        rect = img.get_rect()
        plyr = [img,rect]
        player[2].bleed = 0
    enemy_place = enemy
    ability1 = []
    plyr[1].topleft = (200,400)
    enemy_place[1].topleft = (500,200)
    enemy_place[0] = pygame.transform.scale(enemy[0],(300,330))
    en_attack = False
    min_attack = False
    flag = False
    while alive[2] == True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()   
                if event.key == ord('1'):
                    if room == True:
                        laugh.play()
                    else:
                        player[2].f_attack1()
                    if player[2].cls == 'mage':
                        fireball = mage_fireball()
                        if player[2].minion > 0:
                            mage_with_minion(fireball,place,enemy_place,plyr,enemy,player,en_attack,min_attack)
                        else:
                            abilityone(fireball,place,enemy_place,plyr,enemy,player,en_attack,min_attack)
                    if player[2].cls == 'cleric':
                        holyblow = cleric_holyblow()
                        abilityone(holyblow,place,enemy_place,plyr,enemy,player,en_attack,min_attack)
                    if player[2].cls == 'warrior':
                        default_attack(place,enemy_place,plyr,player,en_attack,min_attack)
                    if player[2].cls == 'warlock':
                        default_attack(place,enemy_place,plyr,player,en_attack,min_attack)
                    if player[2].cls == 'swashbuckler':
                        default_attack(place,enemy_place,plyr,player,en_attack,min_attack)
                    time.sleep(0.5)
                    enemy_attack(place,enemy_place,plyr,player,en_attack,min_attack)        
                    player[2].f_ability0()
                    enemy[2].f_ability0()
                    alive = damage(enemy[2],player[2],alive)
                    pygame.display.update()
                    time.sleep(1)

                if event.key == ord('2'):
                    if room == True:
                        laugh.play()
                    else:
                        player[2].f_attack2()
                    if player[2].cls == 'mage':
                        player[2].f_ability1()
                        fireball = []
                        if player[2].minion > 0:
                            mage_with_minion(fireball,place,enemy_place,plyr,enemy,player,en_attack,min_attack)
                        time.sleep(0.5)
                        enemy_attack(place,enemy_place,plyr,player,en_attack,min_attack)        
                        enemy[2].f_ability0()
                        alive = damage(enemy[2],player[2],alive)
                        pygame.display.update()
                        time.sleep(1)
                    if player[2].cls == 'cleric':
                        empower = cleric_empowerment()
                        empower[1].topleft = (150,350)
                        if player[2].empowered == 1:
                            flag = True
                        else:
                            player[2].empowered = 1
                            flag = False
                        time.sleep(0.5)
                        enemy_attack(place,enemy_place,plyr,player,en_attack,min_attack)
                        if flag != True:
                            player[2].empowered = 0
                        player[2].f_ability1()
                        enemy[2].f_ability0()
                        alive = damage(enemy[2],player[2],alive)
                        pygame.display.update()
                        time.sleep(1)
                    if player[2].cls == 'warrior':
                        tact = warrior_tactics()
                        tact[1].topleft = (150,350)
                        player[2].tactics = 1
                        time.sleep(0.5)
                        enemy_attack(place,enemy_place,plyr,player,en_attack,min_attack)        
                        player[2].f_ability1()
                        enemy[2].f_ability0()
                        alive = damage(enemy[2],player[2],alive)
                        pygame.display.update()
                        time.sleep(1)
                    if player[2].cls == 'warlock':
                        ent = warlock_entropic()
                        abilityone(ent,place,enemy_place,plyr,enemy,player,en_attack,min_attack)
                        time.sleep(0.5)
                        enemy_attack(place,enemy_place,plyr,player,en_attack,min_attack)        
                        player[2].f_ability1()
                        enemy[2].f_ability0()
                        alive = damage(enemy[2],player[2],alive)
                        pygame.display.update()
                        time.sleep(1)
                    if player[2].cls == 'swashbuckler':
                        default_attack(place,enemy_place,plyr,player,en_attack,min_attack)
                        time.sleep(0.5)
                        enemy_attack(place,enemy_place,plyr,player,en_attack,min_attack)        
                        player[2].f_ability1()
                        enemy[2].f_ability0()
                        alive = damage(enemy[2],player[2],alive)
                        pygame.display.update()
                        time.sleep(1)
                        
                if event.key == ord('3'):
                    if room == True:
                        laugh.play()
                    else:
                        player[2].f_attack3()
                    if player[2].cls == 'warrior':
                        default_attack(place,enemy_place,plyr,player,en_attack,min_attack)
                    if player[2].cls == 'mage':
                        fireball = []
                        mage_with_minion(fireball,place,enemy_place,plyr,enemy,player,en_attack,min_attack)
                    if player[2].cls == 'swashbuckler':
                        default_attack(place,enemy_place,plyr,player,en_attack,min_attack)
                    time.sleep(0.5)
                    enemy_attack(place,enemy_place,plyr,player,en_attack,min_attack)
                    player[2].f_ability2()
                    enemy[2].f_ability0()
                    alive = damage(enemy[2],player[2],alive)
                    pygame.display.update()
                    time.sleep(1)
                
                if event.key == ord('q'):
                    if player[2].health_pot >= 1:
                        player[2].f_potion()
                        player[2].health_pot -= 1
                        player[2].health += player[2].stamina*5
                        if player[2].health > player[2].stamina*10:
                            player[2].health = player[2].stamina*10
                        drawText('You healed to full!', font, windowSurface, 0, 0,(255,255,255))
                    else:
                        drawText('You have no potions left.',font,windowSurface,0,0,(255,255,255))
                    pygame.display.update()
                    time.sleep(1)
        if player[2].health < 30:
            LowHPSound.play(-1)
        else:
            LowHPSound.stop()
        if player[2].cls == 'mage':
            mage_battle(place,enemy_place,plyr,enemy,player,en_attack,min_attack)
        elif player[2].cls == 'warrior':
            warrior_battle(place,enemy_place,plyr,enemy,player,en_attack)
        elif player[2].cls == 'cleric':
            cleric_battle(place,enemy_place,plyr,enemy,player,en_attack)
        elif player[2].cls == 'warlock':
            warlock_battle(place,enemy_place,plyr,enemy,player,en_attack)
        elif player[2].cls == 'swashbuckler':
            swashbuckler_battle(place,enemy_place,plyr,enemy,player,en_attack)
        if alive[0] == True and alive[1] == False:
            player[2].lvl += 1
            level_up(player)
            #player_health(player[2].health,plyr,player[2].shield)
            pygame.display.update()
            time.sleep(1)
        #player_health(player[2].health,plyr,player[2].shield)
        pygame.display.update()
        mainClock.tick(FPS_COM)
    return alive

def pick_enemy(enemies):
    rand = random.randint(0,len(enemies)-1)
    enemyImage = pygame.image.load(enemies[rand])
    enemyRect = enemyImage.get_rect()
    if rand == 0:
        enemyType = ogre()
    elif rand == 1:
        enemyType = giant_snake()
    elif rand == 2:
        enemyType = gargoyle()
    elif rand == 3:
        enemyType = dragon()
    elif rand == 4:
        enemyType = cyclops()
    elif rand == 5:
        enemyType = gargantuan()
    elif rand == 6:
        enemyType = zombie()
    data = [enemyImage,enemyRect,enemyType]
    return data

def all_enemies(enemies,locations,difficulty,num):
    if difficulty == 1:
        rand = random.randint(2,3)
    elif difficulty == 2:
        rand = random.randint(5,7)
    elif difficulty == 3:
        rand = random.randint(7,9)
    all_enemies = []
    x = 0
    while x != rand:
        all_enemies.append(pick_enemy(enemies))
        loc = random.randint(0,len(locations[num])-1)
        #print len(locations[num])
        all_enemies[x][1].topleft = locations[num][loc]
        locations[num].remove(locations[num][loc])
        x += 1
    return all_enemies

def coin_drops():
    map_coins = []
    coins = []
    num = random.randint(0,5)
    locations = [(120,20),(240,20),(360,20),(480,20),(600,20),(720,20),(0,130),(120,130),(240,130),(360,130),(480,130),(600,130),(720,130),(0,260),(120,260),(240,260),(360,260),(480,260),(600,260),(720,260),(0,390),(120,390),(240,390),(360,390),(480,390),(600,390),(720,390)]
    for i in range(5):
        for j in range(num):
            thecoin = coin()
            thecoin.append(random.randint(1,5))
            thecoin[1].topleft = locations[random.randint(0,len(locations)-1)]
            coins.append(thecoin)
        map_coins.append(coins)
    return map_coins

def map_enemies(enemies,locations,difficulty):
    map_enemies = []
    for i in range(5):
        map_enemies.append(all_enemies(enemies,locations,difficulty,i))
    return map_enemies

def choose_difficulty():
    windowSurface.blit(dragonia[0],dragonia[1])
    drawText('Please Choose your difficulty',font,windowSurface,300,0,(0,0,0))
    drawText('Beginner(1)',font,windowSurface,300,25,(0,0,0))
    drawText('Normal(2)',font,windowSurface,300,50,(0,0,0))
    drawText('Expert(3)',font,windowSurface,300,75,(0,0,0))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()   
                if event.key == ord('1'):
                    return 1
                if event.key == ord('2'):
                    return 2
                if event.key == ord('3'):
                    return 3

def pick_hero(heroes):
    pygame.display.update()
    drawText('Welcome to Dragonia', font, windowSurface, 0, 0,(0,0,0))
    drawText('Mage(1)', font, windowSurface, 0, 30,(65,105,225))
    drawText('Warrior(2)',font,windowSurface,100, 30,(178,34,34))
    drawText('Cleric(3)',font,windowSurface,225, 30,(0,255,255))
    drawText('Warlock(4)',font,windowSurface,330, 30,(0,100,0))
    drawText('Swashbuckler(5)',font,windowSurface,470, 30,(0,200,100))
    pygame.display.update()
    choosing = True
    while choosing == True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()   
                if event.key == ord('1'):
                    #windowSurface.fill(BACKGROUNDCOLOR)
                    windowSurface.blit(dragonia[0],dragonia[1])
                    drawText('You chose Mage!',font,windowSurface,0,0,(0,0,0))
                    pygame.display.update()
                    time.sleep(1)
                    choice = 0
                    class_ = mage('Kripte')
                    choosing = False
                if event.key == ord('2'):
                    #windowSurface.fill(BACKGROUNDCOLOR)
                    windowSurface.blit(dragonia[0],dragonia[1])
                    drawText('You chose Warrior!',font,windowSurface,0,0,(0,0,0))
                    pygame.display.update()
                    time.sleep(1)
                    choice = 1
                    class_ = warrior('Kripte')
                    choosing = False
                if event.key == ord('3'):
                    #windowSurface.fill(BACKGROUNDCOLOR)
                    windowSurface.blit(dragonia[0],dragonia[1])
                    drawText('You chose Cleric!',font,windowSurface,0,0,(0,0,0))
                    pygame.display.update()
                    time.sleep(1)
                    choice = 2
                    class_ = cleric('Kripte')
                    choosing = False
                if event.key == ord('4'):
                    #windowSurface.fill(BACKGROUNDCOLOR)
                    windowSurface.blit(dragonia[0],dragonia[1])
                    drawText('You chose Warlock!',font,windowSurface,0,0,(0,0,0))
                    pygame.display.update()
                    time.sleep(1)
                    choice = 3
                    class_ = warlock('Kripte')
                    choosing = False
                if event.key == ord('5'):
                    #windowSurface.fill(BACKGROUNDCOLOR)
                    windowSurface.blit(dragonia[0],dragonia[1])
                    drawText('You chose Swashbuckler!',font,windowSurface,0,0,(0,0,0))
                    pygame.display.update()
                    time.sleep(1)
                    choice = 4
                    class_ = swashbuckler('Kripte')
                    choosing = False  
                    
    heroImage = pygame.image.load(heroes[choice])
    heroRect = heroImage.get_rect()
    data = [heroImage,heroRect,class_]
    return data

def class_abilities(player):
    windowSurface.fill(BACKGROUNDCOLOR)
    player[2].f_abilities()
    drawText('Press ENTER to begin.', font, windowSurface, 100, 0,(255,255,255))
    pygame.display.update()
    class_screen = True
    room = waitForPlayerToPressKey(class_screen)
    return room
    
def place():
    places = ['cave_dragonia.png','desert_dragonia.png','water.png','sun.png']
    rand = random.randint(0,len(places)-1)
    placeImage = pygame.image.load(places[rand])
    placeRect = placeImage.get_rect()
    place = [placeImage,placeRect]
    return place

def draw_enemies(the_enemies):
    i = 0
    while i != len(the_enemies):
        windowSurface.blit(the_enemies[i][0],the_enemies[i][1])
        i += 1
        #pygame.display.update()

def draw_potions(potions):
    drawText('Potions: {0}'.format(int(potions)),pygame.font.SysFont('centaur', 30),windowSurface,0,0,(255,255,255))
    
def loot(enemy):
    rand = random.randint(0,100)
    dropped = False
    if enemy[2].name == 'gargoyle':
        if rand >= 0 and rand < 15:
            lootImage = pygame.image.load('sword_dragonia.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'sword']
            dropped = True
        elif rand >= 15 and rand < 25:
            lootImage = pygame.image.load('belt_dragonia.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'belt']
            dropped = True
        elif rand >= 25 and rand < 27:
            lootImage = pygame.image.load('cloak_dragonia.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'cloak']
            dropped = True
        elif rand == 27:
            lootImage = pygame.image.load('legendary_dragonia.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'legendary']
            dropped = True
        elif rand >= 28 and rand < 34:
            lootImage = pygame.image.load('trinket_dragonia.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'trinket']
            dropped = True
        elif rand >= 34 and rand < 53:
            lootImage = pygame.image.load('air_essence.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'air']
            dropped = True
        elif rand >= 53 and rand < 70:
            lootImage = pygame.image.load('earth_essence.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'earth']
            dropped = True
        elif rand >= 70 and rand < 86:
            lootImage = pygame.image.load('fire_essence.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'fire']
            dropped = True
        elif rand >= 86 and rand <= 100:
            lootImage = pygame.image.load('water_essence.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'water']
            dropped = True
        else:
            dropped = False
    elif enemy[2].name == 'snake':
        if rand >= 0 and rand < 5:
            lootImage = pygame.image.load('sword_dragonia.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'sword']
            dropped = True
        elif rand >= 5 and rand < 25:
            lootImage = pygame.image.load('belt_dragonia.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'belt']
            dropped = True
        elif rand >= 25 and rand < 27:
            lootImage = pygame.image.load('cloak_dragonia.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'cloak']
            dropped = True
        elif rand == 27:
            lootImage = pygame.image.load('trinket_dragonia.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'trinket']
            dropped = True
        elif rand >= 28 and rand < 48:
            lootImage = pygame.image.load('air_essence.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'air']
            dropped = True
        elif rand >= 48 and rand < 66:
            lootImage = pygame.image.load('fire_essence.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'fire']
            dropped = True
        elif rand >= 66 and rand < 82:
            lootImage = pygame.image.load('earth_essence.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'earth']
            dropped = True
        elif rand >= 82 and rand <= 100:
            lootImage = pygame.image.load('water_essence.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'water']
            dropped = True
        else:
            dropped = False
    elif enemy[2].name == 'dragon':
        if rand >= 0 and rand < 40:
            lootImage = pygame.image.load('sword_dragonia.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'sword']
            dropped = True
        elif rand >= 40 and rand < 50:
            lootImage = pygame.image.load('belt_dragonia.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'belt']
            dropped = True
        elif rand >= 50 and rand < 57:
            lootImage = pygame.image.load('cloak_dragonia.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'cloak']
            dropped = True
        elif rand >= 58 and rand < 63:
            lootImage = pygame.image.load('legendary_dragonia.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'legendary']
            dropped = True
        elif rand >=63 and rand < 68:
            lootImage = pygame.image.load('trinket_dragonia.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'trinket']
            dropped = True
        elif rand >= 68 and rand < 76:
            lootImage = pygame.image.load('air_essence.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'air']
            dropped = True
        elif rand >= 76 and rand < 84:
            lootImage = pygame.image.load('fire_essence.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'fire']
            dropped = True
        elif rand >= 84 and rand < 92:
            lootImage = pygame.image.load('water_essence.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'water']
            dropped = True
        elif rand >= 92 and rand <= 100:
            lootImage = pygame.image.load('earth_essence.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'earth']
            dropped = True
        else:
            dropped = False
    elif enemy[2].name == 'ogre':
        if rand >= 0 and rand < 5:
            lootImage = pygame.image.load('sword_dragonia.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'sword']
            dropped = True
        elif rand >= 5 and rand < 25:
            lootImage = pygame.image.load('belt_dragonia.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'belt']
            dropped = True
        elif rand >= 25 and rand < 27:
            lootImage = pygame.image.load('cloak_dragonia.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'cloak']
            dropped = True
        elif rand == 27:
            lootImage = pygame.image.load('trinket_dragonia.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'trinket']
            dropped = True
        elif rand >= 28 and rand < 49:
            lootImage = pygame.image.load('air_essence.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'air']
            dropped = True
        elif rand >= 49 and rand < 67:
            lootImage = pygame.image.load('water_essence.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'water']
            dropped = True
        elif rand >= 67 and rand < 85:
            lootImage = pygame.image.load('fire_essence.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'fire']
            dropped = True
        elif rand >= 85 and rand <= 100:
            lootImage = pygame.image.load('earth_essence.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'earth']
            dropped = True
        else:
            dropped = False
    elif enemy[2].name == 'gargantuan':
        if rand >= 0 and rand < 15:
            lootImage = pygame.image.load('sword_dragonia.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'sword']
            dropped = True
        elif rand >= 15 and rand < 45:
            lootImage = pygame.image.load('belt_dragonia.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'belt']
            dropped = True
        elif rand >= 45 and rand < 48:
            lootImage = pygame.image.load('cloak_dragonia.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'cloak']
            dropped = True
        elif rand == 48:
            lootImage = pygame.image.load('legendary_dragonia.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'legendary']
            dropped = True
        elif rand >= 49 and rand < 55:
            lootImage = pygame.image.load('trinket_dragonia.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'trinket']
            dropped = True
        elif rand >= 55 and rand < 74:
            lootImage = pygame.image.load('water_essence.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'water']
            dropped = True
        elif rand >= 74 and rand < 83:
            lootImage = pygame.image.load('fire_essence.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'fire']
            dropped = True
        elif rand >= 83 and rand < 92:
            lootImage = pygame.image.load('earth_essence.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'earth']
            dropped = True
        elif rand >= 92 and rand <= 100:
            lootImage = pygame.image.load('air_essence.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'air']
            dropped = True
        else:
            dropped = False
    elif enemy[2].name == 'cyclops':
        if rand >= 0 and rand < 35:
            lootImage = pygame.image.load('sword_dragonia.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'sword']
            dropped = True
        elif rand >= 35 and rand < 45:
            lootImage = pygame.image.load('belt_dragonia.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'belt']
            dropped = True
        elif rand >= 45 and rand < 52:
            lootImage = pygame.image.load('cloak_dragonia.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'cloak']
            dropped = True
        elif rand >= 52 and rand < 58:
            lootImage = pygame.image.load('eye.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'eye']
            dropped = True
        elif rand >= 58 and rand < 60:
            lootImage = pygame.image.load('legendary_dragonia.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'legendary']
            dropped = True
        elif rand >=60 and rand < 65:
            lootImage = pygame.image.load('trinket_dragonia.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'trinket']
            dropped = True
        elif rand >= 65 and rand < 74:
            lootImage = pygame.image.load('water_essence.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'water']
            dropped = True
        elif rand >= 74 and rand < 83:
            lootImage = pygame.image.load('fire_essence.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'fire']
            dropped = True
        elif rand >= 83 and rand < 92:
            lootImage = pygame.image.load('earth_essence.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'earth']
            dropped = True
        elif rand >= 92 and rand <= 100:
            lootImage = pygame.image.load('air_essence.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'air']
            dropped = True
        else:
            dropped = False
    elif enemy[2].name == 'zombie':
        if rand >= 0 and rand < 4:
            lootImage = pygame.image.load('sword_dragonia.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'sword']
            dropped = True
        elif rand >= 4 and rand < 25:
            lootImage = pygame.image.load('belt_dragonia.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'belt']
            dropped = True
        elif rand >= 25 and rand < 26:
            lootImage = pygame.image.load('cloak_dragonia.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'cloak']
            dropped = True
        elif rand >= 26 and rand < 28:
            lootImage = pygame.image.load('trinket_dragonia.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'trinket']
            dropped = True
        elif rand >= 28 and rand < 49:
            lootImage = pygame.image.load('air_essence.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'air']
            dropped = True
        elif rand >= 49 and rand < 67:
            lootImage = pygame.image.load('water_essence.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'water']
            dropped = True
        elif rand >= 67 and rand < 85:
            lootImage = pygame.image.load('fire_essence.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'fire']
            dropped = True
        elif rand >= 85 and rand <= 100:
            lootImage = pygame.image.load('earth_essence.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'earth']
            dropped = True
        else:
            dropped = False
    if dropped == False:
        lootImage = pygame.image.load('sword_dragonia.png')
        lootRect = lootImage.get_rect()
        data = [lootImage,lootRect,False,'Nothing']
    return data

def choose_map(maps,num):
    MapImage = pygame.image.load(maps[num])
    MapRect = MapImage.get_rect()
    data = [MapImage,MapRect]
    return data

pygame.init()
pygame.FULLSCREEN
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Dragonia')
pygame.display.set_icon(pygame.image.load('dragonia!.png'))
# set up fonts
font = pygame.font.SysFont('centaur', 30)

# set up sounds
DeathSound = pygame.mixer.Sound('death.wav')
laugh = pygame.mixer.Sound('laugh.wav')
LowHPSound = pygame.mixer.Sound('low_hp.wav')


#enemy locations
locations = [(120,20),(240,20),(360,20),(480,20),(600,20),(720,20),(0,130),(120,130),(240,130),(360,130),(480,130),(600,130),(720,130),(0,260),(120,260),(240,260),(360,260),(480,260),(600,260),(720,260),(0,390),(120,390),(240,390),(360,390),(480,390),(600,390),(720,390)]
#enemy setup
enemies = ['ogre.png','snake.png','gargoyle_dragonia.png','dragon.png','cyclops_dragonia.png','gargantuan_dragonia.png','zombie_dragonia.png']
#enemy = pick_enemy(enemies)

#set up load screen
#dragonia = dragonia()
#test
#the_enemies = all_enemies(enemies,locations)
#topScore = 0
bg_map = ['default.png','map_up.png','map_down.png','map_left.png','map_right.png']
the_shop = shop_pic()
the_shop[1].topleft = (400,180)
cur_map = [[],[]]
cur_map[0] = choose_map(bg_map,0)
cur_map[1] = 0
dragonia = dragonia()
windowSurface.blit(dragonia[0],dragonia[1])
while True:
    # set up the start of the game
    drop = False
    default_locs = [(120,20),(240,20),(360,20),(480,20),(600,20),(720,20),(0,130),(120,130),(240,130),(360,130),(480,130),(600,130),(720,130),(0,260),(120,260),(240,260),(360,260),(480,260),(600,260),(720,260),(0,390),(120,390),(240,390),(360,390),(480,390),(600,390),(720,390)]
    up_locs = [(120,20),(240,20),(360,20),(480,20),(600,20),(720,20),(0,130),(120,130),(240,130),(360,130),(480,130),(600,130),(720,130),(0,260),(120,260),(240,260),(360,260),(480,260),(600,260),(720,260),(0,390),(120,390),(240,390),(360,390),(480,390),(600,390),(720,390)]
    down_locs = [(120,20),(240,20),(360,20),(480,20),(600,20),(720,20),(0,130),(120,130),(240,130),(360,130),(480,130),(600,130),(720,130),(0,260),(120,260),(240,260),(360,260),(480,260),(600,260),(720,260),(0,390),(120,390),(240,390),(360,390),(480,390),(600,390),(720,390)]
    left_locs = [(120,20),(240,20),(360,20),(480,20),(600,20),(720,20),(0,130),(120,130),(240,130),(360,130),(480,130),(600,130),(720,130),(0,260),(120,260),(240,260),(360,260),(480,260),(600,260),(720,260),(0,390),(120,390),(240,390),(360,390),(480,390),(600,390),(720,390)]
    right_locs = [(120,20),(240,20),(360,20),(480,20),(600,20),(720,20),(0,130),(120,130),(240,130),(360,130),(480,130),(600,130),(720,130),(0,260),(120,260),(240,260),(360,260),(480,260),(600,260),(720,260),(0,390),(120,390),(240,390),(360,390),(480,390),(600,390),(720,390)]
    map_locations = [default_locs,up_locs,down_locs,left_locs,right_locs]
    score = 0
    moveLeft = moveRight = moveUp = moveDown = False
    pygame.mixer.music.load('background_.ogg')
    pygame.mixer.music.play(-1, 0.0)
    heroes = ['mage_dragonia.png','warrior_dragonia.png','cleric_dragonia.png','warlock_dragonia.png','swashbuckler_dragonia.png']
    #windowSurface.fill(BACKGROUNDCOLOR)
    windowSurface.blit(dragonia[0],dragonia[1])
    player = pick_hero(heroes)
    player[1].topleft = (0,20)
    difficulty = choose_difficulty()
    room = class_abilities(player)
    coins = coin_drops()
    if room == True:
        pygame.mixer.music.stop()
        pygame.mixer.music.load('room_music.wav')
        pygame.mixer.music.play(-1, 0.0)
    the_map_enemies =  map_enemies(enemies,map_locations,difficulty)
    you_win = False
    leveled = False
    while True: # the game loop runs while the game part is playing
        #score += 1 # increase score

       
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == K_LEFT or event.key == ord('a'):
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == ord('w'):
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == ord('s'):
                    moveUp = False
                    moveDown = True

            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                        terminate()
                if event.key == K_LEFT or event.key == ord('a'):
                    moveLeft = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveRight = False
                if event.key == K_UP or event.key == ord('w'):
                    moveUp = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = False

        # Move the player around.
        if moveLeft and player[1].left > 0:
            player[1].move_ip(-1 * PLAYERMOVERATE, 0)
        elif moveLeft and player[1].left <= 0 and cur_map[1] == 0:
            cur_map[0] = choose_map(bg_map,3)
            cur_map[1] = 3
            curlc = player[1].topleft
            player[1].topleft = (curlc[0]+794,curlc[1])
        elif moveLeft and player[1].left <= 0 and cur_map[1] == 4:
            cur_map[0] = choose_map(bg_map,0)
            cur_map[1] = 0
            curlc = player[1].topleft
            player[1].topleft = (curlc[0]+794,curlc[1])
        if moveRight and player[1].right < WINDOWWIDTH:
            player[1].move_ip(PLAYERMOVERATE, 0)
        elif moveRight and player[1].right >= WINDOWWIDTH and cur_map[1] == 3:
            cur_map[0] = choose_map(bg_map,0)
            cur_map[1] = 0
            curlc = player[1].topleft
            player[1].topleft = (curlc[0]-794,curlc[1])
        elif moveRight and player[1].right >= WINDOWWIDTH and cur_map[1] == 0:
            cur_map[0] = choose_map(bg_map,4)
            cur_map[1] = 4
            curlc = player[1].topleft
            player[1].topleft = (curlc[0]-794,curlc[1])
        if moveUp and player[1].top > 0:
            player[1].move_ip(0, -1 * PLAYERMOVERATE)
        elif moveUp and player[1].top <= 0 and cur_map[1] == 0:
            cur_map[0] = choose_map(bg_map,1)
            cur_map[1] = 1
            curlc = player[1].topleft
            player[1].topleft = (curlc[0],curlc[1]+392)
        elif moveUp and player[1].top <= 0 and cur_map[1] == 2:
            cur_map[0] = choose_map(bg_map,0)
            cur_map[1] = 0
            curlc = player[1].topleft
            player[1].topleft = (curlc[0],curlc[1]+392)
        if moveDown and player[1].bottom < WINDOWHEIGHT:
            player[1].move_ip(0, PLAYERMOVERATE)
        elif moveDown and player[1].bottom >= WINDOWHEIGHT and cur_map[1] == 0:
            cur_map[0] = choose_map(bg_map,2)
            cur_map[1] = 2
            curlc = player[1].topleft
            player[1].topleft = (curlc[0],curlc[1]-392)
        elif moveDown and player[1].bottom >= WINDOWHEIGHT and cur_map[1] == 1:
            cur_map[0] = choose_map(bg_map,0)
            cur_map[1] = 0
            curlc = player[1].topleft
            player[1].topleft = (curlc[0],curlc[1]-392)

       
        # Draw the game world on the window.
        #windowSurface.fill(BACKGROUNDCOLOR)
        windowSurface.blit(cur_map[0][0],cur_map[0][1])
        if cur_map[1] == 0:
            windowSurface.blit(the_shop[0],the_shop[1])
        for z in range(len(coins[cur_map[1]])):
            windowSurface.blit(coins[cur_map[1]][z][0], coins[cur_map[1]][z][1])
        # Draw the player's rectangle
        windowSurface.blit(player[0], player[1])
        draw_enemies(the_map_enemies[cur_map[1]])
        if drop != False:
                windowSurface.blit(the_drop[0],the_drop[1])
                #time.sleep(2)
        # add health above enemies and players
        player_health(player[2].health,player,player[2].shield)
        if cur_map[1] == 0 and player[1].colliderect(the_shop[1]):
            moveLeft = moveRight = moveUp = moveDown = False
            shop(player)
        j = 0
        for x in range(5):
            while j!= len(the_map_enemies[x]):
                if player[2].lvl > 1 and leveled == True:
                    the_map_enemies[x][j][2].health += player[2].lvl*25*difficulty
                    if difficulty == 1:
                        the_map_enemies[x][j][2].mod = 0.75
                    elif difficulty == 3:
                        the_map_enemies[x][j][2].mod = 1.25
                    the_map_enemies[x][j][2].miss -= 1
                j += 1
            j = 0
        leveled = False
        for y in range(len(the_map_enemies[cur_map[1]])):
            enemy_health(the_map_enemies[cur_map[1]][y][2].health,the_map_enemies[cur_map[1]][y])
        draw_potions(player[2].health_pot)
        if player[2].shield != 0:
                if player[2].cls == 'mage':
                    ability2 = mage_shield()
                elif player[2].cls == 'warlock':
                    ability2 = warlock_shield()
                current_loc = player[1].topleft
                ability2[1].topleft =  (current_loc[0]-50,current_loc[1]-50)
                windowSurface.blit(ability2[0],ability2[1])
                
        # Check if any of the enemies have hit the player.
        current_enemy = playerHasHitEnemy(player[1], the_map_enemies[cur_map[1]])
        if drop == True:
            picked_up_loot = player[1].colliderect(the_drop[1])
            if picked_up_loot:
                drop = False
                if the_drop[3] == 'sword':
                    drawText('You found a Sword!',font,windowSurface,300,250,(0,0,0))
                    drawText('Press ENTER to continue!',font,windowSurface,0,25,(0,0,0))
                    pygame.display.update()
                    moveLeft = moveRight = moveUp = moveDown = False
                    waitForPlayerToPressKey(False)
                    player[2].f_sword()
                if the_drop[3] == 'belt':
                    drawText('You found a Belt!',font,windowSurface,300,250,(0,0,0))
                    drawText('Press ENTER to continue!',font,windowSurface,0,25,(0,0,0))
                    pygame.display.update()
                    moveLeft = moveRight = moveUp = moveDown = False
                    waitForPlayerToPressKey(False)
                    player[2].f_belt()
                if the_drop[3] == 'cloak':
                    drawText('You found a Cloak!',font,windowSurface,300,250,(0,0,0))
                    drawText('Press ENTER to continue!',font,windowSurface,0,25,(0,0,0))
                    pygame.display.update()
                    moveLeft = moveRight = moveUp = moveDown = False
                    waitForPlayerToPressKey(False)
                    player[2].f_cloak()
                if the_drop[3] == 'eye':
                    drawText('You found the Cyclops\' eye!',font,windowSurface,300,250,(0,0,0))
                    drawText('Press ENTER to continue!',font,windowSurface,0,25,(0,0,0))
                    pygame.display.update()
                    moveLeft = moveRight = moveUp = moveDown = False
                    waitForPlayerToPressKey(False)
                    player[2].f_eye()
                if the_drop[3] == 'legendary':
                    drawText('You found a LEGENDARY weapon.',font,windowSurface,300,250,(0,0,0))
                    drawText('Press ENTER to continue!',font,windowSurface,0,25,(0,0,0))
                    pygame.display.update()
                    moveLeft = moveRight = moveUp = moveDown = False
                    waitForPlayerToPressKey(False)
                    player[2].f_legendary_weapon()
                if the_drop[3] == 'trinket':
                    drawText('You found a SHINY Ring.',font,windowSurface,300,250,(0,0,0))
                    drawText('Press ENTER to continue!',font,windowSurface,0,25,(0,0,0))
                    pygame.display.update()
                    moveLeft = moveRight = moveUp = moveDown = False
                    waitForPlayerToPressKey(False)
                    player[2].f_trinket()
                if the_drop[3] == 'air':
                    drawText('You found an Air Essence.',font,windowSurface,300,250,(0,0,0))
                    drawText('Press ENTER to continue!',font,windowSurface,0,25,(0,0,0))
                    pygame.display.update()
                    moveLeft = moveRight = moveUp = moveDown = False
                    waitForPlayerToPressKey(False)
                    player[2].f_air()
                if the_drop[3] == 'earth':
                    drawText('You found an Earth Essence.',font,windowSurface,300,250,(0,0,0))
                    drawText('Press ENTER to continue!',font,windowSurface,0,25,(0,0,0))
                    pygame.display.update()
                    moveLeft = moveRight = moveUp = moveDown = False
                    waitForPlayerToPressKey(False)
                    player[2].f_earth()
                if the_drop[3] == 'fire':
                    drawText('You found a Fire Essence.',font,windowSurface,300,250,(0,0,0))
                    drawText('Press ENTER to continue!',font,windowSurface,0,25,(0,0,0))
                    pygame.display.update()
                    moveLeft = moveRight = moveUp = moveDown = False
                    waitForPlayerToPressKey(False)
                    player[2].f_fire()
                if the_drop[3] == 'water':
                    drawText('You found a Water Essence.',font,windowSurface,300,250,(0,0,0))
                    drawText('Press ENTER to continue!',font,windowSurface,0,25,(0,0,0))
                    pygame.display.update()
                    moveLeft = moveRight = moveUp = moveDown = False
                    waitForPlayerToPressKey(False)
                    player[2].f_water()
        player_health(player[2].health,player,player[2].shield)
        pygame.display.update()
        if current_enemy != -1:
            loot_drop = the_map_enemies[cur_map[1]][current_enemy][1].topleft
            loot_drop = (loot_drop[0]+20,loot_drop[1]+20)
            moveLeft = moveRight = moveUp = moveDown = False
            drawText('You have encountered an enemy! Prepare to fight!',font,windowSurface,0,0,(0,0,0))
            pygame.display.update()
            time.sleep(1)
            alive = battle(place(),player,the_map_enemies[cur_map[1]][current_enemy])
            if alive[0] == False:
                break
            elif alive[1] == False:
                #print the_enemies
                #print current_enemy
                #print the_enemies[current_enemy]
                the_drop = loot(the_map_enemies[cur_map[1]][current_enemy])
                if the_drop[2] == True:
                    drop = True
                    the_drop[1].topleft = loot_drop
                else:
                    drop = False
                the_map_enemies[cur_map[1]].remove(the_map_enemies[cur_map[1]][current_enemy])
                leveled = True
                if the_map_enemies == []:
                    you_win = True
                    break
            LowHPSound.stop()
            draw_enemies(the_map_enemies[1])
            if drop != False:
                windowSurface.blit(the_drop[0],the_drop[1])
                #time.sleep(2)
            windowSurface.blit(player[0], player[1])
            if player[2].shield != 0:
                if player[2].cls == 'mage':
                    ability2 = mage_shield()
                elif player[2].cls == 'warlock':
                    ability2 = warlock_shield()
                current_loc = player[1].topleft
                ability2[1].topleft =  (current_loc[0]-50,current_loc[1]-50)
                windowSurface.blit(ability2[0],ability2[1])
        pygame.display.update()   
        mainClock.tick(FPS)

    # Stop the game and show the "Game Over" screen.
    if you_win == True:
        windowSurface.fill((0,0,0))
        drawText('You have slain all the enemies!', font, windowSurface, 0, 0,(255,255,255))
        drawText('Press ENTER to start a new game', font, windowSurface, 0, 30,(255,255,255))
        pygame.display.update()
        waitForPlayerToPressKey(False)
    else:
        pygame.mixer.music.stop()
        #gameOverSound.play()
        LowHPSound.stop()
        DeathSound.play()
        windowSurface.fill((255,0,0))
        gover = gameover()
        windowSurface.blit(gover[0],gover[1])
        drawText('GAME OVER', font, windowSurface, 0, 0,(0,0,0))
        drawText('Press ENTER to start a new game.', font, windowSurface, 0, 30,(0,0,0))
        pygame.display.update()
        waitForPlayerToPressKey(False)
        #gameOverSound.stop()
        DeathSound.stop()
    



