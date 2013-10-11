from cx_Freeze import setup, Executable

includefiles = ['mage_minion(alt)_dragonia.png','mage_minion_dragonia.png','warrior_tactics_dragonia.png','eye.png','trinket_dragonia.png','zombie_dragonia.png','gargantuan_dragonia.png','air_essence.png','earth_essence.png','water_essence.png','fire_essence.png','swashbuckler_dragonia.png','sword_dragonia.png','belt_dragonia.png','cloak_dragonia.png','eye.png','legendary_dragonia.png','README.txt','plus.png','warlock_entropicassault_dragonia.png','mage_fireball_dragonia.png','mage_shield_dragonia.png','warlock_bloodshield_dragonia.png','cleric_holyblow_dragonia.png','cleric_empowerment_dragonia.png','background_.ogg','cave_dragonia.png','mage_dragonia.png','sun.png','cleric_dragonia.png','cyclops_dragonia.png','desert_dragonia.png','dragon.png','dragonia.png','dragonia!.png','gameover.wav','gameover_.png','gargoyle_dragonia.png','ogre.png','snake.png','warlock_dragonia.png','warrior_dragonia.png','water.png','sun.png']
includes = ['pygame.py','random.py','sys.py','time.py','copy.py','classes.py','creatures.py']
excludes = []
packages = []

setup(
    name = 'Dragonia',
    version = '1.0.1',
    description = '',
    author = 'Hunt Grayodn',
    author_email = 'huntgraydon@gmail.com',
    options = {'build_exe': {'excludes':excludes,'packages':packages,'include_files':includefiles}}, 
    executables = [Executable('dragonia_graphics.py')]
)
