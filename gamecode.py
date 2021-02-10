import random
import pygame
import sys  # game bnd krne k liye sys.exit the game
from pygame.locals import *
# global variable for the game
fps = 40  # SEETING FRAME  PER SECOND WE ARE GOING OT BLIT ON TRHE SCREEN
screenwidthvar = 700
screenheightvar = 750
# this method form an emtptyblack console screen for the game
screenvar = pygame.display.set_mode((screenwidthvar, screenheightvar))
groundyvar = screenheightvar * 0.73
game_sprites = {}
game_sounds = {}
playervar = 'gallery/sprite/bird2.png'
backgroundvar = 'gallery/sprite/background2.png'
pipevar = 'gallery/sprite/pipe1.png'

def welcomescreen():
    while True:
        for event in pygame.event.get():
            # if player press cross button or escape key then exit thye game
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()

            # if user presses space key or up key then start the game for them
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                return
            else:
                game_sounds['go2'].play()
                screenvar.blit(game_sprites['template'],(0,0))
               # screenvar.blit(game_sprites['base'],(basex,groundyvar))
                pygame.display.update()
                fpsclock.tick(fps)
def maingame():
    score=0
    playerx=int(screenwidthvar/8)
    playery=int(screenheightvar/2)
    basex=0 
     # creating two random pipes (up pipe and down pipe) to blit on the screen whose work as a abstacle for the bird"
    newpipe1=getrandompipe()
    newpipe2=getrandompipe()
    
    # list of upper pipes
    upperpipe=[{'x':screenwidthvar+200,'y':newpipe1[0]['y']},
    {'x':screenwidthvar+200+(screenwidthvar/2),'y':newpipe2[0]['y']}]

    lowerpipe=[{'x':screenwidthvar+200,'y':newpipe1[1]['y']},
    {'x':screenwidthvar+200+(screenwidthvar/2),'y':newpipe2[1]['y']}]

    pipevelx=-5.7
    playervely=-9
    playermaxvely=12
    playerminvely=-8
    playeraccy=1

    playerflapaccv=-8  # speed of the bird while flappping
    playerflapped=False # it is true state when the bird is in flapping mode

    while True:
        for event in pygame.event.get():
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                if playery>0:
                    playervely=playerflapaccv
                    playerflapped=True
                    game_sounds['wings'].play()
        crashtest=iscollide(playerx,playery,upperpipe,lowerpipe)  # this function will return true if the bird get 
        if crashtest:                                             #collide with the pipes.if iscollide():
            return

        # check for the score of player
        playermidpos=playerx+game_sprites['player'].get_width()/2
        for pipe in lowerpipe:
            pipemidpos=pipe['x']+game_sprites['pipe'][1].get_width()/2
            if pipemidpos<=playermidpos<pipemidpos+4:
                score+=1
                print(f"your score is {score}")
                game_sounds['point'].play()
        
        if playervely<playermaxvely and not playerflapped:
            playervely+=playeraccy
        if playerflapped:
            playerflapped=False
        playerheight=game_sprites['player'].get_height()
        playery=playery+min(playervely,groundyvar-playery-playerheight)

        # moves pipes to the left:
        for up ,lp in zip(upperpipe,lowerpipe):
            up['x']+=pipevelx
            lp['x']+=pipevelx

        # the the new pipe to the screen if the present one reach to the left most corber edge of the screen
        if 0<upperpipe[0]['x']<7:
            newpipe=getrandompipe()
            upperpipe.append(newpipe[0])
            lowerpipe.append(newpipe[1])
        # if pipe if out of screen then remove it
        if upperpipe[0]['x']<-game_sprites['pipe'][0].get_width():
            upperpipe.pop(0)
            lowerpipe.pop(0)
        
        # now blits the spritesss
        screenvar.blit(game_sprites['background'],(0,0))
        for up ,lp in zip(upperpipe,lowerpipe):
            screenvar.blit(game_sprites['pipe'][0],(up['x'],up['y']))
            screenvar.blit(game_sprites['pipe'][1],(lp['x'],lp['y']))
            
        screenvar.blit(game_sprites['base'],(basex,groundyvar))
        screenvar.blit(game_sprites['player'],(playerx,playery))
        mydigit=[int(x) for x in list(str(score))]
        width=0
        for digit in mydigit:
            width+=game_sprites['number'][digit].get_width()
        xoffset=(screenwidthvar-width)/30
        for digit in mydigit:
            screenvar.blit(game_sprites['number'][digit],(xoffset,screenheightvar*0.02))
            xoffset+=game_sprites['number'][digit].get_width()
        
        pygame.display.update()
        fpsclock.tick(fps)

