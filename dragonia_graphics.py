import pygame, random, sys,time,copy
from pygame.locals import *
from classes import *
from creatures import *

WINDOWWIDTH = 896
WINDOWHEIGHT = 504
TEXTCOLOR = (255,255,255)
BACKGROUNDCOLOR = (0,0,0)
FPS = 60
PLAYERMOVERATE = 5

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
    font = pygame.font.SysFont('centaur', 15)
    plus = []
    stats = 5
    i = 0
    while i != 5:
        plus.append(plus_sign())
        plus[i][1].topleft = (300,150+(i*17))
        windowSurface.blit(plus[i][0],plus[i][1])
        i += 1
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
         drawText('You are now lvl '+str(player[2].lvl)+'.  Please place 5 stats wherever you like.',font,windowSurface,200,125,TEXTCOLOR)
         drawText('Stamina: '+str(player[2].stamina),font,windowSurface,320,150,TEXTCOLOR)
         drawText('Wisdom: '+str(player[2].wisdom),font,windowSurface,320,167,TEXTCOLOR)
         drawText('Intellect: '+str(player[2].intellect),font,windowSurface,320,184,TEXTCOLOR)
         drawText('Dexterity: '+str(player[2].dexterity),font,windowSurface,320,201,TEXTCOLOR)
         drawText('Strength: '+str(player[2].strength),font,windowSurface,320,218,TEXTCOLOR)
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
             drawText('You are now lvl '+str(player[2].lvl)+'.  Please place 5 stats wherever you like.',font,windowSurface,200,125,TEXTCOLOR)
             drawText('Stamina: '+str(player[2].stamina),font,windowSurface,320,150,TEXTCOLOR)
             drawText('Wisdom: '+str(player[2].wisdom),font,windowSurface,320,167,TEXTCOLOR)
             drawText('Intellect: '+str(player[2].intellect),font,windowSurface,320,184,TEXTCOLOR)
             drawText('Dexterity: '+str(player[2].dexterity),font,windowSurface,320,201,TEXTCOLOR)
             drawText('Strength: '+str(player[2].strength),font,windowSurface,320,218,TEXTCOLOR)
             pygame.display.update()
             player[2].health = player[2].stamina*10
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
    player.health -= enemy.damage
    if enemy.health <= 0 and player.health > 0:
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

def dragonia():
    dragonImage = pygame.image.load('dragonia.png')
    dragonRect = dragonImage.get_rect()
    data = [dragonImage,dragonRect]
    return data

def mage_minion():
    minImage = pygame.image.load('mage_minion_dragonia.png')
    minRect = minImage.get_rect()
    data = [minImage,minRect]
    return data

def alt_mage():
    altImage = pygame.image.load('mage_minion(alt)_dragonia.png')
    altRect = altImage.get_rect()
    data = [altImage,altRect]
    return data

def mage_with_minion(fireball,place,enemy_place,plyr,enemy,player):
    minion = mage_minion()
    for i in range(6):
        minion[1].topleft = (220+(i*50),290)
        windowSurface.blit(place[0],place[1])
        windowSurface.blit(enemy_place[0],enemy_place[1])
        windowSurface.blit(plyr[0],plyr[1])
        windowSurface.blit(minion[0], minion[1])
        enemy_health(enemy[2].health,enemy_place)
        player_health(player[2].health,plyr,player[2].shield)
        if player[2].shield != 0:
            shield = mage_shield()
            shield[1].topleft = (150,350)
            windowSurface.blit(shield[0],shield[1])
        pygame.display.update()
        mainClock.tick(10)
    if fireball != []:
        for i in range(6):
            fireball[1].topleft = (220+(i*50),290)
            windowSurface.blit(place[0],place[1])
            windowSurface.blit(enemy_place[0],enemy_place[1])
            windowSurface.blit(plyr[0],plyr[1])
            windowSurface.blit(fireball[0], fireball[1])
            enemy_health(enemy[2].health,enemy_place)
            player_health(player[2].health,plyr,player[2].shield)
            if player[2].shield != 0:
                shield = mage_shield()
                shield[1].topleft = (150,350)
                windowSurface.blit(shield[0],shield[1])
            pygame.display.update()
            mainClock.tick(10)
        
