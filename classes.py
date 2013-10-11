import random
import sys
import time
import pygame

WINDOWWIDTH = 896
WINDOWHEIGHT = 504
TEXTCOLOR = (255,255,255)
BACKGROUNDCOLOR = (0,0,0)
pygame.init()
font = pygame.font.SysFont('centaur', 22)
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))


def drawText(text, font, surface, x, y, color):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    #print textrect
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

class swashbuckler:
    def __init__(self,name):
        self.cls = 'swashbuckler'
        self.dead = 0
        self.health_pot = 2
        self.name = name
        self.stamina = 15
        self.wisdom = 6
        self.intellect = 3
        self.dexterity = 23
        self.strength = 17
        self.health = self.stamina*10
        self.shield = 0
        self.damage = 0
        self.bleed = 0
        self.dodge = False
        self.miss = 300/(self.dexterity+self.strength)
        self.crit = (self.dexterity+self.intellect+self.wisdom+self.strength)/5
        self.dict = ['SLICES','WOUNDS','HITS','GLANCES','DEMOLISHES','CRITS','MISSES']
        self.abilities = ['Daring Strike(1), Puncture(2)']
        self.lvl = 1
        self.attack1 = pygame.mixer.Sound('swash_attack1.wav')
        self.attack2 = pygame.mixer.Sound('swash_attack1.wav')
        self.attack3 = pygame.mixer.Sound('swash_attack3.wav')
        self.death = pygame.mixer.Sound('player_death.wav')
        self.potion = pygame.mixer.Sound('potion.wav')
    def f_displayStats(self):
        print "Class: ", self.cls, "\nName: ", self.name, "\nStamina: ", self.stamina, "\nWisdom: ", self.wisdom, "\nIntellect: ",self.intellect, "\nDexterity: ",self.dexterity, "\nStrength: ",self.strength, "\nMiss: ",self.miss,"\nCrit: ",self.crit
    def f_abilities(self):
		print "Daring Strike(1). Deals {0} to {1} damage.".format(self.dexterity+self.strength,(self.dexterity+self.strength)*5)
		print "Deals bonus damage to bleeding enemies."
		print "Puncture(2). Deals {0} to {1} damage.".format((self.dexterity+self.strength),(self.dexterity+self.strength)*2)
		print "Causes the enemy to bleed."
		print "Shank(3). Deals {0} to {1} damage.".format(1,self.dexterity*5)
		print "Has a high crit chance and on critical hit causes the enemy to bleed."
		drawText('(1): Daring Strike, Deals '+str(self.dexterity+self.strength)+' to '+str((self.dexterity+self.strength)*5)+' damage. Incresed by Dexterity and Strength.',font,windowSurface,100,30,TEXTCOLOR)
		drawText('Deals bonus damage to bleeding enemies.',font,windowSurface,100,60,TEXTCOLOR)
		drawText('(2): Puncture Deals '+str(self.dexterity+self.strength)+' to '+str((self.dexterity+self.strength)*2)+' damage. Incresed by Dexterity and Strength.',font,windowSurface,100,90,TEXTCOLOR)
		drawText('Causes the enemy to bleed.',font,windowSurface,100,120,TEXTCOLOR)
		drawText('(3): Shank Deals '+str(1)+' to '+str(self.dexterity*5)+' damage. Incresed by Dexterity.',font,windowSurface,100,150,TEXTCOLOR)
		drawText('Has a high crit chance and on critical hit caues the enemy to bleed.',font,windowSurface,100,180,TEXTCOLOR)
                drawText('(Q): Potions.  You have 2 potions that heals you to full.',font,windowSurface,100,210,TEXTCOLOR)
                drawText('     Using these does not cause the enemy to attack.',font,windowSurface,100,240,TEXTCOLOR)
                drawText('(DODGE): The Swashbuckler has a chance to dodge.  This is directly related to his dexterity.',font,windowSurface,100,270,TEXTCOLOR)
    def f_ability0(self):
    	damage = random.randrange(self.dexterity, self.dexterity*5)+self.strength
    	crit = random.randrange(1,100)
        miss = random.randrange(1,100)
        dodge = random.randint(0,100)
        if dodge <= self.dexterity/20:
            self.dodge = True
        else:
            self.dodge = False
        if self.bleed:
        	damage += 20*self.lvl
    	if miss <= self.miss:
            self.damage = 0
            print "You MISS completely!"
            drawText('You MISS completly!',font,windowSurface,0,0,TEXTCOLOR)
        elif crit <= self.crit:
            self.damage = damage*2.5
            print "Your Daring Strike CRITS for {0} damage!".format(self.damage)
            drawText('You hit for '+str(self.damage),font,windowSurface,0,0,TEXTCOLOR)
    	else:
    		self.damage = damage
    		print "Your Daring Strike hits for {0} damage.".format(self.damage)
    		drawText('You hit for '+str(self.damage),font,windowSurface,0,0,TEXTCOLOR)
    	self.f_bleed()
    	
    def f_ability1(self):
    	damage = random.randrange((self.dexterity+self.strength),(self.dexterity+self.strength)*2)
    	crit = random.randrange(1,100)
        miss = random.randrange(1,100)
        dodge = random.randint(0,100)
        if dodge <= self.dexterity/2:
            self.dodge = True
        else:
            self.dodge = False
    	if miss <= self.miss:
            self.damage = 0
            print "You MISS completely!"
            drawText('You MISS completly!',font,windowSurface,0,0,TEXTCOLOR)
        elif crit <= self.crit:
            self.damage = damage*1.5
            self.bleed += 3
            print "Your Puncture CRITS for {0} damage!".format(self.damage)
            drawText('You hit for '+str(self.damage),font,windowSurface,0,0,TEXTCOLOR)
    	else:
    		self.damage = damage
    		self.bleed += 2
    		print "Your Puncture hits for {0} damage.".format(self.damage)
    		drawText('You hit for '+str(self.damage),font,windowSurface,0,0,TEXTCOLOR)
    	self.f_bleed()
    	
    def f_ability2(self):
    	damage = random.randrange(1,self.dexterity*5)
    	crit = random.randrange(1,50)
    	miss = random.randrange(1,100)
    	dodge = random.randint(0,100)
        if dodge <= self.dexterity/2:
            self.dodge = True
        else:
            self.dodge = False
    	if miss <= self.miss:
    		self.damage = 0
    		print "You MISS completely!"
    	elif crit <= self.crit:
    		self.damage = damage*3
    		self.bleed += 2
    		print "Your Shank CRITS for {0} damage!".format(self.damage)
    		print "The enemy is bleeding."
    		drawText('You CRIT for '+str(self.damage),font,windowSurface,0,0,TEXTCOLOR)
    		drawText('Your enemy bleeds.',font,windowSurface,0,30,TEXTCOLOR)
    	else:
    		self.damage = damage
    		print "Your Shank hits for {0} damage.".format(self.damage)
    		drawText('You hit for '+str(self.damage),font,windowSurface,0,0,TEXTCOLOR)
    	self.f_bleed()
    	
    def f_bleed(self):
    	if self.bleed > 0:
    		bleed_damage = (self.lvl*10)*self.bleed
    		self.damage += bleed_damage
    		self.bleed -= 1
    		print "Your enemy's wounds bleed for {0} damage.".format(bleed_damage)
    		drawText("Your enemy's wounds bleed for "+str(bleed_damage),font,windowSurface,0,60,TEXTCOLOR)
    def f_potion(self):
        self.potion.play()
    def f_attack1(self):
        self.attack1.play()
    def f_attack2(self):
        self.attack2.play()
    def f_attack3(self):
        self.attack3.play()
    def f_death(self):
        self.death.play()
    def f_level(self):
        self.miss = 300/(self.dexterity+self.strength)
        self.crit = (self.dexterity+self.intellect+self.wisdom+self.strength)/5
    def f_sword(self):
        self.dexterity += 30
    def f_offhand(self):
        self.dexterity += 15
    def f_belt(self):
        self.stamina += 2
        self.health += 20
    def f_cloak(self):
        self.stamina += 20
        self.health += 200
    def f_trinket(self):
        self.dexterity += 95
    def f_legendary_weapon(self):
        self.dexterity += 200
    def f_eye(self):
        self.stamina += 50
        self.health += 500
    def f_air(self):
        self.dexterity += 2
    def f_earth(self):
        self.strength += 2
    def f_water(self):
        self.wisdom += 2
    def f_fire(self):
        self.intellect += 2