def iscollide(playerx,playery,upperpipe,lowerpipe):
    if playery>groundyvar-50 or playery<0 or playery==479.5:
        game_sounds['hit'].play()
        game_sounds['go1'].play()
        return True
    for pipe in upperpipe:
        pipeheight=game_sprites['pipe'][0].get_height()
        if (playery<pipeheight+pipe['y'] and playerx+game_sprites['player'].get_width()>pipe['x'] and abs(playerx-pipe['x'])<game_sprites['pipe'][0].get_width()):
            
            game_sounds['hit'].play()
            game_sounds['go1'].play()
            return True
    for pipe in lowerpipe:
        if (playery+ game_sprites['player'].get_height() > pipe['y']) and playerx+game_sprites['player'].get_width()>pipe['x'] and abs(playerx-pipe['x'])< game_sprites['pipe'][0].get_width():
            game_sounds['hit'].play()
            game_sounds['go1'].play()
            return True
    return False

def getrandompipe():
    pipeheight=game_sprites['pipe'][0].get_height()
    offset=screenheightvar/4
    y2=offset+random.randrange(10,int(screenheightvar-game_sprites['base'].get_height()-1.2*offset))
    pipex=screenwidthvar+40
    y1=pipeheight-y2+offset
    pipe=[{'x':pipex,'y':-y1} , {'x':pipex,'y':y2}]
    return pipe

# this is the main function from where my game start
pygame.init()  # initialize all pygame modules
fpsclock = pygame.time.Clock()  # specifing timer for the game
# it set a specified caption on top left corner the screen.
pygame.display.set_caption(" THE CRAZY BIRD by y@sh")

# filling the sprites dictonary with the images which we are going to blit on the screen
game_sprites['number'] = (pygame.image.load('gallery/sprite/zero1.png').convert_alpha(),
                          pygame.image.load('gallery/sprite/one1.png').convert_alpha(),

    pygame.image.load(
    'gallery/sprite/two1.png').convert_alpha(),
    pygame.image.load(
    'gallery/sprite/three1.png').convert_alpha(),
    pygame.image.load(
    'gallery/sprite/four1.png').convert_alpha(),
    pygame.image.load(
    'gallery/sprite/five1.png').convert_alpha(),
    pygame.image.load(
    'gallery/sprite/six1.png').convert_alpha(),
    pygame.image.load(
    'gallery/sprite/seven1.png').convert_alpha(),
    pygame.image.load(
    'gallery/sprite/eight1.png').convert_alpha(),
    pygame.image.load('gallery/sprite/nine1.png').convert_alpha())
game_sprites['template'] = pygame.image.load(
    'gallery/sprite/template.png').convert_alpha()
game_sprites['base'] = pygame.image.load(
    'gallery/sprite/ground.png').convert_alpha()
game_sprites['pipe'] = (pygame.transform.rotate(pygame.image.load(pipevar).convert_alpha(), 180),
                        pygame.image.load(pipevar).convert_alpha())
# game soundssss
game_sounds['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
game_sounds['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
game_sounds['point'] = pygame.mixer.Sound(
    'gallery/audio/point.wav')
game_sounds['swoosh'] = pygame.mixer.Sound(
    'gallery/audio/swoosh.wav')
game_sounds['wings'] = pygame.mixer.Sound(
    'gallery/audio/wings1.wav')
game_sounds['go1'] = pygame.mixer.Sound(
    'gallery/audio/gameover3.wav')
game_sounds['go2'] = pygame.mixer.Sound(
    'gallery/audio/gameover1.wav')

game_sprites['background'] = pygame.image.load(backgroundvar).convert()
game_sprites['player'] = pygame.image.load(playervar).convert_alpha()

# GAME LOOP
while True:
    welcomescreen() # show welcome screen to the player untill he press any button yo stop or play the game
    maingame() # most important game function
    