def abilityone(ability1,place,enemy_place,plyr,enemy,player):
    i = 0
    while i != 6:
        if player[2].cls == 'mage':
            ability1[1].topleft = (220+(i*50),290)
        elif player[2].cls == 'cleric':
            ability1[1].topleft = (220+(i*50),400)
        elif player[2].cls == 'warlock':
            ability1[1].topleft = (220+(i*50),400)
        windowSurface.blit(place[0],place[1])
        windowSurface.blit(enemy_place[0],enemy_place[1])
        windowSurface.blit(plyr[0],plyr[1])
        windowSurface.blit(ability1[0], ability1[1])
        enemy_health(enemy[2].health,enemy_place)
        player_health(player[2].health,plyr,player[2].shield)
        if player[2].cls == 'cleric':
            if player[2].empowered == 1:
                ability2 = cleric_empowerment()
                ability2[1].topleft = (150,350)
                windowSurface.blit(ability2[0],ability2[1])
        if player[2].shield != 0:
            if player[2].cls == 'mage':
                ability2 = mage_shield()
            elif player[2].cls == 'warlock':
                ability2 = warlock_shield()
            ability2[1].topleft = (150,350)
            windowSurface.blit(ability2[0],ability2[1])
        pygame.display.update()
        mainClock.tick(10)
        #time.sleep(0.1)
        i += 1

def enemy_attack(place,enemy_place,plyr,player):
    #i = 0
    enemy = enemy_place
    for i in range(6):
        windowSurface.blit(place[0],place[1])
        if player[2].minion > 0:
            plyralt = alt_mage()
            plyralt[1].topleft = (150,350)
            windowSurface.blit(plyralt[0],plyralt[1])
        else:
            windowSurface.blit(plyr[0],plyr[1])
        enemy[1].topleft = (500-(i*50),200)
        windowSurface.blit(enemy[0],enemy[1])
        enemy_health(enemy[2].health,enemy)
        player_health(player[2].health,plyr,player[2].shield)
        if player[2].cls == 'warrior':
            if player[2].tactics > 0:
                tact = warrior_tactics()
                tact[1].topleft = (150,350)
                windowSurface.blit(tact[0],tact[1])
        if player[2].cls == 'cleric':
            if player[2].empowered == 1:
                ability2 = cleric_empowerment()
                ability2[1].topleft = (150,350)
                windowSurface.blit(ability2[0],ability2[1])
        if player[2].shield != 0:
            if player[2].cls == 'mage':
                ability2 = mage_shield()
            elif player[2].cls == 'warlock':
                ability2 = warlock_shield()
            ability2[1].topleft = (150,350)
            windowSurface.blit(ability2[0],ability2[1])
        i += 1
        pygame.display.update()
        #time.sleep(0.1)
        mainClock.tick(10)
    enemy[1].topleft = (500,200)
        
def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # pressing escape quits
                    terminate()
                elif event.key == K_RETURN:
                    return

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
    #print textrect
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

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
    elif player[2].cls == 'cleric':
        img = pygame.image.load('cleric_dragonia.png')
        rect = img.get_rect()
        plyr = [img,rect]
    elif player[2].cls == 'warlock':
        img = pygame.image.load('warlock_dragonia.png')
        rect = img.get_rect()
        plyr = [img,rect]
    enemy_place = enemy
    ability1 = []
    plyr[1].topleft = (200,400)
    enemy_place[1].topleft = (500,200)
    enemy_place[0] = pygame.transform.scale(enemy[0],(300,330))