class warlock:
    def __init__(self,name):
        self.cls = 'warlock'
        self.dead = 0
        self.health_pot = 2
        self.name = name
        self.stamina = 14
        self.wisdom = 15
        self.intellect = 16
        self.dexterity = 9
        self.strength = 7
        self.health = self.stamina*10
        self.shield = 0
        self.damage = 0
        self.miss = 210/(self.intellect+self.wisdom)
        self.crit = (self.intellect+self.strength+self.wisdom+self.dexterity)/5
        self.dict = ['drains','depletes','consumes','leeches','hits','CRITS','misses']
        self.abilities = ['Power Siphon','Entropic Assault']
        self.lvl = 1
        self.attack1 = pygame.mixer.Sound('warlock_attack1.wav')
        self.attack2 = pygame.mixer.Sound('warlock_attack2.wav')
        self.attack3 = pygame.mixer.Sound('warlock_shield.wav')
        self.death = pygame.mixer.Sound('player_death.wav')
        self.potion = pygame.mixer.Sound('potion.wav')
    def f_displayStats(self):
        print "Class: ", self.cls, "\nName: ", self.name,"\nLevel: ",self.lvl, "\nStamina: ", self.stamina, "\nWisdom: ", self.wisdom, "\nIntellect: ",self.intellect, "\nDexterity: ",self.dexterity, "\nStrength: ",self.strength, "\nMiss: ",self.miss,"\nCrit: ",self.crit
    def f_abilities(self):
        font = pygame.font.SysFont('centaur', 20)
        drawText('(1): Power Siphon. This ability does '+str((self.intellect+self.stamina*4/3))+' to '+str(((self.intellect+self.stamina)*5/3))+' damage.  It is increased by your Intellect and Stamina.',font,windowSurface,100,30,TEXTCOLOR)
        drawText('     You are healed for a portion of the damage dealt.',font,windowSurface,100,60,TEXTCOLOR)
        drawText('(2): Entropic Asault.  This ability does '+str((self.intellect+self.wisdom+self.stamina)*5/4)+' to '+str((self.intellect+self.wisdom+self.stamina)*11/2)+' damage. It is increased by Intellect and Stamina.',font,windowSurface,100,90,TEXTCOLOR)
        drawText('     Consumes a portion of your current health.  Even if you miss.',font,windowSurface,100,120,TEXTCOLOR)
        drawText('(3): Blood Armor.  This ablity sacrifices '+str(self.health*0.1)+' to create a '+str(self.health*0.3)+' damage shield.',font,windowSurface,100,150,TEXTCOLOR)
        drawText('     Sacrifices 10% hp for shield 3x as strong.',font,windowSurface,100,180,TEXTCOLOR)
        drawText('(Q): Potions.  You have 2 potions that heals you to full.',font,windowSurface,100,210,TEXTCOLOR)
        drawText('     Using these does not cause the enemy to attack.',font,windowSurface,100,240,TEXTCOLOR)
        print "Power Siphon(1).  This ability does {0} to {1} damage".format((self.intellect+self.stamina*4/3),((self.intellect+self.stamina)*5/3))
        print "Heals you for a portion of damage dealt\n"
        print "Entropic Assault(2). This ability does {0} to {1} damage".format((self.intellect+self.wisdom+self.stamina)*5/4,(self.intellect+self.wisdom+self.stamina)*11/2)
        print "Consumes a portion of you current health. Even if you miss!\n"
        print "Blood Armor(3). This ability sacrafices {0} health to create a {1} damage shield.".format(self.health*0.1,self.health*0.3)
        print " "
    def f_ability0(self):
        damage = random.randint(((self.intellect+self.stamina)*4/3),((self.intellect+self.stamina)*5/3))
        crit = random.randrange(1,100)
        miss = random.randrange(1,100)
        if miss <= self.miss:
            self.damage = 0
            drawText('You MISS completely!',font,windowSurface,0,0,TEXTCOLOR)
            print "You MISS completely!"
        elif crit <= self.crit:
            self.damage = damage*2
            heal_control = round(((self.wisdom/2)+((self.stamina*11)/self.health))/3, 0)
            self.health += (self.damage/5)+heal_control
            dam = str(self.damage)
            heal = str((self.damage/5)+heal_control)
            drawText('Your Power Siphon HITS for '+dam,font,windowSurface,0,0,TEXTCOLOR)
            drawText('and heals you for '+heal,font,windowSurface,0,25,TEXTCOLOR)
            print 'Your Power Siphon {0} for {1} damage.'.format(self.dict[5],self.damage)
            print 'and heals you for {0}.'.format((self.damage/5)+heal_control)
            
        else:
            self.damage = damage
            heal_control = round(((self.wisdom/2)+((self.stamina*11)/self.health))/3, 0)
            self.health += (damage/6)+heal_control
            dam = str(self.damage)
            heal = str((damage/6)+heal_control)
            drawText('Your Power Siphon HITS for '+dam,font,windowSurface,0,0,TEXTCOLOR)
            drawText('and heals you for '+heal,font,windowSurface,0,25,TEXTCOLOR)
            print 'Your Power Siphon {0} for {1} damage.'.format(self.dict[random.randrange(0,4)],self.damage)
            print 'and heals you for {0}.'.format((damage/6)+heal_control)
            
    def f_ability1(self):
        damage = random.randint((self.intellect+self.wisdom+self.stamina)*5/4,(self.intellect+self.wisdom+self.stamina)*11/2)
        crit = random.randrange(1,100)
        miss = random.randrange(1,100)
        sac_hp = round(self.health * (0.17),0)
        if miss <= self.miss:
            self.damage = 0
            self.health -= sac_hp
            dam = str(sac_hp)
            drawText('Your MISS completely!',font,windowSurface,0,0,TEXTCOLOR)
            drawText(dam+' health consumed.',font,windowSurface,0,25,TEXTCOLOR)
            print "You MISS completely!"
            print "{0} health consumed.".format(sac_hp)
        elif crit <= self.crit:
            self.damage = damage*2
            self.health -= sac_hp
            dam = str(self.damage)
            hp = str(sac_hp)
            drawText('Your Entropic Assault CRITS for '+dam,font,windowSurface,0,0,TEXTCOLOR)
            drawText(hp+' health consumed.',font,windowSurface,0,25,TEXTCOLOR)
            print "Your Entropic Assault crits for {0} damage.".format(self.damage)
            print "{0} health consumed.".format(sac_hp)
        else:
            self.damage = damage
            self.health -= sac_hp
            dam = str(self.damage)
            hp = str(sac_hp)
            drawText('Your Entropic Assault HITS for '+dam,font,windowSurface,0,0,TEXTCOLOR)
            drawText(hp+' health consumed.',font,windowSurface,0,25,TEXTCOLOR)
            print "Your Entropic Assault deals {0} damage.".format(self.damage)
            print "{0} health consumed.".format(sac_hp)
            
    def f_ability2(self):
        self.damage = 0
    	sac_hp = round(self.health*0.1,0)
    	sac_shield = round(self.health*0.3,0)
    	self.health -= sac_hp
    	self.shield += sac_shield
    	shield = str(sac_shield)
    	hp = str(sac_hp)
    	drawText('You sacrafice '+hp+' health for '+shield+' shield',font,windowSurface,0,25,TEXTCOLOR)
    	print "You sacrafice {0} health for {1} shield.".format(sac_hp, sac_shield)
    def f_potion(self):
        self.potion.play()
    def f_attack1(self):
        self.attack1.play()
    def f_attack2(self):
        self.attack2.play()
    def f_attack3(self):
        self.attack3.play()
    def f_death(self):
        self.death.play()
    def f_level(self):
        self.miss = 210/(self.intellect+self.wisdom)
        self.crit = (self.intellect+self.strength+self.wisdom+self.dexterity)/5
    def f_sword(self):
        self.intellect += 30
    def f_offhand(self):
        self.stamina += 10
        self.health += 100
    def f_belt(self):
        self.stamina += 2
        self.health += 20
    def f_cloak(self):
        self.stamina += 20
        self.health += 200
    def f_trinket(self):
        self.intellect += 45
    def f_eye(self):
        self.stamina += 50
        self.health += 500
    def f_legendary_weapon(self):
        self.intellect += 100
    def f_air(self):
        self.dexterity += 2
    def f_earth(self):
        self.strength += 2
    def f_water(self):
        self.wisdom += 2
    def f_fire(self):
        self.intellect += 2

