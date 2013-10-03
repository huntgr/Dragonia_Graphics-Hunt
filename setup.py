from cx_Freeze import setup, Executable

includefiles = ['sword.png','belt.png','cloak.png','eye.png','legendary.png','README.txt','plus.png','warlock_entropicassault_dragonia.png','mage_fireball_dragonia.png','mage_shield_dragonia.png','warlock_bloodshield_dragonia.png','cleric_holyblow_dragonia.png','cleric_empowerment_dragonia.png','background_.ogg','cave_dragonia.png','mage_dragonia.png','sun.png','cleric_dragonia.png','cyclops.png','desert.png','dragon.png','dragonia.png','dragonia!.png','gameover.wav','gameover_.png','garg_dragonia_small.png','ogre.png','player.png','snake.png','warlock_dragonia.png','warrior_dragonia.png','water.png','sun.png']
includes = ['pygame.py','random.py','sys.py','time.py','copy.py','classes.py']
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