#    player_place = player
##    enemy_place = enemy
##    player_place[1].topleft = (200,400)
##    enemy_place[1].topleft = (500,200)
##    enemy_place[0] = pygame.transform.scale(enemy[0],(300,330))
    if player[2].cls == 'mage':
        ability2 = mage_shield()
        ability2[1].topleft = (150,350)
    if player[2].cls == 'warlock':
        ability2 = warlock_shield()
        ability2[1].topleft = (150,350)
    if player[2].cls == 'warrior':
        if player[2].tactics > 0:
            player[2].tactics = 0
    while alive[2] == True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()   
                if event.key == ord('1'):
                    if player[2].cls == 'mage':
                        fireball = mage_fireball()
                        if player[2].minion > 0:
                            mage_with_minion(fireball,place,enemy_place,plyr,enemy,player)
                            plyralt = alt_mage()
                            plyralt[1].topleft = (150,350)
                        else:
                            abilityone(fireball,place,enemy_place,plyr,enemy,player)
                    if player[2].cls == 'cleric':
                        holyblow = cleric_holyblow()
                        abilityone(holyblow,place,enemy_place,plyr,enemy,player)
                    windowSurface.blit(place[0],place[1])
                    windowSurface.blit(enemy_place[0],enemy_place[1])
                    if player[2].minion > 0:
                        windowSurface.blit(plyralt[0],plyralt[1])
                    else:
                        windowSurface.blit(plyr[0],plyr[1])
                    enemy_health(enemy[2].health,enemy_place)
                    player_health(player[2].health,plyr,player[2].shield)
                    if player[2].cls == 'warrior':
                        if player[2].tactics > 0:
                            tact = warrior_tactics()
                            tact[1].topleft = (150,350)
                            windowSurface.blit(tact[0],tact[1])
                    enemy_attack(place,enemy_place,plyr,player)        
                    player[2].f_ability0()
                    enemy[2].f_ability0()