class mage:
    def __init__(self,name):
        self.cls = 'mage'
        self.dead = 0
        self.health_pot = 2
        self.name = name
        self.stamina = 8
        self.wisdom = 19
        self.intellect = 20
        self.dexterity = 7
        self.strength = 6
        self.health = self.stamina*10
        self.shield = 0
        self.damage = 0
        self.minion = 0
        self.min_damage = 0
        self.miss = 210/(self.intellect+self.wisdom)
        self.crit = (self.intellect+self.strength+self.wisdom+self.dexterity)/5
        self.dict = ['burns','incinertes','scourches','glances','hits','CRITS','misses']
        self.abilities = ['Fireball']
        self.lvl = 1
        self.attack1 = pygame.mixer.Sound('fireball.wav')
        self.attack2 = pygame.mixer.Sound('mage_shield.wav')
        self.attack3 = pygame.mixer.Sound('mage_pet.wav')
        self.death = pygame.mixer.Sound('player_death.wav')
        self.potion = pygame.mixer.Sound('potion.wav')
    def f_displayStats(self):
        print "Class: ", self.cls, "\nName: ", self.name, "\nLevel: ",self.lvl,"\nStamina: ", self.stamina, "\nWisdom: ", self.wisdom, "\nIntellect: ",self.intellect, "\nDexterity: ",self.dexterity, "\nStrength: ",self.strength, "\nMiss: ",self.miss,"\nCrit: ",self.crit
    def f_abilities(self):
        font = pygame.font.SysFont('centaur', 20)
        drawText('(1): Fireball.  This ability does '+str(self.intellect*2)+' to '+str(self.intellect*7)+' damage.  Its damage is increased by your Intellect.',font,windowSurface,100,30,TEXTCOLOR)
        drawText('(2): Barrier.  This ability creates a magical shield that absorbs '+str(self.intellect+(self.wisdom/2))+' to '+str((self.intellect+(self.wisdom/2))*3)+' damage.',font,windowSurface,100,60,TEXTCOLOR)
        drawText('     The amount absorbed increases based on Intellect and Wisdom',font,windowSurface,100,90,TEXTCOLOR)
        drawText('(3): Summon Minion.  This ability summons a minion that attacks for 4 turns.',font,windowSurface,100,120,TEXTCOLOR)
        drawText('     Its damage is increased by your Intellect and Wisdom.',font,windowSurface,100,150,TEXTCOLOR)
        drawText('(Q): Potions.  You have 2 potions that heals you to full.',font,windowSurface,100,180,TEXTCOLOR)
        drawText('     Using these does not cause the enemy to attack.',font,windowSurface,100,210,TEXTCOLOR)
        print "Fireball(1).  This ability does {0} to {1} damage.\n".format(self.intellect*2,self.intellect*7)
        print "Barrier(2). This ability creates a magical shield that absorbs {0} to {1} damage.".format(self.intellect+(self.wisdom/2),(self.intellect+(self.wisdom/2))*2)
        print " "
    def f_ability0(self):
        if self.minion == 0:
            self.min_damage = 0
        if self.minion > 0:
            damage = random.randrange(self.intellect*2,self.intellect*7)+self.min_damage
            self.minion -= 1
        else:
            damage = random.randrange(self.intellect*2,self.intellect*7)
        crit = random.randrange(1,100)
        miss = random.randrange(1,100)
        if miss <= self.miss:
            self.damage = 0
            if self.minion > 0:
                self.damage = self.min_damage
            drawText('You MISS completely!',font,windowSurface,0,0,TEXTCOLOR)
            if self.minion > 0:
                drawText('Your minion hits for '+str(self.min_damage),font,windowSurface,0,25,TEXTCOLOR)
            print "You MISS completely!"
        elif crit <= self.crit:
            self.damage = damage*2
            dam = str((self.damage/2 - self.min_damage)*2)
            drawText('Your Fireball CRITS for '+dam,font,windowSurface,0,0,TEXTCOLOR)
            if self.minion > 0:
                drawText('Your minion CRITS for '+str(self.min_damage*2),font,windowSurface,0,25,TEXTCOLOR)
            print 'Your Fireball {0} for {1} damage.'.format(self.dict[5],self.damage)
        else:
            self.damage = damage
            dam = str(self.damage-self.min_damage)
            drawText('Your Fireball hits for '+dam,font,windowSurface,0,0,TEXTCOLOR)
            if self.minion > 0:
                drawText('Your minion hits for '+str(self.min_damage),font,windowSurface,0,25,TEXTCOLOR)
            print 'Your Fireball {0} for {1} damage.'.format(self.dict[random.randrange(0,4)],self.damage)
    def f_ability1(self):
    	self.damage = 0
    	if self.minion == 0:
            self.min_damage = 0
        shield = random.randrange(self.intellect+(self.wisdom/2),(self.intellect+(self.wisdom/2))*3)
        self.shield = shield
        shield = str(shield)
        drawText('You create a '+shield+' point shield.',font,windowSurface,0,0,TEXTCOLOR)
        if self.minion > 0:
            self.minion -= 1
            self.damage = self.min_damage
            drawText('Your minion hits for '+str(self.min_damage),font,windowSurface,0,25,TEXTCOLOR)
        print "You create a {0} point shield".format(shield)
     
    def f_ability2(self):
    	self.minion = 4
    	self.f_minion()
    	self.damage = self.min_damage
    	
    def f_minion(self):
    	minion_damage = (self.intellect + self.wisdom)/2
     	if (self.minion):
     		self.min_damage = minion_damage
     		self.minion -= 1
     		if self.minion == 0:
                    self.min_damage = 0
     		drawText('Your minion hits for '+str(minion_damage),font,windowSurface,0,0, TEXTCOLOR)
     		print "Your minion hits for {0} damage.".format(minion_damage)
    def f_potion(self):
        self.potion.play() 		
    def f_attack1(self):
        self.attack1.play()
    def f_attack2(self):
        self.attack2.play()
    def f_attack3(self):
        self.attack3.play()
    def f_death(self):
        self.death.play()
    def f_level(self):
        self.miss = 210/(self.intellect+self.wisdom)
        self.crit = (self.intellect+self.strength+self.wisdom+self.dexterity)/5
    def f_sword(self):
        self.intellect += 30
    def f_offhand(self):
        self.stamina += 10
        self.health += 100
    def f_belt(self):
        self.stamina += 2
        self.health += 20
    def f_cloak(self):
        self.stamina += 20
        self.health += 200
    def f_trinket(self):
        self.intellect += 45
    def f_legendary_weapon(self):
        self.intellect += 100
    def f_eye(self):
        self.stamina += 50
        self.health += 500
    def f_air(self):
        self.dexterity += 2
    def f_earth(self):
        self.strength += 2
    def f_water(self):
        self.wisdom += 2
    def f_fire(self):
        self.intellect += 2
            