##                    if player[2].shield != 0:
##                        windowSurface.blit(ability2[0],ability2[1])
                    alive = damage(enemy[2],player[2],alive)
                    pygame.display.update()
                    time.sleep(1)

                if event.key == ord('2'):
                    if player[2].cls == 'mage':
                        ability2 = mage_shield()
                        ability2[1].topleft = (150,350)
                        windowSurface.blit(place[0],place[1])
                        windowSurface.blit(enemy_place[0],enemy_place[1])
                        fireball = []
                        if player[2].minion > 0:
                            mage_with_minion(fireball,place,enemy_place,plyr,enemy,player)
                            plyralt = alt_mage()
                            plyralt[1].topleft = (150,350)
                        if player[2].minion > 0:
                            windowSurface.blit(plyralt[0],plyralt[1])
                        else:
                            windowSurface.blit(plyr[0],plyr[1])
                        enemy_attack(place,enemy_place,plyr,player)
                        player[2].f_ability1()
                        enemy[2].f_ability0()
                        pygame.display.update()
                    if player[2].cls == 'cleric':
                        empower = cleric_empowerment()
                        empower[1].topleft = (150,350)
                        windowSurface.blit(place[0],place[1])
                        windowSurface.blit(enemy_place[0],enemy_place[1])
                        windowSurface.blit(plyr[0],plyr[1])
                        enemy_health(enemy[2].health,enemy_place)
                        player_health(player[2].health,plyr,player[2].shield)
                        windowSurface.blit(empower[0],empower[1])
                        enemy_attack(place,enemy_place,plyr,player)
                        player[2].f_ability1()
                        enemy[2].f_ability0()
                        pygame.display.update()
                    if player[2].cls == 'warrior':
                        tact = warrior_tactics()
                        tact[1].topleft = (150,350)
                        windowSurface.blit(place[0],place[1])
                        windowSurface.blit(enemy_place[0],enemy_place[1])
                        windowSurface.blit(plyr[0],plyr[1])
                        enemy_health(enemy[2].health,enemy_place)
                        player_health(player[2].health,plyr,player[2].shield)
                        windowSurface.blit(tact[0],tact[1])
                        enemy_attack(place,enemy_place,plyr,player)
                        player[2].f_ability1()
                        enemy[2].f_ability0()
                        pygame.display.update()
                    if player[2].cls == 'warlock':
                        ent = warlock_entropic()
                        abilityone(ent,place,enemy_place,plyr,enemy,player)
                        windowSurface.blit(place[0],place[1])
                        windowSurface.blit(enemy_place[0],enemy_place[1])
                        windowSurface.blit(plyr[0],plyr[1])
                        enemy_health(enemy[2].health,enemy_place)
                        player_health(player[2].health,plyr,player[2].shield)
                        enemy_attack(place,enemy_place,plyr,player)
                        player[2].f_ability1()
                        enemy[2].f_ability0()
                        pygame.display.update()
                    if player[2].cls == 'cleric':
                        if player[2].empowered == 1:
                            ability2 = cleric_empowerment()
                            ability2[1].topleft = (150,350)
                            windowSurface.blit(ability2[0],ability2[1])
                    if player[2].shield != 0:
                        windowSurface.blit(ability2[0],ability2[1])
                    alive = damage(enemy[2],player[2],alive)
                    pygame.display.update()
                    time.sleep(1)
                  
                if event.key == ord('3'):
                    if player[2].cls == 'warlock':
                        ability2 = warlock_shield()
                        ability2[1].topleft = (150,350)
                    if player[2].cls == 'warrior':
                        if player[2].tactics > 0:
                            tact = warrior_tactics()
                            tact[1].topleft = (150,350)
                            windowSurface.blit(tact[0],tact[1])
                    if player[2].cls == 'mage':
                        fireball = []
                        mage_with_minion(fireball,place,enemy_place,plyr,enemy,player)
                        plyralt = alt_mage()
                        plyralt[1].topleft = (150,350)
                        windowSurface.blit(plyralt[0],plyralt[1])
                    if player[2].shield != 0:
                        windowSurface.blit(place[0],place[1])
                        windowSurface.blit(enemy_place[0],enemy_place[1])
                        if player[2].cls == 'mage':
                            windowSurface.blit(plyralt[0],plyralt[1])
                        else:
                            windowSurface.blit(plyr[0],plyr[1])
                        enemy_health(enemy[2].health,enemy_place)
                        player_health(player[2].health,plyr,player[2].shield)
                        windowSurface.blit(ability2[0],ability2[1])
                        pygame.display.update()
                    enemy_attack(place,enemy_place,plyr,player)
                    player[2].f_ability2()
                    enemy[2].f_ability0()
                    alive = damage(enemy[2],player[2],alive)
                    pygame.display.update()
##                    else:
##                        drawText('Ability Not Available Yet!',font,windowSurface,0,0,TEXTCOLOR)
##                    pygame.display.update()
                    time.sleep(1)
                
                if event.key == ord('4'):
                    drawText('Ability Not Available Yet!',font,windowSurface,0,0,TEXTCOLOR)
                    pygame.display.update()
                    time.sleep(1)
                    
        windowSurface.blit(place[0],place[1])
        windowSurface.blit(enemy_place[0],enemy_place[1])
        if player[2].minion > 0:
            plyralt = alt_mage()
            plyralt[1].topleft = (150,350)
            windowSurface.blit(plyralt[0],plyralt[1])
        else:
            windowSurface.blit(plyr[0],plyr[1])
        if player[2].cls == 'warrior':
            if player[2].tactics > 0:
                tact = warrior_tactics()
                tact[1].topleft = (150,350)
                windowSurface.blit(tact[0],tact[1])
        if player[2].cls == 'cleric':
            if player[2].empowered == 1:
                ability2 = cleric_empowerment()
                ability2[1].topleft = (150,350)
                windowSurface.blit(ability2[0],ability2[1])
        if player[2].shield != 0:
            windowSurface.blit(ability2[0],ability2[1])
        player_health(player[2].health,plyr,player[2].shield)
        enemy_health(enemy[2].health,enemy_place)
        ability1 = []
        if alive[0] == True and alive[1] == False:
            player[2].lvl += 1
            level_up(player)
            #player_health(player[2].health,plyr,player[2].shield)
            pygame.display.update()
            time.sleep(1)
        #player_health(player[2].health,plyr,player[2].shield)
        pygame.display.update()
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
    data = [enemyImage,enemyRect,enemyType]
    return data

def all_enemies(enemies,locations):
    rand = random.randint(4,10)
    all_enemies = []
    x = 0
    while x != rand:
        all_enemies.append(pick_enemy(enemies))
        loc = random.randint(0,len(locations)-1)
        all_enemies[x][1].topleft = locations[loc]
        locations.remove(locations[loc])
        x += 1
    return all_enemies

def pick_hero(heroes):
    pygame.display.update()
    drawText('Welcome to Dragonia', font, windowSurface, 0, 0,(0,0,0))
    drawText('Mage(1)', font, windowSurface, 0, 30,(65,105,225))
    drawText('Warrior(2)',font,windowSurface,100, 30,(178,34,34))
    drawText('Cleric(3)',font,windowSurface,225, 30,(0,255,255))
    drawText('Warlock(4)',font,windowSurface,330, 30,(0,100,0))
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
                    
    heroImage = pygame.image.load(heroes[choice])
    heroRect = heroImage.get_rect()
    data = [heroImage,heroRect,class_]
    return data

def class_abilities(player):
    windowSurface.fill(BACKGROUNDCOLOR)
    player[2].f_abilities()
    drawText('Press ENTER to begin.', font, windowSurface, 100, 0,(255,255,255))
    pygame.display.update()
    waitForPlayerToPressKey()
    
def place():
    places = ['cave_dragonia.png','desert.png','water.png','sun.png']
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