class warrior:
    def __init__(self,name):
        self.cls = 'warrior'
        self.dead = 0
        self.health_pot = 2
        self.name = name
        self.stamina = 17
        self.wisdom = 7
        self.intellect = 4
        self.dexterity = 12
        self.strength = 21
        self.health = self.stamina*10
        self.shield = 0
        self.damage = 0
        self.tactics = 0
        self.block = False
        self.miss = 240/(self.strength+self.dexterity)
        self.crit = (self.dexterity+self.intellect+self.wisdom+self.strength)/5
        self.dict = ['SLICES','WOUNDS','HITS','GLANCES','DEMOLISHES','CRITS','MISSES']
        self.abilities = ['Heroic Slash']
        self.lvl = 1
        self.attack1 = pygame.mixer.Sound('warrior_attack1.wav')
        self.attack2 = pygame.mixer.Sound('warrior_attack2.wav')
        self.attack3 = pygame.mixer.Sound('warrior_attack3.wav')
        self.death = pygame.mixer.Sound('player_death.wav')
        self.potion = pygame.mixer.Sound('potion.wav')
    def f_displayStats(self):
        print "Class: ", self.cls, "\nName: ", self.name,"\nLevel: ",self.lvl, "\nStamina: ", self.stamina, "\nWisdom: ", self.wisdom, "\nIntellect: ",self.intellect, "\nDexterity: ",self.dexterity, "\nStrength: ",self.strength, "\nMiss: ",self.miss,"\nCrit: ",self.crit
    def f_abilities(self):
        font = pygame.font.SysFont('centaur', 20)
        drawText('(1): Heroic Slash.  This ability does '+str(self.strength*5/2)+' to '+str(self.strength*4)+' damage.  Its damage is increased by Strength.',font,windowSurface,100,30,TEXTCOLOR)
        drawText('(2): Combat Tactics.  This ability boosts your damage output and crit chance for 3 turns.',font,windowSurface,100,60,TEXTCOLOR)
        drawText('(3): Furious Barrage.  Deals 3 swift strikes, dealing '+str(self.dexterity/2)+' to '+str((self.dexterity*2)+self.strength*3/2)+' damage.',font,windowSurface,100,90,TEXTCOLOR)
        drawText('     Its damage is increased by Dexterity and Strength',font,windowSurface,100,120,TEXTCOLOR)
        drawText('(Q): Potions.  You have 2 potions that heals you to full.',font,windowSurface,100,150,TEXTCOLOR)
        drawText('     Using these does not cause the enemy to attack.',font,windowSurface,100,180,TEXTCOLOR)
        drawText('(BLOCK): The warrior has a chance to block that is directly related to Strength and Dexterity.',font,windowSurface,100,210,TEXTCOLOR)
        print "Heroic Slash(1).  This ability does {0} to {1} damage.\n".format(self.strength*2,self.strength*4)
        print "Combat Tactics(2). This ability boosts your damage output and crit chance for three turns."
        print "Furious Barrage(3). Deals three swift strikes dealing {0} to {1} damage.".format(self.dexterity/2,(self.dexterity*2)+self.strength)
        print " "
    def f_ability0(self):
        block = random.randint(0,100)
        if block <= (self.dexterity+self.strength)/4:
            self.block = True
        else:
            self.block = False
    	if(self.tactics > 0):
    		bonus_damage = round(self.strength*1.5, 0)
    		crit_cap = 85
    		self.tactics -= 1
    		drawText('Primed for battle...',font,windowSurface,0,0,TEXTCOLOR)
    		print "Primed for battle..."
    	else:
    		bonus_damage = 0
    		crit_cap = 100
        damage = random.randrange(self.strength*5/4,self.strength*4)+bonus_damage
        crit = random.randrange(1,crit_cap)
        miss = random.randrange(1,100)
        if miss <= self.miss:
            self.damage = 0
            drawText('You MISS completely!',font,windowSurface,0,25,TEXTCOLOR)
            print "You MISS completely!"
        elif crit <= self.crit:
            self.damage = damage*2
            dam = str(self.damage)
            drawText('Your Heroic Slash CRITS for '+dam,font,windowSurface,0,25,TEXTCOLOR)
            print 'Your Heroic Slash {0} for {1} damage.'.format(self.dict[5],self.damage)
        else:
            self.damage = damage
            dam = str(self.damage)
            drawText('Your Heroic Slash hits for '+dam,font,windowSurface,0,25,TEXTCOLOR)
            print 'Your Heroic Slash {0} for {1} damage.'.format(self.dict[random.randrange(0,5)],self.damage)
    
    def f_ability1(self):
        block = random.randint(0,100)
        if block <= (self.dexterity+self.strength)/4:
            self.block = True
        else:
            self.block = False
        self.damage = 0
    	self.tactics = 3
        drawText('Your prepare yourself for battle!',font,windowSurface,0,0,TEXTCOLOR)
    	print "You prepare your self for battle!"
    	
    def f_ability2(self):
        block = random.randint(0,100)
        if block <= (self.dexterity+self.strength)/4:
            self.block = True
        else:
            self.block = False
    	damage = 0
    	furious_bar = []
    	bonus_damage = 0;
    	if (self.tactics > 0):
    		bonus_damage = self.dexterity/2
    		crit_cap = 85
    		self.tactics -= 1
    	else:
    		bonus_damage = 0;
    		crit_cap = 100
    	for i in range(0,3):
    		crit = random.randrange(0,100)
    		miss = random.randrange(0,crit_cap)
    		if miss <= self.miss:
    			temp_damage = 0
    			furious_bar.append(temp_damage)
    		elif crit <= self.crit:
    			temp_damage = random.randrange(self.dexterity/2,(self.dexterity*2)+self.strength*3/2)*2 + bonus_damage
    			furious_bar.append(temp_damage)
    		else:
    			temp_damage = random.randrange(self.dexterity/2,(self.dexterity*2)+self.strength*3/2) + bonus_damage
    			furious_bar.append(temp_damage)
    	damage += furious_bar[0] + furious_bar[1] + furious_bar[2]
    	self.damage = damage
    	dam1 = str(furious_bar[0])
    	dam2 = str(furious_bar[1])
    	dam3 = str(furious_bar[2])
        drawText('Primed for battle...',font,windowSurface,0,0,TEXTCOLOR)
        drawText('Your furious barrage of blows deal',font,windowSurface,0,25,TEXTCOLOR)
        drawText(dam1+', '+dam2+' and '+dam3,font,windowSurface,0,50,TEXTCOLOR)
    	print "Primed for battle..."
    	print "Your furious barrage of blows deal {0}, {1}, and {2} damage".format(furious_bar[0],furious_bar[1],furious_bar[2])
    def f_potion(self):
        self.potion.play()
    def f_attack1(self):
        self.attack1.play()
    def f_attack2(self):
        self.attack2.play(0,1800)
    def f_attack3(self):
        self.attack3.play(1)
    def f_death(self):
        self.death.play()
    def f_level(self):
        self.miss = 240/(self.strength+self.dexterity)
        self.crit = (self.dexterity+self.intellect+self.wisdom+self.strength)/5
    def f_sword(self):
        self.strength += 30
    def f_offhand(self):
        self.strength += 15
    def f_belt(self):
        self.stamina += 2
        self.health += 20
    def f_cloak(self):
        self.stamina += 20
        self.health += 200
    def f_trinket(self):
        self.strength += 95
    def f_legendary_weapon(self):
        self.strength += 200
    def f_eye(self):
        self.stamina += 50
        self.health += 500
    def f_air(self):
        self.dexterity += 2
    def f_earth(self):
        self.strength += 2
    def f_water(self):
        self.wisdom += 2
    def f_fire(self):
        self.intellect += 2

class cleric:
    def __init__(self,name):
        self.cls = 'cleric'
        self.dead = 0
        self.health_pot = 2
        self.name = name
        self.stamina = 15
        self.wisdom = 10
        self.intellect = 10
        self.dexterity = 9
        self.strength = 18
        self.health = self.stamina*10
        self.shield = 0
        self.damage = 0
        self.empowered = 0
        self.miss = 200/(self.intellect + self.strength)
        self.crit = (self.wisdom + self.intellect+self.dexterity+self.strength)/5
        self.dict = ['cleanses','pierces','glances','devastates','hits','CRITS','misses']
        self.abilities = ['Holy Blow']
        self.lvl = 1
        self.attack1 = pygame.mixer.Sound('cleric_attack1.wav')
        self.attack2 = pygame.mixer.Sound('cleric_attack2.wav')
        self.attack3 = pygame.mixer.Sound('cleric_attack3.wav')
        self.death = pygame.mixer.Sound('player_death.wav')
        self.potion = pygame.mixer.Sound('potion.wav')
    def f_displayStats(self):
        print "Class: ", self.cls, "\nName: ", self.name,"\nLevel: ",self.lvl, "\nStamina: ", self.stamina, "\nWisdom: ", self.wisdom, "\nIntellect: ",self.intellect, "\nDexterity: ",self.dexterity, "\nStrength: ",self.strength, "\nMiss: ",self.miss,"\nCrit: ",self.crit
    def f_abilities(self):
        font = pygame.font.SysFont('centaur', 20)
        drawText('(1): Holy Blow. This ability does '+str(self.strength+self.intellect)+' to '+str((self.strength + self.intellect)*3)+' damage.  Its damage is increased by Strength and Intellect.',font,windowSurface,100,30,TEXTCOLOR)
        drawText('(2): Divine Judgment.  This ability does '+str(self.wisdom*2)+' to '+str(self.wisdom*5)+' damage.  Its damage is increased by Wisdom.',font,windowSurface,100,60,TEXTCOLOR)
        drawText('      Divine Judgment also causes your next ability to have additional effects.',font,windowSurface,100,90,TEXTCOLOR)
        drawText('          Holy Blow does additional damage',font,windowSurface,100,120,TEXTCOLOR)
        drawText('          Divine Judgement heals you.',font,windowSurface,100,150,TEXTCOLOR)
        drawText('          Divin Sagicity grants 1 Wisdom.',font,windowSurface,100,180,TEXTCOLOR)
        drawText('(3): Divine Sagicity. This ability deals damage equal to',font,windowSurface,100,210,TEXTCOLOR)
        drawText('     your Wisdom, heals you and increases your wisdom by 1 if Empowered.',font,windowSurface,100,240,TEXTCOLOR)
        drawText('(Q): Potions.  You have 2 potions that heals you to full.',font,windowSurface,100,270,TEXTCOLOR)
        drawText('     Using these does not cause the enemy to attack.',font,windowSurface,100,300,TEXTCOLOR)
        print "Holy Blow(1).  This ability does {0} to {1} damage.\n".format((self.strength + self.intellect)*3,(self.strength + self.intellect)*4)
        print "Devine Judgment(2). This ability does {0} to {1} damage.".format(self.wisdom*2, self.wisdom*5)
        print "You enter a state of devine empowerment adding addition effects to your next attack."
        print "Holy Blow will deal additional damage, Devine Judgment will heal you, Devine Sagicity grants 2 wisdom."
        print "Devine Sagicity(3) deals {0} damage, heals, and increases your wisdom by 1 if Empowered".format(self.wisdom)
    def f_ability0(self):
        damage = random.randrange((self.strength + self.intellect)*3,(self.strength + self.intellect)*4)
        crit = random.randrange(1,100)
        miss = random.randrange(1,100)
        if self.empowered == 1:
        	damage = round(damage*1.5,0)
        	self.empowered = 0
        if miss <= self.miss:
            self.damage = 0
            drawText('You MISS completely!',font,windowSurface,0,0,TEXTCOLOR)
            print "You MISS completely!"
        elif crit <= self.crit:
            self.damage = damage*2
            dam = str(self.damage)
            drawText('Your Holy Blow CRITS for '+dam,font,windowSurface,0,0,TEXTCOLOR)
            print 'Your Holy Blow {0} for {1} damage.'.format(self.dict[5],self.damage)
        else:
            self.damage = damage
            dam = str(self.damage)
            drawText('Your Holy Blow hits for '+dam,font,windowSurface,0,0,TEXTCOLOR)
            print 'Your Holy Blow {0} for {1} damage.'.format(self.dict[random.randrange(0,5)],self.damage)
        
    def f_ability1(self):
    	damage = random.randrange(self.wisdom*2, self.wisdom*5)
    	crit = random.randrange(1,100)
    	miss = random.randrange(1,100)
    	if self.empowered == 1:
    		self.health += round(damage*0.8, 0)
    		self.empowered = 0
    		heal = str(damage*0.8)
                drawText('You are healed for '+heal,font,windowSurface,0,0,TEXTCOLOR)
    		print "You are healed for {0}".format(damage*0.8)
    	else:
    		self.empowered = 1
                drawText('You feel empowered by a divine force!',font,windowSurface,0,0,TEXTCOLOR)
    		print "You feel empowered by a devine force!"
    	if miss <= self.miss:
    		self.damage = 0
                drawText('You MISS completely!',font,windowSurface,0,0,TEXTCOLOR)
    		print "You Missed!"
    	elif crit <= self.crit:
    		self.damage = damage * 2
    		dam = str(self.damage)
                drawText('Your Devine Judment CRITS for '+dam,font,windowSurface,0,25,TEXTCOLOR)
    		print "Your Devine Judgment CRITS for {0} damage.".format(self.damage)
    	else:
    		self.damage = damage
    		dam = str(self.damage)
                drawText('Your Devine Judment CRITS for '+dam,font,windowSurface,0,25,TEXTCOLOR)
    		print "Your Devine Judgment deals {0} damage.".format(self.damage)
    
    def f_ability2(self):
    	damage = self.wisdom
    	heal_amt = round(self.wisdom*2, 0)
    	if self.empowered == 1:
    		wisdom_gain = 1
    		self.empowered = 0
    	else:
            wisdom_gain = 0
    	self.damage = damage
    	self.wisdom += wisdom_gain
    	self.health += heal_amt
    	if self.health > (self.stamina*10):
            self.health = self.stamina*10
    	wis = str(wisdom_gain)
    	dam = str(self.damage)
    	heal = str(heal_amt)
    	drawText(dam+' damage dealt',font,windowSurface,0,0,TEXTCOLOR)
    	drawText('Healed for '+heal,font,windowSurface,0,25,TEXTCOLOR)
    	drawText('Wisdom boosted by '+wis,font,windowSurface,0,50,TEXTCOLOR)
    	print "{0} damage dealt, healed for {1}, wisdom boosted by {2}.".format(damage, heal_amt, wisdom_gain)
    def f_potion(self):
        self.potion.play()	
    def f_attack1(self):
        self.attack1.play()
    def f_attack2(self):
        self.attack2.play()
    def f_attack3(self):
        self.attack3.play()
    def f_death(self):
        self.death.play()
    def f_level(self):
        self.miss = 200/(self.intellect + self.strength)
        self.crit = (self.wisdom + self.intellect+self.dexterity+self.strength)/5
    def f_sword(self):
        self.intellect += 30
    def f_offhand(self):
        self.strength += 15
    def f_belt(self):
        self.stamina += 2
        self.health += 20
    def f_cloak(self):
        self.stamina += 20
        self.health += 200
    def f_trinket(self):
        self.strength += 45
        self.intellect += 45
    def f_legendary_weapon(self):
        self.strength += 100
        self.intellect += 75
    def f_eye(self):
        self.stamina += 50
        self.health += 500
    def f_air(self):
        self.dexterity += 2
    def f_earth(self):
        self.strength += 2
    def f_water(self):
        self.wisdom += 2
    def f_fire(self):
        self.intellect += 2