def loot(enemy):
    rand = random.randint(0,100)
    dropped = False
    if enemy[2].name == 'gargoyle':
        if rand >= 0 and rand < 15:
            lootImage = pygame.image.load('sword.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'sword']
            dropped = True
        elif rand >= 15 and rand < 25:
            lootImage = pygame.image.load('belt.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'belt']
            dropped = True
        elif rand >= 25 and rand < 30:
            lootImage = pygame.image.load('cloak.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'cloak']
            dropped = True
        elif rand >= 30 and rand < 31:
            lootImage = pygame.image.load('legendary.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'legendary']
            dropped = True
        else:
            dropped = False
    elif enemy[2].name == 'snake':
        if rand >= 0 and rand < 8:
            lootImage = pygame.image.load('sword.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'sword']
            dropped = True
        elif rand >= 8 and rand < 25:
            lootImage = pygame.image.load('belt.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'belt']
            dropped = True
        elif rand >= 25 and rand < 28:
            lootImage = pygame.image.load('cloak.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'cloak']
            dropped = True
        elif rand >= 28 and rand < 29:
            lootImage = pygame.image.load('legendary.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'legendary']
            dropped = True
        else:
            dropped = False
    elif enemy[2].name == 'dragon':
        if rand >= 0 and rand < 40:
            lootImage = pygame.image.load('sword.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'sword']
            dropped = True
        elif rand >= 40 and rand < 50:
            lootImage = pygame.image.load('belt.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'belt']
            dropped = True
        elif rand >= 50 and rand < 57:
            lootImage = pygame.image.load('cloak.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'cloak']
            dropped = True
        elif rand >= 58 and rand < 63:
            lootImage = pygame.image.load('legendary.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'legendary']
            dropped = True
        else:
            dropped = False
    elif enemy[2].name == 'ogre':
        if rand >= 0 and rand < 11:
            lootImage = pygame.image.load('sword.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'sword']
            dropped = True
        elif rand >= 11 and rand < 25:
            lootImage = pygame.image.load('belt.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'belt']
            dropped = True
        elif rand >= 25 and rand < 29:
            lootImage = pygame.image.load('cloak.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'cloak']
            dropped = True
        elif rand >= 29 and rand < 30:
            lootImage = pygame.image.load('legendary.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'legendary']
            dropped = True
        else:
            dropped = False
    elif enemy[2].name == 'cyclops':
        if rand >= 0 and rand < 35:
            lootImage = pygame.image.load('sword.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'sword']
            dropped = True
        elif rand >= 35 and rand < 45:
            lootImage = pygame.image.load('belt.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'belt']
            dropped = True
        elif rand >= 45 and rand < 52:
            lootImage = pygame.image.load('cloak.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'cloak']
            dropped = True
        elif rand >= 52 and rand < 58:
            lootImage = pygame.image.load('eye.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'eye']
            dropped = True
        elif rand >= 58 and rand < 60:
            lootImage = pygame.image.load('legendary.png')
            lootRect = lootImage.get_rect()
            data = [lootImage,lootRect,True,'legendary']
            dropped = True
        else:
            dropped = False
    if dropped == False:
        lootImage = pygame.image.load('sword.png')
        lootRect = lootImage.get_rect()
        data = [lootImage,lootRect,False,'Nothing']
    return data

pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Dragonia')
pygame.display.set_icon(pygame.image.load('dragonia!.png'))
# set up fonts
font = pygame.font.SysFont('centaur', 30)

# set up sounds
gameOverSound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('background_.ogg')

#enemy locations
locations = [(120,20),(240,20),(360,20),(480,20),(600,20),(720,20),(0,130),(120,130),(240,130),(360,130),(480,130),(600,130),(720,130),(0,260),(120,260),(240,260),(360,260),(480,260),(600,260),(720,260),(0,390),(120,390),(240,390),(360,390),(480,390),(600,390),(720,390)]
#enemy setup
enemies = ['ogre.png','snake.png','garg_dragonia_small.png','dragon.png','cyclops.png']
#enemy = pick_enemy(enemies)

#set up load screen
dragonia = dragonia()
#test
the_enemies = all_enemies(enemies,locations)
#topScore = 0
while True:
    # set up the start of the game
    drop = False
    locations = [(120,20),(240,20),(360,20),(480,20),(600,20),(720,20),(0,130),(120,130),(240,130),(360,130),(480,130),(600,130),(720,130),(0,260),(120,260),(240,260),(360,260),(480,260),(600,260),(720,260),(0,390),(120,390),(240,390),(360,390),(480,390),(600,390),(720,390)]
    score = 0
    moveLeft = moveRight = moveUp = moveDown = False
    pygame.mixer.music.play(-1, 0.0)
    heroes = ['mage_dragonia.png','warrior_dragonia.png','cleric_dragonia.png','warlock_dragonia.png']
    #windowSurface.fill(BACKGROUNDCOLOR)
    windowSurface.blit(dragonia[0],dragonia[1])
    player = pick_hero(heroes)
    player[1].topleft = (0,20)
    class_abilities(player)
    the_enemies = all_enemies(enemies,locations)
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
        if moveRight and player[1].right < WINDOWWIDTH:
            player[1].move_ip(PLAYERMOVERATE, 0)
        if moveUp and player[1].top > 0:
            player[1].move_ip(0, -1 * PLAYERMOVERATE)
        if moveDown and player[1].bottom < WINDOWHEIGHT:
            player[1].move_ip(0, PLAYERMOVERATE)

       
        # Draw the game world on the window.
        #windowSurface.fill(BACKGROUNDCOLOR)
        windowSurface.blit(dragonia[0],dragonia[1])
        
        # Draw the player's rectangle
        windowSurface.blit(player[0], player[1])
        draw_enemies(the_enemies)
        if drop != False:
                windowSurface.blit(the_drop[0],the_drop[1])
                #time.sleep(2)
        # add health above enemies and players
        player_health(player[2].health,player,player[2].shield)
        j = 0
        while j!= len(the_enemies):
            if player[2].lvl > 1 and leveled == True:
                the_enemies[j][2].health += player[2].lvl*50
                the_enemies[j][2].miss -= 1
            enemy_health(the_enemies[j][2].health,the_enemies[j])
            j += 1
        leveled = False
        if player[2].shield != 0:
                if player[2].cls == 'mage':
                    ability2 = mage_shield()
                elif player[2].cls == 'warlock':
                    ability2 = warlock_shield()
                current_loc = player[1].topleft
                ability2[1].topleft =  (current_loc[0]-50,current_loc[1]-50)
                windowSurface.blit(ability2[0],ability2[1])
                
        # Check if any of the enemies have hit the player.
        current_enemy = playerHasHitEnemy(player[1], the_enemies)
        if drop == True:
            picked_up_loot = player[1].colliderect(the_drop[1])
            if picked_up_loot:
                drop = False
                if the_drop[3] == 'sword':
                    drawText('You found a Sword!',font,windowSurface,0,0,(0,0,0))
                    drawText('Press ENTER to continue!',font,windowSurface,0,25,(0,0,0))
                    pygame.display.update()
                    moveLeft = moveRight = moveUp = moveDown = False
                    waitForPlayerToPressKey()
                    player[2].f_sword()
                if the_drop[3] == 'belt':
                    drawText('You found a Belt!',font,windowSurface,0,0,(0,0,0))
                    drawText('Press ENTER to continue!',font,windowSurface,0,25,(0,0,0))
                    pygame.display.update()
                    moveLeft = moveRight = moveUp = moveDown = False
                    waitForPlayerToPressKey()
                    player[2].f_belt()
                if the_drop[3] == 'cloak':
                    drawText('You found a Cloak!',font,windowSurface,0,0,(0,0,0))
                    drawText('Press ENTER to continue!',font,windowSurface,0,25,(0,0,0))
                    pygame.display.update()
                    moveLeft = moveRight = moveUp = moveDown = False
                    waitForPlayerToPressKey()
                    player[2].f_cloak()
                if the_drop[3] == 'eye':
                    drawText('You found the Cyclops\' eye!',font,windowSurface,0,0,(0,0,0))
                    drawText('Press ENTER to continue!',font,windowSurface,0,25,(0,0,0))
                    pygame.display.update()
                    moveLeft = moveRight = moveUp = moveDown = False
                    waitForPlayerToPressKey()
                    player[2].f_eye()
                if the_drop[3] == 'legendary':
                    drawText('You found a LEGENDARY weapon.',font,windowSurface,0,0,(0,0,0))
                    drawText('Press ENTER to continue!',font,windowSurface,0,25,(0,0,0))
                    pygame.display.update()
                    moveLeft = moveRight = moveUp = moveDown = False
                    waitForPlayerToPressKey()
                    player[2].f_legendary_weapon()
        player_health(player[2].health,player,player[2].shield)
        pygame.display.update()
        if current_enemy != -1:
            loot_drop = the_enemies[current_enemy][1].topleft
            loot_drop = (loot_drop[0]+20,loot_drop[1]+20)
            moveLeft = moveRight = moveUp = moveDown = False
            drawText('You have encountered an enemy! Prepare to fight!',font,windowSurface,0,0,(0,0,0))
            pygame.display.update()
            time.sleep(1)
            alive = battle(place(),player,the_enemies[current_enemy])
            if alive[0] == False:
                break
            elif alive[1] == False:
                #print the_enemies
                #print current_enemy
                #print the_enemies[current_enemy]
                the_drop = loot(the_enemies[current_enemy])
                if the_drop[2] == True:
                    drop = True
                    the_drop[1].topleft = loot_drop
                else:
                    drop = False
                the_enemies.remove(the_enemies[current_enemy])
                leveled = True
                if the_enemies == []:
                    you_win = True
                    break
            draw_enemies(the_enemies)
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
        waitForPlayerToPressKey()
    else:
        pygame.mixer.music.stop()
        gameOverSound.play()
        windowSurface.fill((255,0,0))
        gover = gameover()
        windowSurface.blit(gover[0],gover[1])
        drawText('GAME OVER', font, windowSurface, 0, 0,(0,0,0))
        drawText('Press ENTER to start a new game.', font, windowSurface, 0, 30,(0,0,0))
        pygame.display.update()
        waitForPlayerToPressKey()
        gameOverSound.stop()
    



